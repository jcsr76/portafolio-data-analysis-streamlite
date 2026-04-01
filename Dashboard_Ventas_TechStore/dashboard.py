import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(layout="wide", page_title="Dashboard de Ventas TechStore")


# --- 1. CARGA Y LIMPIEZA INICIAL ---
@st.cache_data
def cargar_datos():
    # 1. Obtenemos la ruta absoluta de la carpeta donde vive este script (dashboard.py)
    ruta_actual = os.path.dirname(__file__)

    # 2. Construimos la ruta al CSV uniendo la carpeta actual con el nombre del archivo
    ruta_csv = os.path.join(ruta_actual, 'OnlineRetail.csv')

    # 3. Cargamos el archivo usando esa ruta dinámica
    df = pd.read_csv(ruta_csv, encoding='ISO-8859-1')
    df = df[df['Quantity'] > 0]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Total'] = df['Quantity'] * df['UnitPrice']
    return df


df = cargar_datos()

fecha_min = df['InvoiceDate'].min().date()
fecha_max = df['InvoiceDate'].max().date()

# --- 2. CONFIGURACIÓN DE LA BARRA LATERAL ---
with st.sidebar:
    st.header("Filtros")
    rango_fecha = st.date_input("Rango de fechas:", value=(fecha_min, fecha_max), min_value=fecha_min,
                                max_value=fecha_max)

    lista_paises = sorted(list(df['Country'].unique()))
    lista_paises.insert(0, "Global")
    pais_seleccionado = st.selectbox("Selección País", lista_paises)

    top_n_barras = st.slider("Productos en Gráfico de Barras:", 1, 20, 5)

    st.header("Escala Temporal")
    dict_escalas = {"Día": "D", "Semana": "W", "Mes": "ME", "Trimestre": "QE", "Año": "YE"}
    escala_texto = st.radio("Escala", list(dict_escalas.keys()))
    escala_pandas = dict_escalas[escala_texto]

# --- 3. LÓGICA DE FILTRADO ---
if len(rango_fecha) == 2:
    f_inicio, f_fin = rango_fecha
    mask = (df['InvoiceDate'].dt.date >= f_inicio) & (df['InvoiceDate'].dt.date <= f_fin)
    df_intermedio = df.loc[mask]
    if pais_seleccionado != "Global":
        df_filtrado = df_intermedio[df_intermedio['Country'] == pais_seleccionado]
    else:
        df_filtrado = df_intermedio
else:
    st.stop()

# --- 4. TÍTULO DEL DASHBOARD ---
# Usamos un título principal y un subtítulo dinámico
st.title("🚀 Dashboard de Inteligencia de Negocios: Online Retail")
st.markdown(f"### Análisis de Ventas: **{pais_seleccionado}** | Período: **{f_inicio}** a **{f_fin}**")
st.markdown("---")

# --- 5. VISUALIZACIÓN ---
if not df_filtrado.empty:
    # MÉTRICAS
    m1, m2, m3 = st.columns(3)
    m1.metric("Ventas Totales 💰", f"${df_filtrado['Total'].sum():,.2f}")
    m2.metric("Productos Vendidos 📦", f"{df_filtrado['Quantity'].sum():,}")
    m3.metric("Ticket Promedio 🎟️", f"${df_filtrado['Total'].mean():,.2f}")

    st.markdown("---")

    # FILA 1: BARRAS Y TENDENCIA
    c1, c2 = st.columns(2)
    with c1:
        p_top = df_filtrado.groupby('Description')['Total'].sum().reset_index().sort_values('Total',
                                                                                            ascending=False).head(
            top_n_barras)
        st.plotly_chart(px.bar(p_top, x='Total', y='Description', orientation='h',
                               title=f"Top {top_n_barras} Productos").update_yaxes(autorange="reversed"),
                        use_container_width=True)
    with c2:
        v_tiempo = df_filtrado.set_index('InvoiceDate').resample(escala_pandas)['Total'].sum().reset_index()
        st.plotly_chart(
            px.line(v_tiempo, x='InvoiceDate', y='Total', title=f"Tendencia de Ventas ({escala_texto})", markers=True),
            use_container_width=True)

    st.markdown("---")

    # FILA 2: DONA Y TREEMAP
    col_dona, col_tree = st.columns(2)

    with col_dona:
        if pais_seleccionado == "Global":
            v_pais = df_filtrado.groupby('Country')['Total'].sum().reset_index().sort_values('Total', ascending=False)
            v_pais['Pct_Acum'] = v_pais['Total'].cumsum() / v_pais['Total'].sum()
            n_top5_p = v_pais['Country'].iloc[:5].tolist()
            v_pais['Grupo'] = np.where(v_pais['Country'].isin(n_top5_p) | (v_pais['Pct_Acum'] <= 0.80),
                                       v_pais['Country'], 'Otros')
            df_d_final = v_pais.groupby('Grupo')['Total'].sum().reset_index()
            st.plotly_chart(
                px.pie(df_d_final, values='Total', names='Grupo', title='Distribución Geográfica (Pareto)', hole=0.5),
                use_container_width=True)
        else:
            st.info(f"Filtro aplicado: {pais_seleccionado}. Selecciona 'Global' para ver comparativas.")

    with col_tree:
        v_prod = df_filtrado.groupby('Description')['Total'].sum().reset_index().sort_values('Total', ascending=False)
        v_prod['Pct_Acum'] = v_prod['Total'].cumsum() / v_prod['Total'].sum()
        v_prod['Grupo_Pareto'] = np.where(v_prod['Pct_Acum'] <= 0.80, v_prod['Description'],
                                          'Otros Productos (Resto 20%)')
        df_tree_final = v_prod.groupby('Grupo_Pareto')['Total'].sum().reset_index()
        fig_tree = px.treemap(df_tree_final, path=['Grupo_Pareto'], values='Total', title='Pareto de Productos (80/20)',
                              color='Total', color_continuous_scale='Viridis')
        st.plotly_chart(fig_tree, use_container_width=True)

    st.markdown("---")

    # --- 6. TABLA DE DETALLE ---
    with st.expander("📄 Ver detalle transaccional de los datos filtrados"):
        columnas_mostrar = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'Total',
                            'Country']
        st.dataframe(df_filtrado[columnas_mostrar], use_container_width=True, hide_index=True)

else:
    st.warning("No se encontraron datos que coincidan con los filtros aplicados. ⚠️")