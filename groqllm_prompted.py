from groq import Groq
import base64, os
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_TOKEN = os.getenv("GROQ_API_TOKEN")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

client = Groq(api_key=GROQ_API_TOKEN)

def im2text(text_input, image_path):
    """
    Uses Groq to get text info from image

    Args:
        text_input: Optional text to analyze
        image_path: Optional path to image file

    Returns:
        Groq's analysis result
    """

    # Prepare message content
    message_content = []

    # Define the system prompt
    system_prompt = """
    You are an image analyser. Describe the content of the image and any assertion it might be making. \
    The assertions will then be analysed downstream for misinformation against online sources.\
    You can provide a very short summary of your preliminary judgment if you want.
    """

    user_message = f"{system_prompt}\n Image\n:"

    message_content.append({"type": "text", "text": user_message})

    base64_image = encode_image(image_path)
    message_content.append({
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}",
        },
    })

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": system_prompt},
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
    return chat_completion.choices[0].message.content


def final_analysis(summaries: list, original_content):
    nl = "\n"
    sys_prompt = f"""You are a fact-checker. Here is an assertion made by a piece of content\n: {original_content}.
    You are given the following facts, which can be taken to be true. THese are facts that have been searched for online. {(summary+nl for summary in summaries)}\n\n
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": sys_prompt
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": "Please verify the contents provided against the facts provided and provide a verdict. Is what the content alleging true or false?\n Give a brief explanation for your answer.",
            }
        ],

        # The language model which will generate the completion.
        model="llama-3.3-70b-versatile",


        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_completion_tokens=512,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )

    # Print the completion returned by the LLM.
    print(chat_completion.choices[0].message.content)
