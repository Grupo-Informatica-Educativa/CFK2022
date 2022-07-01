import streamlit as st
import plotly.express as px
import utils.plots as plots
from utils.read_data import read_data

#pio.templates.default = "plotly_white"

import pages.c_pages.Formacion.Consolidado_Formacion as page_consolidado_formacion
import pages.c_pages.Formacion.prepost_inicial as page_prepost_inicial



config = plots.get_config()

def app():
    plots.plotly_settings(px)
    st.title('Formación')
    _type = st.selectbox('',["Prepostest Inicial 2022","Consolidado Formación 2020-2022"])
    st.write("##")


    if(_type =="Prepostest Inicial 2022"):
        page_prepost_inicial.app()
    if(_type =="Consolidado Formación 2020-2022"):
        page_consolidado_formacion.app()
    


if __name__ == "__main__":
    app()