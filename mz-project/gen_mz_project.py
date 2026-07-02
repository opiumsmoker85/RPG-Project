import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True)


def dump(name, obj):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def end_list():
    return [{"code": 0, "indent": 0, "parameters": []}]


def cmd(code, params, indent=0):
    return {"code": code, "indent": indent, "parameters": params}


def show_text_block(lines, face_name="", face_index=0, background=0, position=2, indent=0):
    out = [cmd(101, [face_name, face_index, background, position], indent)]
    for line in lines:
        out.append(cmd(401, [line], indent))
    return out


def control_switch(switch_id, value_on=True, indent=0):
    # value: 0 = ON, 1 = OFF
    v = 0 if value_on else 1
    return cmd(121, [switch_id, switch_id, v], indent)


def transfer(map_id, x, y, direction=2, fade=0, indent=0):
    return cmd(201, [0, map_id, x, y, direction, fade], indent)


def wait(frames, indent=0):
    return cmd(230, [frames], indent)


def tint(r, g, b, gray, duration, wait_flag=True, indent=0):
    return cmd(223, [[r, g, b, gray], duration, wait_flag], indent)


def fadeout(indent=0):
    return cmd(221, [], indent)


def fadein(indent=0):
    return cmd(222, [], indent)


def comment_block(lines, indent=0):
    out = [cmd(108, [lines[0]], indent)]
    for line in lines[1:]:
        out.append(cmd(408, [line], indent))
    return out


def blank_page(trigger=0, condition=None, list_commands=None, move_type=0,
               move_route=None, image=None, priority=1, through=False,
               direction_fix=False, move_freq=3, move_speed=3):
    if condition is None:
        condition = {
            "actorId": 1, "actorValid": False,
            "itemId": 1, "itemValid": False,
            "selfSwitchCh": "A", "selfSwitchValid": False,
            "switch1Id": 1, "switch1Valid": False,
            "switch2Id": 1, "switch2Valid": False,
            "variableId": 1, "variableValid": False, "variableValue": 0
        }
    if image is None:
        image = {"characterName": "", "characterIndex": 0, "direction": 2, "pattern": 0, "tileId": 0}
    if move_route is None:
        move_route = {"list": end_list(), "repeat": True, "skippable": False, "wait": False}
    if list_commands is None:
        list_commands = []
    return {
        "conditions": condition,
        "directionFix": direction_fix,
        "image": image,
        "list": list_commands + end_list(),
        "moveFrequency": move_freq,
        "moveRoute": move_route,
        "moveSpeed": move_speed,
        "moveType": move_type,
        "priorityType": priority,
        "stepAnime": False,
        "through": through,
        "trigger": trigger,
        "walkAnime": True,
    }


def switch_cond(switch_id, valid=True):
    return {
        "actorId": 1, "actorValid": False,
        "itemId": 1, "itemValid": False,
        "selfSwitchCh": "A", "selfSwitchValid": False,
        "switch1Id": switch_id, "switch1Valid": valid,
        "switch2Id": 1, "switch2Valid": False,
        "variableId": 1, "variableValid": False, "variableValue": 0
    }


def move_cmd(code, params=None):
    return {"code": code, "parameters": params or []}


# Move-route op codes (Game_Character.ROUTE_*)
MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP = 1, 2, 3, 4
TURN_DOWN, TURN_LEFT, TURN_RIGHT, TURN_UP = 16, 17, 18, 19
ROUTE_WAIT = 15


def event(id_, name, x, y, note, pages):
    return {"id": id_, "name": name, "note": note, "x": x, "y": y, "pages": pages}


# ---------------------------------------------------------------------------
# Switches / Variables (defined inside System.json)
# ---------------------------------------------------------------------------

SWITCHES = [
    "",  # 0 unused
    "Intro_Vista",          # 1
    "Puerta_Forzada",       # 2 -> jugador puede pasar a Mapa 2
    "Tiene_Linterna",       # 3
    "Salio_Del_Subsuelo",   # 4 -> jugador puede caer al pozo (Mapa 3)
    "Incal_Activado",       # 5
]

VARIABLES = [""]  # sin variables numéricas por ahora

# ---------------------------------------------------------------------------
# System.json
# ---------------------------------------------------------------------------

