from _plotly_utils.colors.qualitative import Plotly
import pandas as pd
import plotly.express as px
import streamlit as st

config_chart = {
    'scrollZoom': True, 'displaylogo': False, 'responsive': True,
    'editable': True,
    'toImageButtonOptions': {
        'format': 'png',  # one of png, svg, jpeg, webp
        'filename': 'custom_image',
        'height': None,
        'width': None,
        'scale': 3  # Multiply title/legend/axis/canvas sizes by this factor
    }
}


def relative_bar_chart(columna_total=None, columna_unica=None, pivot=None,
                       ejex=None, color=None, fila=None, columna=None, indices=None, category_orders=None,
                       color_discrete=px.colors.qualitative.Pastel, color_continuous=px.colors.sequential.GnBu,
                       invertir=False, barmode='group', orientation='v'):
    if columna_total == ["Total"]:
        total = pivot[columna_unica].sum()
        pivot['Frecuencia'] = pivot[columna_unica] / total
    elif columna_total == "Preguntas":
        arreglo_indices = [columna_total]
        if fila is not None:
            arreglo_indices.append(fila)
        if columna is not None:
            arreglo_indices.append(columna)
        total = pivot.pivot_table(index=list(set(arreglo_indices)),
                                  values=columna_unica,
                                  aggfunc='sum'
                                  ).rename(columns={columna_unica: "TOTAL"}).reset_index()

        pivot = pivot.merge(total, on=list(set(arreglo_indices)))
        pivot['Frecuencia'] = pivot[columna_unica] / pivot["TOTAL"]
    else:
        total = pivot.pivot_table(index=columna_total,
                                  values=columna_unica,
                                  aggfunc='sum'
                                  ).rename(columns={columna_unica: "TOTAL"}).reset_index()

        pivot = pivot.merge(total, on=columna_total)
        pivot['Frecuencia'] = pivot[columna_unica] / pivot["TOTAL"]

    if not(invertir):
        fig = px.bar(pivot, x=ejex, y="Frecuencia", color=color,
                     facet_row=fila, facet_col=columna, barmode=barmode, color_discrete_sequence=color_discrete,
                     color_continuous_scale=color_continuous, category_orders=category_orders, text="Frecuencia",
                     facet_col_wrap=4, range_y=(0, 1))
        fig.for_each_yaxis(lambda yaxis: yaxis.update(tickformat=',.0%'))
        fig.update_traces(textposition='outside', texttemplate='%{text:,.2%}')
    else:
        fig = px.bar(pivot, x='Frecuencia', y=ejex, color=color,
                     facet_row=fila, facet_col=columna, barmode=barmode, color_discrete_sequence=color_discrete,
                     color_continuous_scale=color_continuous, category_orders=category_orders, text="Frecuencia",
                     facet_col_wrap=4, range_x=(0, 1))
        #fig.update_yaxes(categoryorder="category descending")
        fig.for_each_xaxis(lambda yaxis: yaxis.update(tickformat=',.0%'))
        fig.update_traces(textposition='inside', texttemplate='%{text:,.2%}')

    return fig


def absolute_bar_chart(columna_unica=None, pivot=None, ejex=None, color=None, fila=None, columna=None,
                       category_orders=None, color_discrete=px.colors.qualitative.Pastel,
                       color_continuous=px.colors.sequential.GnBu, orientation='v', invertir=False, barmode='group'):
    if not(invertir):
        fig = px.bar(pivot, x=ejex, y=columna_unica, color=color, facet_row=fila,
                     facet_col=columna, barmode=barmode, color_discrete_sequence=color_discrete,
                     color_continuous_scale=color_continuous, text=columna_unica, facet_col_wrap=4,
                     category_orders=category_orders, orientation=orientation)
    else:
        fig = px.bar(pivot, x=columna_unica, y=ejex, color=color, facet_row=fila,
                     facet_col=columna, barmode=barmode, color_discrete_sequence=color_discrete,
                     color_continuous_scale=color_continuous, text=columna_unica, facet_col_wrap=4,
                     category_orders=category_orders, orientation=orientation)
        #fig.update_yaxes(categoryorder="category descending")
    fig.update_traces(textposition='outside', texttemplate='%{text}')
    fig.update_layout(legend=dict(orientation="h"),
                      template="simple_white")
    return fig


def bar_chart(columna_unica=None, pivot=None, ejex=None, color=None, fila=None, columna=None, indices=None,
              category_orders=None, color_discrete=px.colors.qualitative.Pastel,
              color_continuous=px.colors.sequential.GnBu, key='1', invertir=False):
    # La variable Key puede ser util porque facilita tener un mismo boton (con misma funcionalidad) en lugares diferentes
    if st.checkbox("Ver barras apiladas"):
        barmode = 'stack'
    else:
        barmode = 'group'
    if st.checkbox("Ver barras horizontales"):
        orientation = 'h'
        invertir = True

    else:
        orientation = 'v'

    if st.checkbox("Visualizar frecuencia relativa"):
        if key == '1':
            columna_total = st.multiselect("Relativo respecto a: ", [
                "Total"] + indices, default='Total')
        else:
            # hacer arreglo con fila y columna
            arreglo_indices = []
            if fila is not None:
                arreglo_indices.append(fila)
            if columna is not None:
                arreglo_indices.append(columna)
            columna_total = st.selectbox("Relativo respecto a: ", [
                                         "Total", "Preguntas"] + list(set(arreglo_indices)))
        if len(columna_total) > 1 and 'Total' in columna_total:
            st.warning("Selección errónea. Si desea ver el porcentaje respecto al Total, elimine los demás valores seleccionados, de lo contrario, elimine 'Total' para elegir una combinación personalizada")
            fig = px.bar()
        else:
            fig = relative_bar_chart(columna_total=columna_total,
                                     columna_unica=columna_unica,
                                     pivot=pivot, ejex=ejex, color=color,
                                     fila=fila, columna=columna, indices=indices, category_orders=category_orders,
                                     color_discrete=color_discrete, color_continuous=color_continuous,
                                     invertir=invertir, barmode=barmode, orientation=orientation)
    else:
        fig = absolute_bar_chart(columna_unica=columna_unica,
                                 pivot=pivot, ejex=ejex, color=color,
                                 fila=fila, columna=columna, category_orders=category_orders,
                                 color_discrete=color_discrete, color_continuous=color_continuous,
                                 invertir=invertir, barmode=barmode, orientation=orientation)
    return fig


