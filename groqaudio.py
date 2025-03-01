import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_TOKEN = os.getenv("GROQ_API_TOKEN")

# Initialize the Groq client
client = Groq(api_key=GROQ_API_TOKEN)

# Specify the path to the audio file
filename = os.path.join('src','testspeech.mp3')

# Open the audio file
with open(filename, "rb") as file:
    # Create a translation of the audio file
    translation = client.audio.translations.create(
      file=(filename, file.read()), # Required audio file
      model="whisper-large-v3", # Required model to use for translation
      prompt="Specify context or spelling",  # Optional
      response_format="json",  # Optional
      temperature=0.0  # Optional
    )
    # Print the translation text
    print(translation.text)