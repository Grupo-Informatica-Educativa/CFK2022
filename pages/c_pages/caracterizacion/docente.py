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
        df['Formado TeI'] = "Sí"
        df.loc[df['Formado tecnología e informática']=='No','Formado TeI'] = 'No'
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        st.write("Fecha de actualización", df.Fecha.max())
        col_m1.metric("Número de docentes", len(df.ID.unique()))
        col_m2.metric('Número de instituciones', len(df['Código IE'].unique()))
        col_m3.metric('Promedio de docentes por institución', int(df.groupby('Código IE').ID.nunique().mean()))
        col_m4.metric('Promedio de docentes formados CFK', int(df[df['Formado CFK']=='Sí'].groupby('Código IE').ID.nunique().mean()))

        col1, col2= st.columns(2)

        pivot_1 = pd.pivot_table(df, index='Sexo', values='ID', aggfunc='nunique').reset_index()
        fig_1 = px.bar(pivot_1, x='Sexo', y ='ID',  color='Sexo', text='ID', color_discrete_sequence= px.colors.qualitative.Set2)
        fig_1.update_traces(textposition='outside',
                            texttemplate='%{text}')
        col1.plotly_chart(fig_1, config=config)

        pivot_2 = pd.pivot_table(df, index=['Formado TeI','Sexo'],values='ID', aggfunc='nunique').reset_index()
        fig_2 = px.bar(pivot_2, y='ID', x='Formado TeI', color='Sexo', barmode='group', text='ID', color_discrete_sequence= px.colors.qualitative.Set2)
        fig_2.update_traces(textposition='outside',
                            texttemplate='%{text}')
        col2.plotly_chart(fig_2, config=config)

        country_map()


        st.markdown("### Docentes de tecnología e informática")
        st.write('Estadísticas')
        col1, col2= st.columns(2)

        # Cantidad de materias que ven los profes que dan informatica
        _df = pd.read_feather(f'{DATA_PATH}/preguntas/pregunta1_docentes_pre.feather')
        fig = px.bar(_df,x="Cantidad de Materias",text='Conteo',y="Conteo",color='Nivel',barmode='group',title='¿Qué cantidad de materias enseña el profesor que da informática?',color_discrete_sequence= px.colors.qualitative.Set2)
        fig.update_traces(textposition='outside',
                    texttemplate='%{text}')
        plots.center_title(fig)
        col1.plotly_chart(fig,config=config)

        _df = pd.read_feather(f'{DATA_PATH}/preguntas/pregunta3_docentes_pre.feather')
        fig = px.bar(_df,x='Grado',y='Conteo',color='Sexo',barmode='group',text='Conteo',color_discrete_sequence= px.colors.qualitative.Set2)
        fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['Prescolar','1°','2°','3°','4°','5°','6°','7°','8°','9°','10°','11°']},title="Sexo de los docentes segun el grado")
        fig.update_traces(textposition='outside',
                    texttemplate='%{text}')
        plots.center_title(fig)
        col2.plotly_chart(fig,config=config)
        
        # ¿Cuales son esas materias?
        _df = pd.read_feather(f'{DATA_PATH}/preguntas/pregunta2_docentes_pre.feather')
        st.write(_df)


def prommedio_institucion(df):
    pivot=df.pivot_table(index=['Código IE', 'Sexo'],values='ID', aggfunc='count').reset_index()
    pivot=pivot.rename(columns={'ID':'Cantidad de Docentes'})
    pivot2=pivot.pivot_table(index=['Sexo'],values='Cantidad de Docentes', aggfunc='mean').reset_index().rename(columns={'Cantidad de Docentes':'Promedio de docentes'})


def country_map():
    _,c,_ = st.columns(3)
    c.write('### Cantidad de colegios')
    _,c,c1,_,_ = st.columns(5)
    with open(f"{DATA_PATH}/departamentos.geo.json","rb") as f:
        outlines = json.load(f)

    map_df = pd.read_feather(f'{DATA_PATH}/mapa_directivos.feather')
    fig = px.choropleth_mapbox(map_df, geojson=outlines, locations='Departamento',
                           color="Conteo",
                           color_continuous_scale="Viridis",
                           featureidkey='properties.NOMBRE_DPT',
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=4, center = {"lat": 4.3556, "lon": -74.0451},
                           opacity=0.5
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    c.plotly_chart(fig, config=config)
