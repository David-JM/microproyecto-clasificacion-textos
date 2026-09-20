"""
Clasificador de Textos ODS - Aplicacion Streamlit
=================================================

1. El usuario ingresa un texto libre.
2. El texto se procesa con el mismo pipeline del proyecto
   (TF-IDF -> LSA/TruncatedSVD -> Regresion Logistica), cargado con joblib.
3. Se muestra el Objetivo de Desarrollo Sostenible (ODS) predicho.

Ejecucion local:  streamlit run streamlit_app.py
"""

import sys
from pathlib import Path

import streamlit as st

# Permite importar el paquete `src` sin instalarlo
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from src.ods_labels import ODS_COLORS, ODS_EMOJIS, ODS_LABELS  # noqa: E402
from src.predictor import (  # noqa: E402
    cargar_metadatos,
    cargar_modelo,
    predecir_con_probabilidades,
)

# ---------------------------------------------------------------------------
# Configuracion de la pagina
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Clasificador de Textos ODS",
    page_icon="🌍",
    layout="centered",
)


# ---------------------------------------------------------------------------
# Carga del modelo (cacheada: se ejecuta una sola vez por sesion del servidor)
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Cargando el modelo...")
def obtener_modelo():
    return cargar_modelo()


@st.cache_data
def obtener_metadatos():
    return cargar_metadatos()


# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------
st.title("🌍 Clasificador de Textos ODS")
st.caption(
    "Identifica automaticamente a cual de los Objetivos de Desarrollo "
    "Sostenible de la Agenda 2030 pertenece un texto."
)

try:
    modelo = obtener_modelo()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

meta = obtener_metadatos()

# ---------------------------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Sobre el modelo")
    st.markdown(
        """
**Pipeline**
1. `TfidfVectorizer` (5.000 terminos, min_df=5, max_df=0.85)
2. `TruncatedSVD` - LSA con 15 componentes latentes
3. `LogisticRegression` (C=10)

Serializado con **joblib** e invocado sobre el texto crudo,
tal como se construyo en el notebook del proyecto.
"""
    )
    if meta:
        st.metric("Accuracy en prueba", f"{meta.get('accuracy_test', 0):.2%}")
        st.caption(f"scikit-learn {meta.get('sklearn_version', 'n/d')}")
        st.caption(f"Registros de entrenamiento: {meta.get('n_registros', 'n/d')}")

# ---------------------------------------------------------------------------
# Entrada del usuario
# ---------------------------------------------------------------------------
EJEMPLOS = {
    "— Escribir mi propio texto —": "",
    "Energia renovable": (
        "El gobierno invertira millones de dolares en la construccion de paneles "
        "solares y parques eolicos para reducir las emisiones de carbono y "
        "garantizar el acceso a electricidad limpia en zonas rurales."
    ),
    "Educacion": (
        "Se necesitan mas campanas y programas de becas para garantizar que las "
        "ninas de zonas rurales tengan el mismo acceso a la educacion primaria y "
        "secundaria de calidad que los ninos."
    ),
    "Justicia e instituciones": (
        "El nuevo tratado internacional busca erradicar la corrupcion en las "
        "instituciones publicas, fortalecer el estado de derecho y garantizar "
        "juicios justos e imparciales para todos los ciudadanos."
    ),
    "Agua y saneamiento": (
        "Millones de personas todavia carecen de acceso a agua potable segura y "
        "a servicios basicos de saneamiento, lo que aumenta la propagacion de "
        "enfermedades en las comunidades mas vulnerables."
    ),
}

ejemplo = st.selectbox("Cargar un ejemplo (opcional):", list(EJEMPLOS.keys()))

texto_usuario = st.text_area(
    "Ingresa el texto a clasificar:",
    value=EJEMPLOS[ejemplo],
    height=200,
    placeholder="Escribe o pega aqui un parrafo sobre una problematica social, "
    "economica o ambiental...",
)

analizar = st.button("🔎 Clasificar texto", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Prediccion
# ---------------------------------------------------------------------------
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
        emoji = ODS_EMOJIS.get(prediccion, "🎯")

        st.markdown("### Resultado")
        st.markdown(
            f"""
<div style="background-color:{color};padding:22px 26px;border-radius:12px;
            color:white;">
  <div style="font-size:15px;opacity:.85;letter-spacing:.5px;">
    OBJETIVO DE DESARROLLO SOSTENIBLE PREDICHO
  </div>
  <div style="font-size:30px;font-weight:700;margin-top:6px;">
    {emoji} ODS {prediccion}: {nombre}
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

        st.caption(
            "Prediccion generada por el pipeline TF-IDF → LSA → Regresion "
            "Logistica del microproyecto. Es una sugerencia automatica y puede "
            "requerir validacion experta."
        )

st.divider()
st.caption("Microproyecto 2 · Clasificacion de textos ciudadanos en los 17 ODS")
