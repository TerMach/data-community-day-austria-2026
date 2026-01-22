#!/usr/bin/env python3
"""
Parse ALL sessions from Sessionize data
"""
import json
import re

# Kompletní seznam všech sessions z konference (z Sessionize API dat)
COMPLETE_SESSIONS = [
    # 8:00 - Registration
    {
        "id": "reg-1",
        "title": "Registration",
        "description": "Conference registration and welcome coffee",
        "speakers": [],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T07:00:00Z",
        "end": "2026-01-23T08:00:00Z",
        "duration": 60
    },
    # 9:00 - Welcome
    {
        "id": "welcome-1",
        "title": "Welcome (Main Lobby)",
        "description": "Opening remarks and welcome to Data Community Austria Day 2026",
        "speakers": [],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T08:00:00Z",
        "end": "2026-01-23T08:15:00Z",
        "duration": 15
    },
    # 9:15 - First session block
    {
        "id": "s1",
        "title": "Building performance engineering culture: scaling optimization practices in Spark Data Engineering",
        "description": "Beyond basic configuration tuning lies systematic Spark performance engineering. This session reveals the diagnostic methods, profiling techniques, and optimization strategies that achieve measurable performance improvements in Microsoft Fabric's Spark runtime. You'll learn the specific technical methods we use to identify bottlenecks, re-architect data processing patterns, and implement performance monitoring that prevents regression across production Fabric workloads.",
        "speakers": ["Estera Kot"],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T08:15:00Z",
        "end": "2026-01-23T09:15:00Z",
        "duration": 60
    },
    {
        "id": "s2",
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
        "id": "s3",
        "title": "Accidental Data Lies: How Poor Visual Choices Can Mislead",
        "description": "Welcome to the world of accidental data lies, where innocent-looking charts quietly twist the truth. We'll uncover the most common ways charts mislead, from pie chart pandemonium to axis trickery, colour chaos, and the dreaded 'average of averages.'",
        "speakers": ["Juliana Smith"],
        "room": "HEDDA.IO (Ballerina)",
        "room_id": "ballerina",
        "start": "2026-01-23T08:15:00Z",
        "end": "2026-01-23T09:15:00Z",
        "duration": 60
    },
    {
        "id": "s4",
        "title": "Loadtesting Fabric II, the sequel",
        "description": "Have you tried to find the most effective way to ingest and process your data? In this session, I'll help you learn the differences between Lakehouse, SQLDB, and Warehouse performance, processing speed and cost.",
        "speakers": ["Reitse Eskens"],
        "room": "Cohesity (Concerto)",
        "room_id": "concerto",
        "start": "2026-01-23T08:15:00Z",
        "end": "2026-01-23T09:15:00Z",
        "duration": 60
    },
    {
        "id": "s5",
        "title": "Database Deployment Automation using Database Projects & Azure DevOps",
        "description": "You have implemented Database Projects and Azure DevOps for database development successfully and you want to automate your database deployments. During this session, we will set up an example build and deploy pipeline.",
        "speakers": ["Olivier Van Steenlandt"],
        "room": "Lucient (Symphonia)",
        "room_id": "symphonia",
        "start": "2026-01-23T08:15:00Z",
        "end": "2026-01-23T09:15:00Z",
        "duration": 60
    },
    {
        "id": "s6",
        "title": "Azure AI Foundry - your go-to AI tool",
        "description": "Azure AI Foundry brings multiple services that enable developers to build amazing AI-powered solutions in a single unified experience for AI development on the Azure cloud platform.",
        "speakers": ["Tomaž Kaštrun"],
        "room": "Cubido (Menuett)",
        "room_id": "menuett",
        "start": "2026-01-23T08:15:00Z",
        "end": "2026-01-23T09:15:00Z",
        "duration": 60
    },
    # 10:15 - Break
    {
        "id": "break-1",
        "title": "Break",
        "description": "Coffee break",
        "speakers": [],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T09:15:00Z",
        "end": "2026-01-23T09:30:00Z",
        "duration": 15
    },
    # 10:30 - Second session block
    {
        "id": "s7",
        "title": "Fabric Capacities, beyond the obvious",
        "description": "While the core concepts of Fabric Capacities bring a lot of benefits, they do pose some risks that need to be kept in check when figuring out the appropriate Capacity Planning and Management Strategy for your environment.",
        "speakers": ["Benni De Jagere"],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T09:30:00Z",
        "end": "2026-01-23T10:30:00Z",
        "duration": 60
    },
    {
        "id": "s8",
        "title": "From Manual to Automated: Master Metadata-Driven Design in Fabric",
        "description": "Efficient data management is essential for modern organizations, and automation is key to scalability. In this session, you'll learn how to build a robust metadata-driven framework using Microsoft Fabric SQL Database and Data Factory.",
        "speakers": ["Erwin de Kreuk"],
        "room": "b.telligent (Foxtrott)",
        "room_id": "foxtrott",
        "start": "2026-01-23T09:30:00Z",
        "end": "2026-01-23T10:30:00Z",
        "duration": 60
    },
    {
        "id": "s9",
        "title": "Power BI Meets GitHub: Automating CI/CD Workflows and Collaboration",
        "description": "With Power BI Project files (PBIP), the TMDL format, and GitHub integration, developers now have access to structured version control, collaborative workflows, and CI/CD automation.",
        "speakers": ["Daniel Patkos"],
        "room": "HEDDA.IO (Ballerina)",
        "room_id": "ballerina",
        "start": "2026-01-23T09:30:00Z",
        "end": "2026-01-23T10:30:00Z",
        "duration": 60
    },
    {
        "id": "s10",
        "title": "REST APIs, AI and Vectors in SQL Server 2025",
        "description": "Vector search is at the core of modern AI applications. With SQL Server 2025, you can now store, query, and optimize vector embeddings natively - all within your existing environment, running entirely on-premises.",
        "speakers": ["Ben Weissman (he/him)"],
        "room": "Cohesity (Concerto)",
        "room_id": "concerto",
        "start": "2026-01-23T09:30:00Z",
        "end": "2026-01-23T10:30:00Z",
        "duration": 60
    },
    {
        "id": "s11",
        "title": "Exploring Fabric Semantic Link for Power BI folks!",
        "description": "If you're coming from a Power BI world, Semantic Link allows connections from Fabric Notebooks to read both data and meta data from your Power BI Semantic Model.",
        "speakers": ["Marc Lelijveld"],
        "room": "Lucient (Symphonia)",
        "room_id": "symphonia",
        "start": "2026-01-23T09:30:00Z",
        "end": "2026-01-23T10:30:00Z",
        "duration": 60
    },
    {
        "id": "s12",
        "title": "Designing Reports People Actually Use: A Persona-Driven Approach in Power BI",
        "description": "Many dashboards look polished but fail to drive action because they aren't built for the people making decisions. This session explores how applying personas to Power BI development can transform adoption and trust.",
        "speakers": ["Zita Pelok"],
        "room": "Cubido (Menuett)",
        "room_id": "menuett",
        "start": "2026-01-23T09:30:00Z",
        "end": "2026-01-23T10:30:00Z",
        "duration": 60
    },
    # 11:30 - Break
    {
        "id": "break-2",
        "title": "Break",
        "description": "Coffee break",
        "speakers": [],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T10:30:00Z",
        "end": "2026-01-23T10:45:00Z",
        "duration": 15
    },
    # 11:45 - Third session block
    {
        "id": "s13",
        "title": "Partitioning in Microsoft SQL Server: A Beginner's Guide",
        "description": "Partitioning is a powerful feature in Microsoft SQL Server, designed to enhance manageability and scalability of large datasets. This introductory session aims to demystify the concept of partitioning.",
        "speakers": ["Uwe Ricken"],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T10:45:00Z",
        "end": "2026-01-23T11:45:00Z",
        "duration": 60
    },
    {
        "id": "s14",
        "title": "Empowering Lakehouse Solutions with Apache Arrow and Python Notebooks in Microsoft Fabric",
        "description": "When Microsoft Fabric was released, it introduced Apache Spark as its default engine. Since then, Microsoft has introduced a non-Spark compute option: Python Notebooks.",
        "speakers": ["Christian Henrik Reich"],
        "room": "b.telligent (Foxtrott)",
        "room_id": "foxtrott",
        "start": "2026-01-23T10:45:00Z",
        "end": "2026-01-23T11:45:00Z",
        "duration": 60
    },
    {
        "id": "s15",
        "title": "From Broken Data to Trusted Data Products",
        "description": "Trusted data products don't happen by accident. They require clear rules, visible quality signals, and consistency across systems and pipelines.",
        "speakers": ["Oliver Engels", "Tillmann Eitelberg"],
        "room": "HEDDA.IO (Ballerina)",
        "room_id": "ballerina",
        "start": "2026-01-23T10:45:00Z",
        "end": "2026-01-23T11:45:00Z",
        "duration": 60
    },
    {
        "id": "s16",
        "title": "From Fast to Blazing: Unlocking Peak Performance in Microsoft Fabric Data Warehouse",
        "description": "Let's explore the latest performance enhancements under the hood, giving you a sneak peek into the magic that makes it all run seamlessly.",
        "speakers": ["Filip Popović"],
        "room": "Cohesity (Concerto)",
        "room_id": "concerto",
        "start": "2026-01-23T10:45:00Z",
        "end": "2026-01-23T11:45:00Z",
        "duration": 60
    },
    {
        "id": "s17",
        "title": "From Batch to Stream: Unlocking Databricks for All Your Analytics Needs",
        "description": "This session will demonstrate how to leverage Databricks capabilities to meet modern data platform requirements with governance through DataOps practices.",
        "speakers": ["Vitalija Bartusevičiūtė", "Geir Alstad"],
        "room": "Lucient (Symphonia)",
        "room_id": "symphonia",
        "start": "2026-01-23T10:45:00Z",
        "end": "2026-01-23T11:45:00Z",
        "duration": 60
    },
    {
        "id": "s18",
        "title": "Supercharge Power BI with the Power BI REST API",
        "description": "Power BI is known for its intuitive interface—but under the hood lies a powerful engine: the Power BI REST API. This session is for developers ready to go beyond the UI.",
        "speakers": ["Ynte Jan Kuindersma"],
        "room": "Cubido (Menuett)",
        "room_id": "menuett",
        "start": "2026-01-23T10:45:00Z",
        "end": "2026-01-23T11:45:00Z",
        "duration": 60
    },
    # 12:45 - Lunch
    {
        "id": "lunch-1",
        "title": "Lunch Break",
        "description": "Lunch break",
        "speakers": [],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T11:45:00Z",
        "end": "2026-01-23T12:45:00Z",
        "duration": 60
    },
    # 13:45 - Fourth session block
    {
        "id": "s19",
        "title": "AI behind the Scenes: Use Cases from Idea to Implementation",
        "description": "We present practical AI use cases on Microsoft Azure, covering the journey from the initial idea through key challenges to architecture and technical implementation.",
        "speakers": ["Cornelia Volaucnik", "Theresa Hirz"],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T12:45:00Z",
        "end": "2026-01-23T13:45:00Z",
        "duration": 60
    },
    {
        "id": "s20",
        "title": "JSON in the world of MSSQL",
        "description": "SQL Server 2025 brings long-awaited features such as a native JSON data type, JSON indexing, and other critical improvements.",
        "speakers": ["Damir Matešić"],
        "room": "b.telligent (Foxtrott)",
        "room_id": "foxtrott",
        "start": "2026-01-23T12:45:00Z",
        "end": "2026-01-23T13:45:00Z",
        "duration": 60
    },
    {
        "id": "s21",
        "title": "Govern or Be Governed: Making Power BI Reports Secure, Compliant, and Trusted",
        "description": "Without a strong governance framework, Power BI dashboards risk becoming siloed, untrusted, and non-compliant. This session explores Microsoft's Data Platform and Purview.",
        "speakers": ["Vivek Trivedi"],
        "room": "HEDDA.IO (Ballerina)",
        "room_id": "ballerina",
        "start": "2026-01-23T12:45:00Z",
        "end": "2026-01-23T13:45:00Z",
        "duration": 60
    },
    {
        "id": "s22",
        "title": "OneLake Security for the Power BI Developer",
        "description": "OneLake Security is the new centralized policy engine in Microsoft Fabric. How does this look like from a Power BI Developer perspective?",
        "speakers": ["Gabi Münster"],
        "room": "Cohesity (Concerto)",
        "room_id": "concerto",
        "start": "2026-01-23T12:45:00Z",
        "end": "2026-01-23T13:45:00Z",
        "duration": 60
    },
    {
        "id": "s23",
        "title": "Power BI developer life, reimagined with Fabric",
        "description": "If you're a Power BI developer, what does Fabric really mean for your work? This session explores what the BI developer life looks like in a Fabric world.",
        "speakers": ["Anastasia Salari"],
        "room": "Lucient (Symphonia)",
        "room_id": "symphonia",
        "start": "2026-01-23T12:45:00Z",
        "end": "2026-01-23T13:45:00Z",
        "duration": 60
    },
    # Lightning talks in Menuett room 13:45 - 14:35 (4x 10 min)
    {
        "id": "s24",
        "title": "Back to the Data: Microsoft Fabric's Role in the Future of Manufacturing",
        "description": "This session dives into the transformative potential of Microsoft Fabric in manufacturing, exploring how it can drive efficiency and improve data visibility.",
        "speakers": ["Florian Stein"],
        "room": "Cubido (Menuett)",
        "room_id": "menuett",
        "start": "2026-01-23T12:45:00Z",
        "end": "2026-01-23T12:55:00Z",
        "duration": 10
    },
    {
        "id": "s25",
        "title": "Databricks Medaillon Architektur in 10 Minuten",
        "description": "Die Databricks Medaillon-Architektur ist ein skalierbares Rahmenwerk zur Organisation und Verarbeitung von Daten in einem modernen Data Lakehouse.",
        "speakers": ["Alexander Klein"],
        "room": "Cubido (Menuett)",
        "room_id": "menuett",
        "start": "2026-01-23T12:55:00Z",
        "end": "2026-01-23T13:05:00Z",
        "duration": 10
    },
    {
        "id": "s26",
        "title": "Fabric Data Engineering on Steroids: AI-Powered Development with MCP + Claude",
        "description": "Transform your Microsoft Fabric data engineering workflow from manual coding to AI-assisted automation with VS Code, Model Context Protocol, and Claude AI.",
        "speakers": ["Estera Kot"],
        "room": "Cubido (Menuett)",
        "room_id": "menuett",
        "start": "2026-01-23T13:05:00Z",
        "end": "2026-01-23T13:15:00Z",
        "duration": 10
    },
    {
        "id": "s27",
        "title": "Know the game you are in - and you will not win",
        "description": "Have you ever thought about what game you are in when doing business? In this session I'll tell you a story of two different games and two different outcomes.",
        "speakers": ["Brian Bønk"],
        "room": "Cubido (Menuett)",
        "room_id": "menuett",
        "start": "2026-01-23T13:15:00Z",
        "end": "2026-01-23T13:25:00Z",
        "duration": 10
    },
    {
        "id": "s28",
        "title": "Metadata Scanner API: Unlock Metadata possibilities",
        "description": "Discover how the scanning APIs can unlock hidden metadata and learn how to use it to uncover dependencies and strengthen governance.",
        "speakers": ["Karianne Kies"],
        "room": "Cubido (Menuett)",
        "room_id": "menuett",
        "start": "2026-01-23T13:25:00Z",
        "end": "2026-01-23T13:35:00Z",
        "duration": 10
    },
    # 14:45 - Break
    {
        "id": "break-3",
        "title": "Break",
        "description": "Coffee break",
        "speakers": [],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T13:45:00Z",
        "end": "2026-01-23T14:00:00Z",
        "duration": 15
    },
    # 15:00 - Fifth session block
    {
        "id": "s29",
        "title": "Design Systems for Power BI: Transforming Dashboard Development",
        "description": "In this session, we will explore how design principles can transform data products and maximize their impact with User Experience and design systems.",
        "speakers": ["Paula García Esteban"],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T14:00:00Z",
        "end": "2026-01-23T15:00:00Z",
        "duration": 60
    },
    {
        "id": "s30",
        "title": "Deadlocks – Analysing, Preventing and Mitigating",
        "description": "Deadlocks happen in the best of families. This session discusses how you can get information about deadlocks, analyze XML reports, and prevent them.",
        "speakers": ["Erland Sommarskog"],
        "room": "b.telligent (Foxtrott)",
        "room_id": "foxtrott",
        "start": "2026-01-23T14:00:00Z",
        "end": "2026-01-23T15:00:00Z",
        "duration": 60
    },
    {
        "id": "s31",
        "title": "Unlock the Power of Real-Time Intelligence in Fabric With KQL",
        "description": "Real-time Intelligence in Microsoft Fabric empowers data professionals to seamlessly process and analyze event-driven data with the Kusto Query Language.",
        "speakers": ["Abhinav Jayanty"],
        "room": "HEDDA.IO (Ballerina)",
        "room_id": "ballerina",
        "start": "2026-01-23T14:00:00Z",
        "end": "2026-01-23T15:00:00Z",
        "duration": 60
    },
    {
        "id": "s32",
        "title": "Who's In, Who's Out? Controlling Access in Microsoft Fabric",
        "description": "As organisations rely on Microsoft Fabric, managing access effectively becomes critical. This session explores permissions in Fabric.",
        "speakers": ["Pragati Jain"],
        "room": "Cohesity (Concerto)",
        "room_id": "concerto",
        "start": "2026-01-23T14:00:00Z",
        "end": "2026-01-23T15:00:00Z",
        "duration": 60
    },
    {
        "id": "s33",
        "title": "You Get What You Measure – Data Health Dashboard mit Power BI",
        "description": "Poor data is expensive. In this session, I show how to build a Data Health Dashboard in Power BI that makes data quality measurable and manageable.",
        "speakers": ["Jasmin Simader"],
        "room": "Lucient (Symphonia)",
        "room_id": "symphonia",
        "start": "2026-01-23T14:00:00Z",
        "end": "2026-01-23T15:00:00Z",
        "duration": 60
    },
    {
        "id": "s34",
        "title": "When the firehose causes the Burnout",
        "description": "Burnout is complex and unique to every person. In this session we will be reminded of what burnout actually looks like and how to avoid triggers.",
        "speakers": ["Traci Sewell"],
        "room": "Cubido (Menuett)",
        "room_id": "menuett",
        "start": "2026-01-23T14:00:00Z",
        "end": "2026-01-23T15:00:00Z",
        "duration": 60
    },
    # 16:00 - Break
    {
        "id": "break-4",
        "title": "Break",
        "description": "Coffee break",
        "speakers": [],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T15:00:00Z",
        "end": "2026-01-23T15:15:00Z",
        "duration": 15
    },
    # 16:15 - Final session block
    {
        "id": "s35",
        "title": "10 Pro Tips to Take Your Power BI Reports to the Next Level",
        "description": "In this fast-paced, demo-driven session, I'll share 10 practical, time-saving techniques to take your Power BI dashboards to the next level.",
        "speakers": ["Marjolein Opsteegh"],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T15:15:00Z",
        "end": "2026-01-23T16:15:00Z",
        "duration": 60
    },
    {
        "id": "s36",
        "title": "Data Storytelling - a new hope for your data",
        "description": "In many organizations, data communication feels dry and confusing. This session offers a new hope: the force of Data Storytelling.",
        "speakers": ["Katharina Covadonga Clören"],
        "room": "b.telligent (Foxtrott)",
        "room_id": "foxtrott",
        "start": "2026-01-23T15:15:00Z",
        "end": "2026-01-23T16:15:00Z",
        "duration": 60
    },
    {
        "id": "s37",
        "title": "Dashboard are Dead, Talk to your Data!",
        "description": "With Fabric Data Agents, you can chat with your data! You get a chat interface that understands the context and answers questions in natural language.",
        "speakers": ["Bas Land"],
        "room": "HEDDA.IO (Ballerina)",
        "room_id": "ballerina",
        "start": "2026-01-23T15:15:00Z",
        "end": "2026-01-23T16:15:00Z",
        "duration": 60
    },
    {
        "id": "s38",
        "title": "Using Query Store to Understand and Control Query Performance",
        "description": "The Query Store can help you identify problematic queries and fix their performance in SQL Server and Azure SQL Database.",
        "speakers": ["Grant Fritchey"],
        "room": "Cohesity (Concerto)",
        "room_id": "concerto",
        "start": "2026-01-23T15:15:00Z",
        "end": "2026-01-23T16:15:00Z",
        "duration": 60
    },
    {
        "id": "s39",
        "title": "When Good Isn't Good Enough: How Statistics Reveal the Real Story in Data",
        "description": "Dashboards are great at showing what is happening, but they often hide the real story. We'll apply statistical techniques to uncover hidden insights.",
        "speakers": ["Ana Voicu"],
        "room": "Lucient (Symphonia)",
        "room_id": "symphonia",
        "start": "2026-01-23T15:15:00Z",
        "end": "2026-01-23T16:15:00Z",
        "duration": 60
    },
    {
        "id": "s40",
        "title": "Questioning My SQL Server Faith… So You Don't Have To",
        "description": "SQL Server is facing fierce competition from PostgreSQL. In this session, we'll explore features that set SQL Server apart and compare them.",
        "speakers": ["Gianluca Sartori"],
        "room": "Cubido (Menuett)",
        "room_id": "menuett",
        "start": "2026-01-23T15:15:00Z",
        "end": "2026-01-23T16:15:00Z",
        "duration": 60
    },
    # 17:15 - Raffle
    {
        "id": "raffle-1",
        "title": "Raffle, End of Day",
        "description": "Prize raffle and closing remarks",
        "speakers": [],
        "room": "ACP (Flamenco)",
        "room_id": "flamenco",
        "start": "2026-01-23T16:15:00Z",
        "end": "2026-01-23T16:30:00Z",
        "duration": 15
    }
]

