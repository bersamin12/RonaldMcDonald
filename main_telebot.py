import time
import telebot
import os
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
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
    bot.reply_to(message, "Howdy! Use /analyze to check for misinformation.")

# ✅ Dictionary to track analysis requests
analyze_requests = {}

# ✅ Function to handle /analyze command
@bot.message_handler(commands=['analyze'])
def request_analysis(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Text or Image Only", callback_data="single"),
        InlineKeyboardButton("Both Text and Image", callback_data="both")
    )
    bot.send_message(message.chat.id, "✅ Choose an option:", reply_markup=markup)
    analyze_requests[message.chat.id] = {"user_id": message.from_user.id, "step": "choose_mode"}

@bot.callback_query_handler(func=lambda call: call.data in ["single", "both"])
def handle_callback_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    if chat_id not in analyze_requests or analyze_requests[chat_id]["user_id"] != user_id:
        return

    mode = call.data
    analyze_requests[chat_id]["mode"] = mode

    if mode == "single":
        bot.send_message(chat_id, "✅ Send text or an image for analysis.")
        analyze_requests[chat_id]["step"] = "await_input"
    elif mode == "both":
        bot.send_message(chat_id, "✅ Send the text first.")
        analyze_requests[chat_id]["step"] = "await_text"
        analyze_requests[chat_id]["text"] = None
        analyze_requests[chat_id]["image_path"] = None

# ✅ Function to process user input for analysis
@bot.message_handler(content_types=['text', 'photo'])
def handle_analysis_input(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if the chat is in analyze mode and the correct user is responding
    if chat_id not in analyze_requests or analyze_requests[chat_id]["user_id"] != user_id:
        return  # Ignore messages if /analyze wasn't triggered by the user

    step = analyze_requests[chat_id].get("step")

    if step == "await_input" and message.content_type in ['text', 'photo']:
        if message.content_type == 'text':
            analyze_requests[chat_id]["text"] = message.text
        elif message.content_type == 'photo':
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            analyze_requests[chat_id]["image_path"] = save_file(downloaded_file, "jpg")
        process_analysis(chat_id, message)
        return

    if step == "await_text" and message.content_type == 'text':
        analyze_requests[chat_id]["text"] = message.text
        bot.send_message(chat_id, "✅ Now send the image.")
        analyze_requests[chat_id]["step"] = "await_image"
        return

    if step == "await_image" and message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        analyze_requests[chat_id]["image_path"] = save_file(downloaded_file, "jpg")
        process_analysis(chat_id, message)
        return

    bot.send_message(chat_id, "❌ Unexpected input. Please follow the instructions.")

# ✅ Function to process the analysis
def process_analysis(chat_id, message):
    user_text = analyze_requests[chat_id].get("text")
    image_path = analyze_requests[chat_id].get("image_path")
    
    if user_text and image_path:
        bot.send_message(chat_id, "⏳ Analyzing both text and image for misinformation...")
    elif user_text:
        bot.send_message(chat_id, "⏳ Analyzing text content for misinformation...")
    elif image_path:
        bot.send_message(chat_id, "⏳ Analyzing image content for misinformation...")
    
    result = check_misinformation(text_input=user_text, image_path=image_path)
    bot.send_message(chat_id, result)

    # Remove user from analyze_requests after processing
    analyze_requests.pop(chat_id, None)

# ✅ Start polling (ONLY ONCE)
try:
    print("Bot is running...")
    bot.polling(none_stop=True, interval=0, allowed_updates=["message", "callback_query", "edited_message", "channel_post", "edited_channel_post"])
except KeyboardInterrupt:
    print("Bot stopped.")