system = {
    "gameTitle": "El Incal: Clase R (Demo)",
    "versionId": 1,
    "locale": "es_ES",
    "windowTone": [0, 0, 0, 0],
    "battleBgm": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
    "battleback1Name": "",
    "battleback2Name": "",
    "battlerHue": 0,
    "battlerName": "",
    "currencyUnit": "créditos",
    "defeatMe": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
    "editMapId": 1,
    "elements": ["", "Físico"],
    "equipTypes": ["", "Arma", "Escudo", "Cabeza", "Cuerpo", "Accesorio"],
    "gameoverMe": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
    "optDisplayTp": False,
    "optDrawTitle": True,
    "optExtraExp": False,
    "optFloorDeath": False,
    "optFollowers": True,
    "optSideView": False,
    "optSlipDeath": False,
    "optTransparent": False,
    "partyMembers": [1],
    "skillTypes": ["", "Magia", "Especial"],
    "sounds": [
        {"name": "", "pan": 0, "pitch": 100, "volume": 90} for _ in range(24)
    ],
    "startMapId": 1,
    "startX": 4,
    "startY": 3,
    "switches": SWITCHES,
    "terms": {
        "basic": ["Nv", "HP", "HP", "MP", "MP", "TP", "TP", "EXP", "EXP"],
        "commands": [
            "Luchar", "Huir", "Atacar", "Defender", "Objetos", "Habilidades",
            "Equipo", "Estado", "Formación", "Guardar", "Salir del juego",
            "Opciones", "Peso", None, None, "Usar", "Equipar", "Quitar",
            "Cambiar", None, None, "Nueva Partida", "Continuar", None,
            "Ir a Título", "Cancelar", None, None, "Comprar", "Vender"
        ],
        "params": ["PV máx", "PM máx", "Ataque", "Defensa", "M.Ataque", "M.Defensa", "Agilidad", "Suerte"],
        "messages": {
            "actionFailure": "¡No tuvo efecto en %1!",
            "actorDamage": "%1 sufrió %2 de daño.",
            "actorDrain": "%1 le robó %2 %3 a %4.",
            "actorGain": "%1 recuperó %2 %3.",
            "actorLoss": "%1 perdió %2 %3.",
            "actorNoDamage": "%1 no sufrió daño.",
            "actorNoHit": "¡Fallo! %1 no sufrió daño.",
            "alwaysDash": "Correr siempre",
            "bgmVolume": "Volumen de BGM",
            "bgsVolume": "Volumen de BGS",
            "buffAdd": "¡El %2 de %1 subió!",
            "commandRemember": "Recordar comandos",
            "counterAttack": "¡%1 contraatacó!",
            "criticalToActor": "¡Un golpe crítico!",
            "criticalToEnemy": "¡Un golpe crítico!",
            "debuffAdd": "¡El %2 de %1 bajó!",
            "defeat": "%1 fue derrotado.",
            "emerge": "¡%1 apareció!",
            "enemyDamage": "%1 sufrió %2 de daño.",
            "enemyDrain": "%1 le robó %2 %3 a %4.",
            "enemyGain": "%1 recuperó %2 %3.",
            "enemyLoss": "%1 perdió %2 %3.",
            "enemyNoDamage": "%1 no sufrió daño.",
            "enemyNoHit": "¡Fallo! %1 no sufrió daño.",
            "escapeFailure": "¡Pero no pudo escapar!",
            "escapeStart": "¡%1 empieza a huir!",
            "evasion": "¡%1 esquivó el ataque!",
            "expNext": "hasta el siguiente %1",
            "expTotal": "%1 actual",
            "obtainExp": "¡%1 ganó %2 %3!",
            "obtainGold": "¡%1\\G encontrados!",
            "obtainItem": "¡%1 obtenido!",
            "obtainSkill": "¡%1 aprendió %2!",
            "levelUp": "¡%1 subió a %2 %3!",
            "loadMessage": "Cargar qué partida?",
            "magicEvasion": "¡%1 esquivó el ataque mágico!",
            "magicReflection": "¡%1 reflejó el ataque!",
            "commandRemember2": "",
            "partyName": "%1",
            "possession": "Posesión",
            "preemptive": "¡%1 se adelantó!",
            "saveMessage": "Guardar en qué partida?",
            "showingMessage": "",
            "substitute": "¡%1 protegió a %2!",
            "surprise": "¡%1 fue sorprendido!",
            "useItem": "%1 usó %2.",
            "victory": "¡%1 ganó la batalla!"
        }
    },
    "testBattlers": [],
    "testTroopId": 0,
    "title1Name": "",
    "title2Name": "",
    "titleBgm": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
    "variables": VARIABLES,
    "versionId": 1,
    "victoryMe": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
    "windowTone2": [0, 0, 0, 0],
    "armorTypes": ["", "General"],
    "weaponTypes": ["", "General"],
    "attackMotions": [{"type": 0, "weaponImageId": 0}],
}

