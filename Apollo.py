import customtkinter as ctk
import pyttsx3
import google.generativeai as genai
import webbrowser

# Configure Gemini with your API key
genai.configure(api_key='AIzaSyAWMgIa0ztE3upCG4xgFDt4y8PVEmoEHZo')

# Initialize Gemini model
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def preprocess_input(input_text):
    # Convert to lowercase and trim whitespace
    return input_text.lower().strip()

def postprocess_response(response_text):
    # Capitalize the first letter and ensure proper punctuation
    return response_text.strip().capitalize() + "."

def generate_response(input_text):
    input_text = preprocess_input(input_text)
    response = gemini_model.generate_content(input_text + " (+ your name is Apollo (just in case you needed to know))")
    response_text = postprocess_response(response.text)
    return response_text

def speak(text):
    engine.say(text)
    engine.runAndWait()

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def on_enter_pressed(event=None):
    user_input = input_entry.get()
    if user_input.lower() == 'exit':
        app.quit()
    elif user_input.lower() == 'clear':
        chat_log.delete('1.0', ctk.END)
    elif user_input.lower() == 'help':
        chat_log.insert(ctk.END, "Apollo: Type your message and press Enter or click Send. Type 'exit' to quit, 'clear' to clear the chat log, or 'help' for this message.\n")
    else:
        response = generate_response(user_input)
        chat_log.insert(ctk.END, "You: " + user_input + "\n")
        chat_log.insert(ctk.END, "Apollo: " + response + "\n")
        speak(response)
        input_entry.delete(0, ctk.END)

# Initialize CustomTkinter
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Create the main window
app = ctk.CTk()
app.title("Apollo - Your Personal AI Assistant")
app.geometry("600x800")

# Create a frame for chat log
frame_chat_log = ctk.CTkFrame(app, width=580, height=600)
frame_chat_log.pack(pady=10)

# Create a text widget for chat log with a scrollbar
chat_log = ctk.CTkTextbox(frame_chat_log, width=560, height=580, wrap=ctk.WORD)
chat_log.pack(pady=10)

# Create a frame for input and buttons
frame_input = ctk.CTkFrame(app, width=580, height=100)
frame_input.pack(pady=10)

# Create an entry widget for user input
input_entry = ctk.CTkEntry(frame_input, width=400, height=50)
input_entry.pack(side=ctk.LEFT, padx=10)
input_entry.bind("<Return>", on_enter_pressed)

# Create a button to send input
send_button = ctk.CTkButton(frame_input, text="Send", command=on_enter_pressed)
send_button.pack(side=ctk.LEFT, padx=10)

app.mainloop()
