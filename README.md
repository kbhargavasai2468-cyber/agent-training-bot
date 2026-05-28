# 🏢 SriVarma Properties — Agent Training AI Bot

A smart chatbot that trains real estate agents by answering questions about company policies, pricing, documents, and processes. Supports English and Telugu.

---

## 🚀 How to Run (Step by Step)

### Step 1: Install Python packages
Open your terminal/command prompt in this folder and run:
```
pip install flask openai
```

### Step 2: Run the app
```
python app.py
```

### Step 3: Open in browser
Go to: **http://localhost:5000**

### Step 4: Enter your API key
Paste your OpenAI API key (starts with `sk-`) in the setup screen.

---

## 💬 Features
- Ask questions in English or Telugu
- 6 quick-question shortcuts on the home screen
- Typing animation while AI thinks
- Full conversation memory (last 6 messages)
- Reset chat anytime
- Professional dark UI with gold theme

## 📁 File Structure
```
agent_training_bot/
├── app.py              ← Backend (Flask + AI logic)
├── requirements.txt    ← Dependencies
├── README.md           ← This file
└── templates/
    └── index.html      ← Chat UI
```

## 🛠 Tech Stack
- **Backend**: Python, Flask
- **AI**: OpenAI GPT-3.5 Turbo
- **Frontend**: HTML, CSS, JavaScript
- **Knowledge Base**: Built-in training data (can be extended)