COMPLETE_SPEAKERS = [
    {"id": "estera-kot", "name": "Estera Kot", "title": "CTO @ Clouds on Mars", "bio": "", "photo": "https://sessionize.com/image/b590-200o200o2-DxSmie4fNJd4RuvVRjQoCs.jpg"},
    {"id": "hugo-kornelis", "name": "Hugo Kornelis", "title": "I make SQL Server fast (.com)", "bio": "", "photo": "https://sessionize.com/image/55bb-200o200o2-fBnfDb8PkABgBCfbcUTE6Q.jpg"},
    {"id": "juliana-smith", "name": "Juliana Smith", "title": "Juliana Smith CITP MBCS", "bio": "", "photo": "https://sessionize.com/image/6242-200o200o2-WqLQTtiiHYq5fPMonc1B1Q.jpg"},
    {"id": "reitse-eskens", "name": "Reitse Eskens", "title": "Data Platform Consultant, Microsoft MVP and MCT", "bio": "", "photo": "https://sessionize.com/image/3717-200o200o2-KqKqkDXqA9GynTq1BB67VJ.jpg"},
    {"id": "olivier-van-steenlandt", "name": "Olivier Van Steenlandt", "title": "Expert @ Datashift", "bio": "", "photo": "https://sessionize.com/image/7e20-200o200o2-QuoP9wdmChk3SQDNM1k8pQ.jpg"},
    {"id": "tomaz-kastrun", "name": "Tomaž Kaštrun", "title": "SQL Server developer and data scientist", "bio": "", "photo": "https://sessionize.com/image/5954-200o200o2-11-bb63-4b2a-9d0b-fc6a1a633191.27a89be4-f000-49a5-99de-45683c3e8289.png"},
    {"id": "benni-de-jagere", "name": "Benni De Jagere", "title": "No coffee? No insights!", "bio": "", "photo": "https://sessionize.com/image/3241-200o200o2-V3z1RvRorEUwyHm9dx76wS.png"},
    {"id": "erwin-de-kreuk", "name": "Erwin de Kreuk", "title": "Data Platform MVP | Lead Data and AI", "bio": "", "photo": "https://sessionize.com/image/4cbe-200o200o2-nhVGWjD4SBXDkn28zBz6fP.jpg"},
    {"id": "daniel-patkos", "name": "Daniel Patkos", "title": "BI Architect & Data Visualization Specialist", "bio": "", "photo": "https://sessionize.com/image/c1b0-200o200o2-NMCo9n3WxosZR2hfF6UKMC.jpg"},
    {"id": "ben-weissman", "name": "Ben Weissman (he/him)", "title": "Works with Computers", "bio": "", "photo": "https://sessionize.com/image/a8b7-200o200o2-T9WzEPPKA66X9kW8afm7nk.jpg"},
    {"id": "marc-lelijveld", "name": "Marc Lelijveld", "title": "Data Platform MVP | Technical Evangelist", "bio": "", "photo": "https://sessionize.com/image/372f-200o200o2-fJkGdJaEfH4isPPZMprCGs.jpg"},
    {"id": "zita-pelok", "name": "Zita Pelok", "title": "Senior Data Analyst & Senior BI Developer", "bio": "", "photo": "https://sessionize.com/image/b4e3-200o200o2-MTsVkYfeJzoJvDNhSV35iN.jpg"},
    {"id": "uwe-ricken", "name": "Uwe Ricken", "title": "db Berater GmbH - Managing Director", "bio": "", "photo": "https://sessionize.com/image/dc58-200o200o2-UucES1i3JAjWG4dJujmEtk.jpg"},
    {"id": "christian-henrik-reich", "name": "Christian Henrik Reich", "title": "Sr Solution Architect @ Microsoft", "bio": "", "photo": "https://sessionize.com/image/7f28-200o200o2-05-7515-4051-be19-fda5d0961904.4ba3a96b-52d5-4a1a-8edd-4edd236eb950.jpg"},
    {"id": "oliver-engels", "name": "Oliver Engels", "title": "oh22data AG, CEO", "bio": "", "photo": "https://sessionize.com/image/b3d8-200o200o2-sLUgXE4cZ6Pb946SCnZyg9.jpg"},
    {"id": "tillmann-eitelberg", "name": "Tillmann Eitelberg", "title": "oh22information services GmbH", "bio": "", "photo": "https://sessionize.com/image/973a-200o200o2-c6-3abe-4dfd-a1e8-6720f0c27ddf.a822dd04-c84e-40bc-b263-4a855d85a6e0.jpg"},
    {"id": "filip-popovic", "name": "Filip Popović", "title": "Microsoft, Senior Product Manager", "bio": "", "photo": "https://sessionize.com/image/8649-200o200o2-LF8j53KnCqaobB1R4iDYQT.png"},
    {"id": "vitalija-bartuseviciute", "name": "Vitalija Bartusevičiūtė", "title": "Senior Consultant - Data Engineer", "bio": "", "photo": "https://sessionize.com/image/0de3-200o200o2-RfrWjMWZNZuUNCCRvSzCYC.jpg"},
    {"id": "geir-alstad", "name": "Geir Alstad", "title": "Chief Data Architect, Gabler AS", "bio": "", "photo": "https://sessionize.com/image/747e-200o200o2-EuVdfKptLDtY7r6MoVK4Fd.jpg"},
    {"id": "ynte-jan-kuindersma", "name": "Ynte Jan Kuindersma", "title": "BIRD Automation", "bio": "", "photo": "https://sessionize.com/image/4873-200o200o2-HghfeafiD4jARPUwVcpriu.jpg"},
    {"id": "cornelia-volaucnik", "name": "Cornelia Volaucnik", "title": "ACP Cubido, Data Scientist", "bio": "", "photo": "https://sessionize.com/image/4b2f-200o200o2-99DGrgdn5YGKKQ4g99Qizt.jpg"},
    {"id": "theresa-hirz", "name": "Theresa Hirz", "title": "ACP CUBIDO, Data Scientist", "bio": "", "photo": "https://sessionize.com/image/8e41-200o200o2-9ngBdmNJXBiDkFgfpEBUXU.png"},
    {"id": "damir-matesic", "name": "Damir Matešić", "title": "Microsoft Data Platform MVP | Senior Database Architect", "bio": "", "photo": "https://sessionize.com/image/2acd-200o200o2-KNgo9R8KJGNTFCcrjVzvtE.png"},
    {"id": "vivek-trivedi", "name": "Vivek Trivedi", "title": "Director- Data & AI Services", "bio": "", "photo": "https://sessionize.com/image/40e8-200o200o2-MjC9WvE7APZqKrXCwf98SE.jpg"},
    {"id": "gabi-munster", "name": "Gabi Münster", "title": "Principal Program Manager / Fabric CAT", "bio": "", "photo": "https://sessionize.com/image/d956-200o200o2-N41xhgbYEeqaKix866zva5.jpg"},
    {"id": "anastasia-salari", "name": "Anastasia Salari", "title": "Microsoft MVP | BizApps Principal consultant", "bio": "", "photo": "https://sessionize.com/image/0167-200o200o2-ngLBnruxhdX3ttgdepPozx.jpg"},
    {"id": "florian-stein", "name": "Florian Stein", "title": "b.telligent, Domain Lead Cloud Transformation", "bio": "", "photo": "https://sessionize.com/image/0855-200o200o2-UoufaMwcNVKBwBu3wNwzjC.jpg"},
    {"id": "alexander-klein", "name": "Alexander Klein", "title": "Alexander Klein IT Consulting & Training", "bio": "", "photo": "https://sessionize.com/image/0b48-200o200o2-N9iFjM1EmPurgnCG9juHoG.png"},
    {"id": "brian-bonk", "name": "Brian Bønk", "title": "Founder & MVP", "bio": "", "photo": "https://sessionize.com/image/44aa-200o200o2-pPZcZQbPoK6EkhKGGm8PTi.JPG"},
    {"id": "karianne-kies", "name": "Karianne Kies", "title": "Data Engineer at PwC", "bio": "", "photo": "https://sessionize.com/image/f766-200o200o2-LSc6467apiyLcwX5WeqaHt.png"},
    {"id": "paula-garcia-esteban", "name": "Paula García Esteban", "title": "Data visualization and AI specialist", "bio": "", "photo": "https://sessionize.com/image/7d4b-200o200o2-PiGQSg8UFPZHNYAofXWhbf.png"},
    {"id": "erland-sommarskog", "name": "Erland Sommarskog", "title": "Erland Sommarskog SQL-Konsult AB", "bio": "", "photo": "https://sessionize.com/image/089c-200o200o2-wyx5SceyZmK9ZFAR4adSH5.jpg"},
    {"id": "abhinav-jayanty", "name": "Abhinav Jayanty", "title": "Data Engineer at Quorum", "bio": "", "photo": "https://sessionize.com/image/b031-200o200o2-ax6QEuEbZuRdmeGkhcYwDu.jpeg"},
    {"id": "pragati-jain", "name": "Pragati Jain", "title": "Microsoft MVP - Data Platform, Analytics Manager", "bio": "", "photo": "https://sessionize.com/image/d4a7-200o200o2-a83oKqSSVaThHVqnTcvP7g.jpg"},
    {"id": "jasmin-simader", "name": "Jasmin Simader", "title": "BI Consultant with a passion for Data Health", "bio": "", "photo": "https://sessionize.com/image/b945-200o200o2-3LaLs4DZBPSpdpxhc6g3iz.jpg"},
    {"id": "traci-sewell", "name": "Traci Sewell", "title": "Tech-adjacent mind fixer", "bio": "", "photo": "https://sessionize.com/image/686b-200o200o2-Nf4uNf214MuBmTxTL8KNEi.jpg"},
    {"id": "marjolein-opsteegh", "name": "Marjolein Opsteegh", "title": "Power BI Visualization specialist", "bio": "", "photo": "https://sessionize.com/image/4477-200o200o2-wkc6dCLLwUEpPAQNrzznjd.jpg"},
    {"id": "katharina-cloren", "name": "Katharina Covadonga Clören", "title": "Data Analytics Consultant @ORAYLIS GmbH", "bio": "", "photo": "https://sessionize.com/image/381f-200o200o2-7aTdF51B4gthcnmfhoRzuH.jpg"},
    {"id": "bas-land", "name": "Bas Land", "title": "That Fabric Guy - Data Architect - MVP", "bio": "", "photo": "https://sessionize.com/image/8d4c-200o200o2-a9NwzwtXAwrVAB1gqAuDDj.jpg"},
    {"id": "grant-fritchey", "name": "Grant Fritchey", "title": "Redgate Software Product Advocate, MVP", "bio": "", "photo": "https://sessionize.com/image/4cd3-200o200o2-VoTuSfv49GC4dQvyrtVJo.jpg"},
    {"id": "ana-voicu", "name": "Ana Voicu", "title": "Data Engineer", "bio": "", "photo": "https://sessionize.com/image/32fc-200o200o2-NihFcWkM88tnMP3dnBHCgo.jpg"},
    {"id": "gianluca-sartori", "name": "Gianluca Sartori", "title": "@spaghettidba", "bio": "", "photo": "https://sessionize.com/image/ffd2-200o200o2-c6212d94-d227-448b-8f8f-f46161331407.jpg"}
]

