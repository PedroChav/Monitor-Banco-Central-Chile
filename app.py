import streamlit as st
import bcchapi
from datetime import datetime, timedelta

# ====================================================
#                      BACKEND 
# ====================================================
# conexion api bcentral
user : str = "pe.chavarr@hotmail.com"
pwd : str = "3216EzXw"
siete = bcchapi.Siete(usr=user,pwd=pwd)

@st.cache_data
def buscador_serie(nombre_serie : str):
    df = siete.buscar(nombre_serie)
    return df

@st.cache_data
def buscador_seriesid(id_serie:str,start:str,end:str,nombre=str):
    df_id = siete.cuadro(
        series = [id_serie],
        desde=start,
        hasta=end,
        nombres=[nombre]
    )
    return df_id

@st.cache_data
def buscador_multiseries(id_serie:list,start:str,end:str,nombre=list):
    df_id = siete.cuadro(
        series = id_serie,
        desde=start,
        hasta=end,
        nombres=nombre
    )
    return df_id

def last_labour_day():
    hoy = datetime.now()
    # lunes es 0, domingo es 6
    dia_semana = hoy.weekday()

    if dia_semana == 0:  # Es Lunes
        delta = 3        # Retroceder al Viernes
    elif dia_semana == 6: # Es Domingo
        delta = 2        # Retroceder al Viernes
    else:                # Martes a Sábado
        delta = 1        # Retroceder un día

    ultimo_habil = hoy - timedelta(days=delta)
    return ultimo_habil.strftime("%Y-%m-%d")

def n_years_date(day:str, n:int):
    # Convertir el string de entrada a objeto datetime
    fecha_dt = datetime.strptime(day, "%Y-%m-%d")
    
    try:
        # Intentamos simplemente restar 3 al año
        nueva_fecha = fecha_dt.replace(year=fecha_dt.year - n)
    except ValueError:
        # Este error ocurre si la fecha es un 29 de febrero y 
        # el año resultante no es bisiesto.
        # En ese caso, se ajusta al 28 de febrero.
        nueva_fecha = fecha_dt.replace(year=fecha_dt.year - n, day=28)
        
    # Retornar en el formato solicitado
    return nueva_fecha.strftime("%Y-%m-%d")


# ====================================================
#                     FRONTEND 
# ====================================================

st.title("Buscador API Banco Central de Chile")

with st.expander("Buscador de series", expanded=False):
    st.text_input("Serie", key="serie", value= None)
    if st.session_state.serie != None:
        df_buscador = buscador_serie(nombre_serie = st.session_state.serie)
        st.dataframe(df_buscador)

with st.expander("Visualizador de series"):
    end:str=last_labour_day()
    start:str=n_years_date(day=end, n=3)
    st.text_input("SeriesID", key="seriesid", value= None)
    st.text_input("Nombre de Serie", key="serie_name", value=None)
    st.date_input("Fecha De Inicio", key="start", format="YYYY-MM-DD", value=start)
    st.date_input("Fecha De Termino", key="end", format="YYYY-MM-DD", value=end)
    if st.session_state.seriesid != None:
        df_seriesid = buscador_seriesid(id_serie = st.session_state.seriesid,
                                        start=st.session_state.start,
                                        end=st.session_state.end,
                                        nombre=st.session_state.serie_name
                                        )
        st.dataframe(df_seriesid)

with st.expander("Biblioteca de series"):
    dct_swaps_id:dict={
        "SPC-CLP-2Y":"F022.SPC.TIN.AN02.NO.Z.D",
        "SPC-UF-2Y":"F022.SPC.TIN.AN02.UF.Z.D"
    }
    dct_tpm_id:dict={
        "TPM-DIARIA":"F022.TPM.TIN.D001.NO.Z.D"
    }
    st.selectbox("Seleccione Categoria",options=["Tasas Swaps","TPM"],key="categoria")
    if st.session_state.categoria == "Tasas Swaps":
        lst_options:list=dct_swaps_id.keys()
    elif st.session_state.categoria == "TPM":
        lst_options:list=dct_tpm_id.keys()
    st.multiselect("Seleccione Serie",options=lst_options)

st.session_state