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
  
def check_for_urls(text_input):
    """
    Uses Groq to check for any URLs in the provided text input and returns them in JSON format.
    
    Args:
        text_input: The text to analyze for URLs
    
    Returns:
        A list of URLs found in the text, in JSON format.
    """
    client = Groq(api_key=GROQ_API_TOKEN)
    
    # Define the system prompt to ask Groq for URL detection and output in JSON format
    system_prompt = """
    You are a text analysis assistant. Please identify any URLs present in the provided text input.
    Return the detected URLs in JSON format as a list of strings. If no URLs are found, return an empty list.
    """
    
    # Prepare the message with the text input
    user_message = f"{system_prompt}\n\nText: {text_input}"

    # Send the request to the Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        model="llama-3.2-11b-vision-preview",  # Model for Groq's chat completions
        temperature=0.2,  # Lower temperature for more factual responses
    )

    # Parse the response and ensure it's in JSON format
    response_content = chat_completion.choices[0].message.content

    # Remove everything before and after the '```json' and '```'
    start = response_content.find('```json') + 7  # Find the start index (after '```json')
    end = response_content.rfind('```')  # Find the end index (before '```')
    # Extract the content between the markers
    cleaned_content = response_content[start:end].strip()

    try:
        # Try parsing the response to ensure it's valid JSON
        url_list = json.loads(cleaned_content)
    except json.JSONDecodeError:
        # If parsing fails, return an empty list
        url_list = []

    return url_list

def check_misinformation(text_input=None, image_path=None):
    """
    Uses Groq to detect misinformation in text and/or images.
    
    Args:
        text_input: Optional text to analyze
        image_path: Optional path to image file
    
    Returns:
        Groq's analysis result
    """
    client = Groq(api_key=GROQ_API_TOKEN)
    
    # Prepare message content
    message_content = []
    
    # Define the system prompt
    system_prompt = """
    You are a specialized misinformation detection assistant created to help elderly users identify fake news and misinformation. Follow these guidelines:

    1. Analyze the provided text and/or image carefully for signs of misinformation.
    2. Rate the likelihood of misinformation on a scale from 1-10 (where 10 is definitely fake).
    3. Use simple, clear language appropriate for elderly users who may not be tech-savvy.
    4. Explain your reasoning in a respectful, non-condescending way.
    5. Provide 2-3 relevant official sources (with URLs) where the user can verify information.
    6. If you detect potential misinformation, suggest specific warning signs to look out for.
    7. Never claim certainty when uncertain - acknowledge limitations in your analysis.
    8. For health, safety, or financial topics, emphasize the importance of consulting official sources.

    Your response should follow this format:
    - "MISINFORMATION RATING: [1-10]/10"
    - "MY ANALYSIS: [brief explanation in simple terms]"
    - "WARNING SIGNS: [list specific red flags if rating is 5+]"
    - "VERIFY WITH THESE SOURCES: [list 2-3 relevant official sources with URLs]"
    - "STAY SAFE ONLINE: [one simple tip relevant to this specific content]"
    """
    
    # Add text if provided
    user_message = "Please analyze this content for misinformation:"
    
    # If we have an image, include instructions in the user message
    if image_path:
        user_message = f"{system_prompt}\n\nPlease analyze this content for misinformation:"
    
    if text_input:
        user_message += f"\n\nText: {text_input}"
    
    message_content.append({"type": "text", "text": user_message})
    
    # Add image if provided
    if image_path:
        base64_image = encode_image(image_path)
        message_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
            },
        })
    
    # Create the completion request
    # For vision models, we can't use system messages with images
    # So we'll include our instructions in the user message instead
    if image_path:
        # When images are included, we need to put instructions in the user message
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": message_content}
            ],
            model="llama-3.2-11b-vision-preview",
            temperature=0.2,  # Lower temperature for more factual responses
        )
    else:
        # For text-only analysis, we can use the system message
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message_content}
            ],
            model="llama-3.2-11b-vision-preview",
            temperature=0.2,  # Lower temperature for more factual responses
        )
    
    return chat_completion.choices[0].message.content

# Example usage
if __name__ == "__main__":
    text = "In today's digital age, people are constantly exploring new ways to stay entertained and informed. Many prefer www.tiktok.com/@nianaguerrero/video/7465679997978610951?is_from_webapp=1&sender_device=pc watching videos from a wide range of platforms. For instance, one can easily spend hours on popular platforms like YouTube, scrolling through endless content that spans a variety of topics. Sometimes, a quick browse will lead to surprising discoveries, like those that pop up in the recommendations list. But some users enjoy content that comes with a story or even interactive features. https://www.youtube.com/watch?v=7X2TAY0U0LI If you’ve ever been on the go, you might notice how social media apps like TikTok keep things fresh and engaging. They're filled with a mix of everyday moments and viral trends that are hard to ignore. There’s also the rising popularity of visual platforms like Instagram, where people share clips and stories of their day-to-day life. https://www.instagram.com/reels/DFoV0rzP68Y/ It’s fascinating to see how each of these platforms adapts to new trends while staying true to their core purpose of connecting people."
    urls = check_for_urls(text)
    print(f"URLs found: {urls}", type(urls))


    # # Example with text only
    # text_example = """Singaporean Banking Giant's Top Executive Dismissed Over Secret Profitable Platform Link"""
    # print("ANALYZING TEXT EXAMPLE:")
    # print(check_misinformation(text_input=text_example))
    # print("\n" + "-"*50 + "\n")
    
    # # Example with image only
    # image_example = os.path.join("resource", "image.png")
    # if os.path.exists(image_example):
    #     print("ANALYZING IMAGE EXAMPLE:")
    #     print(check_misinformation(image_path=image_example))
    #     print("\n" + "-"*50 + "\n")
    
    # # Example with both text and image
    # elif os.path.exists(image_example) and text_example:
    #     print("ANALYZING TEXT AND IMAGE EXAMPLE:")
    #     print(check_misinformation(text_input=text_example, image_path=image_example))