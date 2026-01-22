# 🚀 Deployment Guide - Ready to Share!

## Your App is Ready! ✅

Everything is configured and ready to deploy. Follow these simple steps.

## Step 1: Push to GitHub

```bash
# Initialize git (if not done already)
git init
git add .
git commit -m "Conference app ready for deployment"
git branch -M main

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/data-community-austria-2026.git
git push -u origin main
```

**Important:** `config.js` is in `.gitignore` - your API key is safe! ✅

## Step 2: Deploy to Railway (Recommended - Easiest!)

### Why Railway?
- ✅ Free tier available
- ✅ Auto-detects Python
- ✅ Easy setup (5 minutes)
- ✅ Auto-deploys on git push

### Steps:

1. **Go to:** https://railway.app
2. **Sign up** with GitHub
3. **Click** "New Project" → "Deploy from GitHub repo"
4. **Select** your repository
5. **Add environment variable:**
   - Click "Variables" tab
   - Add new variable:
     - Name: `ANTHROPIC_API_KEY`
     - Value: `[paste your API key from config.js]`
6. **Done!** Railway gives you a URL like:
   `https://data-community-austria-2026.railway.app`

## Alternative: Deploy to Render

1. **Go to:** https://render.com
2. **Sign up** with GitHub
3. **Click** "New" → "Web Service"
4. **Connect** your GitHub repo
5. **Settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python server.py`
6. **Add environment variable:**
   - `ANTHROPIC_API_KEY` = `[your API key]`
7. **Create** - wait ~5 minutes

## Step 3: Test Your App

Visit your deployment URL and test:

- ✅ App loads
- ✅ Schedule visible
- ✅ Chatbot responds
- ✅ Session details work
- ✅ Speaker details clickable
- ✅ Favorites work

## Step 4: Share with Colleagues!

Share your app URL:
- Railway: `https://your-app.railway.app`
- Render: `https://your-app.onrender.com`

## Monitor Costs

Check usage anytime at: `https://your-app.com/api/usage`

Example response:
```json
{
  "requests": 15,
  "estimated_cost": 0.35,
  "remaining_budget": 29.65
}
```

## Expected Costs

- **Testing:** ~$0
- **Conference day:** $3-10
- **Maximum:** $30 (hard cap)

## Safety Features Active

1. ✅ 90% questions answered by FAQ (free)
2. ✅ $0.20 spending limit per user
3. ✅ 200 API requests per day
4. ✅ $30 daily budget cap
5. ✅ Auto-disable after Jan 23, 2026

## Troubleshooting

**App doesn't load?**
- Check Railway/Render build logs
- Verify API key in environment variables

**Chatbot doesn't work?**
- Visit `/api/health` endpoint
- Check if `ANTHROPIC_API_KEY` is set

**Need to update?**
```bash
git add .
git commit -m "Update app"
git push
# Auto-deploys!
```

## Progressive Web App (PWA)

Your app can be installed!

**Mobile:**
1. Open in browser
2. "Add to Home Screen"
3. Works like native app!

**Desktop:**
1. Look for install icon in address bar
2. Click to install

## What's Included

✅ Multilingual chatbot (EN/CS/DE)
✅ Full speaker bios (42 speakers)
✅ Session scheduling
✅ Clickable speaker names
✅ Offline PWA support
✅ Spend-based rate limiting
✅ Auto-disable after conference

---

**Ready to deploy!** 🎉

Questions? Check the other .md files for details!
