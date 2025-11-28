import warnings
# Filter out the specific warning about the renaming
warnings.filterwarnings("ignore", category=RuntimeWarning, module="duckduckgo_search")

import os
import requests
from serpapi import GoogleSearch
from duckduckgo_search import DDGS

# --- 1. GOOGLE SEARCH (SerpApi) ---
def serp_search(query, engine="google"):
    print(f"--- [Tool] Searching Google via SerpApi: {query} ---")
    
    params = {
        "engine": engine,
        "q": query,
        "api_key": os.getenv("SERP_API_KEY"),
        "num": 5
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic = results.get("organic_results", [])
        
        cleaned_results = []
        for item in organic:
            cleaned_results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })
        return cleaned_results

    except Exception as e:
        print(f"Error in serp_search: {e}")
        return []

# --- 2. DUCKDUCKGO SEARCH (Free) ---
def duckduckgo_search(query):
    print(f"--- [Tool] Searching DuckDuckGo: {query} ---")
    try:
        # DDGS returns 'href' for link and 'body' for snippet
        results = DDGS().text(keywords=query, max_results=5)
        
        cleaned_results = []
        for r in results:
            cleaned_results.append({
                "title": r.get("title"),
                "link": r.get("href"),
                "snippet": r.get("body")
            })
        return cleaned_results
    except Exception as e:
        print(f"Error in DuckDuckGo search: {e}")
        return []

# --- 3. REDDIT SEARCH (Via Google Site Search) ---
def reddit_search_api(keyword):
    # We use Google restricted to reddit.com for better results
    query = f"site:reddit.com {keyword}"
    return serp_search(query, engine="google")

# --- 4. REDDIT SCRAPER (Direct JSON) ---
def reddit_post_retrieval(urls):
    print(f"--- [Tool] Scraping {len(urls)} Reddit Threads ---")
    
    extracted_content = []
    # Custom User-Agent is required for Reddit
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    for url in urls:
        try:
            # Trick: Add .json to the URL to get raw data
            json_url = url.rstrip("/") + ".json"
            
            response = requests.get(json_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Reddit JSON structure: [Post_Object, Comments_Object]
                post_data = data[0]['data']['children'][0]['data']
                comments_data = data[1]['data']['children']
                
                title = post_data.get("title", "No Title")
                selftext = post_data.get("selftext", "")
                
                # Extract top 5 comments
                comments_text = []
                for i, comment in enumerate(comments_data):
                    if i > 5: break
                    if 'body' in comment['data']:
                        comments_text.append(comment['data']['body'])
                
                full_text = f"Title: {title}\nPost: {selftext}\nComments: {' | '.join(comments_text)}"
                extracted_content.append(full_text)
                
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            continue

    return extracted_content