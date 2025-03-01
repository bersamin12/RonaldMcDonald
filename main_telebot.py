import time
import telebot
import os
from dotenv import load_dotenv
from groqllm_prompted import check_misinformation

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=True)

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
    bot.reply_to(message, "Howdy! Use /analyze, then send text, an image, or both to check for misinformation!")

# ✅ Dictionary to track analysis requests
analyze_requests = {}

# ✅ Function to handle /analyze command
@bot.message_handler(commands=['analyze'])
def request_analysis(message):
    bot.reply_to(message, "✅ Send text, an image, or both for misinformation analysis.")
    analyze_requests[message.chat.id] = message.from_user.id  # Store user ID to track input

# ✅ Function to process user input for analysis
@bot.message_handler(content_types=['text', 'photo'])
def handle_analysis_input(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if the chat is in analyze mode and the correct user is responding
    if chat_id not in analyze_requests or analyze_requests[chat_id] != user_id:
        return  # Ignore messages if /analyze wasn't triggered by the user

    user_text = message.text if message.content_type == 'text' else None
    image_path = None

    # Check if there's an attached photo
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        image_path = save_file(downloaded_file, "jpg")
    
    # Run misinformation check
    if not user_text and not image_path:
        bot.reply_to(message, "❌ Please provide text or an image for analysis.")
        return

    bot.reply_to(message, "⏳ Analyzing content for misinformation...")
    result = check_misinformation(text_input=user_text if user_text else None, image_path=image_path if image_path else None)
    bot.reply_to(message, result)

    # Remove user from analyze_requests after processing
    analyze_requests.pop(chat_id, None)

# ✅ Start polling (ONLY ONCE)
try:
    print("Bot is running...")
    bot.polling(none_stop=True, interval=0, allowed_updates=["message", "edited_message", "channel_post", "edited_channel_post"])
except KeyboardInterrupt:
    print("Bot stopped.")
