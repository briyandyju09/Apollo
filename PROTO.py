# Import all necessary libraries
import random
import webbrowser
import google.generativeai as genai
import os
import shutil  # For moving files
import requests  # For image analysis
import cv2  # For image analysis
import numpy as np
from io import BytesIO
from PIL import Image
from typing import IO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# Configure Gemini with your API key
genai.configure(api_key='AIzaSyDYKGBoGdg-UBmTBLfV5Ql-UJRVlzChh1g')

# Initialize Gemini model
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Eleven Labs API key and client
ELEVENLABS_API_KEY = os.getenv("sk_030849f5720ff120d1e51afd8360dee0aca8622617e8c6a2")
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def text_to_speech_stream(text: str) -> IO[bytes]:
    # Perform the text-to-speech conversion
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  # pre-made voice
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    audio_stream = BytesIO()
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)
    audio_stream.seek(0)
    return audio_stream

# Function to use Eleven Labs for text-to-speech
def speak_with_elevenlabs(text):
    audio_stream = text_to_speech_stream(text)
    with open('response.mp3', 'wb') as audio_file:
        audio_file.write(audio_stream.read())
    os.system('mpg321 response.mp3')  # Requires mpg321 installed on the system

# Function to perform a Google search with a query
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

# Function to preprocess input text
def preprocess_input(input_text):
    return input_text.lower()

# Function to postprocess response text
def postprocess_response(response_text):
    return response_text.capitalize()

# Function to generate a response using Gemini model
def generate_response(input_text, context=""):
    input_text = preprocess_input(input_text)
    response = gemini_model.generate_content(f"{input_text} (+ your name is Apollo {context})")
    response_text = postprocess_response(response.text)
    return response_text

# Function to analyze an image using OpenCV
def analyze_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Simple analysis: detect edges
    edges = cv2.Canny(gray, 100, 200)
    
    # Example: count number of edges (simple feature extraction)
    num_edges = np.sum(edges > 0)
    analysis_result = f"The image contains approximately {num_edges} edges."
    return analysis_result

# Function to move analyzed image to dumps folder
def move_image_to_dumps(image_path):
    dumps_folder = "dumps"
    if not os.path.exists(dumps_folder):
        os.makedirs(dumps_folder)
    shutil.move(image_path, os.path.join(dumps_folder, os.path.basename(image_path)))
    print(f"Moved image to dumps folder: {image_path}")

# Function to speak text using Eleven Labs
def speak(text):
    speak_with_elevenlabs(text)

# Function to interact with Apollo
def chatbot():
    context = ""
    print("Hello Briyan! Apollo Here")

    while True:
        print("You: (wait...)")
        user_input = input("How can I help you today?: ")
        if not user_input:
            continue
        elif user_input.lower() == 'exit':
            print("Goodbye! Have a great day!")
            break
        elif user_input.lower().startswith("analyze image"):
            image_path = user_input.split(" ")[-1]  # Assuming the path is provided
            analysis_result = analyze_image(image_path)
            print("Apollo:", analysis_result)
            speak(analysis_result)
            move_image_to_dumps(image_path)
            # Update context with image analysis result
            context += f" Image analysis result: {analysis_result}"
        else:
            response = generate_response(user_input, context)
            print("Apollo:", response)
            speak(response)
            context += f" {user_input}"  # Add the current input to the context for future responses

if __name__ == "__main__":
    chatbot()

# TODO:
# 1. Improve image analysis using more sophisticated techniques if needed.
# 2. Handle additional context features more robustly.
