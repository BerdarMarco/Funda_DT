"""
En este archivo se encuentran las funciones para el manejo del mercado
"""
from constantes import (
    ERROR_SIN_EQUIPOS, HEADER_EQUIPOS, TEMPLATE_EQUIPO,
    ERROR_INPUT_INVALIDO, ERROR_SELECCION_INVALIDA,
    TEMPLATE_PRESUPUESTO, HEADER_JUGADORES, TEMPLATE_JUGADOR_PRECIO,
    ERROR_JUGADOR_EXISTENTE, ERROR_PRESUPUESTO_INSUFICIENTE,
    MSG_COMPRA_EXITOSA, MSG_PLANTEL_VACIO, TEMPLATE_PLANTEL,
    TEMPLATE_JUGADOR_PLANTEL, MSG_VENTA_EXITOSA, MSG_ALINEACION_DESARMADA)
from validaciones import (
    jugador_en_plantel, indice_valido, es_numero_valido,
    no_repetidos, presupuesto_suficiente)

#Constantes de mercado
DUPLICADO = "DUPLICADO"
SIN_PLATA = "SIN_PLATA"
EXITO = "EXITO"
INPUT_INVALIDO = "INPUT"
ERROR_SELECCION = "ERROR_SELECCION"
SELECCION_EQUIPO = "Seleccione un equipo: "
OPCION_SALIR = "**"
MENU_OPCIONES = """Posiciones:
1. Arquero
2. Defensor
3. Mediocampista
4. Delantero
Ingrese la posición del jugador: """
PEDIR_POSICION = "Ingrese la posición del jugador: "
TEXTO_PAGINACION = "> : Página siguiente\n< : Página anterior\nSeleccione una opción: "
SELECCION_OPCION = "Seleccione una opción: "
SELECCION_VENTA = "Seleccione el jugador a vender: "
PAG_SIGUIENTE = ">"
PAG_ANTERIOR = "<"
LIMITE_PAGINACION = 5
MAPA_POSICIONES = {
    "1": "Arquero",
    "2": "Defensor",
    "3": "Mediocampista",
    "4": "Delantero"
}
#Manejo de errores

def _manejar_error_conversion(op_accion):
    """Imprime el error correspondiente si la conversion de indices fallo"""
    if op_accion == INPUT_INVALIDO:
        print(ERROR_INPUT_INVALIDO)
        return True
    if op_accion == ERROR_SELECCION:
        print(ERROR_SELECCION_INVALIDA)
        return True
    return False

#Funciones de Logica de Compra

def _ejecutar_compras(equipo, nombre_eq, indices, jugadores):
    """
    Ejecuta la compra asumiendo que ya esta todo valido.
    """
    jugadores_a_comprar = [jugadores[ind] for ind in indices]
    jugadores_a_comprar.sort()
    for jugador in jugadores_a_comprar:
        equipo["presupuesto"] -= jugador[2]
        equipo["plantel"].append((jugador[0], jugador[1]))
        equipo["plantel"].sort()
        _mostrar_compra_exitosa(jugador[0], nombre_eq, equipo["presupuesto"])

#Funciones auxiliares de Compra

def _convertir_indices_compra(eleccion, max_jugadores, inicio):
    """
    Convierte la eleccion del usuario a una lista de enteros
    """
    eleccion_unificada = eleccion.replace(",", "-").replace(" ", "")
    numeros_ingresados = eleccion_unificada.split("-")
    indices = []
    for numero in numeros_ingresados:
        if not es_numero_valido(numero):
            return INPUT_INVALIDO
        indice_local = int(numero) - 1
        if not indice_valido(indice_local, max_jugadores):
            return ERROR_SELECCION
        indices.append(inicio + indice_local)
    if not no_repetidos(indices):
        return INPUT_INVALIDO
    return indices

