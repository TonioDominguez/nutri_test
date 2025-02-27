import pandas as pd
import pdfplumber
import re

def leer_pdf(ruta_archivo):
    texto_completo = ""
    try:
        with pdfplumber.open(ruta_archivo) as pdf:
            for pagina in pdf.pages:
                texto_completo += pagina.extract_text() + "\n"
        return texto_completo
    except Exception as e:
        print(f"Error al leer el PDF: {e}")
        return None

def extraer_raciones(texto):
    patrones = [
        r'(\d+)\s*[Rr]aciones?',
        r'(\d+)/(\d+)\s*ración',
        r'(\d+)-(\d+)\s*[Rr]aciones?',
        r'[Pp]ara (\d+) personas?'
    ]

    for patron in patrones:
        match = re.search(patron, texto)
        if match:
            if len(match.groups()) == 2:
                if '-' in texto:
                    return f"{match.group(1)}-{match.group(2)}"
                else:
                    return f"{match.group(1)}/{match.group(2)}"
            return match.group(1)
    return None

def procesar_receta(texto):
    lineas = texto.strip().split('\n')
    nombre = ""
    ingredientes = []
    pasos = []
    raciones = None

    paso_actual = ""
    en_paso = False

    for i, linea in enumerate(lineas):
        linea = linea.strip()

        if linea.startswith('[Receta]'):
            nombre = linea.replace('[Receta]', '').strip()
            # Buscar raciones en las siguientes 2 líneas
            for j in range(1, 3):
                if i + j < len(lineas):
                    rac = extraer_raciones(lineas[i + j])
                    if rac:
                        raciones = rac
                        break

        elif linea.startswith('·'):
            ingredientes.append(linea.replace('·', '').strip())

        elif re.match(r'^\d+\)', linea):
            # Detecta paso enumerado
            if paso_actual:
                pasos.append(paso_actual.strip())
            # Inicia nuevo paso
            paso_actual = linea.split(')', 1)[1].strip()
            en_paso = True

        elif en_paso and linea:
            paso_actual += " " + linea

    if paso_actual:
        pasos.append(paso_actual.strip())

    return {
        'nom': nombre,
        'racions': raciones,
        'ingredients': ingredientes,
        'passos': pasos
    }