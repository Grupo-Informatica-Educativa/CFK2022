import streamlit as st
import pandas as pd
import numpy as np
import utils.plots as plots
import plotly.express as px


config = plots.get_config()

def app():
    st.title('Marco de consolidación 2022')
    marco = pd.read_excel('data/Marco acumulativo.xlsx', index_col=0)
    IE = st.multiselect('Seleccione las instituciones que desea ver: ', list(marco['Código IE'].unique()))

    marco = marco.melt(id_vars='Código IE', var_name='Dimension', value_name='Nivel')
    marco['Nivel'] = pd.Categorical(marco['Nivel'], categories=['1A', '1B', '2A', '2B', '3', '4'], ordered=True)

    if len(IE)>0:
        pl_marco = marco[marco['Código IE'].isin(list(IE))]

        fig = px.line_polar(pl_marco, r="Nivel", theta="Dimension", color="Código IE", line_close=True,
                    category_orders={'Nivel':['1A', '1B', '2A', '2B', '3', '4']})

        st.plotly_chart(fig, config=config)
