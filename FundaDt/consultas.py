"""
Archivo que se encarga de las opciones que solo devuelven cosas ya existentes.
Ver plantel, alineacion y estadistica de jugador mas usado
"""
from constantes import (
    ERROR_SIN_EQUIPOS, MSG_PLANTEL_VACIO,
    TEMPLATE_PLANTEL, TEMPLATE_JUGADOR_PLANTEL,
    MSG_ALINEACION_INEXISTENTE, TEMPLATE_ALINEACION, TEMPLATE_JUGADOR_POSICION,
    TEMPLATE_ESTADISTICA_JUGADORES, MSG_NO_INFORMACION
)
from mercado import _elegir_equipo, _obtener_datos_jugador, _obtener_rol

#Ver Plantel

def _imprimir_plantel(equipo, nombre_eq, datos_jugadores):
    """
    Imprime la lista de jugadores
    """
    print(TEMPLATE_PLANTEL.format(
        nombre_equipo = nombre_eq,
        presupuesto = equipo["presupuesto"]
        ))
    plantel = equipo.get("plantel", [])
    if not plantel:
        print(MSG_PLANTEL_VACIO)
        return
    plantel_ordenado = plantel
    for n, clave in enumerate(plantel_ordenado, start = 1):
        info_jugador = _obtener_datos_jugador(clave, datos_jugadores)
        rol = _obtener_rol(equipo, clave)
        print(TEMPLATE_JUGADOR_PLANTEL.format(
            n = n,
            nombre_jugador = clave[0],
            posicion = info_jugador[1],
            rol_actual = rol,
            precio = info_jugador[2]
        ))

def menu_ver_plantel(equipos, datos_jugadores):
    """
    Funcion principal para la opcion 4 (Ver el plantel)
    """
    if not equipos:
        print(ERROR_SIN_EQUIPOS)
        return
    nombre_eq = _elegir_equipo(equipos)
    if not nombre_eq:
        return
    _imprimir_plantel(equipos[nombre_eq], nombre_eq, datos_jugadores)

#Ver Alineacion
def _agrupar_titulares(titulares, datos_jugadores):
    """
    Separa a los titulares por posicion y los ordena 
    """
    grupos = {"Arquero": [], "Defensor": [], "Mediocampista": [], "Delantero": []}
    for clave in titulares:
        info_jugador = _obtener_datos_jugador(clave, datos_jugadores)
        grupos[info_jugador[1]].append(clave[0])
    return (
        " - ".join(sorted(grupos["Delantero"])),
        " - ".join(sorted(grupos["Mediocampista"])),
        " - ".join(sorted(grupos["Defensor"])),
        " - ".join(sorted(grupos["Arquero"]))
    )

def _armar_bloque_suplentes(suplentes, datos_jugadores):
    """
    Crea un bloque de texto para mostrar a los suplentes
    """
    lineas = []
    suplentes_ordenados = sorted(suplentes)
    for n, clave in enumerate(suplentes_ordenados, start = 1):
        info_jugador = _obtener_datos_jugador(clave, datos_jugadores)
        linea = TEMPLATE_JUGADOR_POSICION.format(
            n = n,
            nombre_jugador = clave[0],
            posicion = info_jugador[1]
        )
        lineas.append(linea)
    return "\n".join(lineas)

def _imprimir_alineacion(alineacion, datos_jugadores):
    """
    Prepara los strings para mostrarlos en el Template
    """
    at, med, df, arq = _agrupar_titulares(alineacion["titulares"], datos_jugadores)
    suplentes_str = _armar_bloque_suplentes(alineacion["suplentes"], datos_jugadores)
    print(TEMPLATE_ALINEACION.format(
        formacion = alineacion["formacion"],
        delanteros = at,
        mediocampistas = med,
        defensores = df,
        arquero = arq,
        capitan = alineacion["capitan"][0] if isinstance(alineacion["capitan"], tuple) else alineacion["capitan"],
        suplentes = suplentes_str
    ), end="")

def menu_ver_alineacion(equipos, datos_jugadores):
    """
    Funcion principal de la opcion 6 (Ver alineacion)
    """
    if not equipos:
        print(ERROR_SIN_EQUIPOS)
        return
    nombre_eq = _elegir_equipo(equipos)
    if not nombre_eq:
        return
    alineacion = equipos[nombre_eq].get("alineacion")
    if not alineacion:
        print(MSG_ALINEACION_INEXISTENTE)
        return
    _imprimir_alineacion(alineacion, datos_jugadores)

def _buscar_lider_posicion(todos_los_usados, datos_jugadores, posicion_objetivo):
    """
    Cuenta la frecuencia con la que aparece cada jugador.
    Encuentra y muestra al jugador mas usado por puesto
    """
    jugadores_posicion = datos_jugadores["por_posicion"].get(posicion_objetivo, [])
    nombres_posicion = [c[0] for c in jugadores_posicion]
    conteos = {}
    for clave in todos_los_usados:
        nombre = clave[0] if isinstance(clave, tuple) else clave
        if nombre in nombres_posicion:
            conteos[nombre] = conteos.get(nombre, 0) + 1
    if not conteos:
        return "N/A"
    ganador = None
    max_usos = -1
    for nombre in sorted(conteos.keys()):
        if conteos[nombre] > max_usos:
            max_usos = conteos[nombre]
            ganador = nombre
    return ganador

def menu_ver_jugador_mas_utilizado(equipos, datos_jugadores):
    """
    Funcion principal para detectar y mostrar al jugador mas usado por cada posicion
    """
    usados_globales = []
    for eq in equipos.values():
        ali = eq.get("alineacion")
        if ali:
            usados_globales.extend(ali.get("titulares", []))
            usados_globales.extend(ali.get("suplentes", []))
    if not usados_globales:
        print(MSG_NO_INFORMACION)
        return
    arq = _buscar_lider_posicion(usados_globales, datos_jugadores, "Arquero")
    df = _buscar_lider_posicion(usados_globales, datos_jugadores, "Defensor")
    med = _buscar_lider_posicion(usados_globales, datos_jugadores, "Mediocampista")
    at = _buscar_lider_posicion(usados_globales, datos_jugadores, "Delantero")

    print(TEMPLATE_ESTADISTICA_JUGADORES.format(
        arquero = arq,
        defensor = df,
        mediocampista = med,
        delantero = at
    ))
