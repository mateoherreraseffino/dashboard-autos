
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Configuración de la página ---
st.set_page_config(page_title="Dashboard de Autos", layout="wide")
st.title("🚗 Dashboard de Autos Usados")

# --- Carga de datos ---
@st.cache_data
def load_data():
    df = pd.read_csv("/content/drive/MyDrive/Trabajo práctico/Archivos/icd-base-tp-economistas.csv")
    df = df[df['price_eur'] > 0]  # Para evitar errores con escala log
    return df

base_tp = load_data()

# --- Filtros interactivos ---
st.sidebar.header("🔎 Filtros")
makers = st.sidebar.multiselect("Marca", options=sorted(base_tp['maker'].dropna().unique()))
fuel_types = st.sidebar.multiselect("Tipo de combustible", options=sorted(base_tp['fuel_type'].dropna().unique()))
transmissions = st.sidebar.multiselect("Transmisión", options=sorted(base_tp['transmission'].dropna().unique()))
year_range = st.sidebar.slider("Año de fabricación", int(base_tp['manufacture_year'].min()),
                               int(base_tp['manufacture_year'].max()),
                               (int(base_tp['manufacture_year'].min()), int(base_tp['manufacture_year'].max())))

# --- Aplicar filtros ---
df = base_tp.copy()
if makers:
    df = df[df['maker'].isin(makers)]
if fuel_types:
    df = df[df['fuel_type'].isin(fuel_types)]
if transmissions:
    df = df[df['transmission'].isin(transmissions)]
df = df[(df['manufacture_year'] >= year_range[0]) & (df['manufacture_year'] <= year_range[1])]

# --- Cálculo de KPIs ---
precio_promedio = df['price_eur'].mean()
km_promedio = df['mileage'].mean()
anio_promedio = df['manufacture_year'].mean()
potencia_promedio = df['engine_power'].mean()
electricos = df['fuel_type'].str.lower().eq('eléctrico').sum()

# --- Mostrar KPIs ---
st.subheader("📌 Indicadores clave")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💶 Precio promedio", f"€{precio_promedio:,.0f}")
col2.metric("📍 Kilometraje promedio", f"{km_promedio:,.0f} km")
col3.metric("🏭 Año promedio", f"{anio_promedio:.0f}")
col4.metric("⚡ Potencia promedio", f"{potencia_promedio:.1f} kW")
col5.metric("🔋 Autos eléctricos", f"{electricos}")

# --- Gráficos ---
st.subheader("📊 Visualizaciones")

col6, col7 = st.columns(2)

# Histograma de precios
with col6:
    fig_hist = px.histogram(df, x='price_eur', nbins=50, log_y=True,
                            title="Distribución de precios (escala log)",
                            labels={'price_eur': 'Precio (€)'})
    st.plotly_chart(fig_hist, use_container_width=True)

# Scatterplot precio vs kilometraje
with col7:
    fig_scatter = px.scatter(df, x='mileage', y='price_eur', color='fuel_type', opacity=0.5, log_y=True,
                             title="Relación precio vs kilometraje",
                             labels={'mileage': 'Kilometraje', 'price_eur': 'Precio (€)'})
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- Muestra de tabla ---
st.subheader("📋 Muestra de datos")
st.dataframe(df.sample(5) if len(df) > 5 else df)
