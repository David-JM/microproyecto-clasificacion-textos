import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from src.ods_labels import ODS_COLORS, ODS_LABELS
from src.predictor import (cargar_modelo, predecir_con_probabilidades)

st.set_page_config(
    page_title="Clasificador de Textos ODS",
    page_icon="🌍",
    layout="centered",
)

@st.cache_resource(show_spinner="Cargando el modelo...")
def obtener_modelo():
    return cargar_modelo()

# Encabezado
st.title("Clasificador de Textos ODS")
st.caption(
    "Identifica automaticamente a cual de los Objetivos de Desarrollo "
    "Sostenible de la Agenda 2030 pertenece un texto."
)

try:
    modelo = obtener_modelo()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

# Entrada del usuario
texto_usuario = st.text_area(
    "Ingresa el texto a clasificar:",
    height=200,
    placeholder="Escribe o pega aqui un parrafo sobre una problematica social, "
    "economica o ambiental...",
)

analizar = st.button("🔎 Clasificar texto", type="primary", use_container_width=True)

# Resultado (prediccion)
if analizar:
    if not texto_usuario.strip():
        st.warning("Por favor ingresa un texto antes de clasificar.")
    elif len(texto_usuario.split()) < 3:
        st.warning(
            "El texto es demasiado corto. Ingresa al menos una frase completa "
            "para obtener una prediccion confiable."
        )
    else:
        with st.spinner("Procesando el texto..."):
            prediccion, ranking = predecir_con_probabilidades(
                modelo, texto_usuario, top_n=3
            )

        nombre = ODS_LABELS.get(prediccion, "Objetivo desconocido")
        color = ODS_COLORS.get(prediccion, "#444444")

        st.markdown("### Resultado")
        st.markdown(
            f"""
<div style="background-color:{color};padding:22px 26px;border-radius:12px;color:white;">
  <div style="font-size:15px;opacity:.85;letter-spacing:.5px;">
    OBJETIVO DE DESARROLLO SOSTENIBLE PREDICHO
  </div>
  <div style="font-size:30px;font-weight:700;margin-top:6px;">
    ODS {prediccion}: {nombre}
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        if ranking:
            confianza = ranking[0][1]
            st.markdown(f"**Confianza del modelo:** {confianza:.1%}")
            st.progress(min(confianza, 1.0))

            with st.expander("Ver los 3 objetivos mas probables"):
                for ods, prob in ranking:
                    etiqueta = ODS_LABELS.get(ods, "Desconocido")
                    st.write(f"**ODS {ods} — {etiqueta}**: {prob:.1%}")
                    st.progress(min(float(prob), 1.0))