def create_complete_data():
    return {
        "event": {
            "name": "Data Community Austria Day 2026",
            "date": "2026-01-23",
            "location": "JUFA Hotel Wien",
            "address": "Mautner-Markhof-Gasse 50, 1110 Wien",
            "timezone": "Europe/Vienna"
        },
        "sessions": COMPLETE_SESSIONS,
        "speakers": COMPLETE_SPEAKERS,
        "rooms": [
            {"id": "flamenco", "name": "ACP (Flamenco)", "floor": None},
            {"id": "foxtrott", "name": "b.telligent (Foxtrott)", "floor": None},
            {"id": "ballerina", "name": "HEDDA.IO (Ballerina)", "floor": None},
            {"id": "concerto", "name": "Cohesity (Concerto)", "floor": None},
            {"id": "symphonia", "name": "Lucient (Symphonia)", "floor": None},
            {"id": "menuett", "name": "Cubido (Menuett)", "floor": None}
        ]
    }

if __name__ == "__main__":
    data = create_complete_data()
    
    with open('data/conference.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Created conference.json with ALL {len(data['sessions'])} sessions!")
    print(f"✓ {len(data['speakers'])} speakers")
    print(f"✓ {len(data['rooms'])} rooms")
    print(f"\nSession breakdown:")
    print(f"  - Regular sessions: {len([s for s in data['sessions'] if s['duration'] == 60 and len(s['speakers']) > 0])}")
    print(f"  - Lightning talks: {len([s for s in data['sessions'] if s['duration'] == 10])}")
    print(f"  - Breaks/Service: {len([s for s in data['sessions'] if len(s['speakers']) == 0])}")
