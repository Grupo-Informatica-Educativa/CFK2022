import streamlit as st
import pandas as pd
import numpy as np
import utils.plots as plots
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

from plotly.subplots import make_subplots
from pages.c_pages.analisis_consolidacion.directivos import app as page_directivos_app
from pages.c_pages.analisis_consolidacion.estudiantes import app as page_estudiantes_app
from pages.c_pages.analisis_consolidacion.docentes import app as page_docentes_app
from pages.c_pages.analisis_consolidacion.lideres import app as page_lideres_app
from pages.c_pages.analisis_consolidacion.plan import app as page_plan_app
from pages.c_pages.analisis_consolidacion.equipos import app as page_equipo_app



config = plots.get_config()

@st.cache
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data
 
def prepare_data(marco):
    marco['Tipo de observación'] = 'Institución'
    marco.loc[marco['Código IE']=='Moda','Tipo de observación'] = "Moda"
    marco.loc[marco['Código IE']=='Promedio','Tipo de observación'] = "Promedio"
    marco['Color IE'] = marco['Código IE'].astype(str).str.replace('Promedio','1000').str.replace('Moda','2000')
    marco['Color IE'] = marco['Color IE'].astype(float).astype(int)
    cols_dimen = marco.filter(regex='^Dimen').columns
    indices = list(set(marco.columns).difference(set(cols_dimen)))

    marco_m = marco.melt(id_vars=indices, var_name='Dim', value_name='Nivel')
    marco_m['Código IE'] = marco_m['Código IE'].astype(str)
    marco_m['Nivel'] = pd.Categorical(marco_m['Nivel'], categories=['1A', '1B', '2A', '2B', '3', '4', '5'], ordered=True)
    dimensiones_dict = dict(zip(["Dimensión "+str(x) for x in range(1,9)],
    ['Liderazgo','Currículo', 'Enseñanza',
    'Dllo profesional','EDI','Ed.Terciaria',
    'Impacto','Género']))

    descripciones={'Dimensión 7': "Logros<br>en cuanto a aprendizajes<br>de todos los estudiantes.",
    'Dimensión 8':"La IE<br>ofrece igualdad<br>de oportunidades a<br>niños y niñas.",
    'Dimensión 2':"Un plan<br>de estudios de TeI que<br>incluya pensamiento<br>computacional o ciencias<br>de la computación",
    'Dimensión 5': "Grado en<br>que la IE es inclusiva",
    "Dimensión 3": "Grando en<br>que estudiantes cuentan con docentes<br>que tienen el conocimiento tecnológico<br>y pedagógico del contenido necesario",
    "Dimensión 1": "Medida en<br>que las directivas se esfuerzan por<br>articular el plan de TeI con la visión",
    'Dimensión 4': "Medida en que<br> los y las docentes<br>tienen acceso a formación<br>profesional docente en PC",
    "Dimensión 6": "Medida en que<br>la IE hace visibles las<br>oportunidades laborales STEM",
    }
    marco_m['Dimensión'] = marco_m['Dim'].replace(dimensiones_dict)
    marco_m['Descripción'] = marco_m['Dim'].replace(descripciones)
    marco_m = marco_m[marco_m['Nivel']!=0]
    return marco_m

def grouped_global_data(marco_m, col_wrap=2):
    pl_marco = marco_m[marco_m['Tipo de observación'] == 'Institución']
    pl_marco = pl_marco.pivot_table(index=['Dimensión','Nivel'],
                                   values='Color IE',
                                   aggfunc='nunique').rename(columns={'Color IE':"Cant.IE"}).reset_index()

    total = pl_marco.groupby('Dimensión')['Cant.IE'].sum().reset_index().rename(columns={"Cant.IE":"Total"})

    pl_marco = pl_marco.merge(total, on='Dimensión')
    pl_marco['Frecuencia'] = pl_marco['Cant.IE'] / pl_marco["Total"]
    dimensiones = marco_m.loc[:,['Dim','Dimensión','Descripción']]
    dimensiones = dimensiones.drop_duplicates()

    pl_marco = pl_marco.merge(dimensiones, on='Dimensión', how='left')
    return pl_marco

def plot1(pl_marco, col_wrap=2):
    ### Gráfica agrupada horizontal
    fig_h = px.bar(pl_marco, y="Dimensión", x="Frecuencia",
                 orientation='h',color="Nivel",
    category_orders={'Nivel':['1A', '1B', '2A', '2B', '3', '4', '5'],
    'Dim':["Dimensión "+str(x) for x in range(1,9)],
    'Dimensión': ['Liderazgo','Currículo','Enseñanza','Dllo profesional',
    'EDI','Ed.Terciaria','Impacto', 'Género']},
                 text='Frecuencia',
    hover_name='Dim',
    hover_data={'Nivel':True, 'Descripción':True},
    color_discrete_sequence=px.colors.qualitative.Pastel, height=600)

    fig_h.for_each_xaxis(lambda yaxis: yaxis.update(tickformat=',.0%'))
    fig_h.update_traces(textposition='inside', texttemplate='%{text:,.1%}')
    st.plotly_chart(fig_h, config=config, use_container_width=True)

