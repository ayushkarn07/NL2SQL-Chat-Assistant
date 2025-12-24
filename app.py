import streamlit as st
import sqlite3
import pandas as pd
from groq import Groq

# ======================================================
# CONFIG
# ======================================================
st.set_page_config(page_title="NL2SQL Chat Assistant", layout="wide")

# ✅ Secure API key (from Streamlit Secrets)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

DB_PATH = "school.db"

# ======================================================
# DATABASE (AUTO INITIALIZATION)
# ======================================================
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    marks INTEGER,
    department TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    dept_code TEXT PRIMARY KEY,
    dept_name TEXT,
    hod TEXT,
    building TEXT
)
""")

# Fresh demo data
cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM departments")

students_data = [
    (1, "Rahul", 20, 85, "CSE"),
    (2, "Anita", 21, 92, "ECE"),
    (3, "Aman", 19, 78, "ME"),
    (4, "Sneha", 22, 88, "CSE"),
    (5, "Rohit", 20, 65, "CE")
]

departments_data = [
    ("CSE", "Computer Science Engineering", "Dr. Sharma", "Block A"),
    ("ECE", "Electronics & Communication", "Dr. Verma", "Block B"),
    ("ME", "Mechanical Engineering", "Dr. Singh", "Block C"),
    ("CE", "Civil Engineering", "Dr. Gupta", "Block D")
]

cursor.executemany(
    "INSERT INTO students VALUES (?, ?, ?, ?, ?)", students_data
)
cursor.executemany(
    "INSERT INTO departments VALUES (?, ?, ?, ?)", departments_data
)

conn.commit()
conn.close()

# ======================================================
# SCHEMA & PROMPTS
# ======================================================
SCHEMA = """
Table: students
Columns:
- id (INTEGER)
- name (TEXT)
- age (INTEGER)
- marks (INTEGER)
- department (TEXT)

Table: departments
Columns:
- dept_code (TEXT)
- dept_name (TEXT)
- hod (TEXT)
- building (TEXT)

Relationship:
- students.department = departments.dept_code
"""

SYSTEM_PROMPT = f"""
You are an expert NL2SQL assistant.

RULES:
1. Use ONLY provided tables and columns
2. SQLite syntax only
3. Only SELECT queries
4. No explanation or comments
5. If question is outside schema, say:
   "I'm designed to provide SQL queries for the database."

Schema:
{SCHEMA}
"""

SUMMARY_PROMPT = """
You are a data analyst.
Give ONE clear, short sentence summarizing the result for a non-technical user.
"""

# ======================================================
# FUNCTIONS
# ======================================================
def generate_sql(question):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def run_query(sql):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return pd.DataFrame(rows, columns=columns)

def load_table(table_name):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

def generate_summary(question, df):
    if df.empty:
        return "No data found."

    prompt = f"""
Question: {question}

Result:
{df.to_string(index=False)}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

# ======================================================
# SESSION STATE
# ======================================================
if "chat" not in st.session_state:
    st.session_state.chat = []

# ======================================================
# UI
# ======================================================
st.title("🤖 NL2SQL Chat Assistant")

# -------- DATABASE PREVIEW (SIDE BY SIDE) --------
st.markdown("## 📋 Database Tables")

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("🎓 Students")
    st.dataframe(load_table("students"), use_container_width=True)

with right_col:
    st.subheader("🏫 Departments")
    st.dataframe(load_table("departments"), use_container_width=True)

st.divider()

# -------- CHAT HISTORY --------
for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown("**📌 Summary**")
            st.success(msg["summary"])

            st.markdown("**🧠 Generated SQL**")
            st.code(msg["sql"], language="sql")

            st.markdown("**📊 Result Table**")
            st.dataframe(msg["df"], use_container_width=True)

# -------- INPUT --------
question = st.chat_input("Ask a question about the database...")

if question:
    st.session_state.chat.append({
        "role": "user",
        "content": question
    })

    try:
        sql = generate_sql(question)

        if not sql.lower().startswith("select"):
            raise ValueError("Invalid SQL generated")

        df = run_query(sql)
        summary = generate_summary(question, df)

        st.session_state.chat.append({
            "role": "assistant",
            "sql": sql,
            "df": df,
            "summary": summary
        })

        st.rerun()

    except Exception:
        st.error("❌ Error processing your query")
