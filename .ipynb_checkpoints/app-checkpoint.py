# Import streamlit
import streamlit as st


# Import each page file
from pages import inicio
from pages import dashboard_cons
from pages import marco
from pages import Avanceconsolidacion


PAGES = {
    "Inicio": inicio,
    "Avance Consolidación": Avanceconsolidacion,
    "Caracterización Inicial": dashboard_cons,
    "Prueba marco": marco
}


def main():
    st.set_page_config(layout="wide")
    st.sidebar.title("CFK 2022")
    pag = st.sidebar.radio("Página: ", list(PAGES.keys()))

    PAGES[pag].app()


if __name__ == "__main__":
    main()