def _verificar_duplicados(indices, jugadores, equipo):
    """Verifica que los jugadores seleccionados no esten previamente en el plantel"""
    hay_duplicado = False
    nombres_en_plantel = [clave[0] for clave in equipo["plantel"]]
    for ind in indices:
        jugador = jugadores[ind]
        if jugador_en_plantel(jugador[0], nombres_en_plantel):
            print(ERROR_JUGADOR_EXISTENTE.format(nombre_jugador = jugador[0]))
            hay_duplicado = True
    return hay_duplicado

def _mostrar_compra_exitosa(nombre_jugador, nombre_equipo, presupuesto):
    """Muestra el mensaje de compra exitosa de un jugador"""
    print(MSG_COMPRA_EXITOSA.format(
            nombre_jugador = nombre_jugador,
            nombre_equipo = nombre_equipo,
            presupuesto = presupuesto
        ))

def _imprimir_pags(jugadores, pagina, limite):
    """
    Muestra a los jugadores correspondientes a la pagina en la que se encuentra el usuario
    """
    inicio = pagina * limite
    fin = inicio + limite
    print(HEADER_JUGADORES)
    for n, jugador in enumerate(jugadores[inicio:fin], start = 1):
        print(TEMPLATE_JUGADOR_PRECIO.format(
            n = n,
            nombre_jugador = jugador[0],
            precio = jugador[2]
        ))

def _es_paginacion(eleccion):
    """Indica si el usuario quiere cambiar de pagina"""
    return eleccion in (PAG_SIGUIENTE, PAG_ANTERIOR)

def _procesar_paginacion(eleccion, pagina, total_jugadores):
    """
    Calcula la nueva pagina segun lo que el usuario elige. 
    """
    if eleccion == PAG_SIGUIENTE:
        if (pagina * LIMITE_PAGINACION) + LIMITE_PAGINACION < total_jugadores:
            return pagina + 1
        print(ERROR_SELECCION_INVALIDA)
    if eleccion == PAG_ANTERIOR:
        if pagina > 0:
            return pagina - 1
        print(ERROR_SELECCION_INVALIDA)
    return pagina

def _obtener_indices_compra(eleccion, jugadores, pagina):
    """Convierte y valida la eleccion del usuario en indices de jugadores"""
    inicio = pagina * LIMITE_PAGINACION
    max_jugadores = len(jugadores[inicio:inicio+LIMITE_PAGINACION])
    op_accion = _convertir_indices_compra(eleccion, max_jugadores, inicio)
    if _manejar_error_conversion(op_accion):
        return None
    return op_accion

def _intentar_compra(eleccion, datos_equipo, equipo_elegido, jugadores, pagina):
    """Intenta efectuar la compra con la eleccion del usuario"""
    indices = _obtener_indices_compra(eleccion, jugadores, pagina)
    if indices is None:
        return False
    if _verificar_duplicados(indices, jugadores, datos_equipo):
        return False
    if not presupuesto_suficiente(indices, jugadores, datos_equipo):
        print(ERROR_PRESUPUESTO_INSUFICIENTE)
        return SIN_PLATA
    _ejecutar_compras(datos_equipo, equipo_elegido, indices, jugadores)
    return EXITO


def _gestionar_tienda(equipo, nombre_eq, jugadores):
    """
    Bucle principal de la tienda
    """
    pagina = 0
    _imprimir_pags(jugadores, pagina, LIMITE_PAGINACION)
    texto_input = TEXTO_PAGINACION
    while True:
        eleccion = input(texto_input).strip()
        texto_input = SELECCION_OPCION
        if eleccion == OPCION_SALIR:
            return None
        if _es_paginacion(eleccion):
            nueva_pag = _procesar_paginacion(eleccion, pagina, len(jugadores))
            if nueva_pag != pagina:
                pagina = nueva_pag
                _imprimir_pags(jugadores, pagina, LIMITE_PAGINACION)
            texto_input = TEXTO_PAGINACION
            continue
        intento_de_compra = _intentar_compra(eleccion, equipo, nombre_eq, jugadores, pagina)
        if intento_de_compra in (EXITO, SIN_PLATA):
            return None

#Funciones de logica de Venta

