import os
import requests
from dotenv import load_dotenv
from serpapi import GoogleSearch
from duckduckgo_search import DDGS

# 1. Load Keys
load_dotenv()
api_key = os.getenv("SERP_API_KEY")

print("="*40)
print("DIAGNOSTIC TEST")
print("="*40)

# CHECK 1: Is the Key Loaded?
if not api_key:
    print("❌ CRITICAL ERROR: SERPAPI_API_KEY is missing from .env file!")
else:
    print(f"✅ API Key found: {api_key[:5]}......")

# CHECK 2: Basic Internet Ping
print("\n--- Test 1: Pinging Google.com ---")
try:
    response = requests.get("https://www.google.com", timeout=5)
    print(f"✅ Internet Connection: OK (Status: {response.status_code})")
except Exception as e:
    print(f"❌ Internet Connection: FAILED. \nError: {e}")

# CHECK 3: SerpApi Direct Test
print("\n--- Test 2: Connecting to SerpApi ---")
try:
    params = {
        "engine": "google",
        "q": "test query",
        "api_key": api_key,
        "num": 1
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "error" in results:
        print(f"❌ SerpApi Returned Error: {results['error']}")
    elif "organic_results" in results:
        print("✅ SerpApi Connection: SUCCESS! (Request Count should increase now)")
    else:
        print(f"⚠️ SerpApi Connected but returned weird data: {results.keys()}")
except Exception as e:
    print(f"❌ SerpApi Connection: FAILED.")
    print(f"Error Details: {e}")

# CHECK 4: DuckDuckGo Test
print("\n--- Test 3: Connecting to DuckDuckGo ---")
try:
    results = DDGS().text("test query", max_results=1)
    if results:
        print("✅ DuckDuckGo Connection: SUCCESS!")
    else:
        print("⚠️ DuckDuckGo returned no results (but didn't crash).")
except Exception as e:
    print(f"❌ DuckDuckGo Connection: FAILED.")
    print(f"Error Details: {e}")

print("="*40)