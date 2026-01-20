import os
import time
import re
import subprocess
import urllib.parse
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Initialize Environment
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class TravelAutomationAgent:
    """
    An autonomous agent designed for Moto Edge 40 to discover travel landmarks,
    generate itineraries using AI Vision, and automate delivery via WhatsApp.
    """
    
    def __init__(self, destination, days, phone_number):
        self.destination = destination
        self.days = days
        self.phone_number = self.phone_number_sanitizer(phone_number)
        self.screenshot_path = "discovery_snapshot.png"

    @staticmethod
    def phone_number_sanitizer(number):
        """Ensures phone number is in correct format for WhatsApp API."""
        return re.sub(r'[^0-9]', '', number)

    def execute_adb(self, command):
        """Safe execution of ADB shell commands."""
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"ADB Error: {e}")

    def discover_landmarks(self):
        """Automates Google Maps to find top-rated attractions and restaurants."""
        print(f"📍 Initializing discovery for: {self.destination}")
        self.execute_adb(["adb", "shell", "am", "force-stop", "com.google.android.apps.maps"])
        
        # Deep Search Query for Rich Metadata
        query = f"best+tourist+landmarks+and+famous+local+food+in+{self.destination}"
        geo_uri = f"geo:0,0?q={urllib.parse.quote(query)}"
        
        self.execute_adb(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", geo_uri, "com.google.android.apps.maps"])
        
        print("⏳ Synchronizing map layers (18s)...")
        time.sleep(18) 
        
        # Clear UI Overlays for unobstructed Vision analysis
        self.execute_adb(["adb", "shell", "input", "keyevent", "4"]) 
        time.sleep(1)
        self.execute_adb(["adb", "shell", "input", "swipe", "500", "1200", "500", "2100", "500"])
        time.sleep(2)

    def generate_ai_itinerary(self):
        """Uses Gemini 2.0 Flash to analyze the screen and generate a detailed plan."""
        print("🧠 Invoking Gemini Vision for spatial analysis...")
        
        self.execute_adb(["adb", "shell", "screencap", "-p", f"/sdcard/{self.screenshot_path}"])
        self.execute_adb(["adb", "pull", f"/sdcard/{self.screenshot_path}", "."])
        
        with open(self.screenshot_path, "rb") as f:
            img_bytes = f.read()

        prompt = f"""
        Act as an expert travel planner. Analyze the provided map pins for {self.destination}.
        Create a detailed {self.days}-day itinerary.
        
        REQUIREMENTS:
        1. STRUCTURE: Start immediately with 'DAY 1'. No introductory text.
        2. DEPTH: For every spot, include 'Travel Time' and 'Estimated Stay'.
        3. GASTRONOMY: Identify and recommend specific restaurant names found on the map.
        4. ALIGNMENT: Each detail must be on its own line for mobile readability.
        5. CLEANLINESS: Use plain text only. Avoid markdown symbols like stars or bolding.
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=[prompt, types.Part.from_bytes(data=img_bytes, mime_type="image/png")]
        )
        return response.text

    def dispatch_via_whatsapp(self, content):
        """Automates WhatsApp delivery using turbo-typing and safe-zone sending."""
        print(f"📲 Delivery initiated for +{self.phone_number}...")
        
        whatsapp_url = f"https://api.whatsapp.com/send?phone={self.phone_number}"
        self.execute_adb(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", whatsapp_url, "com.whatsapp"])
        time.sleep(8)

        # Focus Input Field
        self.execute_adb(["adb", "shell", "input", "tap", "400", "2200"])
        
        print("⚡ Executing Turbo-Typing...")
        lines = content.split('\n')
        for line in lines:
            sanitized_line = re.sub(r'[^a-zA-Z0-9\s\:\!\-\.]', '', line).strip()
            if sanitized_line:
                words = sanitized_line.split()
                for i, word in enumerate(words):
                    self.execute_adb(["adb", "shell", "input", "text", word])
                    if i < len(words) - 1:
                        self.execute_adb(["adb", "shell", "input", "keyevent", "62"]) # Space
                
                self.execute_adb(["adb", "shell", "input", "keyevent", "66"]) # New Line
                time.sleep(0.05)

        # FINAL SEND SEQUENCE
        print("🚀 Executing Precision Send...")
        self.execute_adb(["adb", "shell", "input", "keyevent", "111"]) # Dismiss Keyboard to reset UI
        time.sleep(2)
        
        # Safe-Zone Coordinates (Bottom-Right corner to avoid Video Call/Attachment)
        self.execute_adb(["adb", "shell", "input", "tap", "1050", "2250"]) 
        print("✅ Transmission Successful.")

    def run(self):
        """Main execution flow."""
        try:
            self.discover_landmarks()
            itinerary = self.generate_ai_itinerary()
            print(f"\n--- GENERATED ITINERARY ---\n{itinerary}\n")
            self.dispatch_via_whatsapp(itinerary)
        except Exception as e:
            print(f"Critical System Failure: {e}")

# ==========================================
# Main Execution Entry
# ==========================================
if __name__ == "__main__":
    print("--- TRAVEL AGENT AUTOMATION SYSTEM ---")
    dest = input("Enter Destination: ")
    days = input("Enter Duration (Days): ")
    phone = input("Enter Recipient Phone (e.g. 91xxxxxxxxxx): ")

    agent = TravelAutomationAgent(dest, days, phone)
    agent.run()