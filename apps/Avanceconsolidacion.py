import streamlit as st
import pandas as pd
import numpy as np
import utils.plots as plots
import plotly.express as px
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

config = plots.get_config()

#----

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

@st.cache
def read_database(name, index_col=None):
    return pd.read_excel(name, index_col=index_col)

def app():
    st.title('Avance consolidación 2022')

    tabla = read_database('data/descargables/InstrumentosCFK.xlsx', index_col=0)
    st.write('Fecha de actualización:',tabla.loc[0,'Fecha'])
    tabla2= tabla.drop(columns='Fecha')

    detallada = read_database('data/descargables/Instrumentos_DetalleCFK.xlsx', index_col=0)

    ver_detalle = False
    #ver_detalle = st.checkbox('Ver porcentajes de avance')

    if ver_detalle:
        datos_mostrar = detallada


    else:
        datos_mostrar = tabla2

    columnas = [(x,x[9:].capitalize()) for x in datos_mostrar.columns if "Encuesta" in x]
    columnas = dict(columnas)

    datos_mostrar = datos_mostrar.rename(columns=columnas)

    gb = GridOptionsBuilder.from_dataframe(datos_mostrar)
    gb.configure_pagination(paginationAutoPageSize=False,paginationPageSize=20) #Add pagination
    gb.configure_columns()
    gb.configure_side_bar() #Add a sidebar #gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gb.configure_auto_height(autoHeight=False)
    gridOptions = gb.build()
    #st.write(gridOptions)
    gridOptions["defaultColDef"]['skipHeaderOnAutoSize'] = True
    gridOptions["defaultColDef"]['wrapText'] = True
    gridOptions["columnDefs"][0]['pinned'] = True
    #st.write(gridOptions["columnDefs"][0].keys())



    grid_response = AgGrid(
    datos_mostrar,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT',
    update_mode='NO_UPDATE',
    fit_columns_on_grid_load=False,
    theme= 'streamlit', #Add theme color to the table
    enable_enterprise_modules=False,
    reload_data=False,
    height=630
    )


    df_xlsx = to_excel(datos_mostrar)
    st.download_button(
     label="Descargar Avance Consolidación",
     data=df_xlsx,
     file_name='Avance Consolidación.xlsx',
     mime='text/xlsx',key=1)


    st.write("### Descarga de datos")

    st.write('''Los datos finales están disponibles en Drive para su *descarga*.
    Utilice click derecho para descargar cada uno de los archivos. No intente abrirlo desde Drive''')
    st.write('''
    * :white_check_mark: [Bases de datos](https://drive.google.com/drive/folders/10-vecqL2rtGRXkZ4H6xkI4DY1Z5wr7fw?usp=sharing)
    * :exclamation: [Registros eliminados](https://drive.google.com/drive/folders/1xaulGr1dAuJqx2AwtGRKCcRhm9jQZCUP?usp=sharing)
    ''')
