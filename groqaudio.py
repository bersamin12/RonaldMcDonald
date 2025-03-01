#!/usr/bin/env python3
"""
groqaudio.py

This module handles transcription of audio files using the Groq API.
"""

import os
import argparse
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Groq API token from environment variables
GROQ_API_TOKEN = os.getenv("GROQ_API_TOKEN")
if not GROQ_API_TOKEN:
    raise ValueError("GROQ_API_TOKEN not found in environment variables. "
                    "Please add it to your .env file or export it directly.")

def transcribe_audio(audio_file_path, model="whisper-large-v3", prompt="", temperature=0.0):
    """
    Transcribe audio using the Groq API.
    
    Args:
        audio_file_path (str): Path to the audio file
        model (str): The model to use for transcription (default: "whisper-large-v3")
        prompt (str): Optional context or spelling guidance
        temperature (float): Sampling temperature (default: 0.0)
    
    Returns:
        str: The transcribed text
    """
    # Initialize the Groq client
    client = Groq(api_key=GROQ_API_TOKEN)
    
    # Open the audio file
    with open(audio_file_path, "rb") as file:
        # Create a translation of the audio file
        translation = client.audio.translations.create(
            file=(audio_file_path, file.read()),  # Required audio file
            model=model,  # Required model to use for translation
            prompt=prompt,  # Optional context
            response_format="json",  # Optional format
            temperature=temperature  # Optional temperature
        )
    
    # Return the transcribed text
    return translation.text

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Transcribe audio files using Groq API")
    parser.add_argument("audio_path", help="Path to the audio file")
    parser.add_argument("-o", "--output", help="Path to save the transcript (optional)")
    parser.add_argument("--model", default="whisper-large-v3", help="Model to use (default: whisper-large-v3)")
    parser.add_argument("--prompt", default="", help="Context or spelling guidance")
    parser.add_argument("--temperature", type=float, default=0.0, help="Sampling temperature (default: 0.0)")
    
    args = parser.parse_args()
    
    # Transcribe the audio
    transcript = transcribe_audio(
        args.audio_path, 
        model=args.model,
        prompt=args.prompt,
        temperature=args.temperature
    )
    
    # Save or print the transcript
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"Transcript saved to {args.output}")
    else:
        print(transcript)

if __name__ == "__main__":
    main()