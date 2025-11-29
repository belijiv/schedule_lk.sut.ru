import asyncio
import aioschedule
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from aiogram import Bot

logger = logging.getLogger(__name__)


class AttendanceService:
    def __init__(self, config):
        self.config = config
        self.driver = None
        self.bot = Bot(token=config.telegram_token)
        self.is_running = False
        self.scheduler_task = None

    async def start(self):
        """Запуск сервиса с защитой от повторного запуска"""
        try:
            # ПРОВЕРКА: если уже запущен, не создаем новый браузер
            if self.is_running and self.driver:
                logger.info("Сервис уже запущен, повторный запуск не требуется")
                return True

            logger.info("Запуск сервиса отметки...")

            if not await self._init_browser():
                return False

            if not await self._login():
                return False

            if not await self._navigate_to_schedule():
                return False

            self.is_running = True
            self.scheduler_task = asyncio.create_task(self._run_scheduler())

            logger.info("Сервис отметки успешно запущен")
            return True

        except Exception as e:
            logger.error(f"Ошибка запуска сервиса: {e}")
            return False

    async def stop(self):
        """Остановка сервиса"""
        self.is_running = False

        if self.scheduler_task:
            self.scheduler_task.cancel()
            try:
                await self.scheduler_task
            except asyncio.CancelledError:
                pass

        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

        aioschedule.clear()
        logger.info("Сервис отметки остановлен")
        return True

    async def _init_browser(self):
        try:
            edge_options = Options()

            # Скрытый режим из конфига
            if self.config.headless:
                edge_options.add_argument('--headless')

            edge_options.add_argument('--disable-gpu')
            edge_options.add_argument('--no-sandbox')
            edge_options.add_argument('--disable-dev-shm-usage')

            # Используем путь из конфига или системный
            if self.config.edge_driver_path:
                service = Service(executable_path=self.config.edge_driver_path)
            else:
                service = Service()

            self.driver = webdriver.Edge(service=service, options=edge_options)
            self.driver.implicitly_wait(self.config.webdriver_timeout)

            print("✅ Браузер Edge успешно запущен")
            return True

        except Exception as e:
            print(f"❌ Ошибка инициализации браузера: {e}")
            return False

    async def _login(self):
        """Авторизация на сайте"""
        try:
            self.driver.get("https://lk.sut.ru/cabinet/")

            # Ввод логина
            login_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "users"))
            )
            login_field.clear()
            login_field.send_keys(self.config.login)

            # Ввод пароля
            password_field = self.driver.find_element(By.ID, "parole")
            password_field.clear()
            password_field.send_keys(self.config.password)

            # Нажатие кнопки входа
            login_button = self.driver.find_element(By.ID, "logButton")
            login_button.click()

            # Ожидание загрузки
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "title_item"))
            )
            return True

        except Exception as e:
            logger.error(f"Ошибка авторизации: {e}")
            return False

    async def _navigate_to_schedule(self):
        """Переход к расписанию"""
        try:
            # Клик по вкладке "Учеба"
            study_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'title_item') and contains(., 'Учеба...')]"))
            )
            study_tab.click()

            # Клик по подвкладке "Расписание"
            schedule_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "menu_li_6118"))
            )
            schedule_tab.click()

            # Ожидание загрузки расписания
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            return True

        except Exception as e:
            logger.error(f"Ошибка перехода к расписанию: {e}")
            return False

    async def _schedule_checks(self):
        """Настройка расписания проверок"""
        aioschedule.clear()

        # Внутривузовские пары
        for time_str in self.config.check_times:
            aioschedule.every().day.at(time_str).do(lambda: asyncio.create_task(self.mark_attendance(False)))
            logger.info(f"Настроена проверка в {time_str} (внутривузовские)")

        # Вневузовские пары
        for time_str in self.config.extracurricular_times:
            aioschedule.every().day.at(time_str).do(lambda: asyncio.create_task(self.mark_attendance(True)))
            logger.info(f"Настроена проверка в {time_str} (вневузовские)")

    async def _run_scheduler(self):
        """Запуск планировщика"""
        await self._schedule_checks()
        while self.is_running:
            try:
                await aioschedule.run_pending()
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Ошибка в планировщике: {e}")
                await asyncio.sleep(10)

    async def find_current_lesson(self, is_extracurricular=False):
        """Поиск текущей пары в расписании"""
        try:
            # Получаем текущие день недели и время
            now = datetime.now()
            current_weekday = now.strftime("%A")

            # Русские названия дней недели
            weekdays_ru = {
                'Monday': 'Понедельник',
                'Tuesday': 'Вторник',
                'Wednesday': 'Среда',
                'Thursday': 'Четверг',
                'Friday': 'Пятница',
                'Saturday': 'Суббота',
                'Sunday': 'Воскресенье'
            }

            current_weekday_ru = weekdays_ru.get(current_weekday, '')

            # Поиск заголовка текущего дня
            day_headers = self.driver.find_elements(By.XPATH,
                                                    f"//tr[contains(@style, 'background: #b3b3b3')]//td[contains(., '{current_weekday_ru}')]")

            if not day_headers:
                return None

            # Поиск пар для текущего дня
            day_section = day_headers[0].find_element(By.XPATH, "./..").find_element(By.XPATH,
                                                                                     "following-sibling::tr[1]")
            lessons = []

            # Собираем все пары текущего дня
            next_row = day_section
            while next_row and ('background: #b3b3b3' not in (next_row.get_attribute('style') or '')):
                try:
                    time_cell = next_row.find_element(By.XPATH, "./td[1]")
                    lesson_info = next_row.find_element(By.XPATH, "./td[2]")

                    lesson_data = {
                        'time': time_cell.text.strip(),
                        'name': lesson_info.find_element(By.TAG_NAME, "b").text if lesson_info.find_elements(
                            By.TAG_NAME, "b") else "",
                        'row': next_row
                    }

                    lessons.append(lesson_data)
                except:
                    pass

                next_row = next_row.find_element(By.XPATH, "following-sibling::tr[1]") if next_row else None

            # ПРОСТАЯ ЛОГИКА: возвращаем первую найденную пару для текущего времени
            # Бот сам решает, какая пара идет сейчас на основе времени в расписании
            if lessons:
                return lessons[0]  # Первая найденная пара текущего дня

            return None

        except Exception as e:
            logger.error(f"Ошибка поиска пары: {e}")
            return None

    async def mark_attendance(self, is_extracurricular=False):
        """Основная функция отметки"""
        try:
            if not self.driver:
                if not await self.start():
                    return False

            # Обновляем страницу для актуального расписания
            self.driver.refresh()
            await asyncio.sleep(5)

            lesson = await self.find_current_lesson(is_extracurricular)
            if not lesson:
                logger.info("Текущая пара не найдена")
                return False

            lesson_name = lesson['name']
            lesson_row = lesson['row']

            # Ожидание перед нажатием кнопки
            wait_minutes = self.config.wait_time
            logger.info(f"Ожидание {wait_minutes} минут перед отметкой...")
            await asyncio.sleep(wait_minutes * 60)

            # Поиск кнопки "Начать занятие"
            try:
                buttons_cell = lesson_row.find_element(By.XPATH, "./td[6]")
                buttons = buttons_cell.find_elements(By.TAG_NAME, "a")

                mark_button = None
                for button in buttons:
                    if "Начать занятие" in button.text:
                        mark_button = button
                        break

                if mark_button:
                    mark_button.click()
                    logger.info(f"Отметка на паре: {lesson_name}")

                    # Отправка сообщения в Telegram
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message_type = "вневузовской" if is_extracurricular else "внутривузовской"
                    message = f"✅ Отметка на {message_type} паре: {lesson_name}\nВремя: {timestamp}"

                    await self.bot.send_message(
                        chat_id=self.config.chat_id,
                        text=message
                    )

                    return True
                else:
                    logger.info("Кнопка отметки не найдена")
                    return False

            except Exception as e:
                logger.error(f"Ошибка при нажатии кнопки: {e}")
                return False

        except Exception as e:
            logger.error(f"Ошибка в функции отметки: {e}")
            return False

    def get_next_check_time(self):
        """Получение времени до следующей проверки"""
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M")

            all_times = self.config.check_times + self.config.extracurricular_times
            all_times.sort()

            for time_str in all_times:
                if time_str > current_time:
                    check_time = datetime.strptime(time_str, "%H:%M")
                    current_time_obj = datetime.strptime(current_time, "%H:%M")
                    delta = check_time - current_time_obj
                    minutes = delta.seconds // 60
                    return f"{minutes} мин"

            return "завтра"
        except:
            return "неизвестно"