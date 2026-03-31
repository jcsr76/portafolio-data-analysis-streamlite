# 🚀 Dashboard de Inteligencia de Negocios: Online Retail Analysis

Este proyecto forma parte de mi **Portafolio de Análisis de Datos**. Es una aplicación interactiva desarrollada en Python utilizando **Streamlit**, **Pandas**, **Numpy** y **Plotly** para visualizar y analizar el comportamiento de ventas de una tienda de retail internacional.

## 📊 Objetivo del Dashboard
El propósito de esta herramienta es transformar datos transaccionales brutos en información estratégica. Permite a los tomadores de decisiones identificar tendencias temporales, productos estrella y la distribución geográfica de los ingresos.

### Características Principales:
* **Análisis de Pareto (80/20):** Implementación lógica para identificar el 20% de los productos y países que generan el 80% de las ventas.
* **Filtros Dinámicos:** Segmentación por rango de fechas y país de origen.
* **Visualizaciones Avanzadas:**
    * Gráfico de Barras horizontal para el Top N de productos.
    * Gráfico de Líneas con escala temporal ajustable (Día, Semana, Mes, etc.).
    * Gráfico de Dona para distribución geográfica.
    * **Treemap Interactivo:** Visualización jerárquica de la composición de productos basada en Pareto.
* **Detalle Transaccional:** Tabla interactiva para auditoría de datos mediante el uso de *expanders*.

## 🛠️ Tecnologías Utilizadas
* **Python 3.9+**
* **Pandas & Numpy:** Procesamiento y limpieza de datos.
* **Streamlit:** Framework para la creación del dashboard web.
* **Plotly Express:** Generación de gráficos interactivos.

## 📂 Estructura de Archivos
* `dashboard.py`: Código fuente principal de la aplicación.
* `OnlineRetail.csv`: Dataset con más de 500,000 transacciones de una tienda de regalos en el Reino Unido.
* `requirements.txt`: Lista de dependencias necesarias para desplegar la aplicación en la nube.

## 🚀 Cómo ejecutarlo localmente
1. Clona este repositorio.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
