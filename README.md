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

write the telebot in main_telebot.py. this will callresource_handler

## Setup
Recommended: Use uv and install the dependencies using `uv sync`
otherwise, pip install -r requirements.txt with your python 3.11 environment, but then you will need to update this list manually.


constants: **CREATE** this file on your local machine and copy the API keys here
resourcehandler: routes to functions that handle resource downloads. puts it in resource folder
