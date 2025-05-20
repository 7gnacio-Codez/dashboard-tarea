# Importamos las bibliotecas necesarias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

##########################################################
# CONFIGURACIÓN DEL DASHBOARD
##########################################################

# Configuración básica de la página
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.title("📊 Dashboard Equipo 23 🛒")
st.markdown("""
Supermarket Sales 👋
* **Luis Ignacio Chacón Cabrera**
            """)

# Configuración simple para los gráficos
sns.set_style("whitegrid")

##################################################
# CARGA DE DATOS
##################################################

# Función para cargar datos con cache para mejorar rendimiento
# Función para cargar datos con cache para mejorar rendimiento
@st.cache_data
def cargar_datos():
    # Carga el archivo CSV con datos macroeconómicos
    df = pd.read_csv('data.csv')
    return df
# Cargamos los datos
df = cargar_datos()

##############################################
# CONFIGURACIÓN DE LA BARRA LATERAL
##############################################

st.sidebar.header('Filtros')

unique_branch = sorted(df["Branch"].unique())
unique_city = sorted(df["City"].unique())
unique_customer = sorted(df["Customer type"].unique())
unique_product = sorted(df["Product line"].unique())
unique_payment = sorted(df["Payment"].unique())

branch = st.sidebar.multiselect('Sucursal', unique_branch, unique_branch)
city = st.sidebar.multiselect('Ciudad', unique_city, unique_city)
customer = st.sidebar.multiselect('Tipo de cliente', unique_customer, unique_customer)
gender = st.sidebar.multiselect('Género', ['Male', 'Female'], ['Male', 'Female'])
product = st.sidebar.multiselect('Línea de producto', unique_product, unique_product)
payment = st.sidebar.multiselect('Método de pago', unique_payment, unique_payment)

# ##################################################
# # FILTRADO DE DATOS
# ##################################################

df_selected_sales = df[(df["Branch"].isin(branch)) 
                        & (df["City"].isin(city)) 
                        & (df["Customer type"].isin(customer)) 
                        & (df["Gender"].isin(gender))
                        & (df["Product line"].isin(product))
                        & (df["Payment"].isin(payment))]

# #######################################################
# # SECCIÓN DE MÉTRICAS (PRIMERA FILA)
# #######################################################
st.subheader("Indicadores Clave")
col1, col2, col3, col4 = st.columns(4)

# Mostramos las métricas con formato adecuado
col1.metric("Ventas Totales 🚀", f"${df_selected_sales['Total'].sum():,.1f} ")
col2.metric("Rating promedio ⭐", f"{df_selected_sales['Rating'].mean():.1f}")
col3.metric("Ingreso Bruto Total 📈", f"{df_selected_sales['gross income'].sum():,.1f}")
col4.metric("Total Facturas 📃", f"{df_selected_sales['Invoice ID'].count():.0f}")
st.markdown("---")

#########################################################
# SECCIÓN DE GRÁFICOS (SEGUNDA FILA)
#########################################################
st.subheader("Gráficos de Ventas 💹")
col1, col2= st.columns(2)
# Gráfico de ventas por sucursal
with col1:
    fig, ax = plt.subplots()
    sns.countplot(data=df_selected_sales, x="Branch", palette="Set2", ax=ax)
    ax.set_title("Ventas por Sucursal")
    ax.set_xlabel("Sucursal")
    ax.set_ylabel("Número de Ventas")
    st.pyplot(fig)
    st.write("*Este gráfico compara el 'Número de Ventas' entre las diferentes sucursales. Cada barra representa una sucursal y su altura indica el número de ventas.*")
# Gráfico de ventas por método de pago
with col2:
    fig, ax = plt.subplots()
    sns.countplot(data=df_selected_sales, x="Payment", palette="Set2", ax=ax)
    ax.set_title("Ventas por Método de Pago")
    ax.set_xlabel("Método de Pago")
    ax.set_ylabel("Número de Ventas")
    st.pyplot(fig)
    st.write("*Este gráfico compara el 'Número de Ventas' según los diferentes métodos de pago: Cash, Credit card y Ewallet. Cada barra representa un método de pago y su altura indica el número de ventas realizadas con ese método.*")

col3, col4 = st.columns(2)
# Gráfico de ventas por línea de producto
with col3:
    fig, ax = plt.subplots()
    sns.countplot(data=df_selected_sales, x="Product line", palette="Set2", ax=ax)
    ax.set_title("Ventas por Línea de Producto")
    ax.set_xlabel("Línea de Producto")
    ax.set_ylabel("Número de Ventas")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.write("*Este gráfico permite comparar el rendimiento de ventas entre las diferentes categorías de productos. Cada barra representa una línea de producto diferente. La altura de cada barra indica el número de ventas correspondiente a esa categoría.*")
# Gráfico de ventas por género
with col4:
    fig, ax = plt.subplots()
    sns.countplot(data=df_selected_sales, x="Gender", palette="Set2", ax=ax)
    ax.set_title("Ventas por Género")
    ax.set_xlabel("Género")
    ax.set_ylabel("Número de Ventas")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.write("*Este gráfico compara el número de ventas realizadas a clientes femeninos y masculinos. Cada barra representa un género. La altura de cada barra indica el número de ventas realizadas a clientes de ese género.*")
st.markdown("---")
#########################################################
# SECCIÓN DE GRÁFICOS (TERCERA FILA)
#########################################################
st.subheader("Gráficos de Ventas a lo largo del tiempo 🕰️")
col5, col6 = st.columns(2)

import calendar
df_selected_sales['Date']=pd.to_datetime(df['Date'])
df_2 = df_selected_sales.groupby(['Date'])['Total'].sum().reset_index()
df_2 = df_2.sort_values(by='Date', ascending=True)
df_2['Month'] = df_2['Date'].dt.month.apply(lambda x: calendar.month_abbr[x])
df_2['Day'] = df_2['Date'].dt.day
df_2 = df_2.pivot(index="Day", columns="Month", values="Total")
# Gráfico de ventas por mes
with col5:
    fig, ax = plt.subplots()
    sns.lineplot(data=df_2, color= "blue", linewidth=2.5,marker='o', markersize=7, ax=ax) 
    ax.set(title="Ventas totales a lo largo del tiempo",xlabel="Día", ylabel="Ventas Totales")
    st.pyplot(fig)
    st.write("*Este gráfico de líneas permite comparar la tendencia de las ventas totales a lo largo de los días de tres meses consecutivos: enero, febrero y marzo. El gráfico presenta tres líneas diferentes, cada una representando un mes distinto.*")
#########################################################
# SECCIÓN DE GRÁFICOS (CUARTA FILA)
#########################################################
st.subheader("Tabla de Datos 📉")
if st.button('Presiona aquí para desplegar Tabla de Datos 📉'):
    df_selected_sales = df[(df["Branch"].isin(branch)) 
                        & (df["City"].isin(city)) 
                        & (df["Customer type"].isin(customer)) 
                        & (df["Gender"].isin(gender))
                        & (df["Product line"].isin(product))
                        & (df["Payment"].isin(payment))]
    st.write(df_selected_sales)
    st.write("*Esta tabla proporciona una vista granular de los datos que alimentan el panel de control. Cada fila representa una transacción individual, lo que permite un análisis detallado de las ventas.*")   
# Pie de página simple
st.markdown("---")
st.caption("Dashboard Equipo 23 | Datos: data.csv")
