# Clasificador de Textos ODS 🌍

Aplicación web en **Streamlit** que clasifica un texto libre dentro de los
**Objetivos de Desarrollo Sostenible (ODS)** de la Agenda 2030 de la ONU.

Es el despliegue del microproyecto 2 (`micro_proyecto2.ipynb`): el mismo
pipeline entrenado en el notebook se serializa con `joblib` y se consume desde
la aplicación.

---

## Pipeline

```
Texto crudo
   └─> TfidfVectorizer (lowercase, min_df=5, max_df=0.85, max_features=5000)
        └─> TruncatedSVD  (LSA, 15 componentes latentes)
             └─> LogisticRegression (C=10, max_iter=1000)
                  └─> ODS predicho (1–17)
```

Accuracy sobre el conjunto de prueba: **~72.7 %** (16 clases).

El pipeline completo va dentro de un único objeto `sklearn.pipeline.Pipeline`,
por lo que a la aplicación se le entrega el texto tal cual lo escribe el usuario
y todo el preprocesamiento ocurre internamente.

---

## Estructura del repositorio

```
.
├── streamlit_app.py              # Aplicación principal (punto de entrada)
├── requirements.txt              # Dependencias
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml               # Tema de la aplicación
├── src/
│   ├── __init__.py
│   ├── ods_labels.py             # Catálogo de los 17 ODS
│   ├── predictor.py              # Carga del .joblib y lógica de predicción
│   └── train_model.py            # Entrenamiento y serialización
└── resources/
    ├── data/
    │   └── Datos_textosODS.xlsx  # Dataset (solo para reentrenar)
    └── models/
        ├── ods_pipeline.joblib   # ← Modelo serializado (0.6 MB)
        └── metrics.json          # Métricas y versiones del entrenamiento
```

---

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

### Reentrenar el modelo (opcional)

```bash
python src/train_model.py              # entrena con el 80 % y evalúa
python src/train_model.py --full-fit   # reentrena con el 100 % antes de guardar
```

Esto regenera `resources/models/ods_pipeline.joblib` y `metrics.json`.

---

## Despliegue en Streamlit Community Cloud

1. **Crea el repositorio en GitHub** (público) y sube todos los archivos,
   incluido `resources/models/ods_pipeline.joblib`:

   ```bash
   git init
   git add .
   git commit -m "Despliegue del clasificador de textos ODS"
   git branch -M main
   git remote add origin https://github.com/<tu-usuario>/<tu-repo>.git
   git push -u origin main
   ```

   > El `.joblib` pesa ~0.6 MB, así que no se necesita Git LFS.
   > Verifica que el `.gitignore` no lo esté excluyendo.

2. Entra a **https://share.streamlit.io** e inicia sesión con GitHub.

3. **New app → Deploy a public app from GitHub** y completa:

   | Campo          | Valor              |
   | -------------- | ------------------ |
   | Repository     | `<tu-usuario>/<tu-repo>` |
   | Branch         | `main`             |
   | Main file path | `streamlit_app.py` |

4. Pulsa **Deploy**. La primera construcción tarda 2–4 minutos mientras se
   instalan las dependencias de `requirements.txt`.

5. Cada `git push` a `main` vuelve a desplegar la aplicación automáticamente.

---

## Solución de problemas

| Síntoma | Causa y solución |
| --- | --- |
| `No se encontro el modelo en ...` | El `.joblib` no se subió al repo. Revisa `.gitignore` y ejecuta `git add -f resources/models/ods_pipeline.joblib`. |
| `InconsistentVersionWarning` o error al deserializar | La versión de scikit-learn en la nube no coincide con la del entrenamiento. Mantén el pin `scikit-learn==1.8.0` en `requirements.txt`, o reentrena localmente con la versión que quieras usar y vuelve a subir el `.joblib`. |
| La app no arranca en la nube | Confirma que **Main file path** sea exactamente `streamlit_app.py` y que esté en la raíz del repositorio. |
| Predicciones poco precisas en textos muy cortos | El modelo se entrenó con párrafos; frases de pocas palabras aportan poca señal TF-IDF. |

---

## Notas

Las clases presentes en el dataset son los ODS **1 al 16** (no hay ejemplos del
ODS 17), por lo que el modelo solo puede predecir dentro de ese rango. La salida
es una sugerencia automática y no sustituye la validación de un experto.
