"""
Modulo principal del juego FundaDT con el usuario

"""
import csv
from constantes import (
MSG_FIN, ERROR_INPUT_INVALIDO, ERROR_SELECCION_INVALIDA,
HEADER_CSV_EXPORTAR_JUGADORES, MSG_OK, ERROR_SIN_JUGADORES,
MSG_OK_FECHAS,PROMPT_RUTA, ERROR_IMPORTACION,
HEADER_CSV_EXPORTAR_FECHAS, MSG_SIN_EQUIPOS_FECHAS,
TEMPLATE_PUNTAJE_EQUIPO, PTS_GOL_A_FAVOR, PTS_GOL_EN_CONTRA,
PTS_PENAL_CONVERTIDO, PTS_ASISTENCIA, PTS_AMARILLA, PTS_ROJA, PTS_GOL_VISITANTE,
PTS_DESPEJE, PTS_ATAJADA_EXITOSA, PRESUPUESTO_INICIAL, JUGADOR_DUPLICADO)
from equipos import menu_crear_equipo
from mercado import menu_comprar_jugadores, menu_vender_jugador
from alineaciones import menu_armar_alineacion
from consultas import menu_ver_plantel, menu_ver_alineacion, menu_ver_jugador_mas_utilizado
from validaciones import validar_ruta_csv

# Constantes
IMPORTAR_JUGADORES = "1"
CREAR_EQUIPO = "2"
JUGAR_FECHAS = "9"
OPCIONES_MENU = {
        "3": menu_comprar_jugadores,
        "4": menu_vender_jugador,
        "5": menu_ver_plantel,
        "6": menu_armar_alineacion,
        "7": menu_ver_alineacion,
        "8": menu_ver_jugador_mas_utilizado
    }
MENU_USUARIO = """1) Importar jugadores
2) Crear equipo
3) Comprar jugador
4) Vender jugador
5) Ver plantel
6) Armar alineación
7) Ver alineación
8) Ver jugador más utilizado
9) Jugar fechas
10) Salir
>>> """
SALIR = "10"
EVENTO_GOL = "gol"
EVENTO_ASISTENCIA = "asistencia"
EVENTO_TARJETA = "tarjeta"
EVENTO_ATAJADA = "atajada"
EVENTO_DESPEJE = "despeje"
DETALLE_GOL_EN_CONTRA = "gol_en_contra"
DETALLE_PENAL_CONVERTIDO = "penal_convertido"
DETALLE_AMARILLA = "amarilla"
DETALLE_ROJA = "roja"
DETALLE_ATAJADA_EXITOSA = "atajada_exitosa"
LADO_VISITANTE = "visitante"

def importar_jugadores():
    """Lee un archivo CSV exportado por el parser y devuelve los jugadores en el formato esperado"""
    ruta = input(PROMPT_RUTA).strip()
    if ruta == "**":
        return None
    if not validar_ruta_csv(ruta, HEADER_CSV_EXPORTAR_JUGADORES):
        print(ERROR_IMPORTACION)
        return None
    jugadores_por_nombre = {}
    nombre_a_claves = {}
    jugadores_por_posicion = {
        "Arquero": [],
        "Defensor": [],
        "Mediocampista": [],
        "Delantero": [],
    }
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nombre = row["nombre_jugador"]
                posicion = row["posicion"]
                precio = int(row["precio"])
                clave = (nombre, posicion)
                if clave in jugadores_por_nombre:
                    print(JUGADOR_DUPLICADO.format(nombre_jugador=nombre, posicion=posicion))
                    continue
                jugadores_por_nombre[clave] = {"posicion": posicion, "precio": precio}
                jugadores_por_posicion[posicion].append(clave)
                if nombre not in nombre_a_claves:
                    nombre_a_claves[nombre] = []
                nombre_a_claves[nombre].append(clave)
    except (OSError, csv.Error):
        print(ERROR_IMPORTACION)
        return None
    return {
        "por_nombre": jugadores_por_nombre,
        "por_posicion": jugadores_por_posicion,
        "nombre_a_claves": nombre_a_claves
    }

def main(presupuesto_inicial):
    """
    Funcion encargada del menu principal, hacer que el usuario avance segun su eleccion
    """
    equipos= {}
    jugadores_procesados = {}
    while True:
        opcion = input(MENU_USUARIO).strip()

        if not opcion.isdigit():
            print(ERROR_INPUT_INVALIDO)
            continue
        if opcion == SALIR:
            print(MSG_FIN)
            break
        if opcion == IMPORTAR_JUGADORES:
            jugadores_importados = importar_jugadores()
            if jugadores_importados is not None:
                jugadores_procesados = jugadores_importados
                print(MSG_OK.format(cant=len(jugadores_procesados["por_nombre"])))
        elif opcion == CREAR_EQUIPO:
            if not jugadores_procesados:
                print(ERROR_SIN_JUGADORES)
                continue
            menu_crear_equipo(equipos, presupuesto_inicial)
        elif opcion in OPCIONES_MENU:
            if not jugadores_procesados:
                print(ERROR_SIN_JUGADORES)
                continue
            funcion_elegida = OPCIONES_MENU[opcion]
            funcion_elegida(equipos, jugadores_procesados)
        elif opcion == JUGAR_FECHAS:
            if not jugadores_procesados:
                print(ERROR_SIN_JUGADORES)
                continue
            jugar_fechas(equipos)
        else:
            print(ERROR_SELECCION_INVALIDA)

