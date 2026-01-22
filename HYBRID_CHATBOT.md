# Hybrid Chatbot System - How It Works 🤖

## Overview

Your conference app now has a **smart hybrid chatbot** that minimizes costs while providing excellent user experience!

## 🎯 How It Works

### Step 1: FAQ First (FREE, Instant)
```
User asks question
   ↓
Search 147 FAQ entries
   ↓
Match found? → Return answer (no API call!)
```

**Coverage:**
- ✅ **181 pre-generated Q&A pairs** (updated!)
- ✅ General info (dates, location, rooms)
- ✅ All sessions (summaries, times, speakers)
- ✅ Speaker information
- ✅ Room schedules
- ✅ Time-based queries
- ✅ **Topic recommendations** (AI, Fabric, Data Engineering, etc.)
- ✅ **Session comparisons** (options at same time)

### Step 2: Smart Combining
```
Complex question: "Summarize all sessions in the first block"
   ↓
FAQ matches:
   - "First block sessions"
   - "Summary of session A"
   - "Summary of session B"
   ↓
Combine all answers → Return (still no API call!)
```

### Step 3: Claude API Fallback (Rate Limited)
```
Question not in FAQ
   ↓
Check rate limit (3 questions/user/day)
   ↓
Check budget ($15/day max)
   ↓
Call Claude API → Return answer
```

## 💰 Cost Protection

### Frontend Limits:
- **$0.20 spending per user per day** (~10 API calls = ~100 effective questions with FAQ)
- Stored in browser localStorage
- Resets daily
- Tracks actual spending, not question count

### Backend Limits:
- **200 requests per day max** (safety net)
- **$30 daily budget cap**
- Auto-disables if limit reached
- Real-time cost tracking with actual token usage

### Estimated Costs:

**If 100% FAQ coverage:**
- Cost: **$0** 🎉

**Mixed usage (realistic):**
- 100 attendees
- ~60 ask questions
- Average $0.06 per user
- Cost: **~$3.60** 💰

**Popular usage:**
- 100 active users
- Average $0.10 per user
- Cost: **~$10** 💰

**Heavy usage:**
- 100 users hit $0.20 limit
- Cost: **~$20** 💰

**Maximum possible:**
- Hit $30 budget cap
- Cost: **$30** (hard limit!)

## 📊 What Questions Does FAQ Cover?

### ✅ Fully Covered (100% free):
- "When is the conference?"
- "Where is it?"
- "How many sessions/speakers?"
- "What sessions start at 1:45 PM?"
- "Tell me about session X"
- "Who is speaker Y?"
- "What's in Room Z?"
- "Sessions in first/morning/afternoon block"
- "Summarize session X"

### ⚠️ May Use API:
- "Which session should I attend if I like X?"
- "Compare session A and session B"
- "Create a personalized schedule for me"
- Very unique/creative questions

## 🔧 Configuration

### Adjust Limits:

**Frontend** (app.js):
```javascript
const MAX_SPEND_PER_DAY = 0.20;  // $0.20 per user
```

**Backend** (server.py):
```python
MAX_DAILY_REQUESTS = 200  # Safety net
MAX_DAILY_COST = 30.0     # $30 budget cap
```

### For Smaller Budget:
If you want to be more conservative:
```python
MAX_DAILY_REQUESTS = 100  # Tighter limit
MAX_DAILY_COST = 15.0     # $15 max
```

```javascript
const MAX_SPEND_PER_DAY = 0.10;  // $0.10 per user
```

## 📈 Monitoring

### Check Usage:
```bash
# Visit: http://localhost:5000/api/usage

{
  "date": "2026-01-23",
  "requests": 15,
  "estimated_cost": 0.30,
  "remaining_requests": 85,
  "remaining_budget": 14.70
}
```

### Server Logs Show:
```
📥 Chat request #1: Which sessions start...
✅ API call #1 successful
💰 Today's usage: 1 requests, ~$0.02
```

## 🎯 FAQ Generation

### To Update FAQ:
```bash
# Edit generate_faq.py if needed
python generate_faq.py

# This creates data/faq.json with all Q&A
```

### FAQ Structure:
```json
{
  "question": "Which sessions start at 9:15?",
  "answer": "Sessions at 9:15: ...",
  "keywords": ["9:15", "sessions at", "start 9:15"],
  "category": "time"
}
```

## ✅ Security Features

### Frontend:
- ✅ Rate limiting per user
- ✅ FAQ-first search
- ✅ Daily reset

### Backend:
- ✅ Request counting
- ✅ Cost estimation
- ✅ Budget caps
- ✅ Auto-disable when limit hit
- ✅ Usage logging

### No Exposed Secrets:
- ✅ API key in backend only
- ✅ Environment variables supported
- ✅ Not exposed to client

## 🚀 Deployment Safety

### For 10 Colleagues:
```
Expected: $0-2 for the conference
Budget: $5-15 is very safe
```

### For 100 Attendees:
```
Expected: $2-5 for the conference
Budget: $15 cap ensures safety
Worst case: Hits limit, stops at $15
```

## 📝 What Users See

### When FAQ Answers:
```
User: "Which sessions start at 1:45 PM?"
Bot: "Sessions starting at 13:45: ..."
[Instant, free]
```

### When API Answers:
```
User: "Create a schedule for someone interested in data engineering"
Bot: [Claude's intelligent response]
[~$0.02, counts toward daily limit]
```

### When Limit Hit:
```
User: [After spending $0.20]
Bot: "⚠️ Daily AI spending limit reached ($0.20 per day).
      This helps keep costs under control.
      You can still browse the schedule!
      Tip: Try rephrasing your question - the FAQ might have the answer!"
```

## 🎉 Benefits

### For You:
- ✅ Predictable costs ($3-10 expected, $30 max)
- ✅ Safe for public use
- ✅ No risk of runaway charges
- ✅ Easy monitoring
- ✅ Accurate token-based cost tracking

### For Users:
- ✅ Instant answers (FAQ)
- ✅ Intelligent fallback (Claude)
- ✅ Works offline (FAQ)
- ✅ Multilingual (EN, CS, DE)

---

**Result:** Smart, safe, affordable chatbot! 🚀

**Total Cost for Conference Day:** $3-10 (estimate)
**Maximum Possible Cost:** $30 (hard cap)
**Safety:** Very high! ✅

**Note:** Chatbot automatically disables after January 23, 2026 to prevent costs after the conference.
