import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import utils.plots as plots
from utils.read_data import read_data


st.title("Seguimiento a respuestas GreenTIC")
respuestas = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTtRvfE21QbkKtj0cTQu-jsy56CxGjF4Q3xRIcTk-2emRMVHj30aBSjJWgSC78sxJX-VATwfLhf71xB/pub?gid=1769383466&single=true&output=csv')
respuestas_mostrar = respuestas.loc[:,['Marca temporal', 'Código de tu colegio', '¿Cómo te llamas?']]

st.dataframe(respuestas_mostrar)


st.write("## Total por colegio")
total_colegio = respuestas.pivot_table(index=['Código de tu colegio','Grado'],
 values='Número de lista', aggfunc='count').reset_index().rename(columns={'Código de tu colegio':'Código IE',"Número de lista": "Cantidad estudiantes"})

st.dataframe(total_colegio)