def jugar_fechas(equipos):
    """Lee un archivo de fechas exportado y calcula los puntos por equipo"""
    eventos = _obtener_eventos_fechas()
    if eventos is None:
        return
    if not equipos:
        print(MSG_SIN_EQUIPOS_FECHAS)
        return
    fechas_unicas = {e["fecha_partido"] for e in eventos}
    puntajes_equipos = {nombre: 0 for nombre in equipos}
    for fecha in fechas_unicas:
        evento_fecha = [e for e in eventos if e["fecha_partido"] == fecha]
        puntos_jugadores, jugadores_unicos = _pts_jugadores_fecha(evento_fecha)
        ppf = calcular_ppf(puntos_jugadores, jugadores_unicos)
        puntajes_fecha = _sumar_puntajes_equipos(equipos, puntos_jugadores, ppf)
        for nombre_equipo, puntaje in puntajes_fecha.items():
            puntajes_equipos[nombre_equipo] += puntaje
    ranking = ordenar_ranking(puntajes_equipos)
    print(MSG_OK_FECHAS.format(
        cant_fechas = len(fechas_unicas),
        cant_eventos = len(eventos),
    ))
    for nombre_equipo, puntos in ranking:
        print(TEMPLATE_PUNTAJE_EQUIPO.format(
            nombre_equipo = nombre_equipo,
            puntaje = puntos
        ))

# Funciones aux fechas

def cargar_eventos(ruta):
    """Lee el csv de fechas y devuelve la lista de eventos"""
    eventos = []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                eventos.append(row)
    except OSError:
        print(ERROR_IMPORTACION)
        return None
    return eventos

def calcular_puntos_jugador(tipo_evento, detalle, lado):
    """Devuelve los puntos que suma un evento individual"""
    puntos = 0
    if tipo_evento == EVENTO_GOL:
        if detalle == DETALLE_GOL_EN_CONTRA:
            puntos = PTS_GOL_EN_CONTRA
        elif detalle == DETALLE_PENAL_CONVERTIDO:
            puntos = PTS_PENAL_CONVERTIDO
        elif lado == LADO_VISITANTE:
            puntos = PTS_GOL_VISITANTE
        else:
            puntos = PTS_GOL_A_FAVOR
    if tipo_evento == EVENTO_ASISTENCIA:
        puntos = PTS_ASISTENCIA
    if tipo_evento == EVENTO_TARJETA:
        if detalle == DETALLE_AMARILLA:
            puntos = PTS_AMARILLA
        elif detalle == DETALLE_ROJA:
            puntos = PTS_ROJA
    if tipo_evento == EVENTO_ATAJADA and detalle == DETALLE_ATAJADA_EXITOSA:
        puntos = PTS_ATAJADA_EXITOSA
    if tipo_evento == EVENTO_DESPEJE:
        puntos = PTS_DESPEJE
    return puntos

def calcular_ppf(puntos_jugadores, jugadores_unicos):
    """Calcula los puntos por fecha (ppf)"""
    n = len(jugadores_unicos)
    total_puntos = sum(puntos_jugadores.values())
    ppf = round(total_puntos / n) if n > 0 else 1
    if ppf == 0:
        ppf = 1
    return ppf

def _clave_ranking(equipo_puntaje):
    """Ordena por puntaje descendente, y por nombre ascendente si hay empate"""
    return (-equipo_puntaje[1], equipo_puntaje[0])

def ordenar_ranking(puntajes_equipos):
    """Ordena el ranking de los equipos segun su puntaje"""
    return sorted(puntajes_equipos.items(), key=_clave_ranking)

def _obtener_eventos_fechas():
    """Pide la ruta, valida y devuelve la lista de eventos. Lista vacia si falla."""
    ruta = input(PROMPT_RUTA).strip()
    if ruta == "**":
        return None
    if not validar_ruta_csv(ruta, HEADER_CSV_EXPORTAR_FECHAS):
        print(ERROR_IMPORTACION)
        return None
    eventos = cargar_eventos(ruta)
    if eventos is None:
        return None
    return eventos

def _pts_jugadores_fecha(evento_fecha):
    """Suma los puntos de cada jugador en una fecha"""
    puntos_jugadores = {}
    jugadores_unicos = set()
    for evento in evento_fecha:
        nombre = evento["nombre_jugador"]
        tipo = evento["evento"]
        detalle = evento.get("detalle_evento", "")
        lado = evento.get("lado", "")
        jugadores_unicos.add(nombre)
        puntos = calcular_puntos_jugador(tipo, detalle, lado)
        puntos_jugadores[nombre] = puntos_jugadores.get(nombre, 0) + puntos
    return puntos_jugadores, jugadores_unicos

def _sumar_puntajes_equipos(equipos, puntos_jugadores, ppf):
    """Calcula cuantos puntos suma cada equipo para una fecha dada"""
    puntajes = {}
    for nombre_equipo, equipo in equipos.items():
        alineacion = equipo.get("alineacion")
        if not alineacion:
            puntajes[nombre_equipo] = 0
            continue
        titulares = alineacion.get("titulares", [])
        puntaje = 0
        for titular in titulares:
            nombre_titular = titular[0] if isinstance(titular, tuple) else titular
            if nombre_titular in puntos_jugadores:
                puntos_base = puntos_jugadores[nombre_titular]
                factor_rendimiento = round(puntos_base / ppf)
                puntaje += puntos_base + factor_rendimiento
        puntajes[nombre_equipo] = puntaje
    return puntajes

if __name__ == "__main__":
    main(PRESUPUESTO_INICIAL)
