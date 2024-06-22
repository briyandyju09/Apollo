#import all libs
import pyttsx3
import random
import google.generativeai as genai

# Configure Gemini with your API key
genai.configure(api_key='AIzaSyDYKGBoGdg-UBmTBLfV5Ql-UJRVlzChh1g')

# Initialize Gemini model
gemini_model = genai.GenerativeModel('gemini-1.5-flash')


# Function to perform a Google search with a query
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def preprocess_input(input_text):
    input_text = input_text.lower()
    return input_text

def postprocess_response(response_text):
    response_text = response_text.capitalize()
    response_text += ""
    return response_text

#Prompt to train response:
def generate_response(input_text):
    input_text = preprocess_input(input_text)
    response = gemini_model.generate_content(input_text + "(+ your name is Apollo (just in case u needed to know)")
    response_text = postprocess_response(response.text)
    return response_text

# Function to speak text (Replace with ELEVENLABS soon)
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Function to interact with Apollo
def chatbot():
    print("Hello Briyan! Apollo Here")

    while True:
        print("You: (wait...)")
        user_input = input("How can I help you today?:")
        if user_input is None:
            continue
        elif user_input.lower() == 'exit':
            print("Goodbye! Have a great day!")
            break
        else:
            response = generate_response(user_input)
            print("Apollo:", response)
            speak(response)

if __name__ == "__main__":
    chatbot()

# TODO:
# 1. Add voice from Elevenlabs
# 2. Add image analysis to Gemini
# 3. Add dump features to unused images after analysis
# 4. Add context awareness to Apollo

# End of Apollo.py