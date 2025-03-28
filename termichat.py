import os
import openai
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_terminal_question(question):
    explain_mode = False

    if question.strip().endswith("--explain"):
        explain_mode = True
        question = question.replace("--explain", "").strip()

    system_prompt = (
        "You are a helpful Linux terminal assistant. "
        "If explain mode is ON, provide the shell command AND explain it step by step. "
        "If explain mode is OFF, return ONLY the shell command."
    )

    user_prompt = f"Explain mode: {'ON' if explain_mode else 'OFF'}\nUser question: {question}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    print("🧠 Welcome to TermiChat (type 'exit' or Ctrl+C to quit)\n")
    while True:
        try:
            user_input = input("🧠 TermiChat > ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            answer = ask_terminal_question(user_input)
            print(f"\n💡 Response:\n{answer}\n")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

