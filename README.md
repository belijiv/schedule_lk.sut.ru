# Bot Setup Instructions / Инструкция по установке бота

## System Requirements
For the bot to work properly, you need to install WebDriver for your browser.

### Step 1: Install WebDriver

| Browser | Driver | Download Link | Notes |
|---------|--------|---------------|--------|
| **Chrome** | ChromeDriver | [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/) | Make sure the version matches your browser |
| **Firefox** | GeckoDriver | [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases) | - |
| **Edge** | EdgeDriver | [https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) | - |
| **Safari** | SafariDriver | Built into macOS | Run: `sudo safaridriver --enable` in terminal |

### Installation Guide
1. **Download** the appropriate driver for your browser
2. **Extract** the archive and place the executable file in system PATH
3. **Verify** driver version compatibility with your browser
4. **Alternative**: Specify the driver path directly in your code

### Step 2: Install Dependencies

```
pip install -r requirements.txt
```

## Системные требования
Для корректной работы бота необходимо установить WebDriver для вашего браузера.

### Шаг 1: Установка WebDriver

| Браузер | Драйвер | Ссылка для скачивания | Примечания |
|---------|---------|--------------|---------|
| **Chrome** | ChromeDriver | [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/) | Убедитесь, что версия соответствует вашему браузеру |
| **Firefox** | GeckoDriver | [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases) | - |
| **Edge** | EdgeDriver | [https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) | - |
| **Safari** | SafariDriver | Встроен в macOS | Выполните команду `sudo safaridriver --enable` в терминале |

### Руководство по установке
1. **Скачайте** подходящий драйвер для вашего браузера
2. **Распакуйте** архив и поместите исполняемый файл в системную переменную PATH
3. **Проверьте** совместимость версии драйвера с вашим браузером
4. **Альтернативный вариант**: укажите путь к драйверу непосредственно в коде

### Шаг 2: Установка зависимостей

```
pip install -r requirements.txt
```
