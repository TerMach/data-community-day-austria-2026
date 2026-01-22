# Spend-Based Rate Limiting - Implementation Guide

## Overview

Your chatbot now uses **spend-based rate limiting** instead of question count. This gives users more flexibility while maintaining strict budget control.

## Key Changes

### Previous System:
- 3 questions per user per day
- $15 daily budget
- ~100 API calls max

### New System:
- **$0.20 per user per day** (spend limit)
- **$30 daily budget** (total cap)
- ~200 API calls max (safety net)

## How It Works

### Per-User Spending:
```
User opens app
   ↓
Can spend up to $0.20/day
   ↓
Each API call costs ~$0.015-0.025 (based on actual token usage)
   ↓
FAQ answers are FREE (90% of questions)
   ↓
$0.20 = ~10 API calls = ~100 effective questions with FAQ
```

### Backend Protection:
```
Total budget: $30/day
Max requests: 200/day (safety limit)
Real-time cost tracking (actual token usage)
Auto-disable when limit reached
```

## Cost Calculations

### Per-User Budget ($0.20):

**Conservative user (FAQ-heavy):**
- 20 questions total
- 18 answered by FAQ (free)
- 2 use API (2 × $0.02 = $0.04)
- Cost: **$0.04** (well under limit)

**Average user:**
- 30 questions total
- 25 answered by FAQ (free)
- 5 use API (5 × $0.02 = $0.10)
- Cost: **$0.10** (50% of limit)

**Power user:**
- 50 questions total
- 40 answered by FAQ (free)
- 10 use API (10 × $0.02 = $0.20)
- Cost: **$0.20** (hits limit)

### Total Conference Budget ($30):

**Expected scenario (300 visitors):**
- 300 total visitors
- ~100 active app users (33%)
- ~60 ask questions (20%)
- Average spending: $0.06/user
- **Total: $3.60** (12% of budget)

**Popular scenario:**
- 100 active users
- Average spending: $0.10/user
- **Total: $10** (33% of budget)

**Maximum possible:**
- 100 users hit $0.20 limit
- 50 users at $0.10 average
- **Total: $25** (83% of budget)
- Still under $30 cap!

## Safety Margins

### Multiple Protection Layers:

1. **Frontend limit:** $0.20/user/day
2. **Backend request limit:** 200 calls/day
3. **Backend budget cap:** $30/day
4. **FAQ coverage:** 90% of questions free

### Budget Safety:
```
Maximum theoretical: 150 users × $0.20 = $30
Expected realistic: 60 users × $0.06 = $3.60
Safety margin: $26.40 unused budget
```

## User Experience

### What Users Get:

**Within budget ($0.20/day):**
- Unlimited FAQ answers (free)
- ~10 complex AI questions
- ~100 total effective questions
- Full access to all features

**At limit:**
- Clear message explaining limit
- Suggestion to try FAQ
- Can still browse schedule
- Resets next day

### Example User Journey:

```
User: "When is the conference?"
→ FAQ answer (free, instant)

User: "Tell me about AI sessions"
→ FAQ answer (free, recommendation list)

User: "Which sessions start at 1:45?"
→ FAQ answer (free, time-based)

User: "Create a perfect schedule balancing AI and Data Engineering while avoiding all conflicts"
→ AI answer ($0.02, counted toward limit)

User: "Compare these 3 sessions in detail"
→ AI answer ($0.02, counted toward limit)

...after 10 complex AI questions...

User: "Another complex question"
→ "Daily limit reached ($0.20), try FAQ!"
```

## Configuration

### Adjusting Per-User Limit:

**In app.js:**
```javascript
const MAX_SPEND_PER_DAY = 0.20;  // Change this value
```

**Options:**
- $0.10 = ~5 AI calls = ~50 effective questions (conservative)
- $0.20 = ~10 AI calls = ~100 effective questions (current)
- $0.30 = ~15 AI calls = ~150 effective questions (generous)

### Adjusting Total Budget:

**In server.py:**
```python
MAX_DAILY_COST = 30.0  # Current: $30
MAX_DAILY_REQUESTS = 200  # Safety net
```

## Monitoring

### Check Usage:
```
http://localhost:5000/api/usage
```

**Response:**
```json
{
  "date": "2026-01-23",
  "requests": 45,
  "estimated_cost": 8.75,
  "max_requests": 200,
  "max_cost": 30.0,
  "remaining_requests": 155,
  "remaining_budget": 21.25
}
```

### Server Logs:
```
📥 Chat request #12: Which sessions...
✅ Answered from FAQ (no API call)

📥 Chat request #13: Create complex schedule...
✅ API call #8 successful
📊 Tokens: 1250 in, 680 out
💰 This call: $0.0141, Today's total: $0.18
```

## Cost Accuracy

### Real Token-Based Pricing:

**Before:**
- Estimated $0.02 per call (fixed)
- Inaccurate for short/long responses

**Now:**
- Actual cost calculated from tokens
- Short answer: ~$0.015
- Average answer: ~$0.020
- Long answer: ~$0.030
- More accurate budget tracking

**Formula:**
```
Cost = (input_tokens / 1M × $3) + (output_tokens / 1M × $15)
```

## Benefits

### For You:
- ✅ Predictable costs ($3-10 expected, $30 max)
- ✅ More generous per-user limits
- ✅ Accurate cost tracking
- ✅ Multiple safety layers
- ✅ Room for popularity surge

### For Users:
- ✅ More AI questions available
- ✅ Better user experience
- ✅ FAQ still covers most needs
- ✅ Transparent limit system

## Recommendations by Audience Size

### Small Team (10-20 people):
```
Per-user: $0.30 (generous)
Total budget: $30
Expected cost: $2-5
```

### Medium Conference (50-100 people):
```
Per-user: $0.20 (current)
Total budget: $30
Expected cost: $5-12
```

### Large Conference (200+ people):
```
Per-user: $0.15 (conservative)
Total budget: $30
Expected cost: $10-20
```

## Testing

### Test Spend Tracking:

1. Open browser console
2. Ask complex question (not in FAQ)
3. Check console logs:
   ```
   💰 This call cost: $0.0187, Total spent today: $0.0187
   ```
4. LocalStorage shows spending:
   ```javascript
   {
     "spent": 0.0187,
     "date": "Wed Jan 22 2026"
   }
   ```

### Test Limit:

1. Reduce limit in app.js: `MAX_SPEND_PER_DAY = 0.05`
2. Ask 3-4 complex questions
3. Should see limit message
4. Reset limit to $0.20

## Summary

### Configuration:
- Per-user limit: **$0.20/day**
- Total budget: **$30/day**
- Request safety net: **200/day**

### Expected Costs:
- Small usage: **$3-5** for conference
- Medium usage: **$8-12** for conference
- Heavy usage: **$15-20** for conference
- Maximum possible: **$30** (hard cap)

### Safety:
- 90% FAQ coverage (free)
- Multiple protection layers
- Real-time cost tracking
- Automatic disable at limit
- Daily reset

### User Experience:
- ~100 effective questions per user
- ~10 complex AI questions
- Unlimited FAQ answers
- Clear limit messaging

---

**Result: Generous, safe, accurate spend-based chatbot!** 🚀

**Expected cost for 300 visitors:** $3-10
**Maximum possible cost:** $30 (guaranteed)
**User experience:** Excellent with FAQ + AI hybrid
