# Import streamlit
import streamlit as st

def main():
    st.set_page_config(
    layout="wide",
    page_title="CFK2022",
    page_icon="🤖")
    st.sidebar.title("CFK 2022")

    st.title('Monitoreo y evaluación Coding For Kids 2022')
    st.write('''
    
    
    
    ''')
    st.image('pages/inicio.png',use_column_width=None, width=500)

if __name__=="__main__":
    main()