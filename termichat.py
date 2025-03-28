import os
import subprocess
import openai
from dotenv import load_dotenv
from datetime import datetime

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_terminal_question(question, explain_mode=False):
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

def extract_command(text):
    """Try to extract the first code block or first line that looks like a command"""
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            if part.strip().startswith("bash") or part.strip().startswith("sh"):
                return "\n".join(part.strip().splitlines()[1:])
            elif part.strip():
                return part.strip().splitlines()[0]
    return text.strip().splitlines()[0]

def log_history(question, response):
    with open("history.log", "a") as f:
        f.write(f"[🧠 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {question}\n")
        f.write(f"[💡] {response}\n\n")




if __name__ == "__main__":
    print("🧠 Welcome to TermiChat (type 'exit' or Ctrl+C to quit)\n")
    while True:
        try:
            user_input = input("🧠 TermiChat > ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break

            explain_mode = user_input.endswith("--explain")
            run_mode = user_input.endswith("--run")

            # Support both flags at once
            if "--explain" in user_input:
                explain_mode = True
                user_input = user_input.replace("--explain", "").strip()

            if "--run" in user_input:
                run_mode = True
                user_input = user_input.replace("--run", "").strip()

            # Get AI response
            answer = ask_terminal_question(user_input, explain_mode=explain_mode)
            print(f"\n💡 Response:\n{answer}\n")
            log_history(user_input, answer)

            if run_mode:
                cmd = extract_command(answer)
                print(f"⚠️ Attempting to run:\n{cmd}")
                confirm = input("❓Do you want to run this command? (y/N): ").strip().lower()
                if confirm == "y":
                    try:
                        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                        print(f"\n✅ Output:\n{result.stdout}")
                    except subprocess.CalledProcessError as e:
                        print(f"\n❌ Error:\n{e.stderr}")
                else:
                    print("⏭️ Skipped running the command.")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

