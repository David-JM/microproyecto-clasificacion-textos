# Clasificador de Textos ODS

Aplicación web en **Streamlit** que clasifica un texto libre dentro de los
**Objetivos de Desarrollo Sostenible (ODS)** de la Agenda 2030 de la ONU.


## Estructura del repositorio

```
.
├── streamlit_app.py                # Aplicación principal (punto de entrada)
├── requirements.txt              
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── ods_labels.py               # Catálogo de los 17 ODS
│   ├── model_controller.py         # Carga del .joblib + lógica de predicción
└── resources/
    └── models/
        ├── ods_pipeline.joblib     # Modelo serializado (0.6 MB)
```

## Ejecución local

```bash
git clone https://github.com/<tu-usuario>/<tu-repo>.git
cd <tu-repo>

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run streamlit_app.py
```

La app queda disponible en `http://localhost:8501`.

## Ejecución en la nube

Enlace de la aplicacion ya desplegada en la nube: [Clasificador textos ODS](https://microproyecto-clasificacion-textos.streamlit.app)

---
---

### Ejemplos de textos

El gobierno invertirá millones de dólares en la construcción de paneles solares y parques eólicos para reducir las emisiones de carbono y garantizar el acceso a electricidad limpia en zonas rurales

Millones de personas todavía carecen de acceso a agua potable segura y a servicios básicos de saneamiento, lo que aumenta la propagación de enfermedades en las comunidades más vulnerables

Se necesitan nuevos programas de becas para garantizar que las niñas de zonas rurales tengan el mismo acceso a la educación primaria y secundaria de calidad que los niños