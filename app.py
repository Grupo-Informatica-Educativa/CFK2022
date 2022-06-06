# Import streamlit
import streamlit as st

def main():
    st.set_page_config(
    layout="wide",
    page_title="CFK2022",
    page_icon="🤖")
    st.sidebar.title("CFK 2022")

    st.title('Coding For Kids 2022')

    st.write("Resumen del Proyecto")
    c1 = st.container()
    c1.title('Formación')
    c2 = st.container()
    c2.title('Colegios CFK')
    c3 = st.container()
    c3.title('Comunidad de aprendizaje')
    c4 = st.container()
    c4.title('Greentic')

if __name__=="__main__":
    main()