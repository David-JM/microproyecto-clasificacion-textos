from pathlib import Path
from typing import List, Tuple

import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "resources" / "models" / "ods_pipeline.joblib"

def cargar_modelo(ruta: Path | str = MODEL_PATH):
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontro el modelo en '{ruta}'")
    return joblib.load(ruta)


def predecir(modelo, texto: str) -> int:
    if not texto or not texto.strip():
        raise ValueError("El texto de entrada esta vacio.")
    return int(modelo.predict([texto])[0])


def predecir_con_probabilidades(modelo, texto: str, top_n: int = 3) -> Tuple[int, List[Tuple[int, float]]]:
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