dump("System.json", system)

# ---------------------------------------------------------------------------
# Actors / Classes / Skills / States / Items / Weapons / Armors / Enemies / Troops
# ---------------------------------------------------------------------------

actors = [None, {
    "id": 1,
    "battlerName": "",
    "characterIndex": 0,
    "characterName": "Actor1",
    "classId": 1,
    "equips": [0, 0, 0, 0, 0],
    "traits": [],
    "faceIndex": 0,
    "faceName": "Actor1",
    "initialLevel": 1,
    "maxLevel": 99,
    "name": "John Difool",
    "nickname": "Detective Clase R",
    "note": "",
    "profile": "Un detective degradado que sobrevive en el Subsuelo de Terra-21."
}]
dump("Actors.json", actors)


def param_table():
    # 8 params x 100 levels (index 0..99), crecimiento lineal simple.
    base = [250, 20, 15, 15, 12, 12, 12, 10]
    growth = [12, 1, 1, 1, 1, 1, 1, 1]
    table = []
    for p in range(8):
        row = [base[p] + growth[p] * lvl for lvl in range(100)]
        table.append(row)
    return table


classes = [None, {
    "id": 1,
    "expParams": [30, 20, 30, 30],
    "traits": [],
    "learnings": [],
    "name": "Detective",
    "note": "",
    "params": param_table()
}]
dump("Classes.json", classes)

skills = [None,
    {
        "id": 1, "animationId": 1, "damage": {"critical": False, "elementId": 0, "formula": "a.atk * 4 - b.def * 2", "type": 1, "variance": 20},
        "description": "", "effects": [], "hitType": 1, "iconIndex": 0, "message1": " ataca.", "message2": "",
        "mpCost": 0, "name": "Ataque", "note": "", "occasion": 1, "repeats": 1, "requiredWtypeId1": 0, "requiredWtypeId2": 0,
        "scope": 1, "speed": 0, "stypeId": 1, "successRate": 100, "tpCost": 0, "tpGain": 0
    },
    {
        "id": 2, "animationId": 0, "damage": {"critical": False, "elementId": 0, "formula": "0", "type": 0, "variance": 20},
        "description": "", "effects": [{"code": 39, "dataId": 0, "value1": 0, "value2": 0}], "hitType": 0, "iconIndex": 0,
        "message1": " se defiende.", "message2": "", "mpCost": 0, "name": "Defender", "note": "", "occasion": 1, "repeats": 1,
        "requiredWtypeId1": 0, "requiredWtypeId2": 0, "scope": 11, "speed": 2000, "stypeId": 0, "successRate": 100, "tpCost": 0, "tpGain": 0
    }
]
dump("Skills.json", skills)

states = [None, {
    "id": 1, "autoRemovalTiming": 0, "chanceByDamage": 100, "iconIndex": 1, "maxTurns": 1, "message1": " ha caído.",
    "message2": "", "message3": "", "message4": " se recupera.", "messageType": 1, "minTurns": 1, "motion": 3,
    "name": "K.O.", "note": "", "overlay": 0, "priority": 100, "removeAtBattleEnd": False, "removeByDamage": False,
    "removeByRestriction": False, "removeByWalking": False, "restriction": 4, "stepsToRemove": 100, "traits": [
        {"code": 14, "dataId": 4, "value": 0}
    ]
}]
dump("States.json", states)

weapons = [None]
dump("Weapons.json", weapons)

armors = [None]
dump("Armors.json", armors)

items = [None,
    {
        "id": 1, "animationId": 0, "consumable": False, "damage": {"critical": False, "elementId": 0, "formula": "0", "type": 0, "variance": 20},
        "description": "Ilumina los rincones más oscuros del Subsuelo.", "effects": [], "hitType": 0, "iconIndex": 178,
        "itypeId": 2, "name": "Linterna", "note": "", "occasion": 0, "price": 0, "repeats": 1, "scope": 0, "speed": 0,
        "successRate": 100, "tpGain": 0
    },
    {
        "id": 2, "animationId": 0, "consumable": False, "damage": {"critical": False, "elementId": 0, "formula": "0", "type": 0, "variance": 20},
        "description": "Un objeto de luz viva que parece observarte.", "effects": [], "hitType": 0, "iconIndex": 87,
        "itypeId": 2, "name": "El Incal", "note": "", "occasion": 0, "price": 0, "repeats": 1, "scope": 0, "speed": 0,
        "successRate": 100, "tpGain": 0
    }
]
dump("Items.json", items)

