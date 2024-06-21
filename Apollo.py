
import pyttsx3
import random
import google.generativeai as genai

# Configure Gemini with your API key
genai.configure(api_key='AIzaSyDYKGBoGdg-UBmTBLfV5Ql-UJRVlzChh1g')

# Initialize Gemini model
gemini_model = genai.GenerativeModel('gemini-pro')


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

def generate_response(input_text):
    input_text = preprocess_input(input_text)
    response = gemini_model.generate_content(input_text + "(:Your name is apollo and you are my personal assistant, reply to this message like so and make sure to act accourdingly at all times. ")
    response_text = postprocess_response(response.text)
    return response_text




def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

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