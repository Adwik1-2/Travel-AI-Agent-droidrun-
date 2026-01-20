🚀 DroidRun-Based Autonomous Travel Agent

An autonomous, mobile-native AI agent that bridges the gap between spatial discovery on Google Maps and communication on WhatsApp.
Built using the DroidRun framework, the agent visually perceives real map data, reasons over spatial and time constraints, and autonomously shares structured travel itineraries.

🛠 Problem Statement

Trip planning on mobile devices is highly fragmented. Users manually switch between Google Maps to discover places, Notes to organize information, and WhatsApp to share plans. This repetitive copy–paste–share workflow is time-consuming, error-prone, and results in unstructured itineraries that lack travel-time and spatial context. Traditional chatbot solutions generate static recommendations without access to real-time map state, making them impractical for real-world planning.

💡 Solution Overview

This project introduces an Autonomous Travel Agent that directly operates on real Android applications to eliminate app-to-app friction.

The agent follows a Perception → Reasoning → Action loop:

🔍 Visual Perception

Uses Android Debug Bridge (ADB) to launch Google Maps and capture the live spatial layout of landmarks and restaurants.

🧠 AI Reasoning

Leverages Gemini 2.0 Flash Vision to analyze map context, reason about proximity, travel flow, and realistic time allocation, and generate a day-wise itinerary.

⚙️ Automated Action

Uses the DroidRun execution layer to autonomously compose and send a clean, mobile-optimized itinerary directly via WhatsApp.

🏗 Technical Architecture

Agent Execution Engine: DroidRun Framework

Reasoning Model: Google Gemini 2.0 Flash (Vision)

Mobile Automation: Android Debug Bridge (ADB)

Programming Language: Python 3.x

Communication Channel: WhatsApp (UI-level automation)

🌟 Key Features

Zero Integration Required – Operates directly on existing mobile app UIs

Agentic Workflow – Perception, reasoning, and action on live device state

Context-Aware Planning – Considers spatial proximity and time sequencing

Precision Control – Safe-zone tapping to avoid misclicks (e.g., video calls)

Turbo-Typing – Structured, line-by-line message composition optimized for mobile screens

🚀 Getting Started
Prerequisites

Python 3.10+

Android Debug Bridge (ADB) installed and added to PATH

Google Gemini API Key

Android device with USB Debugging enabled

Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME


Install dependencies:

pip install -r requirements.txt


Create a .env file:

GEMINI_API_KEY=your_api_key_here


Run the agent:

python main.py

📌 Why DroidRun

DroidRun serves as the mobile agent execution layer, enabling the AI to safely and autonomously interact with real Android applications. While Gemini handles reasoning, DroidRun ensures reliable perception and action on live mobile interfaces, transforming the system from a text-only planner into a true autonomous agent.