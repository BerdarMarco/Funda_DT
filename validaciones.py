"""Archivo donde se encuentran las funcionen de validacion"""

import os

MAX_LONG_NOMBRE = 50
def equipo_existente(nombre_nuevo, equipos):
    """Verifica que el equipo no exista previamente antes de crearlo"""
    nombre_nuevo_upper = nombre_nuevo.upper()
    for equipo in equipos:
        if equipo.upper() == nombre_nuevo_upper:
            return True
    return False

def nombre_valido(nombre):
    """Verifica que el nombre tenga solo caracteres,
    cumpliendo con el minimo y maximo de caracteres"""
    nombre_sin_es = nombre.replace(" ","")
    if len(nombre) == 0 or len(nombre) > MAX_LONG_NOMBRE:
        return False
    if not nombre_sin_es.isalpha():
        return False
    return True

def jugador_en_plantel(clave_jugador, plantel):
    """Verifica si el jugador ya fue comprado previamente"""
    return clave_jugador in plantel

def indice_valido(indice, total_elementos):
    """Verifica que el indice ingresado este dentro del rango valido de la lista"""
    return 0 <= indice < total_elementos

def es_numero_valido(parte):
    """Verifica que se ingrese un numero entero positivo"""
    return parte.strip().isdigit()

def no_repetidos(indices):
    """Verifica que no haya indices repetidos en la lista"""
    return len(set(indices)) == len(indices)

def presupuesto_suficiente(indices, jugadores, equipo):
    """Veridica que el presupuesto alcance para comprar todos los jugadores seleccionados"""
    costo_total = sum(jugadores[ind][2] for ind in indices)
    return costo_total <= equipo["presupuesto"]

#TP 3

def es_csv(ruta):
    """Verifica si un archivo es csv"""
    return ruta.lower().endswith(".csv")

def csv_header_valido(ruta, header_esperado):
    """Verifica si el csv tiene un header correcto"""
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            primera = f.readline().strip()
            return primera == header_esperado
    except (OSError, ValueError):
        return False

def validar_ruta_csv(ruta,header_esperado):
    """
    Valida una ruta de archivo csv.
    Devuelve True si es valida, False si no.
    """
    if " " in ruta:
        return False
    if not os.path.exists(ruta) or not ruta.lower().endswith(".csv"):
        return False
    return csv_header_valido(ruta, header_esperado)
