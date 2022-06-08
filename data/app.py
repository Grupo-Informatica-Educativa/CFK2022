# Import streamlit
import streamlit as st


# Import each page file
from c_pages import inicio
from c_pages import dashboard_cons
from c_pages import marco
from c_pages import Avanceconsolidacion


PAGES = {
    "Inicio": inicio,
    "Avance Consolidación": Avanceconsolidacion,
    "Caracterización Inicial": dashboard_cons,
    "Marco de consolidación": marco
}


def main():
    st.set_page_config(
    layout="wide",
    page_title="CFK2022",
    page_icon="👩‍💻")
    st.sidebar.title("CFK 2022")
    pag = st.sidebar.radio("Página: ", list(PAGES.keys()))

    PAGES[pag].app()


if __name__ == "__main__":
    main()
