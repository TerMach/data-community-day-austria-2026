#!/usr/bin/env python3
"""
Parse complete Sessionize data and create structured JSON
"""
import json
import re
from datetime import datetime

# Všechna data ze Sessionize Sessions API (z toho, co jsme získali)
SESSIONS_RAW = """
Building performance engineering culture: scaling optimization practices in Spark Data Engineering
Estera Kot
ACP (Flamenco)
Fri 9:15 am - 10:15 am
Beyond basic configuration tuning lies systematic Spark performance engineering...

Performance and execution plan improvements in SQL Server 2025
Hugo Kornelis
b.telligent (Foxtrott)
Fri 9:15 am - 10:15 am
SQL Server 2025 was announced in November 2024...

Accidental Data Lies: How Poor Visual Choices Can Mislead
Juliana Smith
HEDDA.IO (Ballerina)
Fri 9:15 am - 10:15 am

Loadtesting Fabric II, the sequel
Reitse Eskens
Cohesity (Concerto)
Fri 9:15 am - 10:15 am
"""

# Rooms mapping
ROOMS = {
    "ACP (Flamenco)": {"id": "flamenco", "floor": None},
    "b.telligent (Foxtrott)": {"id": "foxtrott", "floor": None},
    "HEDDA.IO (Ballerina)": {"id": "ballerina", "floor": None},
    "Cohesity (Concerto)": {"id": "concerto", "floor": None},
    "Lucient (Symphonia)": {"id": "symphonia", "floor": None},
    "Cubido (Menuett)": {"id": "menuett", "floor": None}
}

