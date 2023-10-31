import requests
import pandas as pd
from bs4 import BeautifulSoup

def agregar_anio_mes(row):
    fecha = row['DIA_TRANSPORTE']
    anio, mes, _ = fecha.split("-")
    periodo = anio + "-" + mes
    return anio, mes, periodo

def load_data():
    url = 'https://datos.gob.ar/dataset/transporte-sube---cantidad-transacciones-usos-por-fecha'

    df_Transacciones_SUBE = pd.DataFrame()

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select(".pkg-container .pkg-actions a")
        for link in links:
            href = link.get('href')
            if href and '/dataset/transporte' not in href:
                print(href)
                df = pd.read_csv(href)
                df['Anio'], df['Mes'], df['Periodo'] = zip(*df.apply(agregar_anio_mes, axis=1))
                df.rename(columns={
                    'DIA_TRANSPORTE': 'Fecha Viaje',
                    'NOMBRE_EMPRESA': 'Nombre Empresa',
                    'LINEA': 'Linea',
                    'AMBA': 'Amba',
                    'TIPO_TRANSPORTE': 'Tipo Transporte',
                    'JURISDICCION': 'Jurisdiccion',
                    'PROVINCIA': 'Provincia',
                    'MUNICIPIO': 'Municipio',
                    'CANTIDAD': 'Cantidad',
                    'DATO_PRELIMINAR': 'Dato Preliminar'
                }, inplace=True)
                anio = href[-8:-4]
                df_Transacciones_SUBE = pd.concat([df_Transacciones_SUBE, df], ignore_index=True)
    else:
        print("This page could not be accessed:", response.status_code)
    
    return df_Transacciones_SUBE
