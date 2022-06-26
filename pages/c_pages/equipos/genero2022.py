import streamlit as st
import pandas as pd
import plotly.express as px
import utils.plots as plots
import json

from utils.read_data import read_data

config = plots.get_config()
graph_colors = px.colors.qualitative.Set2

# Graficas

def generador_grafica(data=None,discriminado=True):
    if discriminado: 
        fig = px.bar(data,x="Respuesta",y="Porcentaje",text="Porcentaje",color_discrete_sequence=graph_colors,template="plotly_white",color="Género",barmode="group",facet_col="Test")
    else:
        fig = px.bar(data,x="Respuesta",y="Porcentaje",text="Porcentaje",color_discrete_sequence=graph_colors,template="plotly_white",facet_col="Test")

    fig.update_yaxes(range=[0,1.10])
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    fig.for_each_yaxis(lambda yaxis: yaxis.update(tickformat=',.0%'))
    fig.update_traces(textposition='outside', texttemplate='%{text:,.2%}')
    return fig

###########

def grafica_d_inicial():
    data = read_data("genero_2022_d_i")
    return generador_grafica(data)


def grafica_sd_inicial():
    data = read_data("genero_2022_sd_i")
    return generador_grafica(data,False)


## App

opts_map = {
    "Sí":{
        "Inicial": grafica_d_inicial,
    },
    "No":{
        "Inicial": grafica_sd_inicial,
    },
}

def app():
    plots.plotly_settings(px)
    st.write("# Genéro 2021")
    discriminado = st.selectbox("Discriminado por género", ["Sí","No"])
    test = st.selectbox("Tipo", ["Inicial"])
    fig = opts_map[discriminado][test]()
    st.plotly_chart(fig, config=config, use_container_width=True)
