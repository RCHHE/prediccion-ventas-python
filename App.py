import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Configuración de la página web interactiva
st.set_page_config(page_title="Data App - Ventas Predictivas", layout="wide")

st.title("Dashboard de Análisis y Predicción de Ventas")
st.markdown("Esta aplicación web interactiva fue construida **netamente en Python** utilizando Machine Learning para pronosticar la demanda.")

# 1. Cargar la data local
@st.cache_data
def cargar_datos():
    df = pd.read_csv('data_ventas.csv')
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Mes_Index'] = np.arange(1, len(df) + 1)
    return df

df = cargar_datos()

# 2. Métricas Clave (KPIs) en la barra superior
venta_total = df['Venta'].sum()
ticket_promedio = df['Venta'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Venta Total Histórica", f"S/. {venta_total:,.2f}")
col2.metric("Promedio Mensual", f"S/. {ticket_promedio:,.2f}")
col3.metric("Meses Analizados", f"{len(df)} meses")

st.markdown("---")

# Interfaz interactiva: Selector en la barra lateral
st.sidebar.header("Configuración del Modelo")
meses_a_predecir = st.sidebar.slider("Meses a pronosticar para el futuro:", min_value=1, max_value=12, value=6)
complejidad_modelo = st.sidebar.selectbox("Complejidad del algoritmo (Grado Polinomial):", [2, 3, 4], index=1)

# 3. Entrenamiento del Modelo de Machine Learning (Scikit-Learn)
X = df[['Mes_Index']]
y = df['Venta']

poly = PolynomialFeatures(degree=complejidad_modelo)
X_poly = poly.fit_transform(X)

modelo = LinearRegression()
modelo.fit(X_poly, y)

# 4. Predicciones dinámicas según los controles del usuario
ultimo_mes = df['Mes_Index'].max()
meses_futuros = np.arange(ultimo_mes + 1, ultimo_mes + 1 + meses_a_predecir).reshape(-1, 1)
meses_futuros_poly = poly.transform(meses_futuros)
predicciones = modelo.predict(meses_futuros_poly)

fechas_futuras = pd.date_range(start='2025-01-01', periods=meses_a_predecir, freq='MS')
df_futuro = pd.DataFrame({
    'Fecha': fechas_futuras,
    'Venta Proyectada': predicciones
})

# 5. Visualización Gráfica
st.subheader("Tendencia Histórica y Proyección Futura")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df['Fecha'], df['Venta'], label='Histórico Real', color='#2D9CDB', marker='o', linewidth=2)
ax.plot(df_futuro['Fecha'], df_futuro['Venta Proyectada'], label='Predicción Machine Learning', color='#F2C811', linestyle='--', marker='s', linewidth=2)
ax.set_xlabel("Línea de Tiempo")
ax.set_ylabel("Monto de Ventas")
ax.legend()
ax.grid(True, alpha=0.2)

st.pyplot(fig)

# 6. Tablas explicativas e información técnica
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Datos del Pronóstico")
    st.dataframe(df_futuro, use_container_width=True)

with col_der:
    st.subheader("Explicación Técnica")
    st.info(f"""
    El modelo está utilizando una **Regresión Polinomial de Grado {complejidad_modelo}**. 
    A diferencia de una línea recta común, este algoritmo detecta los ciclos de subidas y bajadas anuales (estacionalidad) 
    para proyectar un comportamiento mucho más realista en los meses del futuro.
    """)