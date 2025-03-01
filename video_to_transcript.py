#!/usr/bin/env python3
"""
video_to_transcript.py

This script integrates audio extraction from videos and speech-to-text conversion
using the Groq API. It takes a video file path as input and returns the transcript.
"""

import os
import argparse
import sys
from audiotospeech import extract_audio
from groqaudio import transcribe_audio

def process_video(video_path, output_transcript_path=None):
    """
    Process a video file by extracting its audio and converting speech to text.
    
    Args:
        video_path (str): Path to the input video file
        output_transcript_path (str, optional): Path to save the transcript. If None, 
                                               the transcript is printed to stdout.
    
    Returns:
        str: The transcribed text
    """
    # Create a temporary audio file path
    base_dir = os.path.dirname(video_path)
    temp_audio_path = os.path.join(base_dir, "temp_audio.mp3")
    
    try:
        # Step 1: Extract audio from video
        print(f"Extracting audio from {video_path}...")
        extract_audio(video_path, temp_audio_path)
        
        # Step 2: Transcribe the audio
        print("Transcribing audio...")
        transcript = transcribe_audio(temp_audio_path)
        
        # Step 3: Save or print the transcript
        if output_transcript_path:
            with open(output_transcript_path, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"Transcript saved to {output_transcript_path}")
        else:
            print("\nTranscript:")
            print("-----------")
            print(transcript)
            
        return transcript
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None
    finally:
        # Clean up the temporary audio file
        if os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
            except:
                pass

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Convert video to transcript using Groq API")
    parser.add_argument("video_path", help="Path to the input video file")
    parser.add_argument("-o", "--output", help="Path to save the transcript (optional)")
    
    args = parser.parse_args()
    
    # Process the video
    process_video(args.video_path, args.output)

if __name__ == "__main__":
    main()