enemies = [None]
dump("Enemies.json", enemies)

troops = [None]
dump("Troops.json", troops)

animations = [None]
dump("Animations.json", animations)

tilesets = [None, {
    "id": 1, "flags": [0] * 2048, "mode": 1, "name": "Tileset Subsuelo (placeholder)", "note": "",
    "tilesetNames": ["", "", "", "", "", "", "", ""]
}]
dump("Tilesets.json", tilesets)

common_events = [None]
dump("CommonEvents.json", common_events)

# ---------------------------------------------------------------------------
# Maps
# ---------------------------------------------------------------------------

def base_map(name, width, height, tileset_id, note, events):
    return {
        "autoplayBgm": False, "autoplayBgs": False, "battleback1Name": "", "battleback2Name": "",
        "bgm": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
        "bgs": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
        "disableDashing": False, "displayName": name, "encounterList": [], "encounterStep": 30,
        "height": height, "note": note, "parallaxLoopX": False, "parallaxLoopY": False, "parallaxName": "",
        "parallaxShow": True, "parallaxSx": 0, "parallaxSy": 0, "scrollType": 0, "specifyBattleback": False,
        "tilesetId": tileset_id, "width": width, "data": [0] * (width * height * 6), "events": events
    }


# ---- Map 1: Cuarto de Difool -------------------------------------------
w1, h1 = 9, 7

ev_intro = event(1, "Intro", 4, 3, "", [
    blank_page(
        trigger=3,  # autorun (página sin condición: es la que se usa la primera vez)
        list_commands=(
            show_text_block([
                "Otro día en el paraíso... si por paraíso entendemos",
                "una lata de conservas con vistas al pozo."
            ]) +
            show_text_block([
                "Squawk. Deberías levantarte. Debes dinero. Otra vez."
            ], face_index=0) +
            show_text_block([
                "Deepo, cállate o te vendo por piezas."
            ]) +
            [control_switch(1, True)]
        )
    ),
    blank_page(
        trigger=0,  # página inactiva una vez visto el intro (evita el bucle de autorun)
        condition=switch_cond(1, valid=True),
        list_commands=[]
    )
])

ev_puerta = event(2, "Puerta", 4, 1, "", [
    blank_page(
        trigger=3,
        condition=switch_cond(2, valid=False),
        move_type=0,
        list_commands=[]
    ),
    blank_page(
        trigger=0,  # action button, sólo activo tras la intro
        condition=switch_cond(1, valid=True),
        list_commands=(
            [cmd(108, ["Golpes en la puerta."], 0)] +
            show_text_block([
                "¡Tecno-Tecnocracia! ¡Abra en nombre",
                "del Orden Administrativo!"
            ]) +
            show_text_block([
                "No he hecho nada... esta semana."
            ]) +
            [control_switch(2, True), fadeout(), wait(20),
             transfer(2, 8, 11, 8, 0), fadein()]
        )
    )
])

ev_terminal = event(3, "Terminal", 2, 2, "", [
    blank_page(
        trigger=0,
        list_commands=show_text_block([
            "Terminal de mensajes: 14 avisos de deuda sin leer."
        ])
    )
])

ev_cama = event(4, "Cama", 6, 2, "", [
    blank_page(
        trigger=0,
        list_commands=show_text_block([
            "Una cama que ha visto días mejores. Como tú."
        ])
    )
])

map1 = base_map("Cuarto de Difool", w1, h1, 1,
                 "Mapa 1 - Prólogo. Ver docs/diseno-demo-el-incal.md, Escena 1-2.",
                 [ev_intro, ev_puerta, ev_terminal, ev_cama])

# ---- Map 2: Túneles del Subsuelo ----------------------------------------
w2, h2 = 17, 13

ev_agente = event(1, "Agente", 8, 6, "Patrulla vertical; toca al jugador -> lo atrapa.", [
    blank_page(
        trigger=2,  # event touch
        move_type=3,  # custom
        priority=1,
        move_freq=3,
        move_speed=3,
        move_route={
            "list": [
                move_cmd(MOVE_DOWN), move_cmd(MOVE_DOWN), move_cmd(MOVE_DOWN),
                move_cmd(ROUTE_WAIT, [30]),
                move_cmd(MOVE_UP), move_cmd(MOVE_UP), move_cmd(MOVE_UP),
                move_cmd(ROUTE_WAIT, [30]),
            ] + end_list(),
            "repeat": True, "skippable": True, "wait": False
        },
        list_commands=(
            show_text_block([
                "¡Alto! ¡Casi te atrapan!"
            ]) +
            [fadeout(), wait(15), transfer(2, 2, 11, 8, 0), fadein()]
        )
    )
])

