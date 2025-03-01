from groq import Groq
import base64, os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_TOKEN = os.getenv("GROQ_API_TOKEN")

# Path to your image
image_path = os.path.join("resource", "kitten.jpg")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


# Getting the base64 string
base64_image = encode_image(image_path)

client = Groq(api_key=GROQ_API_TOKEN)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                # to include multiple images, just add more of these blocks
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
    model="llama-3.2-11b-vision-preview",
)

print(chat_completion.choices[0].message.content)
