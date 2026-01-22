#!/usr/bin/env python3
"""
Generate comprehensive FAQ from conference data
This runs ONCE during development to create faq.json
"""

import json
from datetime import datetime

# Load conference data
with open('data/conference.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

faq = []

# Helper function to format time
def format_time(iso_string):
    dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
    return dt.strftime('%H:%M')

# Get real sessions (exclude breaks/registration)
real_sessions = [s for s in data['sessions'] if s['speakers']]

# Group sessions by time block
sessions_by_time = {}
for session in real_sessions:
    time_key = session['start'][:16]  # Group by hour:minute
    if time_key not in sessions_by_time:
        sessions_by_time[time_key] = []
    sessions_by_time[time_key].append(session)

# Sort time blocks
sorted_times = sorted(sessions_by_time.keys())

print(f"Generating FAQ for {len(real_sessions)} sessions...")
print(f"Time blocks: {len(sorted_times)}")

# ===================
# 1. GENERAL QUESTIONS
# ===================

faq.append({
    "question": "When is the conference?",
    "answer": "The Data Community Austria Day 2026 takes place on January 23, 2026 at JUFA Hotel Wien.",
    "keywords": ["when", "date", "day", "time", "kdy", "datum", "wann", "datum"],
    "category": "general"
})

faq.append({
    "question": "Where is the conference?",
    "answer": "The conference is held at JUFA Hotel Wien in Vienna, Austria.",
    "keywords": ["where", "location", "venue", "place", "kde", "místo", "wo", "ort"],
    "category": "general"
})

faq.append({
    "question": "How many sessions are there?",
    "answer": f"There are {len(real_sessions)} sessions (excluding breaks and registration).",
    "keywords": ["how many sessions", "number of sessions", "kolik sessions", "wie viele sessions"],
    "category": "general"
})

faq.append({
    "question": "How many speakers?",
    "answer": f"There are {len(data['speakers'])} speakers at the conference.",
    "keywords": ["how many speakers", "number of speakers", "kolik speakerů", "wie viele speaker"],
    "category": "general"
})

faq.append({
    "question": "What rooms are available?",
    "answer": f"The conference uses {len(data['rooms'])} rooms: {', '.join([r['name'] for r in data['rooms']])}.",
    "keywords": ["rooms", "místnosti", "räume", "which rooms"],
    "category": "general"
})

# ===================
# 2. SESSION SUMMARIES
# ===================

print("Generating session summaries...")
for session in real_sessions:
    time_str = format_time(session['start'])

    # Individual session summary
    faq.append({
        "question": f"Tell me about {session['title']}",
        "answer": f"{session['title']} is at {time_str} in {session['room']} by {', '.join(session['speakers'])}. {session['description']}",
        "keywords": [session['title'].lower(), session['id']] + [s.lower() for s in session['speakers']],
        "category": "session"
    })

    # Session summary (short)
    faq.append({
        "question": f"Summarize {session['title']}",
        "answer": f"{session['description'][:200]}{'...' if len(session['description']) > 200 else ''}",
        "keywords": [f"summarize {session['title'].lower()}", f"summary {session['title'].lower()}"],
        "category": "summary"
    })

# ===================
# 3. SPEAKER QUESTIONS
# ===================

print("Generating speaker info...")
for speaker in data['speakers']:
    # Find speaker's sessions
    speaker_sessions = [s for s in real_sessions if speaker['name'] in s['speakers']]

    if speaker_sessions:
        sessions_list = ', '.join([f'"{s["title"]}" at {format_time(s["start"])}' for s in speaker_sessions])

        # Build speaker info with title and bio
        speaker_info = f"{speaker['name']}"
        if speaker.get('title'):
            speaker_info += f" - {speaker['title']}"

        # Add bio if available
        if speaker.get('bio'):
            answer = f"{speaker_info}\n\n{speaker['bio']}\n\nSpeaking at: {sessions_list}."
        else:
            answer = f"{speaker_info}\n\nSpeaking at: {sessions_list}."

        faq.append({
            "question": f"Who is {speaker['name']}?",
            "answer": answer,
            "keywords": [speaker['name'].lower(), f"who is {speaker['name'].lower()}", f"about {speaker['name'].lower()}", f"tell me about {speaker['name'].lower()}", f"more about {speaker['name'].lower()}", f"information about {speaker['name'].lower()}"],
            "category": "speaker"
        })

# ===================
# 4. TIME-BASED QUESTIONS
# ===================

print("Generating time-based questions...")
for time_key in sorted_times:
    sessions = sessions_by_time[time_key]
    time_str = format_time(time_key)

    # Sessions at specific time
    sessions_list = ' | '.join([f"{s['title']} ({s['room']})" for s in sessions])

    faq.append({
        "question": f"Which sessions start at {time_str}?",
        "answer": f"Sessions starting at {time_str}: {sessions_list}",
        "keywords": [f"sessions at {time_str}", f"{time_str}", f"start {time_str}", f"začínají {time_str}"],
        "category": "time"
    })

# ===================
# 5. ROOM-BASED QUESTIONS
# ===================

print("Generating room-based questions...")
for room in data['rooms']:
    room_sessions = [s for s in real_sessions if s['room_id'] == room['id']]

    if room_sessions:
        sessions_list = '\n'.join([f"• {format_time(s['start'])} - {s['title']}" for s in room_sessions])

        faq.append({
            "question": f"What sessions are in {room['name']}?",
            "answer": f"Sessions in {room['name']}:\n{sessions_list}",
            "keywords": [room['name'].lower(), f"sessions in {room['name'].lower()}", f"room {room['name'].lower()}"],
            "category": "room"
        })

# ===================
# 6. BLOCK-BASED QUESTIONS
# ===================

print("Generating block-based questions...")
# Define blocks (adjust based on your schedule)
blocks = {
    "first": sorted_times[:4] if len(sorted_times) >= 4 else sorted_times,
    "morning": [t for t in sorted_times if '09:' in t or '10:' in t or '11:' in t],
    "afternoon": [t for t in sorted_times if '13:' in t or '14:' in t or '15:' in t],
    "last": sorted_times[-3:] if len(sorted_times) >= 3 else sorted_times
}

for block_name, block_times in blocks.items():
    block_sessions = []
    for time_key in block_times:
        block_sessions.extend(sessions_by_time.get(time_key, []))

    if block_sessions:
        sessions_list = '\n'.join([
            f"• {format_time(s['start'])} - {s['title']} by {', '.join(s['speakers'])}"
            for s in block_sessions
        ])

        faq.append({
            "question": f"Which sessions are in the {block_name} block?",
            "answer": f"Sessions in the {block_name} block:\n{sessions_list}",
            "keywords": [f"{block_name} block", f"{block_name} sessions", f"první blok" if block_name == "first" else ""],
            "category": "block"
        })

# ===================
# 7. TOPIC/INTEREST-BASED RECOMMENDATIONS
# ===================

print("Generating topic-based recommendations...")

# Extract common topics from session titles and descriptions
topics = {
    "AI": ["AI", "artificial intelligence", "machine learning", "ML", "neural", "GPT", "LLM"],
    "Fabric": ["Fabric", "Microsoft Fabric"],
    "Data Engineering": ["data engineering", "pipeline", "ETL", "data integration", "Spark"],
    "Analytics": ["analytics", "analysis", "BI", "business intelligence", "reporting"],
    "Azure": ["Azure", "Microsoft Azure", "cloud"],
    "SQL": ["SQL", "database", "query", "T-SQL"],
    "Python": ["Python", "pandas", "numpy"],
    "Performance": ["performance", "optimization", "tuning", "scaling"],
    "Data Quality": ["data quality", "testing", "validation"],
    "Visualization": ["visualization", "Power BI", "dashboard", "chart"],
    "Data Governance": ["governance", "security", "compliance", "privacy"],
    "Real-time": ["real-time", "streaming", "event", "Kafka"],
    "Data Science": ["data science", "statistics", "modeling", "prediction"],
    "Architecture": ["architecture", "design pattern", "medallion", "lakehouse"]
}

for topic_name, keywords in topics.items():
    # Find sessions matching this topic
    matching_sessions = []

    for session in real_sessions:
        # Check if any keyword appears in title or description
        text = f"{session['title']} {session['description']}".lower()
        if any(keyword.lower() in text for keyword in keywords):
            matching_sessions.append(session)

    if matching_sessions:
        # Create recommendation
        sessions_list = '\n'.join([
            f"• {format_time(s['start'])} - {s['title']} ({s['room']}) by {', '.join(s['speakers'])}"
            for s in matching_sessions
        ])

        recommendation_text = f"Sessions about {topic_name}:\n{sessions_list}"

        # Add multiple question variations
        question_variations = [
            f"I'm interested in {topic_name}",
            f"interested in {topic_name}",
            f"sessions about {topic_name}",
            f"recommend {topic_name}",
            f"schedule for {topic_name}",
            topic_name.lower()
        ]

        faq.append({
            "question": f"What sessions should I attend if I'm interested in {topic_name}?",
            "answer": recommendation_text,
            "keywords": question_variations,
            "category": "recommendation"
        })

# ===================
# 8. SPEAKER EXPERTISE RECOMMENDATIONS
# ===================

print("Generating speaker expertise recommendations...")

# Group sessions by common themes for speaker recommendations
speaker_themes = {}
for session in real_sessions:
    for speaker in session['speakers']:
        if speaker not in speaker_themes:
            speaker_themes[speaker] = []
        speaker_themes[speaker].append(session)

# Create "speakers who talk about X" FAQs
for topic_name, keywords in topics.items():
    relevant_speakers = []

    for speaker, sessions in speaker_themes.items():
        for session in sessions:
            text = f"{session['title']} {session['description']}".lower()
            if any(keyword.lower() in text for keyword in keywords):
                relevant_speakers.append({
                    'name': speaker,
                    'session': session
                })
                break  # Only count speaker once

    if relevant_speakers:
        speakers_list = '\n'.join([
            f"• {s['name']} - {s['session']['title']} at {format_time(s['session']['start'])}"
            for s in relevant_speakers
        ])

        faq.append({
            "question": f"Which speakers talk about {topic_name}?",
            "answer": f"Speakers covering {topic_name}:\n{speakers_list}",
            "keywords": [f"speakers {topic_name.lower()}", f"who talks about {topic_name.lower()}", f"{topic_name.lower()} experts"],
            "category": "recommendation"
        })

# ===================
# 9. COMPARATIVE QUESTIONS
# ===================

print("Generating comparative FAQs...")

# Sessions happening at the same time (choices)
for time_key in sorted_times:
    sessions = sessions_by_time[time_key]
    if len(sessions) > 1:
        time_str = format_time(time_key)

        # Create comparison
        comparison = '\n'.join([
            f"• {s['room']}: {s['title']} by {', '.join(s['speakers'])}\n  {s['description'][:150]}..."
            for s in sessions
        ])

        faq.append({
            "question": f"What are my options at {time_str}?",
            "answer": f"At {time_str}, you can choose from:\n{comparison}",
            "keywords": [f"options {time_str}", f"choose {time_str}", f"which session {time_str}", f"conflict {time_str}"],
            "category": "comparison"
        })

# ===================
# SAVE FAQ
# ===================

output_file = 'data/faq.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(faq, f, indent=2, ensure_ascii=False)

print(f"\nGenerated {len(faq)} FAQ entries")
print(f"Saved to: {output_file}")
print(f"\nCategories:")
for category in ['general', 'session', 'speaker', 'time', 'room', 'block', 'summary', 'recommendation', 'comparison']:
    count = len([q for q in faq if q['category'] == category])
    if count > 0:
        print(f"  - {category}: {count}")
