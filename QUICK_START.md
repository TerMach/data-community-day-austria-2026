# Quick Start - Testing Your Updated Chatbot

## What Was Changed

Your chatbot now uses **spend-based limits** instead of question counts:
- **$0.20 per user per day** (instead of 3 questions)
- **$30 total budget** (instead of $15)
- **Accurate cost tracking** (real token usage)
- **Auto-disable after Jan 23, 2026** (no post-conference costs)

## Start Testing Right Now

### 1. Start the Server

Open your terminal in VS Code and run:
```bash
python server.py
```

You should see:
```
API key loaded successfully

Starting server...
Open: http://localhost:5000
Press Ctrl+C to stop

Using port: 5000
```

### 2. Open the App

Go to: http://localhost:5000

### 3. Test FAQ (FREE Questions)

Try these - they should all be **FREE** (no API call):

```
"When is the conference?"
"Which sessions start at 1:45 PM?"
"Tell me about Hugo Kornelis"
"I'm interested in AI"
"What are my options at 9:15?"
"Sessions about Data Engineering"
```

**What to check:**
- ✅ Instant responses
- ✅ Console shows: "Answered from FAQ (no API call)"
- ✅ No spending tracked

### 4. Test API Calls (COUNTED Questions)

Try these - they will **USE THE API** and count toward your $0.20:

```
"Create a perfect schedule for someone interested in AI and Fabric while avoiding all conflicts"
"Compare the three sessions about performance optimization"
"Which session would be best for a beginner interested in data engineering?"
```

**What to check:**
- ✅ Slightly longer response time
- ✅ Console shows: "Using Claude API for complex question..."
- ✅ Console shows: "💰 This call cost: $0.0187, Total spent today: $0.0187"
- ✅ Spending increases with each call

### 5. Check Your Spending

Open browser console (F12) and look for:
```
💰 This call cost: $0.0187, Total spent today: $0.0187
💰 This call cost: $0.0213, Total spent today: $0.0400
💰 This call cost: $0.0195, Total spent today: $0.0595
```

Or check LocalStorage:
```javascript
localStorage.getItem('apiUsageCount')
// Should show: {"spent":0.0595,"date":"Wed Jan 22 2026"}
```

### 6. Check Usage Dashboard

While server is running, visit:
```
http://localhost:5000/api/usage
```

You'll see:
```json
{
  "date": "2026-01-23",
  "requests": 3,
  "estimated_cost": 0.06,
  "max_requests": 200,
  "max_cost": 30.0,
  "remaining_requests": 197,
  "remaining_budget": 29.94
}
```

### 7. Test the Limit (Optional)

If you want to test hitting the limit:

1. **Temporarily reduce limit** in app.js (line 446):
   ```javascript
   const MAX_SPEND_PER_DAY = 0.05;  // Instead of 0.20
   ```

2. **Refresh browser** (Ctrl+R)

3. **Ask 3-4 complex questions**

4. **You should see:**
   ```
   ⚠️ Daily AI spending limit reached ($0.05 per day).

   This helps keep costs under control.

   You can still browse the schedule and favorites!

   Tip: Try rephrasing your question - the FAQ might have the answer!
   ```

5. **Restore limit** back to 0.20

## What to Expect

### FAQ Questions (90% of usage):
- **Speed:** Instant
- **Cost:** $0.00
- **Count toward limit:** No
- **Examples:** Time queries, session info, speaker info, topic recommendations

### API Questions (10% of usage):
- **Speed:** 2-3 seconds
- **Cost:** $0.015-0.025 each
- **Count toward limit:** Yes
- **Examples:** Complex comparisons, personalized schedules, creative questions

### Per User:
- **Budget:** $0.20 per day
- **Allows:** ~10 API calls
- **Effective:** ~100 total questions (with FAQ)
- **Resets:** Every day at midnight

### Total Conference:
- **Budget:** $30 per day
- **Expected cost:** $3-10
- **Maximum cost:** $30 (hard cap)
- **Protected:** Multiple safety layers

## Verification Checklist

Run through this checklist to verify everything works:

- [ ] Server starts without errors
- [ ] App loads at http://localhost:5000
- [ ] FAQ questions answered instantly (free)
- [ ] Complex questions use API (counted)
- [ ] Console shows spending after API calls
- [ ] LocalStorage tracks spending correctly
- [ ] `/api/usage` endpoint shows statistics
- [ ] Messages display in correct language (EN/CS/DE)
- [ ] Limit message appears after spending $0.20
- [ ] Can still browse schedule after limit

## Console Output Examples

### Server Console:
```
📥 Chat request #1: Create a schedule...
✅ API call #1 successful
📊 Tokens: 1250 in, 680 out
💰 This call: $0.0141, Today's total: $0.14

📥 Chat request #2: Compare these sessions...
✅ API call #2 successful
📊 Tokens: 1100 in, 520 out
💰 This call: $0.0111, Today's total: $0.25
```

### Browser Console:
```
Getting chatbot response for: When is the conference?
✅ Answered from FAQ (no API call)

Getting chatbot response for: Create a perfect schedule...
Using Claude API for complex question...
Detected language: en
Backend response status: 200
API response received successfully
💰 This call cost: $0.0187, Total spent today: $0.0187
```

## Language Testing

Test that the chatbot responds in the correct language:

**English:**
```
"When is the conference?"
→ Should respond in English
```

**Czech:**
```
"Kdy je konference?"
"Řekni mi více o AI sessions"
→ Should respond in Czech
```

**German:**
```
"Wann ist die Konferenz?"
"Erzähl mir mehr über AI Sessions"
→ Should respond in German
```

## Stopping the Server

When you're done testing:
1. Go to terminal where server is running
2. Press **Ctrl+C**
3. Server will stop

## Next Steps

Once testing is complete:

1. ✅ Verify FAQ covers most common questions
2. ✅ Verify spending tracking works correctly
3. ✅ Verify limit messages appear properly
4. ✅ Verify multilingual support works
5. ✅ Verify conference date check (optional)
6. ✅ Adjust limits if needed (app.js and server.py)
7. ✅ Deploy to production (Railway, Render, etc.)

## Configuration Summary

**Current Settings (Recommended for 300 visitors):**

```javascript
// app.js - Line 446
const MAX_SPEND_PER_DAY = 0.20;
```

```python
# server.py - Lines 24-25
MAX_DAILY_REQUESTS = 200
MAX_DAILY_COST = 30.0
```

**Conference Protection:**
```javascript
// app.js - Line 448
const CONFERENCE_DATE = new Date('2026-01-23');
```

```python
# server.py - Line 68
conference_date = datetime(2026, 1, 23).date()
```

## Need Help?

Check these files for detailed information:

- **IMPLEMENTATION_SUMMARY.md** - Complete technical details
- **SPEND_BASED_LIMITS.md** - Comprehensive guide
- **HYBRID_CHATBOT.md** - How the hybrid system works
- **FAQ_COVERAGE.md** - What questions FAQ covers

---

**You're ready to test!** 🚀

**Expected results:**
- 90% questions answered by FAQ (free)
- 10% questions use API (~$0.02 each)
- Total conference cost: $3-10
- Maximum possible cost: $30

**Start testing now by running:** `python server.py`
