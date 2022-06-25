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
        df = df[df['Sexo'].isin(['Femenino',"Masculino"])]
        df['Formado TeI'] = "Sí"
        df.loc[df['Formado tecnología e informática']=='No','Formado TeI'] = 'No'
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        st.write("Fecha de actualización", df.Fecha.max())
        col_m1.metric("Número de docentes", sum(df.groupby('Sexo').ID.nunique()))
        col_m2.metric('Número de instituciones', len(df['Código IE'].unique()))
        col_m3.metric('Promedio de docentes por institución', int(df.groupby('Código IE').ID.nunique().mean()))
        col_m4.metric('Promedio de docentes formados CFK', int(df[df['Formado CFK']=='Sí'].groupby('Código IE').ID.nunique().mean()))

        col1, col2= st.columns(2)
        docentes_sexo(df,col1)
        formado_tei(df,col2)
        promedio_institucion(df,col1)
        promedio_cfk(df,col2)

        formado_cfk_sexo(df)
        formado_cfk_porcentaje(df)
        implementa_porcentaje(df)
        distribucion_cfk(df)


        country_map()


        st.markdown("### Docentes de tecnología e informática")
        st.write('Estadísticas')
        col3, col4= st.columns(2)

        # Cantidad de materias que ven los profes que dan informatica
        _df = pd.read_feather(f'{DATA_PATH}/preguntas/pregunta1_docentes_pre.feather')
        fig = px.bar(_df,x="Cantidad de Materias",text='Conteo',y="Conteo",color='Nivel',barmode='group',title='¿Qué cantidad de materias enseña el profesor que da informática?',color_discrete_sequence= px.colors.qualitative.Set2)
        fig.update_traces(textposition='outside',
                    texttemplate='%{text}')
        plots.center_title(fig)
        col3.plotly_chart(fig,config=config)

        _df = pd.read_feather(f'{DATA_PATH}/preguntas/pregunta3_docentes_pre.feather')
        fig = px.bar(_df,x='Grado',y='Conteo',color='Sexo',barmode='group',text='Conteo',color_discrete_sequence= px.colors.qualitative.Set2)
        fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['Prescolar','1°','2°','3°','4°','5°','6°','7°','8°','9°','10°','11°']},title="Sexo de los docentes segun el grado")
        fig.update_traces(textposition='outside',
                    texttemplate='%{text}')
        plots.center_title(fig)
        col4.plotly_chart(fig,config=config)
        
        # ¿Cuales son esas materias?
        _df = pd.read_feather(f'{DATA_PATH}/preguntas/pregunta2_docentes_pre.feather')
        st.write(_df)


def docentes_sexo(df, col=None):
    pivot_1 = pd.pivot_table(df, index='Sexo', values='ID', aggfunc='nunique').reset_index()
    total = pivot_1['ID'].sum()

    pivot_1['% docentes'] = pivot_1['ID']/total
    st.write(total)
    fig_1 = px.bar(pivot_1, x='Sexo', y ='% docentes',  color='Sexo', title='% de docentes impactados',
                       color_discrete_sequence=px.colors.qualitative.Set2,text='% docentes')
    fig_1.update_traces(textposition='outside')
    plots.percentage_labelsy(fig_1)
    fig_1.update_yaxes(range=(0,1))
    col.plotly_chart(fig_1, config=config)


def formado_tei(df,col=None):
    pivot_2 = pd.pivot_table(df, index=['Formado TeI','Sexo'],values='ID', aggfunc='nunique').reset_index()
    total = pivot_2.groupby('Sexo').ID.sum().reset_index().rename(columns={'ID':'Total'})
    pivot_2 = pivot_2.merge(total, on='Sexo')
    pivot_2['% formado TeI'] = pivot_2['ID']/pivot_2['Total']
    fig_2 = px.bar(pivot_2, y='% formado TeI', x='Formado TeI', color='Sexo',
                   barmode='group', text='% formado TeI', title="% de docentes formados en Tecnología",
                   color_discrete_sequence= px.colors.qualitative.Set2)
    fig_2.update_traces(textposition='outside')
    plots.percentage_labelsy(fig_2)
    fig_2.update_yaxes(range=(0,1))
    col.plotly_chart(fig_2, config=config)

def promedio_institucion(df,col=None):
    pivot=df.pivot_table(index=['Código IE', 'Sexo'],values='ID', aggfunc='count').reset_index()
    pivot=pivot.rename(columns={'ID':'Cantidad de Docentes'})
    pivot2=pivot.pivot_table(index=['Sexo'],values='Cantidad de Docentes',
                             aggfunc='mean').reset_index().rename(columns={'Cantidad de Docentes':'Promedio de docentes'})
    pivot2['Promedio de docentes'] = pivot2['Promedio de docentes'].round(1)
    fig =px.bar(pivot2,x='Sexo', y='Promedio de docentes', title='Promedio de docentes por institución',
                color='Sexo',
                template="plotly_white",text="Promedio de docentes",
                color_discrete_sequence=px.colors.qualitative.Set2)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    plots.text_position(fig)
    col.plotly_chart(fig, config=config,use_container_width=True)

