import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('TkAgg')
plt.rcParams.update({'figure.figsize': (7, 5), 'figure.dpi': 100})

image = Image.open('Bandera.jpg')
doc = 'World_Cities.csv'

st.set_page_config(layout="wide", page_title="Cities List", page_icon=image)

st.title("Cities List DataSet")

@st.cache
def load_data(nrows):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1', nrows=nrows)
    return data

@st.cache
def load_data_byname(name):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1')
    filtered_data_byname = data[data["city"].str.upper().str.contains(name)]
    return filtered_data_byname

@st.cache
def load_data_bycapital(capital):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1')
    filtered_data_by_capital = data[data["admin_name"].str.upper().str.contains(capital, na=False)]
    return filtered_data_by_capital

@st.cache
def load_data_bycountry(coun):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1')
    filtered_data_bycountry = data[data["country"].str.contains(coun, na=False)]
    return filtered_data_bycountry


############ Almacenar Información#############################
data = load_data(100)
save_data = pd.read_csv(doc, delimiter=',')
save_data = load_data(100)

# --- LOGO ---#
st.sidebar.image("Credencial.jpg")
st.sidebar.write("Elizabeth Galindo Pedraza - S20006735")
st.sidebar.markdown("##")

# --- SIDEBAR FILTERS ---#
if st.sidebar.checkbox("Desplegar todos los datos guardados"):
    st.write(data)

buscadorCiudad = st.sidebar.write("Buscar ciudad especifico: ")
buscador = st.sidebar.text_input("Ciudad")
botonCiudad = st.sidebar.button("Buscar")

buscadorCapital = st.sidebar.write("Buscar capital especifica: ")
capital = st.sidebar.text_input("Capital")
botonCapital = st.sidebar.button("Buscar capital")

Country = st.sidebar.selectbox("Selecciona un pais",
                              options=data['country'].unique())
BotonCountry = st.sidebar.button("Buscar por pais")

##### Guardar datos para el histograma ####################
save_data_forHistrograma = pd.DataFrame(save_data)

save_data_forHistrograma_population = save_data_forHistrograma['population'].astype(
    float)
save_data_forHistrograma_population = np.array(
    save_data_forHistrograma_population).astype(float)

limite_Histograma = save_data_forHistrograma_population.min()
limite_Histograma = int(limite_Histograma)

if st.sidebar.checkbox('Mostrar histograma'):
    mostrar = np.histogram(save_data_forHistrograma_population, bins=limite_Histograma,
                           range=(save_data_forHistrograma_population.min(),
                                  save_data_forHistrograma_population.max()),
                           weights=None,
                           density=False)[0]
    st.bar_chart(mostrar)

# Grafica de barras ##############3
save_data_for_Barras = pd.DataFrame(save_data)

save_data_for_Barras_pop = save_data_for_Barras['population'].astype(
    float)
save_data_for_Barras_pais = save_data_for_Barras['city'].astype(
    str)

save_data_for_Barras_pop = np.array(
    save_data_for_Barras_pop)

save_data_for_Barras_pais = np.array(
    save_data_for_Barras_pais)

if st.sidebar.checkbox('Mostrar grafica de barras'):
    dataframe = pd.DataFrame(
        save_data_for_Barras_pop, save_data_for_Barras_pais)
    axis = dataframe.plot.barh(rot=0)
    plt.xlabel("Popular")
    plt.ylabel("Paises")
    plt.title("Popularidad")

    st.bar_chart(plt.show())

##############
save_data_for_Scatter = pd.DataFrame(save_data)
rng = np.random.RandomState(0)

save_data_for_Scatter_pop = save_data_for_Barras['population'].astype(
    float)
save_data_for_Scatter_pais = save_data_for_Barras['city'].astype(
    str)

if st.sidebar.checkbox('Mostrar grafica de dispersión'):
    plt.scatter(save_data_for_Scatter_pop,
                save_data_for_Scatter_pais,
                color='blue',
                alpha=0.4,
                cmap='viridis')
    plt.colorbar()

    st.bar_chart(plt.show())


if botonCiudad:
    filterbyname = load_data_byname(buscador.upper())
    rows = filterbyname.shape[0]
    st.dataframe(filterbyname)

if botonCapital:
    filterbycapital = load_data_bycapital(capital.upper())
    rows = filterbycapital.shape[0]
    st.dataframe(filterbycapital)

if BotonCountry:
    filtered_data_bycountry = load_data_bycountry(Country)
    rows = filtered_data_bycountry.shape[0]
    st.dataframe(filtered_data_bycountry)

