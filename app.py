import streamlit as st
from streamlit_folium import st_folium
import folium
import random
from datetime import datetime

st.set_page_config(page_title="AVESAFE DEMO", layout="wide")

st.title("🦉 AVESAFE - Evaluador de Riesgo Aviar para Recolección Nocturna")
st.markdown("""
Esta aplicación evalúa de forma **predictiva e interactiva** el riesgo de presencia de aves en olivares superintensivos,  
basándose en factores **geográficos y climáticos simulados**. Diseñada para ayudar a tomar decisiones sostenibles.  
""")

# ---------------------- FECHA ----------------------
st.subheader("📅 Selecciona la fecha de recolección")
fecha = st.date_input("Fecha deseada", value=datetime.today())

# ---------------------- MAPA INTERACTIVO ----------------------
st.subheader("🗺️ Haz clic en el mapa para seleccionar tu finca")

mapa = folium.Map(location=[37.5, -4.8], zoom_start=7, tiles="Esri.WorldImagery")
mapa.add_child(folium.LatLngPopup())  # Permite ver las coordenadas al hacer clic

# Mostrar el mapa y guardar el resultado
mapa_resultado = st_folium(mapa, height=500, width=700)

# ---------------------- ANÁLISIS SIMULADO ----------------------
st.subheader("📊 Simulación de condiciones climáticas y análisis de riesgo")

if mapa_resultado["last_clicked"] is not None:
    lat = mapa_resultado["last_clicked"]["lat"]
    lon = mapa_resultado["last_clicked"]["lng"]

    st.success(f"Finca seleccionada en coordenadas: ({lat:.4f}, {lon:.4f})")

    # Simulación del clima
    random.seed(int(lat * lon * fecha.day))
    temperatura = random.randint(10, 26)
    precipitaciones = random.choice(["ninguna", "ligeras", "moderadas", "intensas"])
    distancia_agua_km = round(random.uniform(0.2, 5.5), 1)

    st.markdown(f"""
    - 🌡️ **Temperatura simulada:** {temperatura}°C  
    - 🌧️ **Precipitaciones previstas:** {precipitaciones}  
    - 🏞️ **Distancia al cuerpo de agua más cercano:** {distancia_agua_km} km  
    """)

    # Evaluación del riesgo
    riesgo = 0
    if 14 <= temperatura <= 20:
        riesgo += 3
    if precipitaciones in ["ninguna", "ligeras"]:
        riesgo += 2
    if distancia_agua_km < 2:
        riesgo += 3

    st.subheader("🦅 Riesgo estimado de presencia de aves:")

    if riesgo >= 7:
        st.error("🛑 Riesgo alto: Se recomienda no recolectar.")
        riesgo_label = "ALTO"
    elif riesgo >= 4:
        st.warning("⚠️ Riesgo moderado: Extremar precauciones.")
        riesgo_label = "MODERADO"
    else:
        st.success("✅ Riesgo bajo: Recolección posible.")
        riesgo_label = "BAJO"

    # ---------------------- MEDIDAS PREVENTIVAS ----------------------
    st.subheader("🚨 Medidas preventivas recomendadas")

    if riesgo_label in ["ALTO", "MODERADO"]:
        st.markdown("""
        **Acciones sugeridas para mitigar impacto:**

        - 🛸 Activar **drones con cámara térmica** para detectar aves antes de recolectar.
        - 🔊 Utilizar **altavoces disuasorios** con sonidos de depredadores.
        - 🚫 Evitar recolectar entre las 22:00 y 4:00 si no es imprescindible.
        - 📈 Evaluar riesgo de nuevo tras 48 horas.
        """)
    else:
        st.markdown("No se requieren medidas adicionales. ✔️")

else:
    st.info("Haz clic en el mapa para seleccionar la ubicación de tu finca.")
