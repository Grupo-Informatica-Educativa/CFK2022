import streamlit as st

# Pages
from pages.c_pages.equipos.genero import app as page_equipos_genero


instrumentos_list = ["Equipos","Graficador"]

instrumentos_map = {
    "Equipos": [
        {
            'title': "Género",
            'page': page_equipos_genero
        },
    ]
}


def app():
    instrumento = st.sidebar.radio("Instrumentos",options=instrumentos_list,key="Instrumentos")
    st.sidebar.radio("Página",instrumentos_map[instrumento],format_func=lambda x: x["title"],key="Pagina")['page']()
    


if __name__=="__main__":
    app()