def plot2(pl_marco, col_wrap=2, height=1000):
    ### Gráfica vertical dividida por col
    fig_v = px.bar(pl_marco, y="Frecuencia", x="Nivel", facet_col='Dimensión',
                 barmode='group', facet_col_wrap=col_wrap,
                 orientation='v',
                 category_orders={'Nivel':['1A', '1B', '2A', '2B', '3', '4', '5'],
                                  'Dim':["Dimensión "+str(x) for x in range(1,9)],
                                  'Dimensión': ['Liderazgo','Currículo','Enseñanza','Dllo profesional',
                                                'EDI','Ed.Terciaria','Impacto', 'Género']},
                 text='Frecuencia',
                 hover_name='Dim',
                 hover_data={'Nivel':True, 'Descripción':True},
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                height=height)
    fig_v.for_each_annotation(
        lambda a: a.update(text=a.text.split("=")[-1]))
    fig_v.for_each_yaxis(lambda yaxis: yaxis.update(tickformat=',.0%'))
    fig_v.update_traces(textposition='outside', texttemplate='%{text:,.1%}')
    fig_v.for_each_xaxis(lambda xaxis: xaxis.update(showticklabels=True))
    st.plotly_chart(fig_v, config=config, use_container_width=True, heigth=1200)


def grouped_zone_data(marco_m):
    zonas_marco = marco_m[marco_m['Tipo de observación'] == 'Institución']
    zonas_marco = zonas_marco.pivot_table(index=['Dimensión','Nivel','Zona'],
                                    values='Color IE',
                                    aggfunc='nunique').rename(columns={'Color IE':"Cant.IE"}).reset_index()

    totalz = zonas_marco.groupby(['Dimensión','Zona'])['Cant.IE'].sum().reset_index().rename(columns={"Cant.IE":"Total"})

    zonas_marco = zonas_marco.merge(totalz, on=['Dimensión','Zona'])

    zonas_marco['Frecuencia'] = zonas_marco['Cant.IE'] /zonas_marco["Total"]

    dimensiones = marco_m.loc[:,['Dim','Dimensión','Descripción']]
    dimensiones = dimensiones.drop_duplicates()

    zonas_marco = zonas_marco.merge(dimensiones, on='Dimensión', how='left')
    return zonas_marco

def plot3(zonas_marco, col_wrap=2, height=1000):
    ### Gráfica vertical dividida por col
    fig_z = px.bar(zonas_marco, y="Frecuencia", x="Nivel", facet_col='Dimensión',
                   barmode='group', facet_col_wrap=col_wrap, color='Zona',
                   orientation='v',
                   category_orders={'Nivel':['1A', '1B', '2A', '2B', '3', '4', '5'],
                                    'Dim':["Dimensión "+str(x) for x in range(1,9)],
                                    'Dimensión': ['Liderazgo','Currículo','Enseñanza','Dllo profesional',
                                                  'EDI','Ed.Terciaria','Impacto', 'Género']},
                   text='Frecuencia',
                   hover_name='Dim',
                   hover_data={'Nivel':True, 'Descripción':True},
                   color_discrete_sequence=px.colors.qualitative.Pastel,
                   height=height)
    fig_z.for_each_annotation(
        lambda a: a.update(text=a.text.split("=")[-1]))
    fig_z.for_each_yaxis(lambda yaxis: yaxis.update(tickformat=',.0%'))
    fig_z.for_each_xaxis(lambda xaxis: xaxis.update(showticklabels=True))
    fig_z.update_traces(textposition='outside', texttemplate='%{text:,.0%}')
    st.plotly_chart(fig_z, config=config, use_container_width=True, heigth=1200)


def plot4(pl_marco, col_wrap=2, height=1000, dimensiones=None):
    ### Gráfica vertical dividida por col
    fig_v = px.bar(pl_marco, y="Frecuencia", x="Nivel", facet_col='Dimensión',
                 barmode='group', facet_col_wrap=col_wrap,
                 orientation='v',
                 category_orders={'Nivel':['1A', '1B', '2A', '2B', '3', '4', '5'],
                                  'Dim':["Dimensión "+str(x) for x in range(1,9)],
                                  'Dimensión':dimensiones},
                 text='Frecuencia',
                 hover_name='Dim',
                 hover_data={'Nivel':True, 'Descripción':True},
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                height=height)
    fig_v.for_each_annotation(
        lambda a: a.update(text=a.text.split("=")[-1]))
    fig_v.for_each_yaxis(lambda yaxis: yaxis.update(tickformat=',.0%'))
    fig_v.update_traces(textposition='outside', texttemplate='%{text:,.1%}')
    fig_v.for_each_xaxis(lambda xaxis: xaxis.update(showticklabels=True))
    st.plotly_chart(fig_v, config=config, use_container_width=True, heigth=1200)

