# Quick Start - In 3 Steps! 🚀

## Step 1: Add Your API Key ✅ DONE!

Your `config.js` already has your API key configured.

## Step 2: Start the Backend Server

```bash
# Install dependencies (first time only)
python -m pip install -r requirements.txt

# Start the server
python server.py
```

You should see:
```
API key loaded successfully
Starting server...
Open: http://localhost:5000
```

## Step 3: Open the App

Go to: **http://localhost:5000**

## Test the AI Chatbot

Try asking these questions in **any language**:

### English
```
Which sessions start at 1:45 PM?
Give me an overview of all sessions in the first block
Tell me about Hugo Kornelis
```

### Czech
```
Udělej mi přehled všech přednášek z prvního bloku
Které session začínají ve 13:45?
Řekni mi víc o Hugo Kornelisovi
```

### German
```
Welche Sessions beginnen um 13:45 Uhr?
Fasse jede Session zusammen
```

## What You'll See

The chatbot will:
- ✅ Automatically detect your language
- ✅ Respond in the same language
- ✅ Give intelligent, contextual answers
- ✅ Summarize sessions
- ✅ Answer complex questions

## Troubleshooting

### "Backend Server Not Running"
- Make sure you started `python server.py`
- Use port **5000** not 8000

### "API Error"
- Check your API key in `config.js`
- Make sure it starts with `sk-ant-api03-`
- Restart the server

### Need More Help?
- Read `BACKEND_SETUP.md` for detailed info
- Read `README.md` for full documentation

---

**That's it!** Your intelligent multilingual conference app is ready! 🎉
