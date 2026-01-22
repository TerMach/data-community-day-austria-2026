#!/usr/bin/env python3
"""
Fetch speaker bios from Sessionize API and update conference.json
"""

import json
import requests

# Sessionize API endpoint
SESSIONIZE_API = "https://sessionize.com/api/v2/q7xnnhex/view/All"

print("Fetching data from Sessionize API...")
response = requests.get(SESSIONIZE_API)

if response.status_code != 200:
    print(f"Error: Failed to fetch data (status {response.status_code})")
    exit(1)

sessionize_data = response.json()
print(f"✓ Fetched data successfully")

# Load current conference.json
print("\nLoading current conference.json...")
with open('data/conference.json', 'r', encoding='utf-8') as f:
    conference_data = json.load(f)

print(f"Current speakers: {len(conference_data['speakers'])}")

# Create mapping of speaker names to sessionize data
sessionize_speakers = {}

# Find speakers in sessionize data
if isinstance(sessionize_data, list):
    for item in sessionize_data:
        if 'speakers' in item:
            for speaker in item['speakers']:
                name = speaker.get('fullName') or speaker.get('name')
                if name:
                    sessionize_speakers[name] = speaker
        if 'sessions' in item:
            for session in item['sessions']:
                if 'speakers' in session:
                    for speaker in session['speakers']:
                        name = speaker.get('fullName') or speaker.get('name')
                        if name:
                            sessionize_speakers[name] = speaker

print(f"Found {len(sessionize_speakers)} speakers in Sessionize data")

# Update bios
updated_count = 0
for speaker in conference_data['speakers']:
    name = speaker['name']
    if name in sessionize_speakers:
        sessionize_speaker = sessionize_speakers[name]

        # Update bio if available
        bio = sessionize_speaker.get('bio') or sessionize_speaker.get('biography') or ""
        if bio and bio != speaker.get('bio', ''):
            print(f"\n✓ Updating bio for: {name}")
            print(f"  Bio length: {len(bio)} characters")
            speaker['bio'] = bio
            updated_count += 1

        # Update title if different
        tagline = sessionize_speaker.get('tagLine') or sessionize_speaker.get('title')
        if tagline and tagline != speaker.get('title', ''):
            print(f"  Updating tagline: {tagline}")
            speaker['title'] = tagline

print(f"\n{'='*60}")
print(f"Updated {updated_count} speaker bios")

# Save updated conference.json
print("\nSaving updated conference.json...")
with open('data/conference.json', 'w', encoding='utf-8') as f:
    json.dump(conference_data, f, indent=2, ensure_ascii=False)

print("✓ Conference data updated successfully!")
print("\nNext step: Run 'python generate_faq.py' to regenerate FAQ with bios")