def box_chart(columna_unica=None, pivot=None, ejex=None, color=None, fila=None, columna=None, indices=None,
              category_orders=None):
    fig = px.box(pivot, x=ejex, y=columna_unica,
                 color=color, facet_row=fila,
                 facet_col=columna,
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 facet_col_wrap=4, category_orders=category_orders)
    return fig


def line_chart(columna_unica=None, pivot=None, ejex=None, color=None, fila=None, columna=None, indices=None,
               category_orders=None, color_discrete=px.colors.qualitative.Pastel, lista_agrupadores=None):
    ejey = st.selectbox("Elija eje Y: ", lista_agrupadores)
    fig = px.line(pivot, x=ejex, y=ejey,
                  color=color, facet_row=fila,
                  facet_col=columna,
                  color_discrete_sequence=color_discrete,
                  facet_col_wrap=4,
                  category_orders=category_orders)
    return fig


def scatter_chart(columna_unica=None, pivot=None, ejex=None, color=None, fila=None, columna=None,
                  lista_agrupadores=None, category_orders=None):
    ejey = st.selectbox("Elija eje Y: ", lista_agrupadores)
    fig = px.scatter(pivot, x=ejex, y=ejey,
                     color=color, facet_row=fila,
                     facet_col=columna,
                     color_discrete_sequence=px.colors.qualitative.Pastel,
                     color_continuous_scale=px.colors.sequential.GnBu,
                     facet_col_wrap=4,
                     category_orders=category_orders)
    return fig


def categories_order(answers=None, pregunta=None, orden_cursos=None):
    satisfaction = ["Nada satisfecho", "Un poco satisfecho", "Neutra",
                    "Muy satisfecho", "Totalmente satisfecho", "No puedo asistir"]
    yes_no = ["SI", "NO"]
    de_acuerdo = ["Totalmente en desacuerdo", "En desacuerdo",
                  "Neutro", "De acuerdo", "Totalmente de acuerdo"]
    imagenes = ['Imagen 1', 'Imagen 2', 'Imagen 3',
                            'Imagen 4', 'No sé/No lo conozco']
    raton = [str(x) for x in range(1, 6)]
    secuela = ['2', '3', '6', '8', '9', 'No sé/No lo conozco']
    edades = ['16-20', '21-24', '25-34', '35-44', '45+']
    edades_estudiantes = ['8-10 años', '11-12 años',
                          '13-14 años', '15-16 años', 'No responde']
    formacion = ['Profesional', 'Profesional licenciado', 'Especialista', 'Magister', 'Doctorado',
                 'No responde']
    conozco = ["No la conozco", "La evitaria", "Me interesa poco",
               "Me parece interesante",
               "Está entre mis preferidas"]

    labores_hogar = ['Menos de 1h', 'Entre 1h y 2h',
                     'Entre 2h y 3h', 'Entre 3h y 4h', 'Mas de 5h']
    cargo = ['Primaria', 'Secundaria', 'Ambas', 'Directivo', 'No responde']
    probable = ['Muy probable', 'Probable', 'Poco probable', 'No responde']

    if len(set(satisfaction) - answers) < 2:
        cat_order = satisfaction
    elif len(set(de_acuerdo) - answers) < 2:
        cat_order = de_acuerdo
    elif len(set(yes_no) - answers) < 2:
        cat_order = yes_no
    elif len(set(imagenes) - answers) < 2:
        cat_order = imagenes
    elif len(set(raton) - answers) < 2:
        cat_order = raton
    elif len(set(secuela) - answers) < 2:
        cat_order = secuela
    elif len(set(edades) - answers) < 2:
        cat_order = edades
    elif len(set(labores_hogar) - answers) < 2:
        cat_order = labores_hogar
    elif len(set(conozco)-answers) < 2:
        cat_order = conozco
    elif len(set(cargo)-answers) < 2:
        cat_order = cargo
    elif len(set(probable) - answers) < 2:
        cat_order = probable
    elif 'No sé/No lo conozco' in answers:
        cat_order = [x for x in list(
            answers) if x != 'No sé/No lo conozco'] + ['No sé/No lo conozco']
    else:
        cat_order = list(answers)

    category_orders = {pregunta: cat_order, 'Instrumento': ['Pretest', 'Posttest'],
                       "GENERO": ["Femenino", "Masculino", "Otro", "Prefiero no responder"],
                       'Género': ["Femenino", "Masculino"], 'Curso': orden_cursos,
                       'Edad': edades,
                       'Nivel de formación': formacion,
                       "dificultad del nivel": ['Básico', 'Medio', 'Alto', 'Avanzado'],
                       "5. categoria trofeo": ["Oro", "Plata", "Bronce"], 'Cohorte': ['C1', 'C2']}

    return category_orders