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

    st.write("Nota temporal: En la leyenda de la gráfica 1000 corresponde al promedio y 2000 a la moda de todos los colegios evaluados")

    marco = pd.read_excel('data/Marco acumulativo.xlsx')
    df_xlsx = to_excel(marco)
    st.download_button(
    label="Descargar Resultados por institución",
    data=df_xlsx,
    file_name='Consolidado_Marco.xlsx',
    mime='text/xlsx',key=1)


    marco['Color IE'] = marco['Código IE'].astype(str).str.replace('Promedio','1000').str.replace('Moda','2000')
    marco['Color IE'] = marco['Color IE'].astype(float).astype(int)

    IE = st.multiselect('Seleccione las instituciones que desea ver: ', list(marco['Código IE'].unique()), default=['Moda','Promedio'])
    IE = [str(x) for x in IE]
    marco_m = marco.melt(id_vars=['Código IE', 'Color IE'], var_name='Dim', value_name='Nivel')
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
    if len(IE)>0:

        with st.container():
            separar = st.checkbox('Ver en gráficas separadas', value=False)
            pl_marco = marco_m[marco_m['Código IE'].isin(list(IE))]

            fig = px.line_polar(
            pl_marco, r="Nivel", theta="Dimensión",
            color="Color IE", line_close=True,
            category_orders={'Nivel':['1A', '1B', '2A', '2B', '3', '4', '5'],
            'Dim':["Dimensión "+str(x) for x in range(1,9)],
            'Dimensión': ['Liderazgo','Currículo','Enseñanza','Dllo profesional',
            'EDI','Ed.Terciaria','Impacto', 'Género']},
            hover_name='Dim',
            hover_data={'Color IE': False,'Código IE':True,'Nivel':True, 'Descripción':True},
            range_r=['-1','6'], markers=True, render_mode='svg',
            color_discrete_sequence=px.colors.qualitative.Set2,
            height=600,
            template='plotly_white')
            if not separar:
                if st.checkbox('Ver solo lineas'):
                    fig.update_traces(fill=None)
                else:
                    fig.update_traces(fill='toself')


            fig.update_polars(
                   radialaxis_gridcolor="#b0cbf8",
                   radialaxis_griddash="dot",
                   radialaxis_gridwidth=0.2,
                                    radialaxis_linecolor="#b0cbf8",
                   radialaxis_tickcolor="#b0cbf8",
                angularaxis_gridcolor="#b0cbf8",
            angularaxis_gridwidth=0.2)
                #fig.update_xaxes(gridcolor="#b0cbf8")

            st.plotly_chart(fig, config=config)


        with st.container():
            filas = (len(IE)//2)+1
            spfig = make_subplots(
            cols=2,rows=filas,
            specs=[[{"type": "polar"}]*2]*filas,
            vertical_spacing=0.2, horizontal_spacing=0.2
        )
        # use base go capability and copy wanted parameters from px trace
            fila = 0
            height = 500
            for r, ie in enumerate(pl_marco["Código IE"].unique(),start=1):
                pl_marcot = pl_marco.loc[pl_marco["Código IE"].eq(ie)]

                if r%2 ==0:
                    col= 2

                else:
                    col = 1
                    fila +=1
                    height+=500


                spfig.add_trace(
                    go.Scatterpolar(
                        {
                            **fig.to_dict()["data"][0],
                            **{
                                "r": pl_marcot["Nivel"],
                                "theta": pl_marcot["Dimensión"],
                                "name": str(ie),
                                "marker": {
                                    **fig.to_dict()["data"][0]["marker"],
                                    "color": pl_marcot["Color IE"]},

                                },
                            },
                            fill = "toself",
                    ),

                    row=fila,
                    col=col,

                )
                #spfig.update_layout(polar=dict(radialaxis = dict(visible = False,
                # range = [0, 6])),
                # showlegend = False)
                spfig.update_polars( radialaxis=dict(categoryorder='array',
                categoryarray= ['1A', '1B', '2A', '2B', '3', '4', '5'],
                range=[-1,6],visible = True),
                angularaxis=dict(categoryorder='array',
                categoryarray=['Liderazgo','Currículo','Enseñanza','Dllo profesional',
                'EDI','Ed.Terciaria','Impacto', 'Género'],
                direction='clockwise'
                ))

            # finally copy across layout parameters
            spfig = spfig.update_layout({ **fig.to_dict()["layout"], **spfig.to_dict()["layout"]})
            #spfig.layout.template = fig.layout.template
            #for axis in ["polar","polar2","polar3"]:
            #    spfig.layout[axis]["angularaxis"] = fig.layout.polar["angularaxis"]

            # and we're done...
            spfig.update_layout(height=height, width=1000,title=dict(
                  x=0.5,
                  y=0.2,
                  xanchor='center',
                  yanchor='top',
                  # pad = dict(
                  #            t = 0
                  #           ),
                  font=dict(
                      #family='Courier New, monospace',
                      size=40,
                      color='#000000'
                  )))
            if separar:
                st.plotly_chart(spfig, use_container_width=False)


if __name__=="__main__":
    app()