import streamlit as st
import pandas as pd
import numpy as np
import utils.plots as plots
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

from plotly.subplots import make_subplots

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

def app():
    st.title('Marco de consolidación institucional 2022')
    marco = pd.read_excel('data/Marco con categorias.xlsx')
    df_xlsx = to_excel(marco)
    st.download_button(
    label="Descargar Resultados por institución",
    data=df_xlsx,
    file_name='Consolidado_Marco.xlsx',
    mime='text/xlsx',key=1)

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

    with st.container():
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

        fig = px.bar(pl_marco, y="Dimensión", x="Frecuencia",
                     orientation='h',color="Nivel",
        category_orders={'Nivel':['1A', '1B', '2A', '2B', '3', '4', '5'],
        'Dim':["Dimensión "+str(x) for x in range(1,9)],
        'Dimensión': ['Liderazgo','Currículo','Enseñanza','Dllo profesional',
        'EDI','Ed.Terciaria','Impacto', 'Género']},
                     text='Frecuencia',
        hover_name='Dim',
        hover_data={'Nivel':True, 'Descripción':True},
        color_discrete_sequence=px.colors.qualitative.Pastel)

        fig.for_each_xaxis(lambda yaxis: yaxis.update(tickformat=',.0%'))
        fig.update_traces(textposition='inside', texttemplate='%{text:,.2%}')

    st.plotly_chart(fig, config=config)




if __name__=="__main__":
    app()