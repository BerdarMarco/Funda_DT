"""Constantes globales para FundaDT."""

# ----- mensajes generales -----
MSG_FIN = "Finalizando..."

# ----- templates generales -----
HEADER_EQUIPOS = "Equipos disponibles:"
HEADER_JUGADORES = "Jugadores disponibles:"
TEMPLATE_EQUIPO = "{n}. {nombre_equipo}"

# ----- errores generales -----
ERROR_SELECCION_INVALIDA = "Selección inválida"
ERROR_INPUT_INVALIDO = "Formato de entrada inválido"
ERROR_SIN_EQUIPOS = "No existen equipos registrados"

# ----- crear equipo -----
MSG_EQUIPO_CREADO = (
    "El equipo {nombre_equipo} ha sido creado exitosamente con un presupuesto de ${presupuesto}"
)
ERROR_EQUIPO_EXISTENTE = "Ya existe un equipo con ese nombre"
ERROR_FORMATO_NOMBRE = "Formato de nombre de equipo inválido"

# ----- comprar jugador -----
MSG_COMPRA_EXITOSA = (
    "El jugador {nombre_jugador} fue comprado para el equipo {nombre_equipo}. "
    "El nuevo presupuesto del equipo es: ${presupuesto}"
)
TEMPLATE_PRESUPUESTO = "El presupuesto del equipo es ${presupuesto}"
TEMPLATE_JUGADOR_PRECIO = "{n}. {nombre_jugador} - ${precio}"
ERROR_PRESUPUESTO_INSUFICIENTE = "El presupuesto es insuficiente"
ERROR_JUGADOR_EXISTENTE = "El jugador {nombre_jugador} ya se encuentra en el plantel"

# ----- vender jugador -----
TEMPLATE_PLANTEL = """Equipo: {nombre_equipo}
Presupuesto: ${presupuesto}
Plantel:
"""
TEMPLATE_JUGADOR_PLANTEL = "{n}. {nombre_jugador} ({posicion}) [{rol_actual}] - ${precio}"
MSG_PLANTEL_VACIO = "El equipo no posee jugadores"
MSG_VENTA_EXITOSA = (
    "El jugador {nombre_jugador} fue vendido exitosamente. "
    "El nuevo presupuesto del equipo es: ${presupuesto}"
)
MSG_ALINEACION_DESARMADA = "Atención: La alineación del equipo ha sido desarmada"

# ----- ver plantel -----
# usa las mismas que vender jugador

# ----- armar alineación -----
MSG_ALINEACION_GUARDADA = "La nueva alineación del equipo {nombre_equipo} fue guardada exitosamente"
HEADER_ARQUERO = "> ARQUERO:"
HEADER_DEFENSORES = "> DEFENSORES:"
HEADER_MEDIOCAMPISTAS = "> MEDIOCAMPISTAS:"
HEADER_DELANTEROS = "> DELANTEROS:"
HEADER_SUPLENTES = "> SUPLENTES:"
HEADER_TITULARES = "Los jugadores titulares son:"
TEMPLATE_JUGADOR = "{n}. {nombre_jugador}"
TEMPLATE_JUGADOR_POSICION = "{n}. {nombre_jugador} - [{posicion}]"
ERROR_FORMACION_INVALIDA = "Formación inválida"
MSG_CANTIDAD_JUGADORES_INSUFICIENTE = (
    "No hay suficientes jugadores disponibles para armar esta alineación"
)
ERROR_CANTIDAD_INVALIDA = "Para esta posición se necesita(n) {cantidad} jugador(es)"

# ----- ver alineación -----
TEMPLATE_ALINEACION = """La formación es: {formacion}
Los jugadores titulares son:
Delanteros: {delanteros}
Mediocampistas: {mediocampistas}
Defensores: {defensores}
Arquero: {arquero}
Capitán: {capitan}
Los suplentes son:
{suplentes}
"""
MSG_ALINEACION_INEXISTENTE = "El equipo no posee una alineación definida"

# ----- ver jugador más utilizado -----
TEMPLATE_ESTADISTICA_JUGADORES = """Arquero: {arquero}
Defensor: {defensor}
Mediocampista: {mediocampista}
Delantero: {delantero}
"""
MSG_NO_INFORMACION = "No hay información suficiente para mostrar estadísticas"

# TP3:

PRESUPUESTO_INICIAL = 6_000_000

# ----- prompts -----
PROMPT_RUTA = "Ingrese una ruta: "

# ----- procesar / importar / exportar -----
ERROR_IMPORTACION = "El/los archivos a importar deben existir y ser CSV válidos"
ERROR_EXPORTACION = "Error al exportar el archivo"
MSG_OK = "OK {cant}"
MSG_OK_FECHAS = "OK {cant_fechas} {cant_eventos}"
JUGADOR_DUPLICADO = (
    "El jugador {nombre_jugador} ya fue procesado con posición {posicion}"
)

# ----- headers CSV exportados -----
HEADER_CSV_EXPORTAR_JUGADORES = "nombre_jugador,posicion,precio"
HEADER_CSV_EXPORTAR_FECHAS = "fecha_partido,evento,detalle_evento,nombre_jugador,lado"

# ----- headers CSV crudos (para el parser) -----
HEADER_CSV_JUGADORES = (
    "player_id,version,full_name,height_cm,weight_kg,dob,positions,"
    "overall_rating,potential,preferred_foot,weak_foot,skill_moves,"
    "international_reputation,club_id,club_name,club_league_id,"
    "club_league_name,club_rating,crossing,finishing,heading_accuracy,"
    "short_passing,volleys,dribbling,curve,freekick_accuracy,long_passing,"
    "ball_control,acceleration,sprint_speed,agility,reactions,balance,"
    "shot_power,jumping,stamina,strength,long_shots,aggression,"
    "interceptions,positioning,vision,penalties,composure,marking,"
    "standing_tackle,sliding_tackle"
)

HEADER_CSV_FECHAS = (
    "id_equipo_local,nombre_equipo_local,id_equipo_visitante,"
    "nombre_equipo_visitante,id_partido,fecha_partido,liga,evento,"
    "detalle_evento,minuto,minuto_alargue,equipo_evento,"
    "nombre_equipo_evento,lado_evento,nombre_jugador,fecha_dt,player_id"
)

# ----- jugar fechas -----
ERROR_SIN_JUGADORES = "No hay jugadores cargados en el sistema"
MSG_SIN_EQUIPOS_FECHAS = "Necesitas al menos 1 equipo para procesar la/s fecha/s"
TEMPLATE_PUNTAJE_EQUIPO = "{nombre_equipo}: {puntaje} pts"

# ----- puntajes de eventos -----
PTS_GOL_A_FAVOR = 25
PTS_GOL_EN_CONTRA = -25
PTS_PENAL_CONVERTIDO = 25
PTS_ASISTENCIA = 10
PTS_AMARILLA = -2
PTS_ROJA = -5
PTS_GOL_VISITANTE = 50
PTS_DESPEJE = 1
PTS_ATAJADA_EXITOSA = 1