def plot5(zonas_marco, col_wrap=2, height=1000, dimensiones=None):
    ### Gráfica vertical dividida por col
    fig_z = px.bar(zonas_marco, y="Frecuencia", x="Nivel", facet_col='Dimensión',
                   barmode='group', facet_col_wrap=col_wrap, color='Zona',
                   orientation='v',
                   category_orders={'Nivel':['1A', '1B', '2A', '2B', '3', '4', '5'],
                                    'Dim':["Dimensión "+str(x) for x in range(1,9)],
                                    'Dimensión': dimensiones},
                   text='Frecuencia',
                   hover_name='Dim',
                   hover_data={'Nivel':True, 'Descripción':True},
                   color_discrete_sequence=px.colors.qualitative.Pastel,
                   height=height)
    fig_z.for_each_annotation(
        lambda a: a.update(text=a.text.split("=")[-1]))
    fig_z.for_each_yaxis(lambda yaxis: yaxis.update(tickformat=',.0%'))
    fig_z.for_each_xaxis(lambda xaxis: xaxis.update(showticklabels=True))
    fig_z.update_traces(textposition='outside', texttemplate='%{text:,.0%}')
    st.plotly_chart(fig_z, config=config, use_container_width=True, heigth=1200)

def main_app():
    st.title('Marco de consolidación institucional 2022')
    marco = pd.read_excel('data/Marco con categorias.xlsx')
    df_xlsx = to_excel(marco)
    st.download_button(
    label="Descargar Resultados por institución",
    data=df_xlsx,
    file_name='Consolidado_Marco.xlsx',
    mime='text/xlsx',key=1)

    marco_m=prepare_data(marco)
    pl_marco=grouped_global_data(marco_m)
    zonas_marco = grouped_zone_data(marco_m)

    st.write("### Resultados agrupados por dimensión")
    plot1(pl_marco)
    st.write("### Distribución de clasificación en niveles por dimensión")
    col_wrap = st.slider('Número de gráficas por columna',step=1, min_value=1, max_value=8, value=4 )
    height = st.slider('Alto de la grafica',step=10, min_value=600, max_value=1500)
    plot2(pl_marco, col_wrap, height)
    st.write("Dimensiones 1 a 4")
    dimensiones1_4 = ['Liderazgo','Currículo', 'Enseñanza',
    'Dllo profesional']
    plot4(pl_marco.loc[pl_marco['Dimensión'].isin(dimensiones1_4)], col_wrap, height, dimensiones=dimensiones1_4)

    st.write("Dimensiones 5 a 8")
    dimensiones5_8 = ['EDI','Ed.Terciaria',
    'Impacto','Género']
    plot4(pl_marco.loc[pl_marco['Dimensión'].isin(dimensiones5_8)], col_wrap, height, dimensiones=dimensiones5_8)


    st.write("### Distribución de clasificación en niveles por zona")
    plot3(zonas_marco, col_wrap, height)
    st.write("Dimensiones 1 a 4 por zona")
    plot5(zonas_marco.loc[zonas_marco['Dimensión'].isin(dimensiones1_4)], col_wrap, height, dimensiones=dimensiones1_4)
    st.write("Dimensiones 5 a 8 por zona")
    plot5(zonas_marco[zonas_marco['Dimensión'].isin(dimensiones5_8)], col_wrap, height, dimensiones=dimensiones5_8)

paginas_array = [
        {
            'title': "Principal",
            'page': main_app
        },
        {
            'title': "Estudiantes",
            'page': page_estudiantes_app
        },
        {
            'title': "Docentes",
            'page': page_docentes_app
        },
        {
            'title': "Directivos",
            'page': page_directivos_app
        },
        {
            'title': "Lideres",
            'page': page_lideres_app
        },
        {
            'title': "Plan",
            'page': page_plan_app
        },
         {
            'title': "Equipos",
            'page': page_equipo_app
        }
]




def app():
    ### Doing this the long way due to streamlit being a massive cunt with format_func 
    names = []
    paginas_dict = {}

    for item in paginas_array:
        names.append(item["title"]) 
        paginas_dict[item["title"]] = item["page"]

    selected = st.sidebar.radio("Páginas",options=names)
    paginas_dict[selected]()

if __name__=="__main__":
    app()