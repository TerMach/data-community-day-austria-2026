#!/usr/bin/env python3
"""
Test FAQ matching to verify it catches recommendation questions
"""

import json

# Load FAQ
with open('data/faq.json', 'r', encoding='utf-8') as f:
    faq = json.load(f)

print(f"Loaded {len(faq)} FAQ entries\n")

# Test questions that should be answered by FAQ (FREE)
test_questions = [
    "I'm interested in AI, which sessions should I visit?",
    "Create a schedule for someone interested in Fabric",
    "What sessions are about Data Engineering?",
    "I want to learn about Azure",
    "Sessions about performance optimization?",
    "Which sessions start at 1:45 PM?",
    "What are my options at 9:15?",
    "Tell me about sessions in the first block",
]

def search_faq(question):
    """Simple FAQ matching (mimics frontend logic)"""
    question_lower = question.lower()
    matches = []

    for faq_item in faq:
        score = 0
        for keyword in faq_item['keywords']:
            if keyword.lower() in question_lower:
                score += 10
        if score > 0:
            matches.append({'item': faq_item, 'score': score})

    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[0] if matches else None

print("Testing FAQ matching:\n")
print("=" * 80)

for question in test_questions:
    print(f"\nQ: {question}")
    match = search_faq(question)

    if match:
        print(f"[OK] FAQ Match Found! (score: {match['score']})")
        print(f"   Category: {match['item']['category']}")
        print(f"   Answer preview: {match['item']['answer'][:100]}...")
        print(f"   Cost: $0 (FAQ)")
    else:
        print(f"[X] No FAQ match - would use API")
        print(f"   Cost: ~$0.02 (API call)")

print("\n" + "=" * 80)
print("\nSummary:")
matched = sum(1 for q in test_questions if search_faq(q))
print(f"   FAQ matched: {matched}/{len(test_questions)} questions")
print(f"   Would use API: {len(test_questions) - matched}/{len(test_questions)} questions")
print(f"   Estimated savings: ${matched * 0.02:.2f}")
