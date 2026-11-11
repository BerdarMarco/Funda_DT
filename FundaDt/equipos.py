"""
Aca se encuentran la logica y el I/O de las funciones de crear equipo 
"""
from constantes import (MSG_EQUIPO_CREADO, ERROR_EQUIPO_EXISTENTE, ERROR_FORMATO_NOMBRE)
from validaciones import nombre_valido, equipo_existente

#CONSTANTES
OPCION_SALIR = "**"
PEDIR_NOMBRE_EQUIPO = "Ingrese el nombre del equipo: "

def guardar_equipo(equipos, nombre, presupuesto_inicial):
    """
    Guarda el nuevo equipo creado. Recibe la informacion ya validada.
    No devuelve valor, simplemente modifica el diccionario equipos directamente
    """
    equipos[nombre] = {
            "presupuesto": presupuesto_inicial,
            "plantel": [],
            "alineacion": None
        }
    equipos_ordenados = dict(sorted(equipos.items()))
    equipos.clear()
    for nombre_equipo, datos_equipo in equipos_ordenados.items():
        equipos[nombre_equipo] = datos_equipo

def pedir_nombre_equipo(equipos):
    """Se encarga especificamente de pedir el input.
    Los valida hasta que este sea correcto o el usuario lo cancele"""
    while True:
        nombre = input(PEDIR_NOMBRE_EQUIPO).strip()
        if nombre == "**":
            return None
        if not nombre_valido(nombre):
            print(ERROR_FORMATO_NOMBRE)
            continue
        if equipo_existente(nombre, equipos):
            print(ERROR_EQUIPO_EXISTENTE)
            continue
        return nombre

def menu_crear_equipo(equipos, presupuesto_inicial):
    """
    Orquesta el flujo de creacion de un equipo:
    Pide el nombre al usuario, guarda el equipo e imprime el mensaje de confirmacion.
    No retorna valor
    """
    nombre = pedir_nombre_equipo(equipos)
    if nombre is None:
        return
    guardar_equipo(equipos, nombre, presupuesto_inicial)
    print(MSG_EQUIPO_CREADO.format(nombre_equipo=nombre, presupuesto=presupuesto_inicial))
