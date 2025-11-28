import os
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Import existing logic
from web_operations import serp_search, duckduckgo_search, reddit_search_api, reddit_post_retrieval
from prompts import get_conflict_detection_messages

load_dotenv()

app = FastAPI(title="Search Agent API")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LLM SETUP ---
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
except Exception as e:
    print(f"Warning: LLM setup failed: {e}")
    llm = None

# --- MODELS ---
class SearchRequest(BaseModel):
    query: str

class ConflictRequest(BaseModel):
    google_results: List[Dict[str, Any]]
    reddit_results: List[str] # List of strings (post content)

class ConflictReport(BaseModel):
    agreements: List[str]
    conflicts: List[str]
    unique_google_insights: List[str]
    unique_reddit_insights: List[str]
    final_conflict_report: str

# --- ENDPOINTS ---

@app.post("/api/search/google")
async def search_google(request: SearchRequest):
    try:
        results = serp_search(request.query, engine="google")
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search/reddit")
async def search_reddit(request: SearchRequest):
    try:
        # 1. Search for threads
        search_results = reddit_search_api(request.query)
        
        # 2. Select top 3 URLs (simplified logic for API speed)
        top_urls = [r['link'] for r in search_results[:3]]
        
        # 3. Scrape content
        post_content = reddit_post_retrieval(top_urls)
        
        return {
            "threads": search_results,
            "content": post_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/conflicts")
async def analyze_conflicts(request: ConflictRequest):
    if not llm:
        raise HTTPException(status_code=503, detail="LLM not initialized")
        
    try:
        google_text = "\n".join([f"- {r.get('title', '')}: {r.get('snippet', '')}" for r in request.google_results])
        reddit_text = "\n".join(request.reddit_results[:3])
        
        messages = get_conflict_detection_messages(google_text, reddit_text)
        
        structured_llm = llm.with_structured_output(ConflictReport)
        response = structured_llm.invoke(messages)
        
        return response.model_dump()
    except Exception as e:
        print(f"Analysis Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Search Agent API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
