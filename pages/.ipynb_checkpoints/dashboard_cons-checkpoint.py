import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from utils.read_data import read_data
#pio.templates.default = "plotly_white"

px.defaults.template = "plotly_white"
px.color_discrete_sequence= px.colors.qualitative.Set2
px.defaults.width = 600
px.defaults.height = 400


config = {
    'scrollZoom': True,
    'displaylogo': False,
    'responsive': True,
    'editable': True,
    'toImageButtonOptions': {
        'format': 'png',  # one of png, svg, jpeg, webp
        'filename': 'custom_image',
        'height': None,
        'width': None,
        'scale': 3  # Multiply title/legend/axis/canvas sizes by this factor
    }
}

def app():
    st.title('Consolidación')
    df = read_data('doc_sociodemo')


    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    st.write("Fecha de actualización", df.Fecha.max())
    col_m1.metric("Número de docentes", len(df.ID.unique()))
    col_m2.metric('Número de instituciones', len(df['Código IE'].unique()))
    col_m3.metric('Promedio de docentes por institución', int(df.groupby('Código IE').ID.nunique().mean()))
    col_m4.metric('Promedio de docentes formados CFK', int(df[df['Formado CFK']=='Sí'].groupby('Código IE').ID.nunique().mean()))

    col1, col2= st.columns(2)

    pivot_1 = pd.pivot_table(df, index='Sexo', values='ID', aggfunc='nunique').reset_index()
    fig_1 = px.bar(pivot_1, x='Sexo', y ='ID',  color='Sexo', text='ID', color_discrete_sequence= px.colors.qualitative.Set2)
    fig_1.update_traces(textposition='outside',
                          texttemplate='%{text}')
    col1.plotly_chart(fig_1, config=config)

    pivot_2 = pd.pivot_table(df, index=['Formado tecnología e informática','Sexo'],values='ID', aggfunc='nunique').reset_index()
    fig_2 = px.bar(pivot_2, y='ID', x='Formado tecnología e informática', color='Sexo', barmode='group', text='ID', color_discrete_sequence= px.colors.qualitative.Set2)
    fig_2.update_traces(textposition='outside',
                          texttemplate='%{text}')
    col2.plotly_chart(fig_2, config=config)

    st.markdown("### Docentes de tecnología e informática")
    st.write('Estadísticas')
