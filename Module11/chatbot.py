from ollama import chat

def chat_loop():
    history = []
    print("Welcome to your chatbot! Type 'quit' to exit.\n")

    system_message = {
        "role": "system",
        "content": (
            "You are Lexi, a cheerful and supportive AI Study Buddy. "
            "You help middle school students understand school subjects like math, science, and history. "
            "You always explain ideas in a calm and simple way, using clear examples and easy language. "
            "You speak like a friendly tutor — encouraging, curious, and positive. "
            "At the end of every response, you ask a short follow-up question to help the student keep thinking or practicing."
        )
    }

    history = [system_message]
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "quit":
            break

        history.append({"role": "user", "content": user_input})

        response = chat(
            model="llama3:8b",
            messages=history,
            options = {
                "temperature": 0.9,
                "top_p": 0.95,
                "max_tokens": 120
            }
        )

        reply = response.message.content
        print("Bot:", reply)
        history.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    chat_loop()
