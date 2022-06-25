import streamlit as st
import pandas as pd
import plotly.express as px
import utils.plots as plots
import json

DATA_PATH = "data/c_pages/caracterizacion"
config = plots.get_config()


def app(df=None):
    if df is not None:
        plots.plotly_settings(px)
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        st.write("Fecha de actualización", df.Fecha.max())
        col_m1.metric("Número de estudiantes", sum(df.groupby('Sexo').ID.count()))
        col_m2.metric("Número de niños", len(df[df['Sexo']=='Masculino']))
        col_m3.metric("Número de niñas", len(df[df['Sexo']=='Femenino']))
        col_m4.metric('Promedio de estudiantes por institución', int(df.groupby('Código IE').ID.nunique().mean()))

        col1, col2= st.columns(2)
        est_sexo(df,col1)
        est_disc(df,col2)
        est_sector(df,col1)
        # formado_tei(df,col2)
        # promedio_institucion(df,col1)
        # promedio_cfk(df,col2)
        #
        # formado_cfk(df)
        # formado_cfk_porcentaje(df)
        # implementa_porcentaje(df)
        # distribucion_cfk(df)



def est_sexo(df, col=None):
    pivot_e=df.pivot_table(index=['Código IE', 'Sexo'],values='ID', aggfunc='count').reset_index()
    pivot_e=pivot_e.rename(columns={'ID':'Cantidad de Estudiantes'})
    pivot_e2=pivot_e.pivot_table(index=['Sexo'],values='Cantidad de Estudiantes', aggfunc='mean').reset_index()
    pivot_e2['Frecuencia'] = pivot_e2['Cantidad de Estudiantes']/sum(pivot_e2['Cantidad de Estudiantes'])

    fig =px.bar(pivot_e2,x='Sexo', y='Frecuencia',
                template="plotly_white",
                text='Frecuencia',
                color='Sexo',
                color_discrete_sequence=px.colors.qualitative.Set2,
                title='% Estudiantes por género')
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_traces(textposition='outside')
    plots.percentage_labelsy(fig)
    fig.update_yaxes(range=(0,1))
    col.plotly_chart(fig, config=config)

def est_disc(df, col=None):
    pivot_e4=df.pivot_table(index=['¿Te reconoces como una persona con algún tipo de discapacidad?'],values='ID', aggfunc='count').reset_index()
    pivot_e4=pivot_e4.rename(columns={'ID':'Cantidad de Estudiantes', '¿Te reconoces como una persona con algún tipo de discapacidad?': 'Discapacidad'})
    pivot_e4 = pivot_e4.loc[pivot_e4['Discapacidad'].isin(['Sí','No'])]
    pivot_e4['Frecuencia'] = pivot_e4['Cantidad de Estudiantes']/sum(pivot_e4['Cantidad de Estudiantes'])

    fig =px.bar(pivot_e4,x='Discapacidad', y='Frecuencia',
                template="plotly_white",
                text='Frecuencia',
                color_discrete_sequence=px.colors.qualitative.Set2,
                title='% Estudiantes que se reconocen con discapacidad')
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_traces(textposition='outside')
    plots.percentage_labelsy(fig)
    fig.update_yaxes(range=(0,1))
    col.plotly_chart(fig, config=config)

def est_sector(df, col=None):
    pivot_sec=df.pivot_table(index=['Sector vivienda'],values='ID', aggfunc='count').reset_index()
    pivot_sec=pivot_sec.rename(columns={'ID':'Cantidad de Estudiantes'})
    pivot_sec['Frecuencia'] = pivot_sec['Cantidad de Estudiantes']/sum(pivot_sec['Cantidad de Estudiantes'])

    fig =px.bar(pivot_sec,x='Sector vivienda', y='Frecuencia',
                template="plotly_white",
                text='Frecuencia',
                color_discrete_sequence=px.colors.qualitative.Set2,
                title='% Sector de la vivienda')
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_traces(textposition='outside')
    plots.percentage_labelsy(fig)
    fig.update_yaxes(range=(0,1))
    col.plotly_chart(fig, config=config)
