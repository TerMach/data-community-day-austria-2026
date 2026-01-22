#!/usr/bin/env python3
"""
Process Sessionize data and create structured JSON for the conference app.
"""
import json
import re
from datetime import datetime

# Data ze Sessionize API (zatím mock data, později nahradíme skutečnými)
sessions_data = [
    {
        "id": "1023186",
        "title": "Performance and execution plan improvements in SQL Server 2025",
        "description": "SQL Server 2025 was announced in November 2024, went in public preview in May 2025, and will probably be released at the time of this conference. Join execution plan expert Hugo Kornelis as he takes an in-depth look at some of the new features that affect query performance and execution plans.",
        "speakers": ["Hugo Kornelis"],
        "room": "b.telligent (Foxtrott)",
        "room_id": "foxtrott",
        "start": "2026-01-23T08:15:00Z",
        "end": "2026-01-23T09:15:00Z",
        "duration": 60,
        "floor": None
    },
    {
        "id": "1023187",
        "title": "Building performance engineering culture: scaling optimization practices in Spark Data Engineering",
        "description": "Beyond basic configuration tuning lies systematic Spark performance engineering. This session reveals the diagnostic methods, profiling techniques, and optimization strategies that achieve measurable performance improvements in Microsoft Fabric's Spark runtime.",
        "speakers": ["Estera Kot"],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T08:15:00Z",
        "end": "2026-01-23T09:15:00Z",
        "duration": 60,
        "floor": None
    }
]

speakers_data = [
    {
        "id": "hugo-kornelis",
        "name": "Hugo Kornelis",
        "title": "I make SQL Server fast (.com)",
        "bio": "",
        "photo": "https://sessionize.com/image/55bb-200o200o2-fBnfDb8PkABgBCfbcUTE6Q.jpg"
    },
    {
        "id": "estera-kot",
        "name": "Estera Kot",
        "title": "CTO @ Clouds on Mars",
        "bio": "",
        "photo": "https://sessionize.com/image/b590-200o200o2-DxSmie4fNJd4RuvVRjQoCs.jpg"
    }
]

rooms_data = [
    {"id": "flamenco", "name": "ACP (Flamenco)", "floor": None},
    {"id": "foxtrott", "name": "b.telligent (Foxtrott)", "floor": None},
    {"id": "ballerina", "name": "HEDDA.IO (Ballerina)", "floor": None},
    {"id": "concerto", "name": "Cohesity (Concerto)", "floor": None},
    {"id": "symphonia", "name": "Lucient (Symphonia)", "floor": None},
    {"id": "menuett", "name": "Cubido (Menuett)", "floor": None}
]

def create_conference_data():
    """Create complete conference data structure"""
    conference = {
        "event": {
            "name": "Data Community Austria Day 2026",
            "date": "2026-01-23",
            "location": "JUFA Hotel Wien",
            "timezone": "Europe/Vienna"
        },
        "sessions": sessions_data,
        "speakers": speakers_data,
        "rooms": rooms_data
    }
    return conference

if __name__ == "__main__":
    data = create_conference_data()
    
    # Save to JSON
    with open('data/conference.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Created conference.json with {len(data['sessions'])} sessions")
    print(f"✓ {len(data['speakers'])} speakers")
    print(f"✓ {len(data['rooms'])} rooms")
