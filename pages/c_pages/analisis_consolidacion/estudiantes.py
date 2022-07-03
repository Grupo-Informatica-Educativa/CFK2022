import streamlit as st
import itertools
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.chart_funcs import *
from utils.helper_funcs import *
from utils.answer_funcs import *
from utils.read_data import read_data_xlsx

preguntas_cols = [
    "Un algoritmo es:",
    "¿Para qué sirven los algoritmos?",
    "Un bucle es:",
    "¿Cuál de las siguientes opciones sí le permite al robot completar la misión de fotografiar cada tortuga?",
    "¿Qué mensaje deseaba enviar la líder Wayuú?",
    "¿Cuál de los siguientes códigos permite que el robot complete su misión sembrando café?",
    "¿Cuál será la foto con más vistas?",
    "Ayuda al robot verde a salir del laberinto",
    "Óscar lleva 2 loncheras a la escuela todos los días ¿Cuál de las siguientes afirmaciones es falsa?",
    "¿Cuál de las siguientes hamburguesas tiene los ingredientes A, E y F?",
    "¿Qué botella debe cambiarse de color para que el resultado final sea una botella de color blanco?"
]

respuestas_correctas_estudiantes = {
    "Un algoritmo es:":"Una secuencia lógica de pasos para realizar una tarea",
    "¿Para qué sirven los algoritmos?":"Para planificar la solución a un problema",
    "Un bucle es:":"Un conjunto de instrucciones que se ejecuta mientras se cumpla una condición",
    "¿Cuál de las siguientes opciones sí le permite al robot completar la misión de fotografiar cada tortuga?":"a.",
    "¿Qué mensaje deseaba enviar la líder Wayuú?":"c. Nublado",
    "¿Cuál de los siguientes códigos permite que el robot complete su misión sembrando café?":"a.",
    "¿Cuál será la foto con más vistas?":"c) Julio",
    "Ayuda al robot verde a salir del laberinto":"b.",
    "Óscar lleva 2 loncheras a la escuela todos los días ¿Cuál de las siguientes afirmaciones es falsa?":"c) Si Óscar empaca Deditos para merendar, puede hacer Arroz de pollo para almorzar",
    "¿Cuál de las siguientes hamburguesas tiene los ingredientes A, E y F?":"a.",
    "¿Qué botella debe cambiarse de color para que el resultado final sea una botella de color blanco?":"a) La botella B debe ser verde"
}

caracterizacion_cols = [
    'N registro',
    'Deseo participar en el estudio',
    'Código IE',
    'Grupo',
    'Nombre',
    'Fecha',
    'ID',
    'Número de lista',
    'Edad',
    'Sexo',
    'Sector vivienda',
    'Internet',
    'Uso del dispositivo móvil',
    'Nivel escolaridad madre',
    'Nivel escolaridad padre',
    'Ocupación madre',
    'Ocupación padre',
    '¿Con quién vives?',
    'Grado'
]



@st.cache()
def fetch():
    data = read_data_xlsx("estudiantes2022")
    other_cols = []
    for col in data.columns:
        if col not in caracterizacion_cols:
            other_cols.append(col)
    data = data[caracterizacion_cols + sorted(other_cols)]
    return data.copy()

def app():
    
    col_preguntas = caracterizacion_cols.__len__()
    columna_unica = 'Código IE'
    datos = fetch()
    list_of_ie = datos[columna_unica].unique()
    selected_ies = st.multiselect("Filtrar por código de institución educativa",options=sorted(list_of_ie),help="Por defecto se muestran resultados de todas las IE")
    
    if len(selected_ies)  > 0:
        datos = datos[datos[columna_unica].isin(selected_ies)]
  
    chart_type = st.radio("Tipo de visualización ",
                          ("Barras", "Dispersión", "Cajas", "Tendencia", "Tabla resumen"))

    
    categoria = "Conocimientos"

    if datos is not None:
        pregunta, filtros_def, indices, lista_agrupadores, lista_grupo = filtros(
            datos, col_preguntas, chart_type, categoria, nombres_preguntas={},questions_sorted=False)

        ejex, color, columna, fila = filtros_def

        hasAnswer = False

        if pregunta in respuestas_correctas_estudiantes:
            resp_correct = respuestas_correctas_estudiantes[pregunta]
            datos["Respuesta"] = datos[pregunta].apply(lambda x: "Correcto" if x == resp_correct else "Incorrecto")
            hasAnswer = True
            color = "Respuesta"

        if chart_type != "Tabla resumen":
            height = st.slider(
                "Ajuste el tamaño vertical de la gráfica", 500, 1000)

        orden_grupos = ["I"+str(x) for x in range(87)]

        category_orders = categories_order(
            set(datos[pregunta]), pregunta, orden_grupos)


        if lista_grupo != []:
            datos = datos.loc[datos.Grupo.isin(lista_grupo)]

        if len(datos) == 0:
            st.warning(
                "El / los grupos seleccionados no tienen datos para mostrar")
        elif (fila == "Grupo" or columna == "Grupo") and (len(datos.Grupo.unique()) > 10):
            st.warning(
                "Por favor use los filtros para seleccionar menos grupos")
        elif chart_type == "Tabla resumen":
            # En helper_functs.filtros se devuelve
            # datos.columns[col_preguntas], [None]*4, None, [], lista_cursos
            # cuando no están habilitados los filtros (checkbox)
            filters_off = (pregunta == datos.columns[col_preguntas] and filtros_def == [None]*4
                           and indices == None and lista_agrupadores == [])

        

            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(wrapText=True, autoHeight=True)
            gb.configure_selection()
            gb.configure_grid_options(suppressFieldDotNotation=True)
            gridOptions = gb.build()
            AgGrid(df, gridOptions=gridOptions,
                   fit_columns_on_grid_load=df.columns.shape[0] < 5)
        else:
            # Selecciona tipo de gráfica
            if chart_type == "Barras":
                """ Los diagramas de barra exigen agrupar la información antes de graficar """
                if hasAnswer:
                    indices.append("Respuesta")

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
            # Quita los nombres de los ejes (se ven feos cuando se divide por columnas)
            fig.update_yaxes(col=1, title=None)
            fig.update_xaxes(row=1, title=None)

            fig.update_layout(height=height)

            st.plotly_chart(fig, use_container_width=True, config=config_chart)
