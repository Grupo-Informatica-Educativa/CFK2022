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
    st.write("## ¿Quiénes están socializando su trabajo?")
    grafica_inst(1)
    st.write("## ¿Quiénes no están involucrados en las actividades propuestas?")
    grafica_inst(2)
    st.write("## ¿Quiénes están manipulando los materiales?")
    grafica_inst(3)
    st.write("## ¿Quiénes están ejerciendo roles de liderazgo?")
    grafica_inst(4)


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
    st.plotly_chart(fig,use_container_width=True, config=config)

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
    st.plotly_chart(fig,use_container_width=True, config=config)

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
    st.plotly_chart(fig,use_container_width=True, config=config)


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
    plots.legend_position(fig, orientation='v', xanchor='right', yanchor='top', y=1, x=1.2)
    plots.percentage_labelsy(fig)
    st.plotly_chart(fig,use_container_width=True, config=config)

# ¿Se presentan los objetivos de aprendizaje de la lección?
def grafica_inst(n):
    data = read_data_xlsx("observaciones_gen",n)
    data['Opción'] = data['Opción'].str.split(",").str[0]
    #st.write(list(data['Opción'].unique()))
    total = data.groupby('Opción').ID.nunique().reset_index().rename(columns={'ID':'Total'})

    piv_data = data.pivot_table(index=['Opción','Categoría'],
                                values=['ID'],
                                aggfunc={'ID':'count'}).rename(columns={'ID':'Cant'}).reset_index()

    piv_data = piv_data.merge(total, on='Opción')
    piv_data['Frecuencia'] = piv_data['Cant']/piv_data['Total']
    fig = px.bar(piv_data,
            x='Frecuencia',
            y='Opción',
            color='Categoría',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            text='Frecuencia',
            template="plotly_white", category_orders={'Categoría': ['0 - 20 casi nunca',
                                                                    '20 - 40 poco frecuente',
                                                                    '40 - 60 frecuente',
                                                                    '60 - 80 muy frecuente',
                                                                    '80 - 100 casi siempre'],
                                                      'Opción': ["Sólo los niños",
                                                                 "Principalmente los niños",
                                                                 "Niños y niñas por igual",
                                                                 "Principalmente las niñas",
                                                                 "Sólo las niñas",
                                                                 ]})
    fig.update_layout(autosize=True)
    plots.text_position(fig, pos="inside")
    plots.legend_position(fig, orientation='v', xanchor='right', yanchor='top', y=1, x=1.5)
    plots.percentage_labelsy(fig)
    plots.percentage_labelsx(fig)
    st.plotly_chart(fig,use_container_width=True, config=config)




if __name__=="__main__":
    app()