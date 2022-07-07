import streamlit as st
import plotly.express as px
import utils.plots as plots
from utils.read_data import read_data

#pio.templates.default = "plotly_white"

import pages.c_pages.CAP.pretest_CAP as page_pretest_CAP


config = plots.get_config()

def app():
    plots.plotly_settings(px)
    st.title('Comunidad de Aprendizaje')
    _type = st.selectbox('',["Pretest"])
    st.write("##")


    if(_type =='Pretest'):
        page_pretest_CAP.app()
    


if __name__ == "__main__":
    app()