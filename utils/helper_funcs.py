import pandas as pd
import streamlit as st
from utils.answer_funcs import *


@st.cache(allow_output_mutation=True)
def load_data(file):
    return pd.read_excel(file)


def filtros(datos, col_preguntas, tipo_grafica, categoria=None, nombres_preguntas={}, pregunta_con_numero=True, preguntas_en_ejex=False):
    if tipo_grafica == "Tabla resumen":
        # TODO: guardar la salida de este checkbox
        if not st.checkbox("Habilitar filtros"):
            try:
                cursos = datos.Grupo.unique()
                cursos.sort()
                lista_cursos = st.multiselect(
                    'Seleccione los cursos que desea visualizar', cursos)
            except:
                lista_cursos = []
            # pregunta: se devuelve por defecto la columna del indice col_preguntas
            # (igual esto no se usa y es para que no de error)
            return datos.columns[col_preguntas], [None]*4, None, [], lista_cursos

    lista_filtros = []

    lista_preguntas_subpreguntas = list(datos.iloc[:, col_preguntas:].columns)

    lista_agrupadores = list(datos.iloc[:, 1:col_preguntas].columns)
    if preguntas_en_ejex:
        lista_agrupadores = list(datos.iloc[:, 1:].columns)

    # Se incluyen las preguntas (sean o no divisibles)
    lista_preguntas = set()

    for preg in lista_preguntas_subpreguntas:
        try:
            pos_punto = preg.index(".")
        except:
            pos_punto = 0
        num_preg = preg[:pos_punto]
        pregunta = nombres_preguntas[num_preg] if num_preg in nombres_preguntas else preg
        lista_preguntas.add(pregunta)
    pregunta = st.selectbox("Seleccione la pregunta: ",
                            sorted(list(lista_preguntas)))

    numero = pregunta.split(' ')[0]

    if numero[:-1].isdigit():
        lista_subpreguntas = [
            x for x in datos.columns if x.startswith(numero) and x != pregunta]
    else:
        lista_subpreguntas = []
    if len(lista_subpreguntas) > 0:
        pregunta = st.selectbox(
            "Seleccione la subpregunta:", lista_subpreguntas)

    try:
        cursos = datos.Grupo.unique()
        cursos.sort()
        lista_cursos = st.multiselect(
            'Seleccione los cursos que desea visualizar', cursos)
    except:
        lista_cursos = []

    if tipo_grafica == 'Cajas':
        lista_filtros.append(st.selectbox(
            "Seleccione el eje x", [' '] + lista_agrupadores))
    elif tipo_grafica == 'Dispersión':
        lista_filtros.append(st.selectbox(
            "Seleccione el eje x", lista_agrupadores))
    elif tipo_grafica == 'Tendencia':
        lista_filtros.append(st.selectbox(
            "Seleccione el eje x", lista_agrupadores))

    else:
        lista_filtros.append(st.selectbox("Seleccione el eje x", [
            "Pregunta"] + lista_agrupadores))

    cols = st.columns(3)

    if has_answer(datos, pregunta, categoria, pregunta_con_numero):
        lista_agrupadores_color = ["Eficacia"] + lista_agrupadores
    else:
        lista_agrupadores_color = lista_agrupadores

    for index, col in enumerate(cols):
        with col:
            if index == 0:
                lista_filtros.append(st.selectbox("Dividir por color", [
                    " ", "Pregunta"] + lista_agrupadores_color))
            elif index == 1:
                lista_filtros.append(st.selectbox("Dividir por columna", [
                    " ", "Pregunta"] + lista_agrupadores))
            elif index == 2:
                lista_filtros.append(st.selectbox("Dividir por fila", [
                    " ", "Pregunta"] + lista_agrupadores))

    filtros_def = [None if x == ' ' else x for x in lista_filtros]
    filtros_def = [pregunta if x == "Pregunta" else x for x in filtros_def]
    indices = list(set(filtros_def).difference([None]))

    return pregunta, filtros_def, indices, lista_agrupadores, lista_cursos


