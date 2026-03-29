import streamlit as st
import bcchapi

# ====================================================
#                      BACKEND 
# ====================================================
# conexion api bcentral
user : str = "progaska.m@gmail.com"
pwd : str = "tubdag-rarhyz-juWjo8"
siete = bcchapi.Siete(usr=user,pwd=pwd)

def buscador_serie(nombre_serie : str):
    df = siete.buscar(nombre_serie)
    return df



# ====================================================
#                     FRONTEND 
# ====================================================

st.title("Buscador API Banco Central de Chile")

with st.expander("Buscador de series", expanded=True):
    st.text_input("Serie", key="serie", value= None)
    if st.session_state.serie != None:
        df_buscador = buscador_serie(nombre_serie = st.session_state.serie)
        st.dataframe(df_buscador)

with st.expander("Visualizador de series"):
    st.markdown("Modulo en Desarrollo")

with st.expander("Biblioteca de series"):
    st.markdown("Trabajando para usted")

st.session_state