import json
import os
import sys
import re

# ---------------- CONFIGURACIÓN ----------------
ARCHIVO_PRINCIPAL = 'movies.json' 
CARPETA_SALIDA = 'enlaces_eliminados' 
# -----------------------------------------------

def procesar_json():
    if not os.path.exists(ARCHIVO_PRINCIPAL):
        print(f"❌ ERROR CRÍTICO: No se encontró '{ARCHIVO_PRINCIPAL}'.")
        sys.exit(1) 

    # 1. Leer los dominios ingresados desde GitHub Actions
    dominios_env = os.environ.get('DOMINIOS_A_ELIMINAR', '')
    if not dominios_env:
        print("⚠️ No se ingresaron dominios para eliminar. No hay nada que hacer.")
        sys.exit(0)

    # Limpiar espacios y separar por comas (ej: "nuevo.com,  otro.net " -> ["nuevo.com", "otro.net"])
    lista_dominios = [d.strip() for d in dominios_env.split(',') if d.strip()]
    print(f"🔍 Buscando los siguientes dominios: {lista_dominios}")

    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    with open(ARCHIVO_PRINCIPAL, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Crear diccionario dinámico para agrupar los eliminados según el dominio
    eliminados_dinamicos = {dominio: [] for dominio in lista_dominios}
    
    # 2. Procesar el JSON
    for categoria in data:
        if 'samples' in categoria:
            samples_limpios = []
            
            for sample in categoria['samples']:
                url = sample.get('url', '')
                fue_eliminado = False
                
                # Revisar si la URL contiene alguno de los dominios ingresados
                for dominio in lista_dominios:
                    if dominio in url:
                        eliminados_dinamicos[dominio].append(sample)
                        fue_eliminado = True
                        break # Si ya encontró coincidencia, pasa al siguiente sample
                
                if not fue_eliminado:
                    samples_limpios.append(sample)
            
            categoria['samples'] = samples_limpios

    # 3. Guardar JSON principal limpio
    with open(ARCHIVO_PRINCIPAL, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 4. Guardar archivos dinámicos y mostrar resumen
    for dominio, lista_eliminados in eliminados_dinamicos.items():
        if lista_eliminados:
            # Limpiar el nombre del dominio para usarlo como archivo (ej: nuevo.com -> nuevo_com)
            nombre_seguro = re.sub(r'[^a-zA-Z0-9]', '_', dominio)
            ruta_archivo = f'{CARPETA_SALIDA}/eliminados_{nombre_seguro}.json'
            
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(lista_eliminados, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Se eliminaron {len(lista_eliminados)} enlaces del dominio '{dominio}'.")

    print("🚀 Limpieza completada exitosamente.")

if __name__ == '__main__':
    procesar_json()