def create_full_conference_data():
    """Create complete conference data from all available sources"""
    
    # Pro teď vytvoříme ukázková data - v reálné aplikaci by se parsoval celý HTML
    sessions = [
        {
            "id": "session-1",
            "title": "Registration",
            "description": "Conference registration and welcome coffee",
            "speakers": [],
            "room": "ACP (Flamenco)",
            "room_id": "flamenco",
            "start": "2026-01-23T07:00:00Z",
            "end": "2026-01-23T08:00:00Z",
            "duration": 60
        },
        {
            "id": "session-2",
            "title": "Welcome (Main Lobby)",
            "description": "Opening remarks and welcome",
            "speakers": [],
            "room": "ACP (Flamenco)",
            "room_id": "flamenco",
            "start": "2026-01-23T08:00:00Z",
            "end": "2026-01-23T08:15:00Z",
            "duration": 15
        },
        {
            "id": "session-3",
            "title": "Building performance engineering culture: scaling optimization practices in Spark Data Engineering",
            "description": "Beyond basic configuration tuning lies systematic Spark performance engineering. This session reveals the diagnostic methods, profiling techniques, and optimization strategies that achieve measurable performance improvements in Microsoft Fabric's Spark runtime.",
            "speakers": ["Estera Kot"],
            "room": "ACP (Flamenco)",
            "room_id": "flamenco",
            "start": "2026-01-23T08:15:00Z",
            "end": "2026-01-23T09:15:00Z",
            "duration": 60
        },
        {
            "id": "session-4",
            "title": "Performance and execution plan improvements in SQL Server 2025",
            "description": "SQL Server 2025 was announced in November 2024, went in public preview in May 2025, and will probably be released at the time of this conference. Join execution plan expert Hugo Kornelis as he takes an in-depth look at some of the new features that affect query performance and execution plans.",
            "speakers": ["Hugo Kornelis"],
            "room": "b.telligent (Foxtrott)",
            "room_id": "foxtrott",
            "start": "2026-01-23T08:15:00Z",
            "end": "2026-01-23T09:15:00Z",
            "duration": 60
        },
        {
            "id": "session-5",
            "title": "Accidental Data Lies: How Poor Visual Choices Can Mislead",
            "description": "Welcome to the world of accidental data lies, where innocent-looking charts quietly twist the truth. We'll uncover the most common ways charts mislead, from pie chart pandemonium to axis trickery.",
            "speakers": ["Juliana Smith"],
            "room": "HEDDA.IO (Ballerina)",
            "room_id": "ballerina",
            "start": "2026-01-23T08:15:00Z",
            "end": "2026-01-23T09:15:00Z",
            "duration": 60
        },
        {
            "id": "session-6",
            "title": "Loadtesting Fabric II, the sequel",
            "description": "Have you tried to find the most effective way to ingest and process your data? This session will help you learn the differences between Lakehouse, SQLDB, and Warehouse performance.",
            "speakers": ["Reitse Eskens"],
            "room": "Cohesity (Concerto)",
            "room_id": "concerto",
            "start": "2026-01-23T08:15:00Z",
            "end": "2026-01-23T09:15:00Z",
            "duration": 60
        },
        {
            "id": "session-7",
            "title": "Database Deployment Automation using Database Projects & Azure DevOps",
            "description": "You have implemented Database Projects and Azure DevOps for database development successfully and you want to automate your database deployments.",
            "speakers": ["Olivier Van Steenlandt"],
            "room": "Lucient (Symphonia)",
            "room_id": "symphonia",
            "start": "2026-01-23T08:15:00Z",
            "end": "2026-01-23T09:15:00Z",
            "duration": 60
        },
        {
            "id": "session-8",
            "title": "Azure AI Foundry - your go-to AI tool",
            "description": "Azure AI Foundry brings multiple services that enable developers to build amazing AI-powered solutions in a single unified experience.",
            "speakers": ["Tomaž Kaštrun"],
            "room": "Cubido (Menuett)",
            "room_id": "menuett",
            "start": "2026-01-23T08:15:00Z",
            "end": "2026-01-23T09:15:00Z",
            "duration": 60
        },
        {
            "id": "session-break-1",
            "title": "Break",
            "description": "Coffee break",
            "speakers": [],
            "room": "ACP (Flamenco)",
            "room_id": "flamenco",
            "start": "2026-01-23T09:15:00Z",
            "end": "2026-01-23T09:30:00Z",
            "duration": 15
        },
        {
            "id": "session-9",
            "title": "Fabric Capacities, beyond the obvious",
            "description": "While the core concepts of Fabric Capacities bring benefits, they pose some risks that need management strategies.",
            "speakers": ["Benni De Jagere"],
            "room": "ACP (Flamenco)",
            "room_id": "flamenco",
            "start": "2026-01-23T09:30:00Z",
            "end": "2026-01-23T10:30:00Z",
            "duration": 60
        },
        {
            "id": "session-10",
            "title": "Lunch Break",
            "description": "Lunch",
            "speakers": [],
            "room": "ACP (Flamenco)",
            "room_id": "flamenco",
            "start": "2026-01-23T11:45:00Z",
            "end": "2026-01-23T12:45:00Z",
            "duration": 60
        }
    ]
    
    speakers = [
        {
            "id": "estera-kot",
            "name": "Estera Kot",
            "title": "CTO @ Clouds on Mars",
            "bio": "",
            "photo": "https://sessionize.com/image/b590-200o200o2-DxSmie4fNJd4RuvVRjQoCs.jpg"
        },
        {
            "id": "hugo-kornelis",
            "name": "Hugo Kornelis",
            "title": "I make SQL Server fast (.com)",
            "bio": "",
            "photo": "https://sessionize.com/image/55bb-200o200o2-fBnfDb8PkABgBCfbcUTE6Q.jpg"
        },
        {
            "id": "juliana-smith",
            "name": "Juliana Smith",
            "title": "Juliana Smith CITP MBCS",
            "bio": "",
            "photo": "https://sessionize.com/image/6242-200o200o2-WqLQTtiiHYq5fPMonc1B1Q.jpg"
        },
        {
            "id": "reitse-eskens",
            "name": "Reitse Eskens",
            "title": "Data Platform Consultant at Axians Business Analytics, Microsoft MVP and MCT",
            "bio": "",
            "photo": "https://sessionize.com/image/3717-200o200o2-KqKqkDXqA9GynTq1BB67VJ.jpg"
        }
    ]
    
    rooms = [
        {"id": "flamenco", "name": "ACP (Flamenco)", "floor": None},
        {"id": "foxtrott", "name": "b.telligent (Foxtrott)", "floor": None},
        {"id": "ballerina", "name": "HEDDA.IO (Ballerina)", "floor": None},
        {"id": "concerto", "name": "Cohesity (Concerto)", "floor": None},
        {"id": "symphonia", "name": "Lucient (Symphonia)", "floor": None},
        {"id": "menuett", "name": "Cubido (Menuett)", "floor": None}
    ]
    
    return {
        "event": {
            "name": "Data Community Austria Day 2026",
            "date": "2026-01-23",
            "location": "JUFA Hotel Wien",
            "address": "Mautner-Markhof-Gasse 50, 1110 Wien",
            "timezone": "Europe/Vienna"
        },
        "sessions": sessions,
        "speakers": speakers,
        "rooms": rooms
    }

if __name__ == "__main__":
    data = create_full_conference_data()
    
    with open('data/conference.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Created conference.json with {len(data['sessions'])} sessions")
    print(f"✓ {len(data['speakers'])} speakers")
    print(f"✓ {len(data['rooms'])} rooms")
