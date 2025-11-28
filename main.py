import os
from dotenv import load_dotenv
from typing import Annotated, List, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Import our custom files
from web_operations import serp_search, duckduckgo_search, reddit_search_api, reddit_post_retrieval
from prompts import (
    get_google_analysis_messages,
    get_duckduckgo_analysis_messages,
    get_reddit_analysis_messages,
    get_conflict_detection_messages,
    get_synthesis_messages
)

load_dotenv()

# --- SETUP GEMINI ---
llm = ChatGoogleGenerativeAI(model=	"gemini-2.5-flash")

# --- DEFINE STATE ---
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_question: str
    
    # Raw Results (Lists)
    google_results: list
    duckduckgo_results: list
    reddit_results: list
    
    # Filtered/Scraped Data
    selected_reddit_urls: list[str]
    reddit_post_data: list
    
    # Analyses (Strings)
    google_analysis: str
    duckduckgo_analysis: str
    reddit_analysis: str
    conflict_report: dict
    final_answer: str

# --- DEFINE NODES ---

def google_search_node(state: AgentState):
    query = state["user_question"]
    results = serp_search(query, engine="google")
    return {"google_results": results}

def duckduckgo_search_node(state: AgentState):
    query = state["user_question"]
    results = duckduckgo_search(query)
    return {"duckduckgo_results": results}

def reddit_search_node(state: AgentState):
    query = state["user_question"]
    results = reddit_search_api(query)
    return {"reddit_results": results}

def select_reddit_urls_node(state: AgentState):
    # print("--- [Node] Selecting Best Reddit Threads ---")
    reddit_results = state.get("reddit_results", [])
    if not reddit_results:
        return {"selected_reddit_urls": []}
        
    # Format threads for Gemini to read
    context_str = "\n".join([f"{i}. {r['title']} ({r['link']})" for i, r in enumerate(reddit_results)])
    
    # Define Structured Output
    class RedditURLSelection(BaseModel):
        selected_urls: List[str] = Field(description="List of 3 best reddit URLs from the provided text")

    prompt = f"""
    User Query: {state['user_question']}
    
    Reddit Threads Found:
    {context_str}
    
    Select the top 3 URLs that are most likely to answer the query. Return ONLY the URLs.
    """
    
    try:
        structured_llm = llm.with_structured_output(RedditURLSelection)
        response = structured_llm.invoke(prompt)
        return {"selected_reddit_urls": response.selected_urls}
    except Exception as e:
        print(f"Selection Error: {e}, picking top 3 defaults.")
        return {"selected_reddit_urls": [r['link'] for r in reddit_results[:3]]}

def scrape_reddit_content_node(state: AgentState):
    urls = state.get("selected_reddit_urls", [])
    content = reddit_post_retrieval(urls)
    return {"reddit_post_data": content}

# --- ANALYSIS NODES ---
def analyze_google(state: AgentState):
    print("--- [Node] Analyzing Google Data ---")
    results = state["google_results"]
    context = "\n".join([f"Title: {r['title']}\nSnippet: {r['snippet']}" for r in results])
    messages = get_google_analysis_messages(state["user_question"], context)
    response = llm.invoke(messages)
    return {"google_analysis": response.content}

def analyze_duckduckgo(state: AgentState):
    print("--- [Node] Analyzing DuckDuckGo Data ---")
    results = state["duckduckgo_results"]
    context = "\n".join([f"Title: {r['title']}\nSnippet: {r['snippet']}" for r in results])
    messages = get_duckduckgo_analysis_messages(state["user_question"], context)
    response = llm.invoke(messages)
    return {"duckduckgo_analysis": response.content}

def analyze_reddit(state: AgentState):
    # print("--- [Node] Analyzing Reddit Data ---")
    
    # Use .get() to be safe
    posts = state.get("reddit_post_data", [])
    
    # If there are no posts, return a default message IMMEDIATELY
    if not posts:
        return {"reddit_analysis": "No relevant Reddit threads were found for this query."}

    context = "\n\n".join(posts)
    messages = get_reddit_analysis_messages(state["user_question"], context)
    response = llm.invoke(messages)
    return {"reddit_analysis": response.content}

