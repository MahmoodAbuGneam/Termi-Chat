import os
import sys
import subprocess
import openai
from dotenv import load_dotenv
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

# using the 'rich' console to make the terminal look betterr 
console = Console()

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

def is_dangerous_command(cmd: str) -> bool:
    dangerous_keywords = [
        "rm -rf /", "rm -rf", "rm *", "rm -r",
        ":(){ :|:& };:",  # fork bomb
        "mkfs", "mkfs.ext4", "mkfs.btrfs", "mkfs.xfs",
        "dd if=", "dd of=", "mv /", "mv *", ">:",
        "kill -9 1", "killall -9 init", "kill -9 0",
        "poweroff", "shutdown", "reboot",
        "chmod 000", "chown root",
        "/dev/sda", "/dev/null", ">/dev/sda", ">/dev/null",
        ">:"
    ]
    cmd_lower = cmd.lower().replace("  ", " ").strip()
    return any(keyword in cmd_lower for keyword in dangerous_keywords)

def handle_request(full_input: str, explain_mode=False, run_mode=False, original_input=None):
    answer = ask_terminal_question(full_input, explain_mode=explain_mode)
    console.print(f"\n[bold yellow]💡 Response:[/]\n{answer}\n")

    # Log the full input with flags, if provided
    log_history(original_input or full_input, answer)

    cmd = extract_command(answer)

    if is_dangerous_command(cmd):
        console.print("[bold red on yellow]🚨 DANGER:[/] This command could harm your system.")
        console.print("[red]Be careful before running it manually or using --run.[/]\n")

    if run_mode:
        console.print(f"[bold red]⚠️ Attempting to run:[/] {cmd}")
        confirm = Prompt.ask("❓ Do you want to run this command? (y/N)").strip().lower()
        if confirm == "y":
            try:
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                console.print(f"\n[bold green]✅ Output:[/]\n{result.stdout}")
            except subprocess.CalledProcessError as e:
                console.print(f"\n[bold red]❌ Error:[/]\n{e.stderr}")
        else:
            console.print("⏭️ Skipped running the command.")




def print_help():
    console.print("""
[bold blue]
TermiChat - AI-powered Linux terminal assistant

Usage:
  ai "your question" [--explain] [--run]
  ai                        # to enter interactive mode
  ai --help                # show this help message
  ai --about               # show info about TermiChat
[/]
""")

def print_about():
    console.print("""
[bold green]
🧠 TermiChat
An AI-powered Linux terminal assistant created by Mahmood Gneam.
Originally built for personal productivity, now shared with the world.

GitHub: https://github.com/MahmoodAbuGneam/Termi-Chat
LinkedIn: https://www.linkedin.com/in/mahmoodgneam/
[/]
""")






def main():
    # One-shot mode
    if len(sys.argv) > 1:
        if "--help" in sys.argv:
            print_help()
            return
        elif "--about" in sys.argv:
            print_about()
            return
        else:
            full_input = " ".join(sys.argv[1:]).strip()
            explain_mode = "--explain" in full_input
            run_mode = "--run" in full_input

            if explain_mode:
                full_input = full_input.replace("--explain", "").strip()
            if run_mode:
                full_input = full_input.replace("--run", "").strip()

            handle_request(full_input, explain_mode, run_mode)
            return  # Exit after one-shot

    # Interactive mode
    console.print("🧠 Welcome to TermiChat (type 'exit' or Ctrl+C to quit)\n")
    while True:
        try:
            user_input = Prompt.ask("[bold cyan]🧠 TermiChat >[/]").strip()

            if user_input.lower() in ["exit", "quit"]:
                console.print("👋 Goodbye!")
                break

            explain_mode = "--explain" in user_input
            run_mode = "--run" in user_input

            if explain_mode:
                user_input = user_input.replace("--explain", "").strip()
            if run_mode:
                user_input = user_input.replace("--run", "").strip()

            handle_request(user_input, explain_mode, run_mode)

        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
