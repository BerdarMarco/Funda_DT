"""
Encargado de la gestion tactica y alineacion de equipos
"""
from mercado import _elegir_equipo, _obtener_datos_jugador
from constantes import (
    ERROR_SIN_EQUIPOS, ERROR_INPUT_INVALIDO, ERROR_FORMACION_INVALIDA,
    ERROR_SELECCION_INVALIDA, MSG_CANTIDAD_JUGADORES_INSUFICIENTE,
    ERROR_CANTIDAD_INVALIDA, MSG_ALINEACION_GUARDADA, TEMPLATE_JUGADOR,
    TEMPLATE_JUGADOR_POSICION, HEADER_ARQUERO, HEADER_DEFENSORES,
    HEADER_MEDIOCAMPISTAS, HEADER_DELANTEROS, HEADER_SUPLENTES, HEADER_TITULARES
)
# Constantes

OPCION_SALIR = "**"
PEDIR_FORMACION = "Ingrese formación: "
PEDIR_SUPLENTES = "Seleccione 5 jugadores: "
PEDIR_CAPITAN = "Seleccione un capitán: "
PEDIR_TITULARES = "Seleccione {cant} jugador(es): "
ERROR_SELECCION = "SELECCION"
INPUT_INVALIDO = "INPUT"
ERROR_FORMATO = "FORMATO"
ERROR_CANTIDAD = "CANTIDAD"

#Sub funciones de logica
def _parsear_formacion(texto):
    """
    Convierte la formacion de un string a una lista
    """
    partes = texto.split("-")
    if len(partes) != 3:
        return None
    for p in partes:
        if not p.strip().isdigit():
            return None
    return [int(p.strip()) for p in partes]

def _formacion_valida(nums):
    """
    Revisa que la formacion solicitada sume 10 jugadores sin contar al arquero
    """
    defensores, mediocampistas, delanteros = nums
    if defensores == 0 or mediocampistas == 0 or delanteros == 0:
        return False
    return (defensores + mediocampistas + delanteros) == 10

def _contar_posiciones(plantel, datos_jugadores):
    """
    Cuenta cuantos jugadores hay por posicion
    """
    cantidades = {
        "Arquero": 0,
        "Defensor": 0,
        "Mediocampista": 0,
        "Delantero": 0
    }
    for clave in plantel:
        info_jugador = _obtener_datos_jugador(clave, datos_jugadores)
        cantidades[info_jugador[1]] += 1
    return cantidades

def _disponibilidad(plantel, datos_jugadores, formacion):
    """
    Verifica si hay jugadores suficientes para armar la formacion
    """
    if len(plantel) < 16:
        return False
    cantidades = _contar_posiciones(plantel, datos_jugadores)
    defensores, mediocampistas, delanteros = formacion
    if cantidades["Arquero"] < 1:
        return False
    if cantidades["Defensor"] < defensores:
        return False
    if cantidades["Mediocampista"] < mediocampistas or cantidades["Delantero"] < delanteros:
        return False
    return True

def _procesar_indices(partes, max_jugadores):
    """
    Filtra y valida los numeros ingresados
    """
    indices = []
    for p in partes:
        p = p.strip()
        if not p.isdigit():
            return ERROR_FORMATO
        ind = int(p) - 1
        if ind in indices:
            return ERROR_FORMATO
        if ind < 0 or ind >= max_jugadores:
            return ERROR_SELECCION
        indices.append(ind)
    return indices

def _validar_indices_alineacion(eleccion, max_jugadores, cant_req):
    """
    Valida el input ingresado con el formato defensores-mediocampistas-atacantes
    Solicitado para armar la formacion. ejemplo(4-3-3)
    """
    eleccion_unificada = eleccion.replace(",", "-").replace(" ", "")
    if cant_req > 1 and "-" not in eleccion_unificada:
        return ERROR_FORMATO
    partes = eleccion_unificada.split("-")
    if len(partes) != cant_req:
        return ERROR_CANTIDAD
    return _procesar_indices(partes, max_jugadores)

def _filtrar_posiciones_plantel(plantel, datos_jugadores, posicion):
    """
    Devuelve una lista ordenada de jugadores en la posicion elegida
    """
    jugadores_posicion = datos_jugadores["por_posicion"].get(posicion, [])
    nombres_posicion = [c[0] for c in jugadores_posicion]
    return sorted([clave for clave in plantel if clave[0] in nombres_posicion])

#Sub funciones de utilidad
def _errores_seleccion(res, cantidad_req):
    """
    Muestra el error en cada caso si es que hay
    """
    if res == ERROR_CANTIDAD:
        print(ERROR_CANTIDAD_INVALIDA.format(cantidad = cantidad_req))
    if res == ERROR_FORMATO:
        print(ERROR_INPUT_INVALIDO)
    if res == ERROR_SELECCION:
        print(ERROR_SELECCION_INVALIDA)

def _pedir_formacion():
    """
    Bucle encargado de pedir la formacion
    """
    while True:
        f = input(PEDIR_FORMACION).strip()
        if f == OPCION_SALIR:
            return None
        nums = _parsear_formacion(f)
        if not nums:
            print(ERROR_INPUT_INVALIDO)
            continue
        if not _formacion_valida(nums):
            print(ERROR_FORMACION_INVALIDA)
            continue
        return nums

