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