def filtros_tabla(datos, col_preguntas, tipo_grafica, categoria=None, arreglo_preguntas=[], analisis=False):
    lista_filtros = []

    lista_agrupadores = list(datos.iloc[:, 1:col_preguntas].columns)

    lista_preguntas = [str("Pregunta ") + arreglo_preguntas[x].split(' ')[0][:-1]
                       for x in range(len(arreglo_preguntas))]
    pregunta = st.selectbox("Seleccione la pregunta: ",
                            lista_preguntas)
    pregunta = arreglo_preguntas[lista_preguntas.index(pregunta)]

    lista_cursos = []

    if tipo_grafica == 'Cajas' or tipo_grafica == 'Dispersión':
        lista_filtros.append(st.selectbox(
            "Seleccione el eje x", lista_agrupadores))
    else:
        if not analisis:
            lista_filtros.append(st.selectbox("Seleccione el eje x", [
                                 "Pregunta"] + lista_agrupadores))
        else:
            lista_filtros.append(st.selectbox(
                "Seleccione el eje x", ["Pregunta"]))

    cols = st.columns(3)

    if has_answer(datos, pregunta, categoria):
        lista_agrupadores_color = ["Eficacia"] + lista_agrupadores
    else:
        lista_agrupadores_color = lista_agrupadores

    for index, col in enumerate(cols):
        with col:
            if index == 0:
                if not analisis:
                    lista_filtros.append(st.selectbox("Dividir por color", [
                                         " ", "Pregunta"] + lista_agrupadores_color))
                else:
                    lista_filtros.append(st.selectbox(
                        "Dividir por color", ["Pregunta"]))
            elif index == 1:
                if not analisis:
                    lista_filtros.append(st.selectbox("Dividir por columna", [
                                         " ", "Pregunta"] + lista_agrupadores))
                else:
                    lista_filtros.append(st.selectbox(
                        "Dividir por columna", [" "] + lista_agrupadores))
            elif index == 2:
                if not analisis:
                    lista_filtros.append(st.selectbox("Dividir por fila", [
                                         " ", "Pregunta"] + lista_agrupadores))
                else:
                    lista_filtros.append(st.selectbox(
                        "Dividir por fila", [" "] + lista_agrupadores))

    filtros_def = [None if x == ' ' else x for x in lista_filtros]
    filtros_def = [pregunta if x == "Pregunta" else x for x in filtros_def]
    indices = list(set(filtros_def).difference([None]))

    return pregunta, filtros_def, indices, lista_agrupadores, lista_cursos


def filtros_multiselect_vertical(datos, col_preguntas, tipo_grafica, columnas_filtros=None):
    if columnas_filtros is not None and columnas_filtros != []:
        for col in columnas_filtros:
            options = datos[col].unique()
            options = ["NR" if pd.isna(x) else x for x in options]
            # options.sort()
            filtro_list = st.multiselect(
                f"Seleccione {col.lower()}(s):", options)
            if filtro_list != []:
                datos = datos.loc[datos[col].isin(filtro_list)]

    lista_filtros = []

    lista_agrupadores = list(datos.iloc[:, 1:col_preguntas].columns)

    if tipo_grafica == 'Cajas':
        lista_filtros.append(st.selectbox(
            "Seleccione el eje x", [' '] + lista_agrupadores))
    elif tipo_grafica == 'Dispersión':
        lista_filtros.append(st.selectbox(
            "Seleccione el eje x", lista_agrupadores))
    else:
        lista_filtros.append(st.selectbox(
            "Seleccione el eje x", list(dict.fromkeys(columnas_filtros + lista_agrupadores))))

    cols = st.columns(3)
    _list = list(dict.fromkeys([" "] + columnas_filtros + lista_agrupadores))
    with cols[0]:
        lista_filtros.append(st.selectbox(
            "Dividir por color", _list))
    with cols[1]:
        lista_filtros.append(st.selectbox(
            "Dividir por columna", _list))
    with cols[2]:
        lista_filtros.append(st.selectbox(
            "Dividir por fila", _list))

    filtros_def = [None if x == ' ' else x for x in lista_filtros]
    indices = list(set(filtros_def).difference([None]))

    try:
        columns_lower = [col.lower() for col in datos.columns]
        i = columns_lower.index('respuesta')
        pregunta = datos.columns[i]
    except:
        pregunta = st.selectbox(
            "Seleccione la columna de respuestas:", datos.columns)
    return datos, pregunta, filtros_def, indices, lista_agrupadores


def pivot_data(datos, indices, columna_unica):
    return datos.pivot_table(index=indices,
                             values=columna_unica,
                             aggfunc="count").reset_index()