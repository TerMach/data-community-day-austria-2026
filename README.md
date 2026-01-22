# Data Community Austria Day 2026 - Conference App 🎯

Progressive Web App (PWA) for Data Community Austria Day 2026 with intelligent multilingual AI chatbot.

## 🌟 Features

- 📅 **Complete conference schedule** - all 48 sessions
- 🔍 **Filter by rooms** - focus on specific tracks
- ⭐ **My Schedule** - personalized schedule with favorite sessions
- 🤖 **AI Chatbot** - intelligent assistant supporting **EN, CS, DE**
- 📱 **PWA** - installable on mobile (Android & iOS)
- 💾 **Offline support** - works without internet
- 🎨 **Modern UI** - responsive design

## 🤖 AI Chatbot Capabilities

The chatbot uses Claude AI and can handle complex questions in **three languages**:

**English:**
- "Which sessions start at 1:45 PM?"
- "Summarize each session in 2 sentences"
- "Tell me about Hugo Kornelis"

**Czech:**
- "Které přednášky začínají ve 13:45?"
- "Připrav mi shrnutí každé přednášky na 2 věty"

**German:**
- "Welche Sessions beginnen um 13:45 Uhr?"
- "Fasse jede Session in 2 Sätzen zusammen"

The chatbot automatically detects the language and responds accordingly!

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/[your-username]/data-community-app.git
cd data-community-app
```

### 2. Set up Claude API (Required for AI chatbot)

**Step 1:** Get your API key
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Go to **Settings** → **API Keys**
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-api03-...`)

**Step 2:** Add API key to config.js
1. Open `config.js` in your editor
2. Replace `YOUR_API_KEY_HERE` with your actual key:

```javascript
const CONFIG = {
    ANTHROPIC_API_KEY: 'sk-ant-api03-xxxxxxxxxxxxx'
};
```

3. Save the file
4. ⚠️ **NEVER commit config.js to git!** (It's already in .gitignore)

### 3. Start the Backend Server

The AI chatbot needs a backend server to work (browsers block direct API calls).

```bash
# Install Python dependencies (first time only)
python -m pip install -r requirements.txt

# Start the backend server
python server.py
```

You should see:
```
API key loaded successfully

Starting server...
Open: http://localhost:5000
```

### 4. Open the App

Open your browser to: **http://localhost:5000**

🎉 The chatbot now works with full AI capabilities in all 3 languages!

## 🔒 API Key Security

### For Local Development:
- Use `config.js` (already in .gitignore)
- Never commit your API key

### For GitHub Pages Deployment:
If you want to deploy with chatbot enabled:
1. **Option A:** Use a backend proxy (recommended)
2. **Option B:** Use environment variables with GitHub Actions

⚠️ **IMPORTANT:** Never expose API keys in client-side code on public websites!

### Without API Key:
The app works perfectly fine without an API key:
- Schedule, filters, and favorites work normally
- Chatbot falls back to basic rule-based responses
- Shows helpful message about setting up Claude AI

## 📂 Project Structure

```
data-community-app/
├── index.html              # Main HTML
├── styles.css              # CSS styles
├── app.js                  # JavaScript logic
├── config.js               # API configuration (DO NOT COMMIT!)
├── config.example.js       # Template for config.js
├── manifest.json           # PWA manifest
├── sw.js                   # Service Worker
├── data/
│   └── conference.json     # Conference data (48 sessions, 42 speakers)
└── README.md
```

## 🛠 Tech Stack

- **Frontend:** Vanilla JavaScript (no framework needed)
- **AI:** Claude API (Anthropic) - Sonnet 4.5
- **PWA:** Service Workers, Web App Manifest
- **Storage:** LocalStorage for favorites
- **Hosting:** GitHub Pages (free)

## 🎨 Customization

### Change colors:
```css
/* In styles.css: */
:root {
    --primary: #2563eb;     /* Primary color */
    --secondary: #10b981;   /* Secondary color */
}
```

### Update conference data:
```python
# Run the build script:
python3 build_full_data.py
```

## 📱 Install as App

**Android:**
1. Open app in Chrome
2. Menu (⋮) → "Add to Home Screen"

**iOS:**
1. Open in Safari
2. Share → "Add to Home Screen"

## 💰 Claude API Costs

**Free Tier:**
- $5 free credit for new accounts
- ~50,000 tokens
- Enough for 100-200 chatbot queries

**After free tier:**
- Claude Sonnet 4: ~$3 per million input tokens
- For small conferences: $1-2/month typically

## 🌍 Multilingual Support

The chatbot automatically detects:
- **English** (default)
- **Czech** (detects: který, která, kde, kdy, jak...)
- **German** (detects: welche, wo, wann, wie...)

All UI is in English, but chatbot adapts to user's language!

## 🚢 Deployment

### GitHub Pages:
```bash
# Push to GitHub
git add .
git commit -m "Initial commit"
git push origin main

# Enable GitHub Pages
# Settings → Pages → Source: main branch
```

Your app will be at: `https://[username].github.io/data-community-app/`

## 🤝 Sharing with Colleagues

Share the URL: `https://[username].github.io/data-community-app/`
- Each user has their own "My Schedule" (stored locally)
- Everyone can use the AI chatbot (uses your API key)

## 📄 License

MIT License - free to use for any purpose.

## ⭐ Credits

Built with Claude AI 🤖

---

**Questions?** Open an Issue on GitHub!
