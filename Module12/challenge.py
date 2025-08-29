from ollama import chat

PERSONALITIES = {
    "tutor": (
        "You are Lexi, a cheerful and supportive AI Study Buddy and math tutor. "
        "You help middle school students understand school subjects like math, science, and history. "
        "Explain step-by-step in simple words with short examples. "
        "Be calm, encouraging, and positive. "
        "End every response with a short follow-up question."
    ),
    "pirate": (
        "You are Captain Chuckles, a playful pirate comedian. "
        "Use light pirate slang (like 'Ahoy!', 'Arr!'), be friendly and silly. "
        "Give helpful answers, then end with a tiny pirate-themed joke or pun."
    ),
}

DEFAULT_ROLE = "tutor"

params = {
    "temperature": 0.9,
    "top_p": 0.95,
    "max_tokens": 120
}


history = []      
current_role = DEFAULT_ROLE


def make_system_message(role_key: str) -> dict:
    """Build the system message for the given role/personality."""
    prompt = PERSONALITIES[role_key]
    return {"role": "system", "content": prompt}


def reset_history_with_role(role_key: str):
    """Reset conversation to a fresh system message for the role."""
    global history, current_role
    current_role = role_key
    history = [make_system_message(role_key)]


def print_status():
    """Show current role and parameters."""
    print("\n[Status]")
    print(f"- role: {current_role}")
    print(f"- temperature: {params['temperature']}")
    print(f"- top_p: {params['top_p']}")
    print(f"- max_tokens: {params['max_tokens']}\n")


def print_help():
    print(
        "\nCommands:\n"
        "  /role tutor            -> switch to Tutor personality (resets chat)\n"
        "  /role pirate           -> switch to Pirate personality (resets chat)\n"
        "  /temp 0.3              -> set temperature (0.0–1.2)\n"
        "  /top_p 0.9             -> set top_p (0.1–1.0)\n"
        "  /max_tokens 160        -> set max tokens for each reply\n"
        "  /reset                 -> reset conversation with current role\n"
        "  /status                -> show current settings\n"
        "  /help                  -> show this help\n"
        "  quit                   -> exit\n"
    )


def handle_command(text: str) -> bool:
    """
    Try to handle a slash command.
    Returns True if it was a command (and handled), False if not a command.
    """
    global params

    if not text.startswith("/"):
        return False

    parts = text.strip().split()
    cmd = parts[0].lower()

    if cmd == "/role":
        if len(parts) < 2:
            print("Usage: /role <tutor|pirate>")
            return True
        role = parts[1].lower()
        if role not in PERSONALITIES:
            print(f"Unknown role '{role}'. Options: {', '.join(PERSONALITIES.keys())}")
            return True
        reset_history_with_role(role)
        print(f"[Switched role to '{role}' and reset conversation.]")
        return True

    if cmd == "/temp":
        if len(parts) < 2:
            print("Usage: /temp <value e.g., 0.7>")
            return True
        try:
            val = float(parts[1])
            params["temperature"] = val
            print(f"[temperature set to {val}]")
        except ValueError:
            print("Please provide a number, e.g., /temp 0.7")
        return True

    if cmd == "/top_p":
        if len(parts) < 2:
            print("Usage: /top_p <value e.g., 0.9>")
            return True
        try:
            val = float(parts[1])
            params["top_p"] = val
            print(f"[top_p set to {val}]")
        except ValueError:
            print("Please provide a number, e.g., /top_p 0.9")
        return True

    if cmd == "/max_tokens":
        if len(parts) < 2:
            print("Usage: /max_tokens <integer e.g., 160>")
            return True
        try:
            val = int(parts[1])
            params["max_tokens"] = val
            print(f"[max_tokens set to {val}]")
        except ValueError:
            print("Please provide a whole number, e.g., /max_tokens 160")
        return True

    if cmd == "/reset":
        reset_history_with_role(current_role)
        print("[Conversation reset.]")
        return True

    if cmd == "/status":
        print_status()
        return True

    if cmd == "/help":
        print_help()
        return True

    print("Unknown command. Type /help for options.")
    return True


def chat_loop():
    print("Welcome to your multi-role chatbot! Type 'quit' to exit.")
    print("Type /help for commands (role switching & parameter tuning).\n")

    reset_history_with_role(DEFAULT_ROLE)
    print_status()

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break

        if handle_command(user_input):
            continue

        history.append({"role": "user", "content": user_input})

        response = chat(
            model="llama3:8b",
            messages=history,
            options={
                "temperature": params["temperature"],
                "top_p": params["top_p"],
                "max_tokens": params["max_tokens"],
                "num_predict": params["max_tokens"],
            }
        )

        reply = response.message.content.strip() if hasattr(response, "message") else ""
        if not reply:
            reply = "[No response]"

        print("Bot:", reply)
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    chat_loop()
