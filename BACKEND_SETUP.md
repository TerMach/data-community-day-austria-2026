# Backend Setup Guide 🚀

The AI chatbot requires a backend server to work due to browser security (CORS) restrictions.

## Why Do We Need a Backend?

Browsers block direct API calls from JavaScript to external APIs like Claude for security reasons. The backend acts as a proxy:

```
Browser → Your Backend → Claude API → Your Backend → Browser
```

## Quick Setup

### 1. Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

This installs:
- **Flask** - Web server
- **Flask-CORS** - Handle cross-origin requests
- **Requests** - Make API calls to Claude

### 2. Make Sure API Key is in config.js

Your `config.js` should have your Anthropic API key:

```javascript
const CONFIG = {
    ANTHROPIC_API_KEY: 'sk-ant-api03-xxxxxxxxxxxxx'
};
```

The backend will automatically read this file.

### 3. Start the Backend Server

```bash
python server.py
```

You should see:

```
✅ API key loaded successfully

🚀 Starting server...
   Open: http://localhost:5000
   Press Ctrl+C to stop
```

### 4. Open the App

Open your browser to: **http://localhost:5000**

(Note: Use port **5000** not 8000 - the backend serves everything)

## Testing the Chatbot

Try these questions in different languages:

**English:**
- "Which sessions start at 1:45 PM?"
- "Give me an overview of all sessions in the first block, summarize each in 2 sentences"
- "Tell me about Hugo Kornelis"

**Czech:**
- "Udělej mi přehled všech přednášek z prvního bloku"
- "Které session začínají ve 13:45?"

**German:**
- "Welche Sessions beginnen um 13:45 Uhr?"
- "Fasse jede Session zusammen"

## Troubleshooting

### "Backend Server Not Running"

**Problem:** The frontend can't connect to the backend.

**Solution:**
1. Make sure `server.py` is running
2. Check you're using **http://localhost:5000** (not 8000)
3. Look at the terminal for error messages

### "API Key Not Configured"

**Problem:** The backend can't find your API key.

**Solution:**
1. Check `config.js` exists and has your key
2. Restart the server: `Ctrl+C` then `python server.py`

### "API Error: 401"

**Problem:** Your API key is invalid.

**Solution:**
1. Get a new key from https://console.anthropic.com/
2. Update `config.js`
3. Restart the server

### "API Error: 429"

**Problem:** Rate limit exceeded (too many requests).

**Solution:**
- Wait a few minutes
- Check your usage at console.anthropic.com
- Consider upgrading if needed

### Import Error: No module named 'flask'

**Problem:** Dependencies not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

## How It Works

### Backend (server.py)

```python
@app.route('/api/chat', methods=['POST'])
def chat():
    # Receives question from frontend
    # Calls Claude API
    # Returns response to frontend
```

### Frontend (app.js)

```javascript
async getChatbotResponse(message) {
    // Send question to backend
    const response = await fetch('/api/chat', {
        method: 'POST',
        body: JSON.stringify({ message, prompt })
    });
    // Display response
}
```

## API Endpoints

### POST /api/chat
Request:
```json
{
    "message": "Which sessions start at 1:45 PM?",
    "prompt": "[full context + question]",
    "language": "en"
}
```

Response:
```json
{
    "content": [
        {
            "text": "Here are the sessions..."
        }
    ]
}
```

### GET /api/health
Check if server is running:
```json
{
    "status": "ok",
    "api_key_configured": true
}
```

## Production Deployment

For production (GitHub Pages, Netlify, etc.), you have options:

### Option 1: Serverless Functions (Recommended)
- **Vercel** - Free tier, easy setup
- **Netlify Functions** - Free tier
- **AWS Lambda** - Scalable

### Option 2: Backend Server
- **Railway.app** - Free tier
- **Render** - Free tier
- **Heroku** - Paid

### Option 3: Edge Functions
- **Cloudflare Workers** - Fast, global
- **Deno Deploy** - Edge runtime

## Security Notes

⚠️ **Important:**
- Never commit `config.js` (already in .gitignore)
- The backend reads the API key securely
- For production, use environment variables
- Consider rate limiting for public deployments

## Development vs Production

**Development (Local):**
```bash
python server.py
# Opens on localhost:5000
```

**Production:**
- Deploy backend separately
- Update frontend to use production API URL
- Use environment variables for API key

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Start server: `python server.py`
3. ✅ Open: http://localhost:5000
4. ✅ Test chatbot in multiple languages
5. 🚀 Deploy to production (optional)

---

**Need help?** Check the main README.md or open an issue!
