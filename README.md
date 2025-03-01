# RonaldMcDonald

File structure

.
├── README.md
├── constants.py
├── logs
│   └── tiktok_data.json
├── main_telebot.py
├── pyproject.toml
├── resource (downloads go here)
├── resource_handler.py
├── .env

write the telebot in main_telebot.py. this will callresource_handler

## Setup
Recommended: Use uv and install the dependencies using `uv sync`
otherwise, pip install -r requirements.txt with your python 3.11 environment, but then you will need to update this list manually.


.env: **CREATE** this file on your local machine and copy the API keys here
resourcehandler: routes to functions that handle resource downloads. puts it in resource folder

# Tech Stack Overview


## Core Components
- **Telegram Bot API**: Interface for building bots on Telegram
- **Python**: Main programming language
- **EnsembleData API**: Web scraping services for social media platforms
- **ExaData API**: Web search capabilities
- **Groq API**: AI model hosting and inference
  - llama-3.2-11b-vision-preview: Multimodal vision model
  - whisper-large-v3: Audio transcription model

## Supporting Libraries
- **Beautiful Soup**: HTML parsing and web scraping
- **MoviePy**: Video editing and processing

## Architecture Overview

This stack combines messaging, data collection, AI processing, and multimedia handling capabilities:

1. **User Interface**: Telegram bot provides the chat interface
2. **Backend Processing**: Python handles the application logic
3. **Data Collection**:
   - EnsembleData API extracts content from social platforms
   - ExaData API provides web search capabilities
   - Beautiful Soup supplements with custom web scraping
4. **AI Processing**:
   - Groq API provides access to large language models
   - llama-3.2-11b-vision for image understanding
   - whisper-large-v3 for audio transcription
5. **Media Handling**: MoviePy processes videos

This setup would be excellent for building a versatile assistant that can search the web, process social media content, understand images, transcribe audio, and manipulate video content—all accessible through a Telegram chat interface.
