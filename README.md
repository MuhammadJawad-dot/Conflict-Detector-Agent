# ⚡ Conflict Detector Agent

## 🚀 About
The **Conflict Detector Agent** is an AI-powered tool that helps detect conflicts or contradictions in text from multiple sources.  
It’s designed to provide clear insights, highlight contradictions, and generate a concise summary for any user query.

---

## 📂 How It Works

1. **User Input:**  
   The user enters a query or text in the interface.

2. **Multi-Source Search:**  
   The system searches multiple platforms in parallel:  
   - **Google** – Fetches search results using SerpAPI  
   - **DuckDuckGo** – Fetches results via DuckDuckGo API  
   - **Reddit** – Retrieves relevant discussion threads

3. **Reddit Processing:**  
   - **Select Top Threads:** The AI picks the 3 most relevant Reddit threads  
   - **Scrape Content:** Retrieves the text content of the selected threads for analysis

4. **Analysis Nodes:**  
   - **Google & DuckDuckGo:** AI reviews results and extracts key information  
   - **Reddit:** AI summarizes discussion content from Reddit posts  

5. **Conflict Detection:**  
   - Compares Google and Reddit analyses to detect agreements, contradictions, and unique insights  
   - Generates a structured conflict report with a brief summary  

6. **Final Synthesis:**  
   - Merges all analyses and the conflict report to generate a **comprehensive answer**  
   - This final answer is displayed as a research report  

7. **Graph-Based Workflow:**  
   - Uses a **state graph** where each task (search, analyze, detect conflicts, synthesize) is a node  
   - Edges define execution order, ensuring proper sequencing and parallel processing where possible  

---

## 📂 Project Structure
- `frontend/` – ReactJS interface for users to input queries and see results  
- `backend/` – FastAPI backend that handles AI analysis and conflict detection  
- `.env` – Environment variables (kept private for security)  

---

## 📌 Features
- ✅ Detects conflicts in English text  
- ✅ Highlights contradictions and agreements  
- ✅ Multi-source analysis (Google, DuckDuckGo, Reddit)  
- ✅ Generates a structured, easy-to-read final report  
- ✅ Modular design for scalability and future improvements
- 
## 🤝 Contributing
Contributions are welcome!  
1. Fork the repo  
2. Create your branch: `git checkout -b feature-name`  
3. Commit your changes: `git commit -m 'Add new feature'`  
4. Push branch: `git push origin feature-name`  
5. Open a Pull Request  
---
## 📫 Contact
- GitHub: [MuhammadJawad-dot](https://github.com/MuhammadJawad-dot)  
- Email: jawadintzar123@gmail.com