def promedio_cfk(df,col=None):
    pivotf=df.pivot_table(index=['Formado CFK','Sexo'],values='ID', aggfunc='nunique').reset_index()
    pivotf=pivotf.rename(columns={'ID':'Cantidad de Docentes'})
    pivotf = pivotf.loc[pivotf['Formado CFK']=='Sí',:]
    pivotf['Promedio de docentes'] = round(pivotf['Cantidad de Docentes']/252,1)
    fig =px.bar(pivotf,x='Formado CFK',
                y='Promedio de docentes',
                barmode='group',
                template="plotly_white",
                color='Sexo',
                text='Promedio de docentes',
                title='Promedio de docentes formados en CFK',
                color_discrete_sequence=px.colors.qualitative.Set2)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_traces(textposition='outside',
                    texttemplate='%{text}')
    col.plotly_chart(fig, config=config,use_container_width=True)

def distribucion_cfk(df,col=None):
    pivotf=df.loc[df['Formado CFK']=='Sí',:].pivot_table(index=['Código IE'],values='ID', aggfunc='nunique').reset_index()
    pivotf=pivotf.rename(columns={'ID':'Cantidad de Docentes'})
    #total = pivotf.groupby(['Cantidad de Docentes','Sexo'])['Código IE'].count().reset_index()
    pivotf = pivotf.groupby(['Cantidad de Docentes'])['Código IE'].count().reset_index().rename(columns={'Código IE':'Cant IE'})
    pivotf['Frecuencia'] = pivotf['Cant IE']  / 252
    #pivotf['Promedio de docentes'] = round(pivotf['Cantidad de Docentes']/252,1)
    fig =px.bar(pivotf,x='Cantidad de Docentes',
                y='Frecuencia',
                barmode='group',
                template="plotly_white",
                text='Frecuencia',
                title='Distribución de docentes formados en CFK',
                color_discrete_sequence=px.colors.qualitative.Set2)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_traces(textposition='outside')
    plots.percentage_labelsy(fig)
    fig.update_yaxes(range=(0,1))
    st.plotly_chart(fig, config=config,use_container_width=True)


def formado_cfk_sexo(df,col=None):
    pivotf=df.pivot_table(index=['Formado CFK','Sexo'],values='ID', aggfunc='nunique').reset_index()
    pivotf=pivotf.rename(columns={'ID':'Cantidad de Docentes'})
    total = pivotf.groupby('Formado CFK')['Cantidad de Docentes'].sum().reset_index().rename(columns={'Cantidad de Docentes':'Total'})
    pivotf = pivotf.merge(total, on='Formado CFK')
    pivotf['Frecuencia'] = pivotf['Cantidad de Docentes']/pivotf['Total']
    fig =px.bar(pivotf,x='Formado CFK',
                y='Frecuencia',
                barmode='group',
                color='Sexo',
                template="plotly_white",
                text='Frecuencia',
                title='Cantidad de docentes formados en CFK',
                color_discrete_sequence=px.colors.qualitative.Set2)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_traces(textposition='outside',
                    texttemplate='%{text}')
    plots.percentage_labelsy(fig)
    fig.update_yaxes( range=(0,1.05))
    st.plotly_chart(fig, config=config,use_container_width=True)

def formado_cfk_porcentaje(df,col=None):
    pivotf=df.pivot_table(index=['Formado CFK'],values='ID', aggfunc='nunique').reset_index()
    pivotf=pivotf.rename(columns={'ID':'Cantidad de Docentes'})
    total = len(set(df.ID))
    pivotf['% formado CFK'] = pivotf['Cantidad de Docentes']/total

    fig =px.bar(pivotf,x='Formado CFK',
                y='% formado CFK',
                template="plotly_white",
                text='% formado CFK',
                title='% de docentes formados en CFK',
                color_discrete_sequence=px.colors.qualitative.Set2)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    plots.text_position(fig, pos="outside")
    plots.percentage_labelsy(fig)
    fig.update_yaxes( range=(0,1.05))
    st.plotly_chart(fig, config=config,use_container_width=True)


def implementa_porcentaje(df,col=None):
    pivotf=df.pivot_table(index=['Formado CFK','Implementa fichas', 'Sexo'],values='ID', aggfunc='nunique').reset_index()
    pivotf=pivotf.rename(columns={'ID':'Cantidad de Docentes'})
    pivotf = pivotf.loc[pivotf['Formado CFK']=='Sí',:]
    total = pivotf.groupby('Sexo')['Cantidad de Docentes'].sum().reset_index().rename(columns={'Cantidad de Docentes':'Total'})
    pivotf = pivotf.merge(total, on='Sexo')
    pivotf['% implementa fichas'] = pivotf['Cantidad de Docentes']/pivotf['Total']

    fig =px.bar(pivotf,x='Implementa fichas',
                y='% implementa fichas',
                color='Sexo',
                barmode='group',
                template="plotly_white",
                text='% implementa fichas',
                title='% de docentes formados en CFK que implementan fichas',
                color_discrete_sequence=px.colors.qualitative.Set2)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    plots.text_position(fig, 'outside')
    plots.percentage_labelsy(fig)
    fig.update_yaxes( range=(0,1.05))
    st.plotly_chart(fig, config=config,use_container_width=True)

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

    st.plotly_chart(fig, config=config)
