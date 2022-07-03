import streamlit as st

from utils.read_data import read_data_xlsx

def app():
    data = read_data_xlsx("directivos2022")
    st.write(data)