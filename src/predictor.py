"""
Capa de inferencia: carga el pipeline serializado y expone la prediccion.

El pipeline guardado con joblib ya contiene TODO el preprocesamiento
(TF-IDF + LSA), por lo que aqui se le entrega el texto crudo tal como lo
escribe el usuario, exactamente igual que en el notebook.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "resources" / "models" / "ods_pipeline.joblib"
METRICS_PATH = BASE_DIR / "resources" / "models" / "metrics.json"


def cargar_modelo(ruta: Path | str = MODEL_PATH):
    """Carga el pipeline entrenado desde disco."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontro el modelo en '{ruta}'. "
            "Ejecuta `python src/train_model.py` para generarlo."
        )
    return joblib.load(ruta)


def cargar_metadatos(ruta: Path | str = METRICS_PATH) -> dict:
    """Lee las metricas del entrenamiento; devuelve {} si no existen."""
    ruta = Path(ruta)
    if not ruta.exists():
        return {}
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def predecir(modelo, texto: str) -> int:
    """Devuelve el numero de ODS predicho para un texto libre."""
    if not texto or not texto.strip():
        raise ValueError("El texto de entrada esta vacio.")
    return int(modelo.predict([texto])[0])


def predecir_con_probabilidades(
    modelo, texto: str, top_n: int = 3
) -> Tuple[int, List[Tuple[int, float]]]:
    """
    Devuelve (ods_predicho, [(ods, probabilidad), ...]) ordenado de mayor a menor.

    Si el clasificador no expone `predict_proba` se retorna solo la prediccion
    con una lista vacia de probabilidades.
    """
    if not texto or not texto.strip():
        raise ValueError("El texto de entrada esta vacio.")

    prediccion = int(modelo.predict([texto])[0])

    if not hasattr(modelo, "predict_proba"):
        return prediccion, []

    probabilidades = modelo.predict_proba([texto])[0]
    clases = modelo.classes_
    ranking = sorted(
        ((int(c), float(p)) for c, p in zip(clases, probabilidades)),
        key=lambda par: par[1],
        reverse=True,
    )
    return prediccion, ranking[:top_n]
