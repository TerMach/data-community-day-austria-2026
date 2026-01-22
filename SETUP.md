# Setup Instructions 🚀

Quick guide to get your conference app running with AI chatbot.

## 1. Get Claude API Key

### Step 1: Create Anthropic Account
1. Go to **https://console.anthropic.com/**
2. Click **Sign Up** (or Sign In if you have an account)
3. Complete registration

### Step 2: Generate API Key
1. In the console, go to **Settings** → **API Keys**
2. Click **Create Key**
3. Give it a name (e.g., "Conference App")
4. **Copy the key** - it looks like: `sk-ant-api03-xxxxxxxxxxxxx`
5. ⚠️ Save it somewhere safe - you won't see it again!

## 2. Add API Key to App

### Open config.js
1. Open the file `config.js` in your text editor
2. Find this line:
   ```javascript
   ANTHROPIC_API_KEY: 'YOUR_API_KEY_HERE'
   ```

3. Replace `YOUR_API_KEY_HERE` with your actual key:
   ```javascript
   ANTHROPIC_API_KEY: 'sk-ant-api03-xxxxxxxxxxxxx'
   ```

4. **Save the file**

### Example:
```javascript
const CONFIG = {
    ANTHROPIC_API_KEY: 'sk-ant-api03-abc123def456ghi789jkl012mno345'
};
```

## 3. Run the App

### Option A: Python
```bash
python3 -m http.server 8000
```
Then open: **http://localhost:8000**

### Option B: Node.js
```bash
npx serve
```
Then open the URL shown in terminal

## 4. Test the Chatbot

1. Click the **🤖 Chatbot** tab
2. Try these questions:

**English:**
- "Which sessions start at 1:45 PM?"
- "Tell me about Hugo Kornelis"
- "Summarize the first session"

**Czech:**
- "Které přednášky začínají ve 13:45?"
- "Co je v místnosti Room 1?"

**German:**
- "Welche Sessions beginnen um 13:45 Uhr?"
- "Fasse die erste Session zusammen"

## 5. Security Check ✅

**Before committing to Git:**

1. Verify `.gitignore` contains:
   ```
   config.js
   ```

2. Check what will be committed:
   ```bash
   git status
   ```

3. **config.js should NOT appear in the list!**

4. If it does appear:
   ```bash
   git rm --cached config.js
   echo "config.js" >> .gitignore
   ```

## Troubleshooting 🔧

### Chatbot shows "API not configured"
- Check if `config.js` exists
- Verify API key is correctly copied
- Reload the page (Ctrl+Shift+R)

### API Error 401 (Unauthorized)
- Your API key is invalid or expired
- Generate a new key in console.anthropic.com

### API Error 429 (Rate Limit)
- You've exceeded free tier limits
- Check usage at console.anthropic.com
- Consider upgrading or waiting

### Chatbot responds in wrong language
- The language detection is automatic based on keywords
- Try using more specific language keywords
- Example: Use "Které" instead of "Which" for Czech

## API Costs 💰

**Free Tier:**
- $5 credit for new accounts
- ~100-200 chatbot queries
- Perfect for testing!

**Paid Tier:**
- ~$3 per million input tokens
- For a small conference: $1-2/month

## What's Next?

- ✅ App is running with AI chatbot
- ✅ Test all features (Schedule, My Schedule, Chatbot)
- ✅ Install as PWA on your phone
- 🚀 Deploy to GitHub Pages (optional)

---

**Need help?** Check README.md or open an issue on GitHub!
