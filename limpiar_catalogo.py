import json
import os
import sys

# ---------------- CONFIGURACIÓN ----------------
ARCHIVO_PRINCIPAL = 'movies.json' 
CARPETA_SALIDA = 'enlaces_eliminados' 

# Archivos de salida dentro de la carpeta
OUT_BITLY = f'{CARPETA_SALIDA}/eliminados_bitly.json'
OUT_GODNA = f'{CARPETA_SALIDA}/eliminados_godna.json'
OUT_POMF2 = f'{CARPETA_SALIDA}/eliminados_pomf2.json'
OUT_SIN_INFO = f'{CARPETA_SALIDA}/eliminados_sin_info.json'

# Dominios a buscar (SIN http:// ni https:// para atrapar ambos)
DOMINIOS = {
    'bitly': 'bit.ly', 
    'godna': 'godna94.pp.ua',
    'pomf2': 'pomf2.lain.la'
}
# -----------------------------------------------

def procesar_json():
    if not os.path.exists(ARCHIVO_PRINCIPAL):
        print(f"❌ ERROR CRÍTICO: No se encontró '{ARCHIVO_PRINCIPAL}'. Asegúrate de que el nombre sea exacto y esté en la raíz del repositorio.")
        sys.exit(1) 

    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    with open(ARCHIVO_PRINCIPAL, 'r', encoding='utf-8') as f:
        data = json.load(f)

    eliminados = {
        'bitly': [],
        'godna': [],
        'pomf2': []
    }
    eliminados_sin_info = [] 
    
    data_limpia = []

    for categoria in data:
        # A. Extraer y eliminar la categoría entera "Sin información"
        if categoria.get('name') == "Sin información":
            eliminados_sin_info.append(categoria)
            continue 

        # B. Procesar los enlaces de las demás categorías
        if 'samples' in categoria:
            samples_limpios = []
            
            for sample in categoria['samples']:
                url = sample.get('url', '')
                
                # Al buscar solo 'bit.ly', atrapará http://bit.ly y https://bit.ly
                if DOMINIOS['bitly'] in url:
                    eliminados['bitly'].append(sample)
                elif DOMINIOS['godna'] in url:
                    eliminados['godna'].append(sample)
                elif DOMINIOS['pomf2'] in url:
                    eliminados['pomf2'].append(sample)
                else:
                    samples_limpios.append(sample)
            
            categoria['samples'] = samples_limpios
        
        data_limpia.append(categoria)

    # Guardar el JSON original actualizado (limpio)
    with open(ARCHIVO_PRINCIPAL, 'w', encoding='utf-8') as f:
        json.dump(data_limpia, f, indent=2, ensure_ascii=False)

    # Guardar los JSON con los eliminados
    if eliminados['bitly']:
        with open(OUT_BITLY, 'w', encoding='utf-8') as f:
            json.dump(eliminados['bitly'], f, indent=2, ensure_ascii=False)
            
    if eliminados['godna']:
        with open(OUT_GODNA, 'w', encoding='utf-8') as f:
            json.dump(eliminados['godna'], f, indent=2, ensure_ascii=False)

    if eliminados['pomf2']:
        with open(OUT_POMF2, 'w', encoding='utf-8') as f:
            json.dump(eliminados['pomf2'], f, indent=2, ensure_ascii=False)
            
    if eliminados_sin_info:
        with open(OUT_SIN_INFO, 'w', encoding='utf-8') as f:
            json.dump(eliminados_sin_info, f, indent=2, ensure_ascii=False)
            
    print(f"✅ Limpieza completada. Archivos generados en la carpeta '{CARPETA_SALIDA}'.")

if __name__ == '__main__':
    procesar_json()
