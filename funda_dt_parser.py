"""Modulo del programa FundaDt con el parser de archivos"""
import csv
import os
from constantes import (
    MSG_FIN, ERROR_INPUT_INVALIDO, PROMPT_RUTA,
    ERROR_IMPORTACION, ERROR_EXPORTACION, MSG_OK, JUGADOR_DUPLICADO,
    HEADER_CSV_JUGADORES, HEADER_CSV_FECHAS,
    HEADER_CSV_EXPORTAR_FECHAS, HEADER_CSV_EXPORTAR_JUGADORES
)
from validaciones import (
    es_csv, csv_header_valido,
)

#Constantes:
SALIR = "**"
MENU_PARSER = """1) Procesar jugadores
2) Exportar jugadores
3) Procesar fechas
4) Exportar fechas
5) Salir
>>> """
POSICION_DETALLE_A_GENERAL = {
    "GK": "Arquero",
    "CB": "Defensor",
    "LB": "Defensor",
    "RB": "Defensor",
    "CDM": "Mediocampista",
    "LDM": "Mediocampista",
    "CM": "Mediocampista",
    "CAM": "Mediocampista",
    "LM": "Mediocampista",
    "RM": "Mediocampista",
    "LW": "Delantero",
    "RW": "Delantero",
    "ST": "Delantero",
}
ATRIBUTOS_PG = [
    "crossing", "finishing", "heading_accuracy", "short_passing", "volleys",
    "dribbling", "curve", "freekick_accuracy", "long_passing", "ball_control",
    "acceleration", "sprint_speed", "agility", "reactions", "balance",
    "shot_power", "jumping", "stamina", "strength", "long_shots",
    "aggression", "interceptions", "positioning", "vision", "penalties",
    "composure", "marking", "standing_tackle", "sliding_tackle",
]

def main():
    """
    Menu principal del parser.
    Muestra las opciones y delega a las funciones correspondientes.
    """
    jugadores_procesados = {}
    fechas_procesadas = []
    while True:
        opcion = input(MENU_PARSER).strip()
        if opcion == "5":
            print(MSG_FIN)
            break
        if opcion == "1":
            procesar_jugadores(jugadores_procesados)
        elif opcion == "2":
            exportar_jugadores(jugadores_procesados)
        elif opcion == "3":
            procesar_fechas(fechas_procesadas)
        elif opcion == "4":
            exportar_fechas(fechas_procesadas)
        else:
            print(ERROR_INPUT_INVALIDO)

# FUNCIONES PRINCIPALES:

def procesar_jugadores(jugadores_procesados):
    """Funcion principal que orquesta las demas funciones de procesar a los jugadores"""
    rutas_input = input(PROMPT_RUTA).strip()
    if rutas_input == SALIR:
        return
    if not rutas_input:
        print(ERROR_IMPORTACION)
        return
    rutas = rutas_input.split()
    archivos = obtener_archivos_csv(rutas, HEADER_CSV_JUGADORES)
    if archivos is None:
        print(ERROR_IMPORTACION)
        return
    if not archivos:
        print(MSG_OK.format(cant=0))
        return
    datos_procesados = _procesar_archivos_jugadores(archivos)
    if datos_procesados is None:
        print(ERROR_IMPORTACION)
        return
    nuevos_jugadores, duplicados = datos_procesados
    pga = calcular_pga(nuevos_jugadores)
    jugadores_finales = {
        clave: {
            "posicion": datos_jugador["posicion"],
            "precio": _calcular_precio_final(datos_jugador, pga)
        }
        for clave, datos_jugador in nuevos_jugadores.items()
    }
    for dup in duplicados:
        print(JUGADOR_DUPLICADO.format(
            nombre_jugador=dup[0],
            posicion=dup[1]
        ))
    jugadores_procesados.clear()
    jugadores_procesados.update(jugadores_finales)
    print(MSG_OK.format(cant=len(jugadores_procesados)))

def exportar_jugadores(jugadores_procesados):
    """Exporta a los jugadores procesados a un archivo csv.
    Si no hay jugadores cargados, muestra OK 0 y sale.
    Valida la ruta (sin espacios, extencion .csv, directorio existente)."""
    ruta = input(PROMPT_RUTA).strip()
    if ruta == SALIR:
        return
    if " " in ruta:
        print(ERROR_EXPORTACION)
        return
    if not es_csv(ruta):
        print(ERROR_EXPORTACION)
        return
    directorio_padre = os.path.dirname(ruta)
    if directorio_padre and not os.path.exists(directorio_padre):
        print(ERROR_EXPORTACION)
        return
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER_CSV_EXPORTAR_JUGADORES.split(","))
            for clave, info_jugador in jugadores_procesados.items():
                nombre, posicion = clave
                writer.writerow([nombre, posicion, info_jugador["precio"]])
        print(MSG_OK.format(cant=len(jugadores_procesados)))
    except OSError:
        print(ERROR_EXPORTACION)

