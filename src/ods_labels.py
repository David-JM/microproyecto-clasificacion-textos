ODS_LABELS = {
    1: "Fin de la pobreza",
    2: "Hambre cero",
    3: "Salud y bienestar",
    4: "Educacion de calidad",
    5: "Igualdad de genero",
    6: "Agua limpia y saneamiento",
    7: "Energia asequible y no contaminante",
    8: "Trabajo decente y crecimiento economico",
    9: "Industria, innovacion e infraestructura",
    10: "Reduccion de las desigualdades",
    11: "Ciudades y comunidades sostenibles",
    12: "Produccion y consumo responsables",
    13: "Accion por el clima",
    14: "Vida submarina",
    15: "Vida de ecosistemas terrestres",
    16: "Paz, justicia e instituciones solidas",
    17: "Alianzas para lograr los objetivos",
}

ODS_COLORS = {
    1: "#E5243B", 2: "#DDA63A", 3: "#4C9F38", 4: "#C5192D", 5: "#FF3A21",
    6: "#26BDE2", 7: "#FCC30B", 8: "#A21942", 9: "#FD6925", 10: "#DD1367",
    11: "#FD9D24", 12: "#BF8B2E", 13: "#3F7E44", 14: "#0A97D9", 15: "#56C02B",
    16: "#00689D", 17: "#19486A",
}

ODS_EMOJIS = {
    1: "🏠", 2: "🌾", 3: "❤️", 4: "📚", 5: "⚖️", 6: "💧", 7: "⚡", 8: "💼",
    9: "🏭", 10: "🤝", 11: "🏙️", 12: "♻️", 13: "🌍", 14: "🐟", 15: "🌳",
    16: "🕊️", 17: "🌐",
}


def describir_ods(numero) -> str:
    """Devuelve una cadena legible del tipo 'ODS 7 - Energia asequible...'."""
    numero = int(numero)
    return f"ODS {numero} - {ODS_LABELS.get(numero, 'Objetivo desconocido')}"
