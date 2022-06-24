import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.chart_funcs import *
from utils.helper_funcs import *
from utils.answer_funcs import *

files = [
    {
        "title": "Autoeficacia",
        "file":  "Autoeficacia.xlsx",
    },
    {
        "title": "Conocimientos",
        "file":  "Conocimiento.xlsx",
        "respuestas": {
            "24": "3",
            "25": "El programa no funciona, debe capturar nuevamente el valor de la temperatura luego de encender el ventilador",
            "26": "6",
            "27": "10",
            "28": "II y III",
            "29": "La segunda expresión es verdadera si “(a O b)” es verdadero",
            "31": "Está equivocada, el resultado es 120.",
        }
    },
    {
        "title": "Género",
        "file":  "Género.xlsx",
    }
]

# Nombre de las preguntas por el indice
# Esto se usará para aquellas preguntas que tengan subpreguntas
nombres_preguntas = {
    "12":"12. Estrategias en clase",
    "15": "15. Afirmaciones autoeficacia técnologica",
    "17": "17. Practicas",
    "18": "18. Integración Pensamiento Computacional",
    "20": "20. Prácticas pedagógicas",
    "22": "22. Estrategias contra dificultades"
}


def app():
    st.write("""# Pretest Inicial C1""")

    file = f"data/descargables/Inicial_Pre_Y_Post_Cohorte1.xlsx"
    # Nombre de la columna cuyos datos son únicos para cada respuesta
    columna_unica = '1. Cédula'
    
    chart_type = st.radio("Tipo de visualización ",
                          ("Barras", "Dispersión", "Cajas", "Tendencia", "Tabla resumen"))

    categoria = st.selectbox("Seleccione la categoría", files,
                             format_func=lambda itemArray: itemArray['title'])
    file = f"data/c_pages/cohorte1/inicial/{categoria['file']}"
    
    col_preguntas = 20

    if file:
        datos = load_data(file)
        datos = datos.rename(columns={'Tipo':'Instrumento'})

        pregunta, filtros_def, indices, lista_agrupadores, lista_grupo = filtros(
            datos, col_preguntas, chart_type, categoria, nombres_preguntas=nombres_preguntas)

        ejex, color, columna, fila = filtros_def
        if chart_type != "Tabla resumen":
            height = st.slider(
                "Ajuste el tamaño vertical de la gráfica", 500, 1000)

        if color == "Eficacia":
            datos = graph_answer(datos, pregunta, categoria)

        orden_grupos = ["I"+str(x) for x in range(87)]

        if categoria['title'] == 'Conocimientos':
            if pregunta == 'Puntaje Conocimiento':
                datos[pregunta] = datos[pregunta].astype(float)
            else:
                datos[pregunta] = datos[pregunta].astype(str)

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
