import streamlit as st
import pandas as pd

st.write("""
#Estagio 2 appweb
Hello *UNI7!*
"""
)

df =  pd.read_csv("my_data.csv")
st.line_chart(df)