def vender_jugadores(equipo, nombre_jugador, precio):
    """
    Orquesta las modificaciones dentro del equipo al vender un jugador,
    llamando a las funciones auxiliares
    """
    _sumar_presupuesto(equipo, precio)
    _eliminar_jugador(equipo, nombre_jugador)
    desarmo_alineacion = _desarmar_alineacion(equipo, nombre_jugador)
    return desarmo_alineacion

#Funciones auxiliares de venta

def _sumar_presupuesto(equipo, precio):
    """Suma el dinero ganado por la venta de algun jugador"""
    equipo["presupuesto"] += precio

def _eliminar_jugador(equipo, nombre_jugador):
    """Elimina al jugador vendido del plantel"""
    equipo["plantel"].remove(nombre_jugador)

def _desarmar_alineacion(equipo, nombre_jugador):
    """Revisa si el jugador pertenecia a la alineacion (Suplente o titular).
    Y si es el caso desarma la formacion"""
    if not equipo.get("alineacion"):
        return False
    al = equipo["alineacion"]
    nombre = nombre_jugador[0] if isinstance(nombre_jugador, tuple) else nombre_jugador
    titulares = al.get("titulares", [])
    suplentes = al.get("suplentes", [])
    for t in titulares:
        if (isinstance(t, tuple) and t[0] == nombre) or (not isinstance(t, tuple) and t == nombre):
            equipo["alineacion"] = None
            return True
    for s in suplentes:
        if (isinstance(s, tuple) and s[0] == nombre) or (not isinstance(s, tuple) and s == nombre):
            equipo["alineacion"] = None
            return True
    return False

def _mostrar_venta_exitosa(nombre_jugador, presupuesto, desarmo_alineacion):
    """Muestra el mensaje de venta exitosa y, si corresponde, el mensaje de alineacion"""
    print(MSG_VENTA_EXITOSA.format(
        nombre_jugador = nombre_jugador[0],
        presupuesto = presupuesto
    ))
    if desarmo_alineacion:
        print(MSG_ALINEACION_DESARMADA)

#Sub funciones del menu de compras y ventas
def _mostrar_equipos(nombres):
    """
    Imprime la lista de equipos disponibles
    """
    print(HEADER_EQUIPOS)
    for n, nombre in enumerate(nombres, start=1):
        print(TEMPLATE_EQUIPO.format(
            n = n,
            nombre_equipo = nombre))

def _elegir_equipo(equipos):
    """
    Pide y valida el equipo
    """
    nombres = list(equipos.keys())
    _mostrar_equipos(nombres)
    while True:
        eleccion = input(SELECCION_EQUIPO).strip()
        if eleccion == OPCION_SALIR:
            return None
        if not eleccion.isdigit():
            print(ERROR_INPUT_INVALIDO)
            continue
        ind = int(eleccion) - 1
        if not indice_valido(ind, len(nombres)):
            print(ERROR_SELECCION_INVALIDA)
            continue
        return nombres[ind]

def _elegir_posicion():
    """
    Pide y valida la posicion
    """
    mapa = MAPA_POSICIONES
    texto_input = MENU_OPCIONES
    while True:
        eleccion = input(texto_input).strip()
        texto_input = PEDIR_POSICION
        if eleccion == OPCION_SALIR:
            return None
        if not eleccion.isdigit():
            print(ERROR_INPUT_INVALIDO)
            continue
        if eleccion in mapa:
            return mapa[eleccion]
        print(ERROR_SELECCION_INVALIDA)

def logica_filtrar_jugadores(datos_jugadores, posicion_buscada):
    """
    Filtra a los jugadores por posicion y los ordena en orden alfabetica
    """
    claves = datos_jugadores["por_posicion"].get(posicion_buscada, [])
    disponibles = []
    for clave in claves:
        info_jugador = datos_jugadores["por_nombre"][clave]
        disponibles.append([clave[0], info_jugador["posicion"], info_jugador["precio"]])
    disponibles.sort()
    return disponibles

