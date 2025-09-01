from gtts import gTTS
import os
import platform

def text_to_speech():
    print("Welcome to Text-to-Speech App!")
    user_text = input("Enter the text you want to convert to speech: ")

    if not user_text.strip():
        print("You must enter some text!")
        return

    language = input("Enter language code (default 'en'): ") or "en"
    filename = input("Enter a filename (without extension, default 'output'): ") or "output"

    try:
        # Generate speech
        tts = gTTS(text=user_text, lang=language)
        tts.save(f"{filename}.mp3")
        print(f"Audio file '{filename}.mp3' created successfully! Playing now...")

        # Play the audio file depending on OS
        if platform.system() == "Windows":
            os.system(f"start {filename}.mp3")
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open {filename}.mp3")
        else:  # Linux
            os.system(f"xdg-open {filename}.mp3")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    text_to_speech()
