import json
import os

# ---------------- CONFIGURACIÓN ----------------
ARCHIVO_PRINCIPAL = 'movies.json' # Nombre de tu archivo original en la raíz
CARPETA_SALIDA = 'enlaces_eliminados' # Carpeta donde se guardarán los eliminados

# Archivos de salida dentro de la carpeta
OUT_BITLY = f'{CARPETA_SALIDA}/eliminados_bitly.json'
OUT_GODNA = f'{CARPETA_SALIDA}/eliminados_godna.json'
OUT_POMF2 = f'{CARPETA_SALIDA}/eliminados_pomf2.json'

# Dominios a buscar
DOMINIOS = {
    'bitly': 'https://bit.ly/3HrWOIG',
    'godna': 'https://godna94.pp.ua',
    'pomf2': 'https://pomf2.lain.la'
}
# -----------------------------------------------

def procesar_json():
    if not os.path.exists(ARCHIVO_PRINCIPAL):
        print(f"Error: No se encontró el archivo {ARCHIVO_PRINCIPAL}")
        return

    # Crear la carpeta para los eliminados si no existe
    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    # Leer el JSON original
    with open(ARCHIVO_PRINCIPAL, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Diccionarios para guardar los bloques enteros eliminados
    eliminados = {
        'bitly': [],
        'godna': [],
        'pomf2': []
    }

    # Procesar categorías y samples
    for categoria in data:
        if 'samples' in categoria:
            samples_limpios = []
            
            for sample in categoria['samples']:
                url = sample.get('url', '')
                
                # Filtrar y separar por dominio
                if DOMINIOS['bitly'] in url:
                    eliminados['bitly'].append(sample)
                elif DOMINIOS['godna'] in url:
                    eliminados['godna'].append(sample)
                elif DOMINIOS['pomf2'] in url:
                    eliminados['pomf2'].append(sample)
                else:
                    samples_limpios.append(sample)
            
            # Reemplazar la lista vieja con la lista limpia
            categoria['samples'] = samples_limpios

    # 1. Guardar el JSON original actualizado (limpio)
    with open(ARCHIVO_PRINCIPAL, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 2. Guardar los 3 nuevos JSON con los eliminados en su carpeta
    if eliminados['bitly']:
        with open(OUT_BITLY, 'w', encoding='utf-8') as f:
            json.dump(eliminados['bitly'], f, indent=2, ensure_ascii=False)
            
    if eliminados['godna']:
        with open(OUT_GODNA, 'w', encoding='utf-8') as f:
            json.dump(eliminados['godna'], f, indent=2, ensure_ascii=False)

    if eliminados['pomf2']:
        with open(OUT_POMF2, 'w', encoding='utf-8') as f:
            json.dump(eliminados['pomf2'], f, indent=2, ensure_ascii=False)
            
    print(f"Limpieza completada. Archivos eliminados guardados en la carpeta '{CARPETA_SALIDA}'.")

if __name__ == '__main__':
    procesar_json()
