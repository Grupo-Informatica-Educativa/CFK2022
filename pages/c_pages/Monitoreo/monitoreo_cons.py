import streamlit as st
import pandas as pd
import numpy as np
import utils.plots as plots
import plotly.express as px
import plotly.graph_objects as go
from utils.read_data import read_data

from plotly.subplots import make_subplots

config = plots.get_config()

def app():
    plots.plotly_settings(px)
    st.title('Monitoreo Componente consolidación')
    st.write("## Número de visitas momento 1")
    grafica1()
    st.write("## % de cumplimiento de las actividades por institución")
    grafica2()
    st.write("## % de cumplimiento por actividades")
    grafica3()


# Observaciones acorde a asignaturas STEM - No STEM
def grafica1():
    data = read_data("mon_cons",1)
    data['Cantidad visitas'] = data['Cantidad visitas'].astype(str)
    fig = px.bar(data, x='Cantidad visitas', y='Frecuencia',
             color_discrete_sequence=px.colors.qualitative.Set2,
             template="plotly_white",
             text = 'Frecuencia')
    fig.update_layout(autosize=True)
    plots.text_position(fig)
    plots.legend_position(fig)
    plots.percentage_labelsy(fig)
    st.plotly_chart(fig,use_container_width=True, config=config)

# Número de Observaciones por Tipo de sesión
def grafica2():
    data = read_data("mon_cons",2)
    #data['% Cumplimiento'] = data['% Cumplimiento'].astype(str)
    fig = px.bar(data, x='% Cumplimiento', y='Frecuencia',
             color_discrete_sequence=px.colors.qualitative.Set2,
             template="plotly_white",
             text = 'Frecuencia')
    fig.update_layout(autosize=True)
    plots.text_position(fig)
    plots.legend_position(fig)
    plots.percentage_labelsy(fig)
    plots.percentage_labelsx(fig)
    st.plotly_chart(fig,use_container_width=True, config=config)

# ¿Se presentan los objetivos de aprendizaje de la lección?
def grafica3():
    data = read_data("mon_cons",3)
    fig = px.bar(data, y='Actividad', x='Frecuencia', orientation='h',
             color_discrete_sequence=px.colors.qualitative.Set2,
             template="plotly_white",
             text = 'Frecuencia')
    fig.update_layout(autosize=True)
    plots.text_position(fig)
    plots.legend_position(fig)
    plots.percentage_labelsx(fig)
    plots.percentage_labelsy(fig)

    st.plotly_chart(fig,use_container_width=True, config=config)



if __name__=="__main__":
    app()