def procesar_fechas(fechas_procesadas):
    """Lee archivos csv de fechas y guarda la informacion"""
    rutas_input = input(PROMPT_RUTA).strip()
    if rutas_input == SALIR:
        return
    if not rutas_input:
        print(ERROR_IMPORTACION)
        return
    rutas = rutas_input.split()
    archivos = obtener_archivos_csv(rutas, HEADER_CSV_FECHAS)
    if archivos is None:
        print(ERROR_IMPORTACION)
        return
    if not archivos:
        print(MSG_OK.format(cant=0))
        return
    nuevas_fechas = []
    for archivo in archivos:
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    nuevas_fechas.append(row)
        except (OSError, csv.Error):
            print(MSG_OK.format(cant=0))
            return
    fechas_procesadas.clear()
    fechas_procesadas.extend(nuevas_fechas)
    print(MSG_OK.format(cant=len(fechas_procesadas)))

def exportar_fechas(fechas_procesadas):
    """Funcion que se encarga de exportar fechas"""
    ruta = input(PROMPT_RUTA).strip()
    if ruta == SALIR:
        return
    if " " in ruta:
        print(ERROR_EXPORTACION)
        return
    if not es_csv(ruta):
        print(ERROR_EXPORTACION)
        return
    directorio_padre = os.path.dirname(ruta)
    if directorio_padre and not os.path.exists(directorio_padre):
        print(ERROR_EXPORTACION)
        return
    exportar_eventos = _contruir_eventos_a_exportar(fechas_procesadas)
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER_CSV_EXPORTAR_FECHAS.split(","))
            for ev in exportar_eventos:
                writer.writerow([
                    ev["fecha_partido"],
                    ev["evento"],
                    ev["detalle_evento"],
                    ev["nombre_jugador"],
                    ev["lado"],
                ])
        print(MSG_OK.format(cant=len(exportar_eventos)))
    except OSError:
        print(ERROR_EXPORTACION)

# FUNCIONES AUXILIARES:

def listar_csvs_en_directorio(directorio, header):
    """Lista todos los csv validos en un directorio"""
    archivos = []
    try:
        nombres = os.listdir(directorio)
    except (FileNotFoundError, NotADirectoryError, PermissionError):
        return []
    for nombre in nombres:
        ruta_completa = os.path.join(directorio, nombre)
        if os.path.isdir(ruta_completa):
            archivos.extend(listar_csvs_en_directorio(ruta_completa, header))
        elif es_csv(ruta_completa):
            if csv_header_valido(ruta_completa, header):
                archivos.append(ruta_completa)
    return archivos

def obtener_archivos_csv(rutas, header):
    """Procesa rutas y devuelve los csv validos"""
    archivos = []
    for ruta in rutas:
        if not os.path.exists(ruta):
            return None
        if os.path.isdir(ruta):
            archivos_dir = listar_csvs_en_directorio(ruta, header)
            archivos.extend(archivos_dir)
        else:
            if not es_csv(ruta):
                return None
            if not csv_header_valido(ruta, header):
                return None
            archivos.append(ruta)
    return archivos

def mapear_posiciones(posicion_detalle):
    """Convierte las posiciones especificas en las posiciones
    generales que se usan en el programa (GK -> Arquero)"""
    return POSICION_DETALLE_A_GENERAL.get(posicion_detalle, None)

def calcular_atributos_compuestos(row):
    """Calcula los atributos de los jugadores para devolverlos de manera que se entienda mejor"""
    def valor_numerico(campo):
        return float(row[campo])
    ritmo = round((valor_numerico("acceleration") + valor_numerico("sprint_speed")) / 2)
    regate = round((valor_numerico("dribbling")
                + valor_numerico("ball_control") + valor_numerico("agility")) / 3)
    tiro = round((valor_numerico("finishing")
                + valor_numerico("shot_power") + valor_numerico("long_shots")) / 3)
    pase = round((valor_numerico("short_passing")
                + valor_numerico("long_passing") + valor_numerico("vision")) / 3)
    defensa = round(
        (valor_numerico("marking") + valor_numerico("standing_tackle")
        + valor_numerico("sliding_tackle") + valor_numerico("interceptions")) / 4)
    juego_aereo = round((valor_numerico("heading_accuracy") + valor_numerico("jumping")) / 2)
    saque = round((valor_numerico("long_passing") + valor_numerico("shot_power")) / 2)
    return ritmo, regate, tiro, pase, defensa, juego_aereo, saque

