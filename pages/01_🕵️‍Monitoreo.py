import streamlit as st
import plotly.express as px
import utils.plots as plots
from utils.read_data import read_data

#pio.templates.default = "plotly_white"

import pages.c_pages.Monitoreo.monitoreo_cons as page_monitoreo


config = plots.get_config()

def app():
    plots.plotly_settings(px)
    st.title('Monitoreo')
    _type = st.selectbox('Elija el grupo que desea ver',["Consolidación"])
    st.write("##")


    if(_type =='Consolidación'):
        page_monitoreo.app()
    


if __name__ == "__main__":
    app()