import streamlit as st
import pandas as pd
import numpy as np
import utils.plots as plots
import plotly.express as px
import plotly.graph_objects as go
from utils.read_data import read_data_xlsx

from plotly.subplots import make_subplots

config = plots.get_config()

def app():
    plots.plotly_settings(px)
    st.title('Observaciones e Instantaneas')
    st.write("## Prácticas pedagógicas implementadas por docentes")
    grafica01_1()
    st.write("## Prácticas pedagógicas implementadas por docentes por género")
    grafica01_2()
    st.write("## Cantidad de prácticas implementadas")
    grafica02_1()
    st.write("## Cantidad de prácticas implementadas por género")
    grafica02_2()
    # st.write("## ¿Se presentan los objetivos de aprendizaje de la lección?")
    # grafica3()
    # st.write("## Exploración de los conocimientos previos")
    # grafica4()
    # st.write("## Actividad desconectada")
    # grafica5()
    # st.write("## Momentos Progresión Usa-Modifica-Crea")
    # grafica6()
    # st.write("¿Se usa el vocabulario adecuado para la enseñanza del pensamiento computacional (terminología correcta)?")
    # grafica7()
    # st.write("¿Se hace uso de la memoria colectiva?")
    # grafica8()
    # st.write("Fidelidad de implementación de la ficha")
    # grafica9()
    # st.write("Cantidad de graficas pedagogicas implementadas")
    # grafica10()

# Observaciones acorde a asignaturas STEM - No STEM
def grafica01_1():
    data = read_data_xlsx("observaciones_gen","01")
    #print(data['Prácticas implementadas'].unique())
    pract_og = [' Se estimula el liderazgo femenino',
                'Los retos de programación se enmarcan en una narrativa',
                'Se dedica tiempo de la clase a hacer reflexiones sobre equidad de género']
    pract_gr = ['Liderazgo femenino',
                'Narrativa',
                'Reflexión']
    dict_practicas = dict(zip(pract_og,pract_gr))
    data['Practicas'] = data['Prácticas implementadas'].replace(dict_practicas)
    data['Total'] = len(data)
    piv_data = data.pivot_table(index=['Practicas'],
                                values=['id', 'Total'],
                                aggfunc={'id':'count', 'Total':'max'}).rename(columns={'id':'Cant'}).reset_index()
    piv_data['Frecuencia'] = piv_data['Cant']/piv_data['Total']
    #st.write(piv_data)
    fig = px.bar(piv_data,x='Frecuencia',y='Practicas',
                 color=None,
                 barmode="group",
                 orientation='h',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template="plotly_white",
                 text='Frecuencia')
    fig.update_layout(autosize=True)
    plots.text_position(fig)
    plots.legend_position(fig)
    plots.percentage_labelsy(fig)
    plots.percentage_labelsx(fig)
    st.plotly_chart(fig,use_container_width=True)

def grafica01_2():
    data = read_data_xlsx("observaciones_gen","01")
    #print(data['Prácticas implementadas'].unique())
    #st.write(data)
    pract_og = [' Se estimula el liderazgo femenino',
                'Los retos de programación se enmarcan en una narrativa',
                'Se dedica tiempo de la clase a hacer reflexiones sobre equidad de género']
    pract_gr = ['Liderazgo femenino',
                'Narrativa',
                'Reflexión']
    dict_practicas = dict(zip(pract_og,pract_gr))
    data['Practicas'] = data['Prácticas implementadas'].replace(dict_practicas)

    piv_data = data.pivot_table(index=['Practicas','Género'],
                                values=['id'],
                                aggfunc={'id':'count'}).rename(columns={'id':'Cant'}).reset_index()
    total = data.groupby('Género').id.nunique().reset_index().rename(columns={'id':'Total'})
    piv_data = piv_data.merge(total, on='Género')
    piv_data['Frecuencia'] = piv_data['Cant']/piv_data['Total']

    fig = px.bar(piv_data,x='Frecuencia',y='Practicas',
                 color='Género',
                 barmode="group",
                 orientation='h',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template="plotly_white",
                 text='Frecuencia')
    fig.update_layout(autosize=True)
    plots.text_position(fig)
    plots.legend_position(fig)
    plots.percentage_labelsy(fig)
    plots.percentage_labelsx(fig)
    st.plotly_chart(fig,use_container_width=True)

# Número de Observaciones por Tipo de sesión
def grafica02_1():
    data = read_data_xlsx("observaciones_gen","02")
    #st.write(data.columns)
    data['Total'] = len(data)
    data['Cantidad de prácticas implementadas'] = data['Cantidad de prácticas implementadas'].astype(str)
    piv_data = data.pivot_table(index=['Cantidad de prácticas implementadas'],
                                values=['id', 'Total'],
                                aggfunc={'id':'count', 'Total':'max'}).rename(columns={'id':'Cant'}).reset_index()
    piv_data['Frecuencia'] = piv_data['Cant']/piv_data['Total']
    #st.write(piv_data)
    fig = px.bar(piv_data,y='Frecuencia',x='Cantidad de prácticas implementadas',
                 color=None,
                 barmode="group",
                 orientation='v',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template="plotly_white",
                 text='Frecuencia')
    fig.update_layout(autosize=True)
    fig.update_yaxes( range=(0,1))
    plots.text_position(fig)
    plots.legend_position(fig)
    plots.percentage_labelsy(fig)
    st.plotly_chart(fig,use_container_width=True)


def grafica02_2():
    data = read_data_xlsx("observaciones_gen","02")
    #st.write(data)
    data['Cantidad de prácticas implementadas'] = data['Cantidad de prácticas implementadas'].astype(str)
    col_i = 'Cantidad de prácticas implementadas'
    piv_data = data.pivot_table(index=[col_i,'Género'],
                                values=['id'],
                                aggfunc={'id':'count'}).rename(columns={'id':'Cant'}).reset_index()
    total = data.groupby('Género').id.nunique().reset_index().rename(columns={'id':'Total'})
    piv_data = piv_data.merge(total, on='Género')
    piv_data['Frecuencia'] = piv_data['Cant']/piv_data['Total']

    fig = px.bar(piv_data,y='Frecuencia',x=col_i,
                 color='Género',
                 barmode="group",
                 orientation='v',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 template="plotly_white",
                 text='Frecuencia')
    fig.update_layout(autosize=True)
    fig.update_yaxes(range=(0,1))
    plots.text_position(fig)
    plots.legend_position(fig)
    plots.percentage_labelsy(fig)
    st.plotly_chart(fig,use_container_width=True)

# ¿Se presentan los objetivos de aprendizaje de la lección?
def grafica3():
    data = read_data_xlsx("observaciones_gen",3)
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
    data = read_data_xlsx("observaciones_gen",4)
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
    data = read_data_xlsx("observaciones_gen",5)
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
    data = read_data_xlsx("observaciones_gen",6)
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
    data = read_data_xlsx("observaciones_gen",7)
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
    data = read_data_xlsx("observaciones_gen",8)
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
    data = read_data_xlsx("observaciones_gen",9)
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
    data = read_data_xlsx("observaciones_gen",10)
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