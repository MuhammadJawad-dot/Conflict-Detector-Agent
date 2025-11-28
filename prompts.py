from langchain_core.messages import SystemMessage, HumanMessage

def get_google_analysis_messages(user_question, google_results):
    return [
        SystemMessage(content="You are a research assistant. Analyze Google Search results and provide a factual summary."),
        HumanMessage(content=f"User Question: {user_question}\n\nGoogle Results:\n{google_results}\n\nSummarize the key facts.")
    ]

from langchain_core.messages import SystemMessage, HumanMessage

def get_google_analysis_messages(user_question, google_results):
    return [
        SystemMessage(content="You are a research assistant. Analyze Google Search results and provide a factual summary."),
        HumanMessage(content=f"User Question: {user_question}\n\nGoogle Results:\n{google_results}\n\nSummarize the key facts.")
    ]

def get_duckduckgo_analysis_messages(user_question, ddg_results):
    return [
        SystemMessage(content="You are a research assistant. Analyze DuckDuckGo Search results."),
        HumanMessage(content=f"User Question: {user_question}\n\nDuckDuckGo Results:\n{ddg_results}\n\nSummarize the key facts, ignoring duplicates from other sources.")
    ]

def get_reddit_analysis_messages(user_question, reddit_post_data):
    return [
        SystemMessage(content="You are a forum analyst. Extract public sentiment, personal experiences, and unique advice from Reddit discussions."),
        HumanMessage(content=f"User Question: {user_question}\n\nReddit Discussions:\n{reddit_post_data}\n\nSummarize the community consensus and specific advice.")
    ]

def get_conflict_detection_messages(google_results, reddit_results):
    return [
        SystemMessage(content="You are a Conflict Detector. Compare information from Google Search (Mainstream/Official) and Reddit (Community/Personal). Identify agreements, disagreements, and unique insights."),
        HumanMessage(content=f"""
        Analyze these two data sets:
        
        --- GOOGLE RESULTS ---
        {google_results}
        
        --- REDDIT RESULTS ---
        {reddit_results}
        
        Produce a JSON object with:
        - agreements: list of matching facts/opinions
        - conflicts: list of contradictions or disagreements
        - unique_google_insights: what only Google mentioned
        - unique_reddit_insights: what only Reddit mentioned
        - final_conflict_report: a brief summary of the differences
        """)
    ]

def get_synthesis_messages(user_question, google_analysis, ddg_analysis, reddit_analysis, conflict_report=None):
    
    conflict_text = ""
    if conflict_report:
        conflict_text = f"""
        --- CONFLICT REPORT ---
        Agreements: {conflict_report.get('agreements', [])}
        Conflicts: {conflict_report.get('conflicts', [])}
        Summary: {conflict_report.get('final_conflict_report', 'No conflicts detected.')}
        """

    return [
        SystemMessage(content="You are a Lead Researcher. Combine reports from Google, DuckDuckGo, and Reddit into a single comprehensive answer."),
        HumanMessage(content=f"""
        User Question: {user_question}
        
        1. Google Report: {google_analysis}
        2. DuckDuckGo Report: {ddg_analysis}
        3. Reddit Report: {reddit_analysis}
        
        {conflict_text}
        
        Construct the final answer. Start with a direct answer, then provide summarize details from the sources. 
        If there are conflicts between official sources (Google) and community (Reddit), explicitly highlight them using the Conflict Report data.
        """)
    ]