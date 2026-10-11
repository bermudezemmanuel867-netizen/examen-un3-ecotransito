import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sistema EcoTránsito CDMX", layout="wide")
st.title("Sistema EcoTránsito CDMX - Panel Analítico")

@st.cache_data
def cargar_datos():
    data = {
        'ID_Registro': ['REG-001', 'REG-002', 'REG-003', 'REG-004', 'REG-005', 'REG-007', 'REG-008', 'REG-009', 'REG-010'],
        'Timestamp': ['2026-10-01 08:00:00', '2026-10-01 09:00:00', '2026-10-01 10:00:00', '2026-10-01 11:00:00', '2026-10-01 12:00:00', '2026-10-01 14:00:00', '2026-10-01 15:00:00', '2026-10-01 16:00:00', '2026-10-01 17:00:00'],
        'Zona_Estacion': ['Centro Historico', 'Centro Historico', 'Centro Historico', 'Zona Oriente', 'Zona Oriente', 'Zona Sur', 'Zona Sur', 'Zona Sur', 'Zona Sur'],
        'Concentracion_PM25': [35.4, 42.1, 38.75, 120.5, 81.3, 18.2, 20.1, 19.5, 19.5],
        'Nivel_NO2': [42.1, 48.5, 51.0, 89.2, 82.0, 22.4, 25.1, 25.1, 25.1],
        'Indice_Trafico_Vehicular': [85.0, 92.5, 88.0, 98.0, 91.2, 45.0, 42.1, 41.55, 41.0]
    }
    return pd.DataFrame(data)

df = cargar_datos()

st.sidebar.header("Filtros de Visualización")
zonas_disponibles = df['Zona_Estacion'].unique().tolist()
zonas_seleccionadas = st.sidebar.multiselect(
    "Selecciona las Zonas de Estación:",
    options=zonas_disponibles,
    default=zonas_disponibles
)

if zonas_seleccionadas:
    df_filtrado = df[df['Zona_Estacion'].isin(zonas_seleccionadas)]
else:
    df_filtrado = df.copy()

st.subheader("Indicadores Clave de Rendimiento (KPIs)")
col1, col2, col3 = st.columns(3)

total_lecturas = len(df_filtrado)
promedio_pm25 = df_filtrado['Concentracion_PM25'].mean() if total_lecturas > 0 else 0
max_trafico = df_filtrado['Indice_Trafico_Vehicular'].max() if total_lecturas > 0 else 0

col1.metric("Total Lecturas Activas", f"{total_lecturas}")
col2.metric("Promedio PM₂.₅", f"{promedio_pm25:.2f} µg/m³")
col3.metric("Índice Máx. Tráfico Vehicular", f"{max_trafico:.1f}")

st.markdown("---")

tab1, tab2 = st.tabs(["📊 Gráfico de Dispersión (Plotly)", "🔥 Mapa de Calor (Seaborn)"])

with tab1:
    st.subheader("Relación: Índice de Tráfico vs Concentración PM₂.₅")
    if not df_filtrado.empty:
        fig_scatter = px.scatter(
            df_filtrado,
            x="Indice_Trafico_Vehicular",
            y="Concentracion_PM25",
            color="Zona_Estacion",
            hover_data=['Timestamp'],
            title="Dispersión por Zona de Estación"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para la zona seleccionada.")

with tab2:
    st.subheader("Matriz de Correlación (Pearson)")
    if not df_filtrado.empty:
        numeric_df = df_filtrado.select_dtypes(include=['float64', 'int64'])
        corr_matrix = numeric_df.corr(method='pearson')
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax, linewidths=0.5)
        st.pyplot(fig)
    else:
        st.warning("No hay datos suficientes para calcular la correlación.")
