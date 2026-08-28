# 🩺 MediGuide AI
# DEMO LINK
https://mediguide-ai-m8v5j5kuxzejxzmum89mam.streamlit.app/

## AI-Powered Medical Symptom Assessment and Patient Guidance Assistant

MediGuide AI is an educational Streamlit prototype that uses
LangChain and an OpenAI chat model to generate structured,
safety-focused preliminary symptom guidance.

The application does NOT provide confirmed medical diagnoses
and is not a replacement for professional medical advice.

---

# Features

- Patient age input
- Gender selection
- Multiple symptom selection
- Additional free-text symptoms
- Symptom duration
- Severity slider from 1-10
- Existing medical conditions
- Current medications
- Additional notes
- English and Urdu output
- OpenAI ChatOpenAI integration
- PromptTemplate
- ChatPromptTemplate
- SystemMessage
- HumanMessage
- AIMessage demonstration
- LLMChain
- Structured JSON response
- Safe JSON parsing
- Streaming response
- InMemoryCache
- SQLiteCache
- Streamlit dashboard
- Urgency levels
- Medical safety disclaimers

---

# Project Structure

```text
medical_ai_assistant/
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
└── src/
    ├── __init__.py
    ├── config.py
    ├── prompts.py
    ├── chains.py
    ├── cache_manager.py
    └── utils.py
