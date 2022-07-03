import streamlit as st

# Pages
from pages.c_pages.equipos.genero import app as page_equipos_genero
from pages.c_pages.equipos.genero2022 import app as page_equipos_genero_2022



instrumentos_list = ["Equipos"]

instrumentos_map = {
    "Equipos": [
        {
            'title': "Género 2021",
            'page': page_equipos_genero
        },
         {
            'title': "Género 2022",
            'page': page_equipos_genero_2022
        },
    ],
    "Graficador": [
        {
            'title': "",
            'page': None
        },
    ]
}


def app():
    instrumento = st.sidebar.radio("Instrumentos",options=instrumentos_list,key="Instrumentos")
    st.sidebar.radio("Página",instrumentos_map[instrumento],format_func=lambda x: x["title"],key="Pagina")['page']()
    


if __name__=="__main__":
    app()