def _obtener_datos_jugador(clave_jugador, datos_jugadores):
    """
    Busca un jugador por nombre en el diccionario de jugadores y,
    devuelve una lista [nombre, posicion, precio]
    """
    info_j = datos_jugadores["por_nombre"].get(clave_jugador)
    if info_j:
        return [clave_jugador[0], info_j["posicion"], info_j["precio"]]
    return None

def _obtener_rol(equipo, clave_jugador):
    """
    Busca el rol actual de un jugador en la alineacion
    """
    alineacion = equipo.get("alineacion")
    if not alineacion:
        return "Reserva"
    titulares = alineacion.get("titulares", [])
    suplentes = alineacion.get("suplentes", [])
    for t in titulares:
        if (isinstance(t, tuple) and t == clave_jugador) or (not isinstance(t, tuple) and t == clave_jugador):
            return "Titular"
    for s in suplentes:
        if (isinstance(s, tuple) and s == clave_jugador) or (not isinstance(s, tuple) and s == clave_jugador):
            return "Suplente"
    return "Reserva"

def _mostrar_plantel_venta(equipo, nombre_eq, datos_jugadores):
    """
    Imprime el plantel actual
    """
    print(TEMPLATE_PLANTEL.format(
        nombre_equipo = nombre_eq,
        presupuesto = equipo["presupuesto"]))
    plantel_ordenado = equipo["plantel"]
    for n, clave in enumerate(plantel_ordenado, start=1):
        info_jugador = _obtener_datos_jugador(clave, datos_jugadores)
        rol = _obtener_rol(equipo, clave)
        print(TEMPLATE_JUGADOR_PLANTEL.format(
            n = n,
            nombre_jugador = clave[0],
            posicion = info_jugador[1],
            rol_actual = rol,
            precio = info_jugador[2]
        ))
    return plantel_ordenado

def _indice_jugador_a_vender(max_jugadores):
    """
    Valida el input de ventas
    """
    while True:
        eleccion = input(SELECCION_VENTA).strip()
        if eleccion == OPCION_SALIR:
            return None
        if not eleccion.isdigit():
            print(ERROR_INPUT_INVALIDO)
            continue
        ind = int(eleccion) - 1
        if not indice_valido(ind, max_jugadores):
            print(ERROR_SELECCION_INVALIDA)
            continue
        return ind

#Funciones principales del menu de compra y venta
def menu_comprar_jugadores(equipos, datos_jugadores):
    """
    Funcion principal que maneja las sub funciones
    """
    if not equipos:
        print(ERROR_SIN_EQUIPOS)
        return None
    equipo_elegido = _elegir_equipo(equipos)
    if not equipo_elegido:
        return None
    equipo = equipos[equipo_elegido]
    print(TEMPLATE_PRESUPUESTO.format(presupuesto=equipo["presupuesto"]))
    posicion = _elegir_posicion()
    if not posicion:
        return None
    jugadores = logica_filtrar_jugadores(datos_jugadores, posicion)
    _gestionar_tienda(equipo, equipo_elegido, jugadores)
    return None

def menu_vender_jugador(equipos, datos_jugadores):
    """
    Menu principal para la venta de jugadores
    """
    if not equipos:
        print(ERROR_SIN_EQUIPOS)
        return None
    equipo_elegido = _elegir_equipo(equipos)
    if not equipo_elegido:
        return None
    equipo = equipos[equipo_elegido]
    plantel_ordenado = _mostrar_plantel_venta(equipo, equipo_elegido, datos_jugadores)
    if not plantel_ordenado:
        print(MSG_PLANTEL_VACIO)
        return None
    while True:
        ind = _indice_jugador_a_vender(len(plantel_ordenado))
        if ind is None:
            return None
        jugador_a_vender = plantel_ordenado[ind]
        info_jugador = _obtener_datos_jugador(jugador_a_vender, datos_jugadores)
        precio = info_jugador[2]
        desarmo_alineacion = vender_jugadores(equipo, jugador_a_vender, precio)
        _mostrar_venta_exitosa(jugador_a_vender, equipo["presupuesto"], desarmo_alineacion)
        return None
