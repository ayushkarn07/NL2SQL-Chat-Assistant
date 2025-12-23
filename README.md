# 🤖 NL2SQL Chat Assistant (Streamlit + Groq)

A Streamlit Interface - **Natural Language to SQL (NL2SQL)** application that lets users ask questions in plain English and receive:

-  Automatically generated **SQLite SQL queries**
-  Query results displayed as tables
-  One-line **human-friendly summaries**
-  Full **chat history** with a bottom input bar

Built using **Streamlit**, **SQLite**, **Groq LLMs**, and **Python**.
## URL
https://nl2sqlayush.streamlit.app/

---

## 🚀 Features

- Natural language → SQL conversion (NL2SQL)
- SQLite relational database support
- Chat-based UI with message history
- SQL query shown **exactly as generated**
- Result tables displayed **without modification**
- LLM-generated natural language summary
- Safe execution (**SELECT queries only**)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----------|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite |
| LLM | Groq (LLaMA-3.1-8B) |
| Data Processing | Pandas |

---
1.  **Install Dependencies**:
    ```bash
    pip install streamlit groq pandas
    ```
2. Environment Setup
    ```bash
    os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY"
    ```
3. Run the Application
   ```bash
    streamlit run app.py
    ```
## SnapShots
<img width="959" height="410" alt="image" src="https://github.com/user-attachments/assets/7e8cbb84-fc96-4d69-8ce4-6bef46bb30db" />
<img width="917" height="398" alt="image" src="https://github.com/user-attachments/assets/033237bd-4437-4317-9f4a-da2ab5710de2" />
<img width="940" height="401" alt="image" src="https://github.com/user-attachments/assets/4cf75408-1d6c-4ea6-ab5b-b0e237159f2d" />


