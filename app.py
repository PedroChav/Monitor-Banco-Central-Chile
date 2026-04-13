import streamlit as st

#========================================================
#                         PAGES
#========================================================


page_api = st.Page(
    page="pages/api_explore.py",
    title="Buscador API Banco Central"
    )

page_dash_rf = st.Page(
    page="pages/dashboard_rf.py",
    title="Analisis Renta Fija Local"
    )

pg = st.navigation(
        {
            "Dashboards": [page_dash_rf],
            "Herramientas": [page_api]
        },
        position="top"
    )

pg.run()