def _pedir_titulares(header, disponibles, cant_req):
    """
    Bucle encargado de elegir los titulares
    """
    print(header)
    for n, clave in enumerate(disponibles, start = 1):
        print(TEMPLATE_JUGADOR.format(n=n, nombre_jugador=clave[0]))
    while True:
        eleccion = input(PEDIR_TITULARES.format(cant=cant_req)).strip()
        if eleccion == OPCION_SALIR:
            return None
        res = _validar_indices_alineacion(eleccion, len(disponibles), cant_req)
        if isinstance(res, str):
            _errores_seleccion(res, cant_req)
            continue
        return [disponibles[i] for i in res]

def _pedir_suplentes(plantel, titulares, datos_jugadores):
    """
    Bucle encargado de elegir a los 5 suplentes
    """
    disponibles = sorted([j for j in plantel if j not in titulares])
    print(HEADER_SUPLENTES)
    for n, clave in enumerate(disponibles, start = 1):
        info_jugador = _obtener_datos_jugador(clave, datos_jugadores)
        print(TEMPLATE_JUGADOR_POSICION.format(
            n = n,
            nombre_jugador = clave[0],
            posicion = info_jugador[1]
        ))
    while True:
        eleccion = input(PEDIR_SUPLENTES).strip()
        if eleccion == OPCION_SALIR:
            return None
        res = _validar_indices_alineacion(eleccion, len(disponibles), 5)
        if isinstance(res, str):
            _errores_seleccion(res, 5)
            continue
        return [disponibles[i] for i in res]

def _validar_capitan(eleccion, max_jugadores):
    """
    Valida el numero del capitan
    """
    if not eleccion.isdigit():
        return INPUT_INVALIDO
    ind = int(eleccion) - 1
    if ind < 0 or ind >= max_jugadores:
        return ERROR_SELECCION
    return ind

def _pedir_capitan(titulares, datos_jugadores):
    """
    Bucle encargado de elegir al capitan
    """
    print(HEADER_TITULARES)
    ordenados = sorted(titulares)
    for n, clave in enumerate(ordenados, start = 1):
        info_jugador = _obtener_datos_jugador(clave, datos_jugadores)
        print(TEMPLATE_JUGADOR_POSICION.format(
            n = n,
            nombre_jugador = clave[0],
            posicion = info_jugador[1]
            ))
    while True:
        eleccion = input(PEDIR_CAPITAN).strip()
        if eleccion == OPCION_SALIR:
            return None
        ind = _validar_capitan(eleccion, len(ordenados))
        if ind == INPUT_INVALIDO:
            print(ERROR_INPUT_INVALIDO)
            continue
        if ind == ERROR_SELECCION:
            print(ERROR_SELECCION_INVALIDA)
            continue
        return ordenados[ind]

def _ejecutar_titulares(plantel, formacion, datos_jugadores):
    """
    Pide las posiciones en orden
    """
    defensores, mediocampistas, delanteros = formacion
    pos = [
        (HEADER_ARQUERO, "Arquero", 1),
        (HEADER_DEFENSORES, "Defensor", defensores),
        (HEADER_MEDIOCAMPISTAS, "Mediocampista", mediocampistas),
        (HEADER_DELANTEROS, "Delantero", delanteros)
    ]
    titulares = []
    for header, rol, cant in pos:
        disponibles = _filtrar_posiciones_plantel(plantel, datos_jugadores, rol)
        elegidos = _pedir_titulares(header, disponibles, cant)
        if not elegidos:
            return None
        titulares.extend(elegidos)
    return titulares

#Funciones principales
def _preparar_alineacion(equipos, datos_jugadores):
    """
    Valida el equipo y la formacion
    """
    nombre_eq = _elegir_equipo(equipos)
    if not nombre_eq:
        return None, None
    equipo = equipos[nombre_eq]
    formacion = _pedir_formacion()
    if not formacion:
        return None, None
    if not _disponibilidad(equipo["plantel"], datos_jugadores, formacion):
        print(MSG_CANTIDAD_JUGADORES_INSUFICIENTE)
        return None, None
    return nombre_eq, formacion

def _ejecutar_selecciones(equipo, formacion, datos_jugadores):
    """
    Elegir titulares, suplente y capitan
    """
    titulares = _ejecutar_titulares(equipo["plantel"], formacion, datos_jugadores)
    if not titulares:
        return None
    suplentes = _pedir_suplentes(equipo["plantel"], titulares, datos_jugadores)
    if not suplentes:
        return None
    capitan = _pedir_capitan(titulares, datos_jugadores)
    if not capitan:
        return None
    return titulares, suplentes, capitan

def menu_armar_alineacion(equipos, datos_jugadores):
    """
    Funcion principal donde se ejecutan las subfunciones juntas
    """
    if not equipos:
        print(ERROR_SIN_EQUIPOS)
        return
    nombre_eq, formacion = _preparar_alineacion(equipos, datos_jugadores)
    if not nombre_eq:
        return
    equipo = equipos[nombre_eq]
    op_acciones = _ejecutar_selecciones(equipo, formacion, datos_jugadores)
    if not op_acciones:
        return
    titulares, suplentes, capitan = op_acciones
    equipo["alineacion"] = {
        "formacion": f"{formacion[0]}-{formacion[1]}-{formacion[2]}",
        "titulares": titulares,
        "suplentes": suplentes,
        "capitan": capitan
    }
    print(MSG_ALINEACION_GUARDADA.format(nombre_equipo=nombre_eq))