ev_vecina = event(2, "Vecina", 3, 9, "", [
    blank_page(
        trigger=0,
        condition=switch_cond(3, valid=False),
        list_commands=(
            show_text_block([
                "Toma. Te va a hacer falta más que a mí.",
                "Y ten cuidado con las patrullas."
            ]) +
            [cmd(126, [1, 0, 1, 1]), control_switch(3, True)]
        )
    ),
    blank_page(
        trigger=0,
        condition=switch_cond(3, valid=True),
        list_commands=show_text_block([
            "Corre. No mires atrás."
        ])
    )
])

ev_salida = event(3, "Pozo de ventilación", 15, 1, "", [
    blank_page(
        trigger=1,  # player touch
        list_commands=(
            show_text_block([
                "Difool se arroja al pozo de ventilación..."
            ]) +
            [control_switch(4, True), fadeout(), wait(20),
             transfer(3, 4, 18, 8, 0), fadein()]
        )
    )
])

map2 = base_map("Túneles del Subsuelo", w2, h2, 1,
                 "Mapa 2 - Sigilo. Ver docs/diseno-demo-el-incal.md, Escena 3.",
                 [ev_agente, ev_vecina, ev_salida])

# ---- Map 3: El Pozo (cinemática de caída) --------------------------------
w3, h3 = 9, 20

ev_caida = event(1, "Caida", 4, 19, "", [
    blank_page(
        trigger=3,  # autorun
        condition=switch_cond(4, valid=True),
        list_commands=(
            [comment_block(["Cinemática de caída: recorre los estratos de Terra-21."])[0]] +
            [tint(80, 0, 0, 0, 20, True)] +
            show_text_block(["Un piso de burócratas grises los mira caer sin inmutarse."]) +
            [tint(0, 80, 0, 0, 20, True)] +
            show_text_block(["Más abajo, comerciantes gritan precios a nadie."]) +
            [tint(0, 0, 80, 0, 20, True)] +
            show_text_block(["Deepo comenta cada estrato con desprecio profesional."]) +
            [tint(0, 0, 0, 0, 30, True), fadeout(), wait(20),
             transfer(4, 4, 6, 2, 0), fadein()]
        )
    )
])

map3 = base_map("El Pozo", w3, h3, 1,
                 "Mapa 3 - Cinemática de caída. Ver docs/diseno-demo-el-incal.md, Escena 4.",
                 [ev_caida])

# ---- Map 4: Cámara del Incal ---------------------------------------------
w4, h4 = 9, 9

ev_incal = event(1, "El Incal", 4, 4, "", [
    blank_page(
        trigger=0,  # action button (página sin condición: se usa antes del clímax)
        list_commands=(
            show_text_block(["¿Qué... qué es esto?"]) +
            show_text_block([
                "Eso, Difool, es una pregunta",
                "que va a cambiarte la vida."
            ]) +
            [control_switch(5, True), cmd(126, [2, 0, 1, 1]),
             tint(255, 255, 255, 0, 60, True), wait(40),
             comment_block(["FIN DE LA DEMO - El Incal continuará."])[0],
             fadeout(), wait(60)]
        )
    ),
    blank_page(
        trigger=0,  # tras el clímax, ya no se puede repetir la escena
        condition=switch_cond(5, valid=True),
        list_commands=[]
    )
])

map4 = base_map("Cámara del Incal", w4, h4, 1,
                 "Mapa 4 - Clímax. Ver docs/diseno-demo-el-incal.md, Escena 5.",
                 [ev_incal])

dump("Map001.json", map1)
dump("Map002.json", map2)
dump("Map003.json", map3)
dump("Map004.json", map4)

map_infos = [
    None,
    {"id": 1, "expanded": False, "name": "Cuarto de Difool", "order": 1, "parentId": 0, "scrollX": 0, "scrollY": 0},
    {"id": 2, "expanded": False, "name": "Túneles del Subsuelo", "order": 2, "parentId": 0, "scrollX": 0, "scrollY": 0},
    {"id": 3, "expanded": False, "name": "El Pozo", "order": 3, "parentId": 0, "scrollX": 0, "scrollY": 0},
    {"id": 4, "expanded": False, "name": "Cámara del Incal", "order": 4, "parentId": 0, "scrollX": 0, "scrollY": 0},
]
dump("MapInfos.json", map_infos)

print("OK - archivos generados en", OUT)
for f in sorted(os.listdir(OUT)):
    print(" -", f)
