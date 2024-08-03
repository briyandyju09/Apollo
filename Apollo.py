import customtkinter as ctk
import pyttsx3
import google.generativeai as genai
import webbrowser


genai.configure(api_key='AIzaSyAWMgIa0ztE3upCG4xgFDt4y8PVEmoEHZo')

# Initialize Gemini model
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)


def preprocess_input(input_text):
    """Converts input text to lowercase and trims whitespace."""
    return input_text.lower().strip()


def postprocess_response(response_text):
    """Capitalizes the first letter and ensures proper punctuation."""
    return response_text.strip().capitalize() + "."


def generate_response(input_text):
    """Preprocesses input, generates response using Gemini, and postprocesses."""
    input_text = preprocess_input(input_text)
    response = gemini_model.generate_content(input_text)
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
        chat_log.insert(ctk.END, "Type your message and press Enter or click Send. Type 'exit' to quit, 'clear' to clear the chat log, or 'help' for this message.\n")
    else:
        response = generate_response(user_input)
        chat_log.insert(ctk.END, f"{response}\n")
        speak(response)
        input_entry.delete(0, ctk.END)



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.title("Apollo - Your Personal AI Assistant")
app.geometry("600x500")

# Create a frame for the chat log
chat_log_frame = ctk.CTkFrame(app, width=600, height=400)
chat_log_frame.pack(pady=10)

# Create a textbox for the chat log with word wrapping
chat_log = ctk.CTkTextbox(chat_log_frame, width=580, height=380, wrap=ctk.WORD)
chat_log.pack(padx=10, pady=10)

# Create a frame for user input and the send button
input_frame = ctk.CTkFrame(app, width=600, height=100)
input_frame.pack(pady=10)

# Create an entry widget for user input with a larger font size
input_entry = ctk.CTkEntry(input_frame, width=400, height=40, font=("Arial", 16))
input_entry.pack(side=ctk.LEFT, padx=10)
input_entry.bind("<Return>", on_enter_pressed)

# Create a stylish send button with rounded corners
send_button = ctk.CTkButton(input_frame, text="Send", command=on_enter_pressed, corner_radius=10)

app.mainloop()
