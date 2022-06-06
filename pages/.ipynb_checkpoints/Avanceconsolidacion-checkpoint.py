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
def read_database(name):
    return pd.read_excel(name)

def app():
    st.title('Avance Consolidación 2022')
    
    tabla = pd.read_excel('data/InstrumentosCFK.xlsx', index_col=0)
    st.write('Fecha de actualización:',tabla.loc[0,'Fecha'])
    tabla2= tabla.iloc[:,:-1]
    gb = GridOptionsBuilder.from_dataframe(tabla2)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    #gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()
    grid_response = AgGrid(
    tabla2,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=True,
    theme= 'streamlit', #Add theme color to the table
    enable_enterprise_modules=False,
    height=400, 
    width='100%',
    reload_data=True
    )
    
    
    st.write("### Descarga de datos")

    
    b_col1, b_col2, b_col3 = st.columns(3)
    
    with b_col1:
        df_xlsx = to_excel(tabla2)
        st.download_button(
         label="Descargar Avance Consolidación",
         data=df_xlsx,
         file_name='Avance Consolidación.xlsx',
         mime='text/xlsx',key=1
        )
        docentes = read_database('data/descargables/DocentesCFK.xlsx')
        df_xlsx = to_excel(docentes)
        st.download_button(
         label="Descargar Base de datos docentes",
         data=df_xlsx,
         file_name='Docentes.xlsx',
         mime='text/xlsx',key=0
        )
        
    with b_col2:
        estudiantes = read_database('data/descargables/EstudiantesCFK.xlsx')
        df_xlsx = to_excel(estudiantes)
        st.download_button(
         label="Descargar Base de datos estudiantes",
         data=df_xlsx,
         file_name='Estudiantes.xlsx',
         mime='text/xlsx', key=2
        )
        directivos = read_database('data/descargables/DirectivosCFK.xlsx')
        df_xlsx = to_excel(directivos)
        st.download_button(
         label="Descargar Base de datos directivos",
         data=df_xlsx,
         file_name='Directivos.xlsx',
         mime='text/xlsx', key=2
        )
    
    with b_col3:
        plan = read_database('data/descargables/PlanCFK.xlsx')
        df_xlsx = to_excel(plan)
        st.download_button(
         label="Descargar Base de datos Plan de area",
         data=df_xlsx,
         file_name='Plan.xlsx',
         mime='text/xlsx',key=3
        )
        
        plan = read_database('data/descargables/LiderCFK.xlsx')
        df_xlsx = to_excel(plan)
        st.download_button(
         label="Descargar Base de datos Lider de area",
         data=df_xlsx,
         file_name='Lider.xlsx',
         mime='text/xlsx',key=4
        )

    
    
    #st.download_button(label='Descargar Avance', export, file_name='Avance_Consolidación.csv',mime='text/csv')