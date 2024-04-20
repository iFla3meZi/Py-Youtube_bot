import os
import re
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from pytube import YouTube

# Замените на ваш токен бота
API_TOKEN = '6809549157:AAGf3dqiL3m-4nTMztTYf5XGRgvbdbtRiw8'

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем экземпляры бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Функция для очистки имени файла
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне ссылку на видео с YouTube, и я помогу тебе его скачать.")

# Обработчик ссылок на видео YouTube
@dp.message_handler(regexp=r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})')
async def process_youtube_link(message: types.Message):
    youtube_link = message.text
    try:
        # Получаем информацию о видео
        video = YouTube(youtube_link)
        video_id = video.video_id
        video_title = video.title

        # Создаем клавиатуру с опциями для скачивания
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton("Скачать видео", callback_data=f"download_video:{video_id}"))
        keyboard.add(types.InlineKeyboardButton("Скачать аудио (MP3)", callback_data=f"download_audio:{video_id}"))

        await message.reply(f"Видео: {video_title}\nВыберите опцию для скачивания:", reply_markup=keyboard)
    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке ссылки: {e}")

@dp.callback_query_handler(Text(startswith="download_video:"))
async def process_download_video(callback_query: types.CallbackQuery):
    _, video_id = callback_query.data.split(':', 1)
    try:
        video = YouTube(f"https://www.youtube.com/watch?v={video_id}")

        # Получаем список доступных для скачивания прогрессивных потоков
        resolutions = sorted(set(stream.resolution for stream in video.streams.filter(progressive=True)), 
                             key=lambda r: int(r[:-1]), reverse=True)

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for resolution in resolutions:
            keyboard.add(types.InlineKeyboardButton(f"{resolution}", callback_data=f"download_video_res:{video_id}:{resolution}"))

        await callback_query.message.edit_text("Выберите разрешение для скачивания видео", reply_markup=keyboard)
    except Exception as e:
        await callback_query.message.reply(f"Произошла ошибка: {e}")

# Обработчик выбора опции для скачивания аудио
@dp.callback_query_handler(Text(startswith="download_audio:"))
async def process_download_audio(callback_query: types.CallbackQuery):
    _, video_id = callback_query.data.split(':', 1)
    video = YouTube(f"https://www.youtube.com/watch?v={video_id}")

    audio_stream = video.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download(output_path="downloads", filename=f"{sanitize_filename(video.title)}.mp3")
    with open(audio_file, 'rb') as audio:
        await callback_query.message.answer_audio(audio, caption=f"{video.title}.mp3")
    os.remove(audio_file)

# Обработчик выбора разрешения видео для скачивания
@dp.callback_query_handler(Text(startswith="download_video_res:"))
async def process_video_resolution(callback_query: types.CallbackQuery):
    _, remainder = callback_query.data.split(':', 1)
    video_id, resolution = remainder.split(':', 1)
    video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
    
    # Выбираем прогрессивный поток соответствующего разрешения
    stream = video.streams.filter(progressive=True, res=resolution, file_extension='mp4').first()
    if stream:
        # Скачиваем видео
        video_file_path = stream.download(output_path="downloads")
        
        # Отправляем пользователю файл
        with open(video_file_path, 'rb') as final_video:
            await callback_query.message.answer_video(final_video, caption=f"Видео: {video.title} [{resolution}]")
        
        # Удаляем временный файл
        os.remove(video_file_path)
    else:
        await callback_query.message.answer("Видео с таким разрешением не найдено.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
