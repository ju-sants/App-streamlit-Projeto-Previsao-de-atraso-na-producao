import streamlit as st
import pandas as pd


st.set_page_config(page_title="Tabelas", page_icon=r"C:\Users\yamim\OneDrive\Documentos\App Streamlit Projeto Predição Dias Atrasados\Imgs\Home_PageIcon1.png", layout="wide")

df = pd.read_excel('Data/processed/df_scaled.xlsx')
df = df.drop(columns='Unnamed: 0')

st.write(df)