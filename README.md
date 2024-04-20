# YouTube Video Downloader Telegram Bot
# Этот проект представляет собой Telegram-бота, который позволяет пользователям скачивать видео и аудио с YouTube. Бот распознает ссылки на видео YouTube, отправленные пользователями, и предоставляет удобный интерфейс для выбора опций скачивания.

# Функциональность
# 1) Распознавание ссылок на видео YouTube, отправленных пользователями.
# 2) Возможность скачивания видео в оригинальном формате с выбором разрешения.
# 3) Возможность скачивания аудио из видео в формате MP3.
# 4) Удобный интерфейс с использованием встроенной клавиатуры для выбора опций скачивания.

# Технологии
Python 3.x
aiogram 2.25.1 - библиотека для создания Telegram-ботов
pytube - библиотека для работы с видео на YouTube

# Установка и запуск
Клонируйте репозиторий:
#<code>git clone https://github.com/your-username/youtube-video-downloader-bot.git#<code>
# Перейдите в директорию проекта:
#<code>cd youtube-video-downloader-bot#<code>
# Установите зависимости:
#<code>pip install -r requirements.txt<code>
# Замените 'YOUR_BOT_TOKEN' в файле bot.py на токен вашего Telegram-бота, полученный от BotFather.
# Запустите бота:
#<code> python bot.py<code> 

# Использование
1) Найдите вашего бота в Telegram по имени, которое вы указали при регистрации бота у BotFather.
2) Отправьте боту ссылку на видео YouTube, которое вы хотите скачать.
3) Выберите опцию скачивания (видео или аудио) с помощью встроенной клавиатуры.
4) Если вы выбрали опцию скачивания видео, выберите желаемое разрешение из доступных вариантов.
5) Бот отправит вам выбранный файл (видео или аудио) для скачивания.
