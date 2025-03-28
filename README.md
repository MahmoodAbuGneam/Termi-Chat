# 🧠 TermiChat

**TermiChat** is an AI-powered terminal assistant that helps you work smarter with your Linux shell. Ask questions in natural language and get back suggested shell commands — with optional explanations, auto-run mode, safety warnings, and logging.

Made with ❤️ by [Mahmood Gneam](https://www.linkedin.com/in/mahmoodgneam/) — for personal use, now shared with the world.

---

## ✨ Features

- 🔍 Ask natural-language questions about Linux commands
- 💬 Interactive or one-shot usage
- 🧠 `--explain` flag for detailed command breakdowns
- ⚙️ `--run` flag to safely execute suggested commands
- 📜 `--history` logging built-in (to `history.log`)
- 🆘 `--help` flag to get usage instructions
- ℹ️ `--about` flag to learn about TermiChat
- 🔐 Dangerous command detection with warnings
- 🎨 Beautiful CLI styling with `rich`

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/MahmoodAbuGneam/Termi-Chat.git
cd termichat
```

### 2. Set up a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add your API key
Create a `.env` file:
```bash
touch .env
nano .env
```
Paste the following line with your own OpenAI API key:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
🔐 Don’t have an API key yet?
→ Get one from: [openAI API](https://platform.openai.com/account/api-keys)

### 4. Make it globally accessible
```bash
chmod +x ai
sudo ln -s $(pwd)/ai /usr/local/bin/ai
```

---

## 💡 Usage

### One-shot (single question)
```bash
ai "how do I list all hidden files?" --explain
```

### Interactive mode
```bash
ai
```

### With auto-run
```bash
ai "create a folder called test in /tmp" --run
```

---

## 🆘 Help
```bash
ai --help
```
Outputs:
```
TermiChat - AI-powered Linux terminal assistant

Usage:
  ai "your question" [--explain] [--run]
  ai                        # to enter chat mode
  ai --help                # show this message
  ai --about               # show info about this tool
```

---

## ℹ️ About
**TermiChat** was created by Mahmood Gneam as a personal project to make working in the terminal smarter and friendlier. It uses OpenAI’s GPT to turn questions into shell commands, adds smart features like explanation, danger detection, auto-run, and logs everything in a clean CLI interface.

If you find it helpful, feel free to use it, improve it, or share it. 🙌

📇 Connect on [LinkedIn](https://www.linkedin.com/in/mahmoodgneam/)

---

## 🧔 Author
**Mahmood Gneam**  
[LinkedIn](https://www.linkedin.com/in/mahmoodgneam/)

