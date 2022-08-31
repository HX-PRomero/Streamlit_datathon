import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

st.set_page_config(page_title = 'Datathon',layout = 'wide')

primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"

image = Image.open('images/portada.jpg')
st.image(image)

titulo = Image.open('images/titulo.png')
st.image(titulo)
st.markdown("<br></br>",unsafe_allow_html=True)

title= 'selection' 
st.markdown("<br></br>",unsafe_allow_html=True)


# Se importa csv
metrics=pd.read_csv('metrics.csv')
metrics = metrics.sort_values('ECM').reset_index(drop=True)

names = metrics.Nombre.values
selector = st.selectbox(
    'Seleccione su nombre',
    names,
    index=0)


# Se calculan valores relevantes
puesto = int(metrics[metrics.Nombre==selector].index.values+1)
error = metrics[metrics.Nombre==selector].ECM
error = float(np.round(error,5))
best = np.round(metrics.ECM.values[0],5)
worst = np.round(metrics.ECM.values[-1],5)

# Se expone resultado
col1, col2 = st.columns(2)
with col1:
    copa = Image.open('images/copa.webp')
    st.image(copa)

with col2:
    st.markdown(f"<h1 style='text-align:center; color:black;'> Puesto: {puesto} </h1>",unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center; color:yellow;'> ECM {error} </h1>",unsafe_allow_html=True)

    st.markdown("<br></br>",unsafe_allow_html=True)

    st.markdown(f"<h1 style='text-align:left; color:green;'> Mejor marca: {best}  </h1>",unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:left; color:red;'> Peor marca: {worst} </h1>",unsafe_allow_html=True)

# Gráfica total alumnos
st.markdown("<br></br>",unsafe_allow_html=True)
fig = px.histogram(metrics, x="ECM", nbins=7,text_auto=True)
fig.update_layout(title={
    'text': 'Métricas globales',
    'y':0.9,
    'x':0.5,
    'font_size':25,
    'xanchor': 'center',
    'yanchor': 'top'},
    xaxis_title="ECM",
    yaxis_title="Cantidad de alumnos")

st.plotly_chart(fig)
