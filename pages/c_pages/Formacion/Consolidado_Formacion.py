import streamlit as st
import pandas as pd
import plotly.express as px
import utils.plots as plots
from utils.read_data import read_data, read_data_xlsx
import streamlit as st
from utils.chart_funcs import *
from utils.helper_funcs import *

files =[{
        "title": "Integrados Formacion",
        "file":  'integrados_formacion'
    }]


def app():
    st.title("Consolidado formación")

    chart_type = st.radio("Tipo de visualización ",
                          ("Barras", "Dispersión", "Cajas", "Tendencia"))
    # Nombre del archivo con los datos

    categoria = st.selectbox("Seleccione la categoría", files,
                             format_func=lambda itemArray: itemArray['title'])

    # Nombre de la columna cuyos datos son únicos para cada respuesta
    columna_unica = 'CC'
    # A partir de esta columna comienzan las preguntas (columnas de interés)
    col_preguntas = 5


    file=True
    if file:
        datos = read_data_xlsx(files[0]["file"])
        datos = datos.dropna(subset=['Género'])
        datos['Género'] = datos['Género'].replace({1:'Masculino',2:'Femenino'})
        datos = datos[datos['Género'].isin(['Masculino', 'Femenino'])]
        datos['Año'] = datos['Año'].astype(str)
        #st.dataframe(datos.head())

        pregunta, filtros_def, indices, lista_agrupadores, lista_grupos = filtros(
            datos, col_preguntas, chart_type)

        ejex, color, columna, fila = filtros_def
        height = st.slider(
            "Ajuste el tamaño vertical de la gráfica", 500, 1000)

        if color == "Eficacia":
            datos = graph_answer(datos, pregunta, categoria)


        if categoria['title'] == 'Conocimientos':
            if pregunta == 'Puntaje Conocimiento':
                datos[pregunta] = datos[pregunta].astype(float)
            else:
                datos[pregunta] = datos[pregunta].astype(str)

        orden_grupos = ["A"+str(x) for x in range(36)]
        category_orders = categories_order(
            set(datos[pregunta]), pregunta, orden_grupos)

        if lista_grupos != []:
            datos = datos.loc[datos.Grupo.isin(lista_grupos)]
        if len(datos) == 0:
            st.warning(
                "El / los grupos seleccionados no tienen datos para mostrar")
        elif (fila == "Grupo" or columna == "Grupo") and (len(datos.Grupo.unique()) > 10):
            st.warning(
                "Por favor use los filtros para seleccionar menos grupos")
        else:
            # Selecciona tipo de gráfica
            if chart_type == "Barras":
                """ Los diagramas de barra exigen agrupar la información antes de graficar """
                pivot = pivot_data(datos, indices, columna_unica)
                fig = bar_chart(columna_unica=columna_unica,
                                pivot=pivot, ejex=ejex, color=color,
                                fila=fila, columna=columna, indices=indices,
                                category_orders=category_orders)
            elif chart_type == "Cajas":
                fig = box_chart(columna_unica=pregunta,
                                pivot=datos, ejex=ejex, color=color,
                                fila=fila, columna=columna, indices=indices, category_orders=category_orders)
                fig.update_yaxes(col=1, title=None)
            elif chart_type == "Tendencia":
                fig = line_chart(columna_unica=columna_unica,
                                 pivot=datos, ejex=ejex, color=color, indices=indices,
                                 fila=fila, columna=columna,
                                 lista_agrupadores=datos.columns.tolist(),
                                 category_orders=category_orders)
            else:
                fig = scatter_chart(columna_unica=columna_unica,
                                    pivot=datos, ejex=ejex, color=color,
                                    fila=fila, columna=columna,
                                    lista_agrupadores=datos.columns.tolist(),
                                    category_orders=category_orders)

            # Evita que los títulos de las subfiguras sean de forma VARIABLE=valor
            fig.for_each_annotation(
                lambda a: a.update(text=a.text.split("=")[-1]))
            fig.update_yaxes(col=1, title=None)
            fig.update_xaxes(row=1, title=None)

            fig.update_layout(height=height)

            st.plotly_chart(fig, use_container_width=True, config=config_chart)

if __name__ == "__main__":
    app()