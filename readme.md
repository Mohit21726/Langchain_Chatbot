# AI Chatbot (LangChain + LangGraph)

This project is an AI-powered **Finance Chatbot** built with **LangChain** and **LangGraph**.  
It integrates an LLM API with contextual learning, finance-specific tools, and conversation orchestration.  
The chatbot supports **multi-threaded responses** for better concurrency and uses **LangSmith** for observability and debugging.  

---

## 🚀 Features
- **LLM Integration**: Connected to a Large Language Model API for natural finance-related conversations.  
- **Contextual Learning**: Maintains chat history and provides context-aware responses.  
- **API Tools**: Integrated LangChain tools to fetch live market and financial data.  
- **Multi-threaded Chatbot**: Added threading to handle multiple queries simultaneously.  
- **LangGraph Orchestration**: Manages conversation flow with modular graph-based execution.  
- **LangSmith Tracking**: Tracks and monitors LLM requests, responses, and performance.  

---

## 🛠️ Tech Stack
- **LangChain** – LLM orchestration framework  
- **LangGraph** – Graph-based conversational flow control  
- **LangSmith** – LLM observability & debugging  
- **Python 3.10+** – Core backend  
- **Threading** – For concurrent chatbot responses  
- **API** – External API integration for market/financial data  

##Setup
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
pip install -r requirements.txt

GEMINI_API_KEY=your_llm_api_key
FINANCE_API_KEY=your_finance_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
