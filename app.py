from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Asegurarse de que existen los directorios necesarios
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# API base URL
QURAN_API_URL = "http://api.alquran.cloud/v1"

# Diccionario de nombres de Surahs en español
SURAH_NAMES_ES = {
    1: "La Apertura", 2: "La Vaca", 3: "La Familia de Imran", 4: "Las Mujeres", 
    5: "La Mesa Servida", 6: "Los Ganados", 7: "Los Lugares Elevados", 8: "Los Botines",
    9: "El Arrepentimiento", 10: "Jonás", 11: "Hud", 12: "José", 13: "El Trueno",
    14: "Abraham", 15: "Al-Hiyr", 16: "Las Abejas", 17: "El Viaje Nocturno",
    18: "La Caverna", 19: "María", 20: "Ta-Ha", 21: "Los Profetas", 22: "La Peregrinación",
    23: "Los Creyentes", 24: "La Luz", 25: "El Criterio", 26: "Los Poetas",
    27: "Las Hormigas", 28: "El Relato", 29: "La Araña", 30: "Los Bizantinos",
    31: "Luqman", 32: "La Prosternación", 33: "Los Coligados", 34: "Saba",
    35: "El Originador", 36: "Ya Sin", 37: "Los Ordenados en Filas", 38: "Sad",
    39: "Los Grupos", 40: "El Perdonador", 41: "Los Versículos Detallados", 42: "La Consulta",
    43: "Los Ornamentos", 44: "El Humo", 45: "La Arrodillada", 46: "Las Dunas",
    47: "Muhammad", 48: "La Victoria", 49: "Las Habitaciones", 50: "Qaf",
    51: "Los Vientos", 52: "El Monte", 53: "La Estrella", 54: "La Luna",
    55: "El Misericordioso", 56: "El Acontecimiento", 57: "El Hierro", 58: "La Discusión",
    59: "El Destierro", 60: "La Examinada", 61: "La Fila", 62: "El Viernes",
    63: "Los Hipócritas", 64: "El Desengaño", 65: "El Divorcio", 66: "La Prohibición",
    67: "El Reino", 68: "El Cálamo", 69: "La Inevitable", 70: "Las Vías de Ascenso",
    71: "Noé", 72: "Los Genios", 73: "El Envuelto", 74: "El Arropado",
    75: "La Resurrección", 76: "El Ser Humano", 77: "Los Enviados", 78: "La Noticia",
    79: "Los Ángeles Arrancadores", 80: "El Ceño", 81: "El Arrollamiento",
    82: "La Ruptura", 83: "Los Defraudadores", 84: "El Resquebrajamiento",
    85: "Las Constelaciones", 86: "El Astro Nocturno", 87: "El Altísimo",
    88: "El Día Angustiante", 89: "La Aurora", 90: "La Ciudad", 91: "El Sol",
    92: "La Noche", 93: "La Mañana", 94: "El Sosiego", 95: "La Higuera",
    96: "El Coágulo", 97: "El Decreto", 98: "La Evidencia", 99: "El Terremoto",
    100: "Los Corceles", 101: "El Día Aterrador", 102: "La Competencia",
    103: "El Tiempo", 104: "El Difamador", 105: "El Elefante", 106: "Los Quraysh",
    107: "La Ayuda Mínima", 108: "La Abundancia", 109: "Los Incrédulos",
    110: "El Socorro", 111: "Las Fibras de Palmera", 112: "El Monoteísmo Puro",
    113: "El Amanecer", 114: "Los Hombres"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/surahs')
def get_surahs():
    try:
        # Obtener lista de Surahs
        response = requests.get(f"{QURAN_API_URL}/surah")
        response.raise_for_status()
        data = response.json()
        
        # Agregar nombres en español
        for surah in data['data']:
            surah['nameSpanish'] = SURAH_NAMES_ES.get(surah['number'], surah['englishName'])
            
        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error al obtener Surahs: {str(e)}")
        return jsonify({"error": "No se pudieron obtener las Surahs"}), 500

@app.route('/surah/<int:surah_number>')
def get_surah(surah_number):
    try:
        # Obtener Ayahs de una Surah específica en árabe
        arabic = requests.get(f"{QURAN_API_URL}/surah/{surah_number}")
        arabic.raise_for_status()
        
        # Obtener traducción en español
        spanish = requests.get(f"{QURAN_API_URL}/surah/{surah_number}/es.asad")
        spanish.raise_for_status()
        
        # Si la primera traducción falla, intentar con otra
        if spanish.json().get('code') != 200:
            spanish = requests.get(f"{QURAN_API_URL}/surah/{surah_number}/es.garcia")
            spanish.raise_for_status()
        
        arabic_data = arabic.json()
        # Agregar nombre en español
        arabic_data['data']['nameSpanish'] = SURAH_NAMES_ES.get(surah_number, arabic_data['data']['englishName'])
        
        return jsonify({
            "arabic": arabic_data,
            "spanish": {
                "data": [spanish.json()["data"]]
            }
        })
    except Exception as e:
        app.logger.error(f"Error al obtener Surah {surah_number}: {str(e)}")
        return jsonify({"error": "No se pudo obtener la Surah"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
