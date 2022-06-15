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
    st.title('Observaciones e Instantaneas')
    st.write("## Observaciones acorde a asignaturas STEM - No STEM")
    grafica1()
    st.write("## Número de Observaciones por Tipo de sesión")
    grafica2()
    st.write("## ¿Se presentan los objetivos de aprendizaje de la lección?")
    grafica3()
    st.write("## Exploración de los conocimientos previos")
    grafica4()
    st.write("## Actividad desconectada")
    grafica5()
    st.write("## Momentos Progresión Usa-Modifica-Crea")
    grafica6()
    st.write("¿Se usa el vocabulario adecuado para la enseñanza del pensamiento computacional (terminología correcta)?")
    grafica7()
    st.write("¿Se hace uso de la memoria colectiva?")
    grafica8()
    st.write("Fidelidad de implementación de la ficha")
    grafica9() 
    st.write("Cantidad de graficas pedagogicas implementadas")
    grafica10()

# Observaciones acorde a asignaturas STEM - No STEM
def grafica1():
    data = read_data("observaciones",1)
    fig = px.bar(data,x='Sesión',y='Count',
             color="isSTEM",
             barmode="group",
             color_discrete_sequence=px.colors.qualitative.Set2,
             template="plotly_white",
            # title="Observaciones acorde asignaturas STEM - NO STEM",
             text_auto=True)
    fig.update_layout(autosize=True)
    plots.text_position(fig)
    plots.legend_position(fig)
    plots.labels(fig)
    st.plotly_chart(fig,use_container_width=True)

# Número de Observaciones por Tipo de sesión
def grafica2():
    data = read_data("observaciones",2)
    fig = px.bar(data,x='Percentage',
             y='Sesión', 
             orientation='h',
             color_discrete_sequence=px.colors.qualitative.Set2,
             template="plotly_white",
             text_auto="0.3s")
    plots.text_position(fig,"inside")
    plots.labels(fig,"Porcentaje de observaciones")
    st.plotly_chart(fig,use_container_width=True)

# ¿Se presentan los objetivos de aprendizaje de la lección?
def grafica3():
    data = read_data("observaciones",3)
    fig = px.bar(data,
            x='Respuesta',
            y='Número de observaciones',
            color_discrete_sequence=px.colors.qualitative.Set2,
            text_auto=True,
            template="plotly_white")
    plots.text_position(fig)
    st.plotly_chart(fig,use_container_width=True)

# Exploración de los conocimientos previos"
def grafica4():
    data = read_data("observaciones",4)
    fig = px.bar(data,
            x='Respuesta',
            y='Número de observaciones',
            color_discrete_sequence=px.colors.qualitative.Set2,
            text_auto=True,
            template="plotly_white")
    plots.text_position(fig)
    st.plotly_chart(fig,use_container_width=True)

# Actividad desconectada
def grafica5():
    data = read_data("observaciones",5)
    fig = px.bar(data,x='Observacion',y='Número de observaciones',
                color="Pregunta",
                barmode="group",
                color_discrete_sequence=px.colors.qualitative.Set2,
                template="plotly_white",
                text_auto=True)
    plots.text_position(fig)
    plots.legend_position(fig)
    fig.update_layout(xaxis_title=None)
    st.plotly_chart(fig,use_container_width=True)

# Momentos Progresión Usa-Modifica-Crea
def grafica6():
    data = read_data("observaciones",6)
    fig = px.bar(data,x='Conteo',y='Tipo',
             color="Accion",
             barmode="group",
             color_discrete_sequence=px.colors.qualitative.Set2,
             template="plotly_white",
             orientation='h',
             text_auto=True)
    plots.text_position(fig)
    plots.legend_position(fig)
    plots.labels(fig)
    st.plotly_chart(fig,use_container_width=True)

# ¿Se usa el vocabulario adecuado para la enseñanza del pensamiento computacional (terminología correcta)?
def grafica7():
    data = read_data("observaciones",7)
    fig = px.bar(data,
            x='Respuesta',
            y='Número de observaciones',
            color_discrete_sequence=px.colors.qualitative.Set2,
            text_auto=True,
            template="plotly_white")
    plots.text_position(fig)
    plots.labels(fig)
    st.plotly_chart(fig,use_container_width=True)

# ¿Se hace uso de la memoria colectiva?
def grafica8():
    data = read_data("observaciones",8)
    fig = px.bar(data,
        x='Porcentaje de observaciones',
        orientation='h',
        y='Respuesta',
        color_discrete_sequence=px.colors.qualitative.Set2,
        text_auto='0.3s',
        template="plotly_white")
    plots.text_position(fig)
    fig.update_layout(yaxis_title=None)
    st.plotly_chart(fig,use_container_width=True)

# Fidelidad de implementación de la ficha
def grafica9():
    data = read_data("observaciones",9)
    fig = px.bar(data,
        x='Respuesta',
        y='Número de observaciones',
        color_discrete_sequence=px.colors.qualitative.Set2,
        text_auto='0.3s',
        template="plotly_white")
    plots.text_position(fig)
    fig.update_layout(yaxis_title=None)
    st.plotly_chart(fig,use_container_width=True)

# Cantidad de graficas pedagogicas implementadas
def grafica10():
    data = read_data("observaciones",10)
    fig = px.bar(data,
        x='Cantidad',
        y='Porcentaje de observaciones',
        color_discrete_sequence=px.colors.qualitative.Set2,
        text_auto='0.3s',
        template="plotly_white")
    plots.text_position(fig)
    plots.labels(fig)
    st.plotly_chart(fig,use_container_width=True)



if __name__=="__main__":
    app()