def conflict_detector_node(state: AgentState):
    print("--- [Node] Detecting Conflicts ---")
    
    google_results = state.get("google_results", [])
    reddit_results = state.get("reddit_post_data", [])
    
    # If missing data, skip conflict detection
    if not google_results or not reddit_results:
        return {"conflict_report": {}}
        
    # Format for analysis
    google_text = "\n".join([f"- {r['title']}: {r['snippet']}" for r in google_results])
    reddit_text = "\n".join(reddit_results[:3]) # Limit to top 3 threads to save tokens
    
    messages = get_conflict_detection_messages(google_text, reddit_text)
    
    # Define Structured Output for the report
    class ConflictReport(BaseModel):
        agreements: List[str] = Field(description="List of matching facts or opinions")
        conflicts: List[str] = Field(description="List of contradictions or disagreements")
        unique_google_insights: List[str] = Field(description="Information found only in Google results")
        unique_reddit_insights: List[str] = Field(description="Information found only in Reddit results")
        final_conflict_report: str = Field(description="A brief summary of the differences")

    try:
        structured_llm = llm.with_structured_output(ConflictReport)
        response = structured_llm.invoke(messages)
        return {"conflict_report": response.model_dump()}
    except Exception as e:
        print(f"Conflict Detection Error: {e}")
        return {"conflict_report": {}}

def synthesize_node(state: AgentState):
    print("--- [Node] Synthesizing Final Answer ---")
    
    # --- SAFE GET METHOD (Fixes the Crash) ---
    # We use .get(key, default_value) so it never fails
    g_analysis = state.get("google_analysis", "Google search returned no data.")
    d_analysis = state.get("duckduckgo_analysis", "DuckDuckGo search returned no data.")
    r_analysis = state.get("reddit_analysis", "No Reddit discussions found.")
    conflict_report = state.get("conflict_report", {})

    messages = get_synthesis_messages(
        state["user_question"],
        g_analysis,
        d_analysis,
        r_analysis,
        conflict_report
    )
    
    try:
        response = llm.invoke(messages)
        return {"final_answer": response.content}
    except Exception as e:
        return {"final_answer": f"Error generating answer: {e}"}
    

# --- BUILD GRAPH ---
graph_builder = StateGraph(AgentState)

# Add Nodes
graph_builder.add_node("google", google_search_node)
graph_builder.add_node("duckduckgo", duckduckgo_search_node)
graph_builder.add_node("reddit_search", reddit_search_node)
graph_builder.add_node("reddit_select", select_reddit_urls_node)
graph_builder.add_node("reddit_scrape", scrape_reddit_content_node)
graph_builder.add_node("analyze_google", analyze_google)
graph_builder.add_node("analyze_duckduckgo", analyze_duckduckgo)
graph_builder.add_node("analyze_reddit", analyze_reddit)
graph_builder.add_node("conflict_detector", conflict_detector_node)
graph_builder.add_node("synthesize", synthesize_node)

# Add Edges (Logic Flow)
# 1. Start all searches in parallel
graph_builder.add_edge(START, "google")
graph_builder.add_edge(START, "duckduckgo")
graph_builder.add_edge(START, "reddit_search")

# 2. Simple paths (Search -> Analyze)
graph_builder.add_edge("google", "analyze_google")
graph_builder.add_edge("duckduckgo", "analyze_duckduckgo")

# 3. Complex path (Reddit Search -> Select -> Scrape -> Analyze)
graph_builder.add_edge("reddit_search", "reddit_select")
graph_builder.add_edge("reddit_select", "reddit_scrape")
graph_builder.add_edge("reddit_scrape", "analyze_reddit")

# 4. Conflict Detection (Wait for Google & Reddit Analysis)
graph_builder.add_edge("analyze_google", "conflict_detector")
graph_builder.add_edge("analyze_reddit", "conflict_detector")

# 5. Merge all into Synthesis
graph_builder.add_edge("conflict_detector", "synthesize")
graph_builder.add_edge("analyze_duckduckgo", "synthesize")

graph_builder.add_edge("synthesize", END)

# Compile
graph = graph_builder.compile()

# --- RUNNER ---
if __name__ == "__main__":
    print("--- Multi-Agent Search System (Gemini + SerpApi + DDG) ---")
    q = input("What do you want to research? ")
    
    initial_state = {"user_question": q}
    result = graph.invoke(initial_state)
    
    print("\n" + "="*50)
    print("FINAL RESEARCH REPORT")
    print("="*50 + "\n")
    print(result["final_answer"])