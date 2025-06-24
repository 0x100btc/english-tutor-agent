# English Voice Tutor Bot

This is a modular Telegram bot for English tutoring, powered by OpenAI and voice features.

## 📁 Project Structure

```
english_voice_tutor/
├── main.py
├── handlers/
│   └── __init__.py
│   └── command.py
│   └── quiz.py
├── services/
│   └── openai_agent.py
│   └── tts.py
│   └── stripe.py
├── db/
│   └── models.py
│   └── database.py
├── shared/
│   └── utils.py
├── tests/
│   └── __init__.py
├── requirements.txt
└── .gitignore
```

## 🧠 Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the bot:

```bash
python main.py
```

## ⚙️ Git Usage

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/english_voice_tutor.git
git branch -M main
git push -u origin main
```

## 🐍 Poetry (Optional)

如果你想改用 Poetry：

```bash
poetry init
poetry add openai python-telegram-bot flask gtts stripe
```
