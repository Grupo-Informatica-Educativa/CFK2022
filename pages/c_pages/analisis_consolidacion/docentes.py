import streamlit as st
import itertools
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.chart_funcs import *
from utils.helper_funcs import *
from utils.answer_funcs import *
from utils.read_data import read_data, read_data_xlsx


files = [
    {
        "title": "Apoyo",
        "file":  "docentes2022_consolidacion_apoyo",
    },
    {
        "title": "Conocimientos",
        "file":  "docentes2022_consolidacion_conocimiento",
        "respuestas": {
            "Un algoritmo es:":"Una secuencia lógica de pasos para realizar una tarea.",
            "¿Para qué sirven los algoritmos?":"Para planificar la solución a un problema",
            "Un bucle es:":"Un conjunto de instrucciones que se ejecuta mientras se cumpla una condición",
            '¿Cuál es el error conceptual de Tim?':"Cree que, si la condición se cumple, todo lo que sigue se va a ejecutar",
            '¿Cuál es el error conceptual de Ana?':"No tiene claro el concepto de bucle y por eso no logra identificar que A y C hacen lo mismo"
        }
    },
    {
        "title": "Autoeficacia",
        "file":  "docentes2022_consolidacion_autoeficacia",
    },
        {
        "title": "Genero",
        "file":  "docentes2022_consolidacion_genero",
    },
]

def stats(datos_og,selected_ies):
    st.write("**Puntaje promedio IE**")
    total = len(selected_ies) 
    cols = st.columns(total)
    hasPromedio = False
    if "Promedio" in selected_ies:
        promedio = datos_og[datos_og['Código IE'] == 'Promedio']['conocimiento'].iloc[0]
        cols[0].metric("Promedio nacional",promedio)
        cols.pop(0)
        selected_ies.remove('Promedio')
        total -= 1
        hasPromedio = True

    for (ie,col) in zip(selected_ies,cols):
        val = round(datos_og[datos_og['Código IE'] == ie]['conocimiento'].mean(),2)
        if hasPromedio:
            col.metric("IE "+str(ie),f"{val} %",f"{round(val-promedio,2)}%")
        else:
            col.metric("IE "+str(ie),f"{val} %" )

@st.experimental_memo
def fetch_data(file):
    return read_data_xlsx(file)

def app():
    # Nombre de la columna cuyos datos son únicos para cada respuesta
    columna_unica = 'ID'
    
    chart_type = st.radio("Tipo de visualización ",
                          ("Barras", "Dispersión", "Cajas", "Tendencia", "Tabla resumen"))

    categoria = st.selectbox("Seleccione la categoría", files,
                             format_func=lambda itemArray: itemArray['title'])
    file = categoria['file']
    
    col_preguntas = 15

    

    if file:
        datos = fetch_data(file)
        #datos = datos.rename(columns={'Tipo':'Instrumento'})
        #datos = datos[datos['4. Género'].isin(['Femenino','Masculino'])]

        list_of_ie = datos['Código IE'].unique()
        list_of_ie = filter(lambda x: type(x) is int, list_of_ie)
        selected_ies = st.multiselect("Filtrar por código de institución educativa",options=sorted(list_of_ie)+["Promedio"],help="Por defecto se muestran resultados de todas las IE")
        datos_og = datos.copy()
        if len(selected_ies)  > 0:
            datos = datos[datos['Código IE'].isin(selected_ies)]

        pregunta, filtros_def, indices, lista_agrupadores, lista_grupo = filtros(
            datos, col_preguntas, chart_type, categoria, nombres_preguntas={})


        ejex, color, columna, fila = filtros_def

        
        hasAnswer = False

        if categoria['title'] == 'Conocimientos':
            if pregunta in categoria['respuestas']:
                resp_correct = categoria['respuestas'][pregunta]
                datos["Respuesta"] = datos[pregunta].apply(lambda x: "Correcto" if x == resp_correct else "Incorrecto")
                hasAnswer = True
                color = "Respuesta"
        if chart_type != "Tabla resumen":
            height = st.slider(
                "Ajuste el tamaño vertical de la gráfica", 500, 1000)

        if color == "Eficacia":
            datos = graph_answer(datos, pregunta, categoria)

        orden_grupos = ["I"+str(x) for x in range(87)]

        category_orders = categories_order(
            set(datos[pregunta]), pregunta, orden_grupos)

        if categoria['title'] == 'Conocimientos' and len(selected_ies) > 0 :
            stats(datos_og,selected_ies)

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

            if filters_off:
                df = datos.iloc[:, 1:]  # Don't show ids
            else:
                df = pivot_data(datos, indices, columna_unica)

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
