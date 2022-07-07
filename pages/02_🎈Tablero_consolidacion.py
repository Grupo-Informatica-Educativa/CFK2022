import streamlit as st
import plotly.express as px
import utils.plots as plots
from utils.read_data import read_data

#pio.templates.default = "plotly_white"

import pages.c_pages.caracterizacion.docente as page_docente
import pages.c_pages.caracterizacion.estudiante as page_estudiante


config = plots.get_config()

def app():
    plots.plotly_settings(px)
    st.title('Consolidación')
    _type = st.selectbox('Elija el grupo que desea ver',["Estudiantes","Docentes","Directivos"])
    st.write("##")

    df = get_data(_type)

    if(_type =='Docentes'):
        page_docente.app(df)
    if(_type =='Estudiantes'):
        page_estudiante.app(df)
    

# Helpers

def get_data(name):
    if (name == 'Estudiantes'):
        return read_data('est_sociodemo')
    if (name == 'Directivos'):
        return read_data('dir_sociodemo')
    if (name == 'Docentes'):
        return read_data('doc_sociodemo')

if __name__ == "__main__":
    app()