# code for the telebot goes here
import time
from TelegramBotModule import telebot

bot = telebot.TeleBot("7740250658:AAF-_pMjuzjj8aOiLnB7apeLXjjdDV67VAw")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    filename = f"image_{int(time.time())}.jpg"  # Unique filename
    with open(filename, "wb") as image_file:
        image_file.write(downloaded_file)
    
    bot.reply_to(message, f"Image saved as {filename}!")

bot.infinity_polling()