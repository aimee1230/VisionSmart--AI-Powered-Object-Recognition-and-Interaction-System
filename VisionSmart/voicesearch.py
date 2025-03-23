import speech_recognition as sr

def listen_for_commands():
    """Captures voice input"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        return command.lower()
    except sr.UnknownValueError:
        return "Sorry, I didn't understand that."

def process_voice_command(command, detected_object):
    """Processes user commands related to detected objects"""
    if "where can I buy" in command:
        return f"You can buy {detected_object} here: [Amazon Link]"
    elif "what is" in command:
        return f"{detected_object} is a commonly used item."
    else:
        return "I am not sure, but I can find out!"
