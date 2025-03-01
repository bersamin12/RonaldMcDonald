import time
import telebot
import os
from dotenv import load_dotenv
from groqllm_prompted import check_misinformation

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

SAVE_DIR = "src"
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ Function to save files
def save_file(file_data, file_type):
    filename = f"{file_type}_{int(time.time())}.{file_type}"
    file_path = os.path.join(SAVE_DIR, filename)

    with open(file_path, "wb") as file:
        file.write(file_data)

    return file_path  # Return the saved file path

# ✅ Function to handle /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy! Send a photo, video, or text, and I'll save it. Use /analyze to check for misinformation!")

# ✅ Function for saving photos
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    file_path = save_file(downloaded_file, "jpg")
    bot.reply_to(message, f"✅ Image saved as {file_path}!")

# ✅ Function for saving videos
@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    file_path = save_file(downloaded_file, "mp4")
    bot.reply_to(message, f"✅ Video saved as {file_path}!")

# ✅ Function for misinformation analysis
@bot.message_handler(commands=['analyze'])
def analyze_misinformation(message):
    user_text = message.text.replace("/analyze", "").strip()
    image_path = None

    # Check if there's an attached photo
    if message.reply_to_message and message.reply_to_message.photo:
        file_id = message.reply_to_message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        image_path = save_file(downloaded_file, "jpg")

    # Run misinformation check
    if not user_text and not image_path:
        bot.reply_to(message, "❌ Please provide text or reply to an image to analyze.")
        return

    bot.reply_to(message, "⏳ Analyzing content for misinformation...")
    result = check_misinformation(text_input=user_text if user_text else None, image_path=image_path if image_path else None)
    bot.reply_to(message, result)

# ✅ Start polling (ONLY ONCE)
try:
    print("Bot is running...")
    bot.polling(none_stop=True, interval=0)
except KeyboardInterrupt:
    print("Bot stopped.")