def calcular_pg(row):
    """Calcula el promedio general (pg) de un jugador sumando los 29 atributos y,
    dividiendo por 29"""
    total = sum(float(row[campo]) for campo in ATRIBUTOS_PG)
    return round(total / 29)

def calcular_precio_base(posicion, compuestos, reactions):
    """Calcula el precio base del jugador segun su posicion y atributos compuestos"""
    ritmo, regate, tiro, pase, defensa, juego_aereo, saque = compuestos
    if posicion == "Arquero":
        return (round((ritmo + reactions + saque) / 3) + 5) * 3500
    if posicion == "Defensor":
        return (round((defensa + juego_aereo + ritmo) / 3) + 5) * 2000
    if posicion == "Mediocampista":
        return (round((pase + regate + tiro) / 3) + 5) * 3500
    if posicion == "Delantero":
        return (round((ritmo + regate + tiro) / 3) + 5) * 4000
    return 0

def calcular_pga(jugadores_dict):
    """Calcula el promedio general atributo (pga) de todos los jugadores procesados"""
    if not jugadores_dict:
        return 1
    total_pg = sum(j["pg"] for j in jugadores_dict.values())
    pga = round(total_pg / len(jugadores_dict))
    return max(pga, 1)

def calcular_factor(pg, pga):
    """Calcula el factor de un jugador comparando su PG con el PGA"""
    return round(pg / pga) + 1

def mapear_evento(evento, detalle, lado):
    """Mapea eventos del csv crudo al formato de exportacion"""
    mapeo = {
        ("gol", ""): ("gol", "", lado),
        ("gol", "gol"): ("gol", "", lado),
        ("gol", "gol_en_contra"): ("gol", "gol_en_contra", lado),
        ("gol", "penal_convertido"): ("gol", "penal_convertido", lado),
        ("asistencia", ""): ("asistencia", "", lado),
        ("tarjeta", "amarilla"): ("tarjeta", "amarilla", lado),
        ("tarjeta", "roja"): ("tarjeta", "roja", lado),
        ("atajada", "atajada_exitosa"): ("atajada", "atajada_exitosa", lado),
        ("despeje", ""): ("despeje", "", lado),
        ("penal_definicion", "convierte"): ("gol", "penal_convertido", lado),
    }
    clave = (evento, detalle,)
    valor_mapeado = mapeo.get(clave)
    if valor_mapeado is None:
        return None, None, None
    return valor_mapeado

def _extraer_jugador(row):
    """Lee una fila del csv y devuelve (clave, datos) o None si se ignora"""
    posicion = mapear_posiciones(row["positions"].strip())
    if posicion is None:
        return None
    nombre = row["full_name"].strip()
    compuestos = calcular_atributos_compuestos(row)
    pg = calcular_pg(row)
    reactions = float(row["reactions"])
    precio_base = calcular_precio_base(posicion, compuestos, reactions)
    if precio_base == 0:
        return None
    clave = (nombre, posicion)
    datos_jugador = {
        "nombre": nombre,
        "posicion": posicion,
        "pg": pg,
        "precio_base": precio_base
    }
    return clave, datos_jugador

def _calcular_precio_final(jugador, pga):
    """Aplica el factor al precio base"""
    factor = calcular_factor(jugador["pg"], pga)
    return round(jugador["precio_base"] * factor)

def _procesar_archivos_jugadores(archivos):
    """Lee los csv y devuelve (nuevos_jugadores, duplicados) o None si falla"""
    nuevos_jugadores = {}
    duplicados = set()
    for archivo in archivos:
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    jugador_extraido = _extraer_jugador(row)
                    if jugador_extraido is None:
                        continue
                    clave, datos_jugador = jugador_extraido
                    if clave in nuevos_jugadores:
                        duplicados.add(clave)
                    else:
                        nuevos_jugadores[clave] = datos_jugador
        except (OSError, csv.Error):
            return None
    return nuevos_jugadores, duplicados

def _contruir_eventos_a_exportar(fechas_procesadas):
    """Construye la lista de eventos listos para exportar"""
    exportar_eventos = []
    for row in fechas_procesadas:
        evento = row.get("evento", "")
        detalle = row.get("detalle_evento", "")
        lado = row.get("lado_evento", "")
        nombre = row.get("nombre_jugador", "")
        fecha = row.get("fecha_partido", "")
        evento_mapeado, detalle_mapeado, lado_mapeado = mapear_evento(evento, detalle, lado)
        if evento_mapeado is None:
            continue
        exportar_eventos.append({
            "fecha_partido": fecha,
            "evento": evento_mapeado,
            "detalle_evento": detalle_mapeado,
            "nombre_jugador": nombre,
            "lado": lado_mapeado,
        })
    return exportar_eventos

if __name__ == "__main__":
    main()
