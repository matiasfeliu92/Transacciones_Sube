import streamlit as st
import pandas as pd
import os
import plotly.express as px
from etl.Transacciones_SUBE_etl import load_data

st.set_page_config(layout="wide")

with st.spinner('Loading dashboard, please wait...'):
    df_Transacciones_SUBE = load_data()
    
st.spinner('')

st.title('Reporte de transacciones de SUBE')

container_1 = st.container()

df_Transacciones_SUBE_periodo = df_Transacciones_SUBE.groupby(['Anio', 'Mes'])['Cantidad'].size().reset_index(name='Count').sort_values('Count', ascending=False)
fig_1 = px.scatter(df_Transacciones_SUBE_periodo, x='Mes', y='Count', color='Anio',
                   labels={'Mes': 'Mes', 'Count': 'Cantidad de Viajes', 'Anio': 'Año'})

with container_1:
    st.header('¿En que periodos se registraron la mayor cantidad de transacciones de SUBE?')
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df_Transacciones_SUBE_periodo.head(10), use_container_width=True)

    with col2:
        st.plotly_chart(fig_1, use_container_width=True)

container_2 = st.container()

df_Transacciones_SUBE_por_anio = df_Transacciones_SUBE.groupby('Anio').size().reset_index(name='count')
fig_2 = px.pie(df_Transacciones_SUBE_por_anio, values='count', names='Anio')

with container_2:
    st.header('¿En que año se registro la mayor cantidad de transacciones de SUBE?')
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df_Transacciones_SUBE_por_anio, use_container_width=True)

    with col2:
        st.plotly_chart(fig_2, use_container_width=True)

container_3 = st.container()

df_promedio_transacciones_mes = df_Transacciones_SUBE.groupby(['Anio', 'Mes'])['Cantidad'].mean().reset_index().sort_values('Cantidad', ascending=False)

fig_3 = px.scatter(df_promedio_transacciones_mes, x='Mes', y='Cantidad', color='Anio',
              labels={'Mes': 'Mes', 'Cantidad': 'Promedio de Viajes', 'Anio': 'Año'})

with container_3:
    st.header('¿Cual es el promedio de transacciones por mes en cada año?')
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df_promedio_transacciones_mes.head(10), use_container_width=True)

    with col2:
        st.plotly_chart(fig_3, use_container_width=True)