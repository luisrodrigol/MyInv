import streamlit as st
import psycopg2
import pandas as pd

@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from usuarios_login limit 20")

data=pd.DataFrame(rows)
data.columns=['LOGIN','SENHA','NOME','EMAIL','TELEFONE']
st.table(data)