import time
import telebot
import os
import re
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from groqllm_prompted import im2text, final_analysis
from exallm import web_search
from resource_handler import resourceHandler

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

# ✅ Dictionary to track analysis requests
analyze_requests = {}

# ✅ Function to handle /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy! Send either text or an image for analysis after using /analyze. I will process it and provide the analysis.")

# ✅ Function to handle /analyze command
@bot.message_handler(commands=['analyze'])
def request_analysis(message):
    bot.send_message(message.chat.id, "✅ Please send either text or an image for analysis.")
    analyze_requests[message.chat.id] = {"user_id": message.from_user.id, "step": "await_input"}

# ✅ Function to handle user input (text or image)
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
            bot.send_message(chat_id, "✅ Analyzing text content for misinformation...")

            # Check for URL in text
            url_pattern = r"https?://[^\s]+"  # Matches http:// or https:// followed by non-whitespace characters
            urls = re.findall(url_pattern, message.text)

            if urls:
                final_result, web_facts = resourceHandler(url=urls[0], text=message.text, analyze_misinformation=True)
            
            else:
                # Perform web search
                web_facts = web_search(message.text)[0]  # Get first search summary
                print(web_facts, type(web_facts))
                # Final analysis including web search facts
                final_result = final_analysis(original_content=message.text, summaries=web_facts)
            
            bot.send_message(chat_id, f"Web Search Findings: {web_facts}")
            bot.send_message(chat_id, f"Final Verdict: {final_result}")
        
        elif message.content_type == 'photo':
            # If it's an image, process it using the im2text function
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            image_path = save_file(downloaded_file, "jpg")
            
            bot.send_message(chat_id, "✅ Analyzing image content for misinformation...")
            
            # Extract text from image
            result = im2text(text_input=None, image_path=image_path)

            # Check for URL in text
            url_pattern = r"https?://[^\s]+"  # Matches http:// or https:// followed by non-whitespace characters
            urls = re.findall(url_pattern, result)

            if urls:
                final_result, web_facts = resourceHandler(url=urls[0], text=message.text, analyze_misinformation=True)

            else:
                # Perform web search
                web_facts = web_search(result)[0]  # Get first search summary
                
                # Final analysis including web search facts
                final_result = final_analysis(original_content=result, summaries=web_facts)
            
            bot.send_message(chat_id, f"Extracted Text: {result}")
            bot.send_message(chat_id, f"Web Search Findings: {web_facts}")
            bot.send_message(chat_id, f"Final Verdict: {final_result}")

        # Remove the user from analyze_requests after processing
        analyze_requests.pop(chat_id, None)


# ✅ Start polling (ONLY ONCE)
try:
    print("Bot is running...")
    bot.polling(none_stop=True, interval=0, allowed_updates=["message", "callback_query", "edited_message", "channel_post", "edited_channel_post"])
except KeyboardInterrupt:
    print("Bot stopped.")
