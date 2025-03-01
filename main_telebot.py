# code for the telebot goes here
import time
import telebot
import os

bot = telebot.TeleBot("7740250658:AAF-_pMjuzjj8aOiLnB7apeLXjjdDV67VAw")

SAVE_DIR = "src"

# Ensure the 'src' folder exists
os.makedirs(SAVE_DIR, exist_ok=True)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    filename = f"image_{int(time.time())}.jpg"  # Unique filename
    file_path = os.path.join(SAVE_DIR, filename)  # Save inside 'src' folder

    with open(file_path, "wb") as image_file:
        image_file.write(downloaded_file)
    
    bot.reply_to(message, f"Image saved as {file_path}!")

def polling():
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(5)

polling()