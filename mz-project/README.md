# El Incal: Clase R (Demo) — Esqueleto de proyecto RPG Maker MZ

Este directorio contiene los **datos del proyecto** (`data/*.json`) para el demo
descrito en `../docs/diseno-demo-el-incal.md`. No incluye el motor de RPG Maker
MZ (`js/rmmz_*.js`, `index.html`) ni los gráficos/audio del RTP, porque son
archivos propios del software con licencia — los genera automáticamente el
propio programa al crear un proyecto nuevo.

## Qué contiene `data/`

| Archivo | Contenido |
|---|---|
| `System.json` | Título, switches, moneda, términos en español, punto de inicio (Mapa 1). |
| `Actors.json` | John Difool (Actor 1), usando gráficos placeholder `Actor1` del RTP. |
| `Classes.json`, `Skills.json`, `States.json`, `Weapons.json`, `Armors.json`, `Enemies.json`, `Troops.json`, `Animations.json`, `CommonEvents.json` | Stubs mínimos válidos (el demo no tiene combate; están para que la base de datos no quede rota). |
| `Items.json` | Objetos de trama: "Linterna" y "El Incal" (ítems clave). |
| `Tilesets.json` | Un tileset placeholder **sin imágenes asignadas** (`tilesetNames` vacío) — hay que asignarlo tú en el editor. |
| `MapInfos.json`, `Map001.json`–`Map004.json` | Los 4 mapas del demo, con los eventos, diálogos y lógica de la sección 6 del documento de diseño ya implementados como comandos de evento reales. |

## Qué implementan los mapas

1. **Mapa 1 — Cuarto de Difool:** evento autorun de introducción (Difool/Deepo) y
   evento de puerta que dispara la irrupción y transfiere al Mapa 2.
2. **Mapa 2 — Túneles del Subsuelo:** el Agente patrulla (Move Route personalizado)
   y atrapa al jugador por "Event Touch" devolviéndolo al punto de entrada; la
   Vecina da la Linterna la primera vez; el evento de salida transfiere al Mapa 3.
3. **Mapa 3 — El Pozo:** cinemática autorun (Tint Screen + texto ambiental) que
   transfiere automáticamente al Mapa 4.
4. **Mapa 4 — Cámara del Incal:** evento final con el ítem "El Incal", tinte a
   blanco, mensaje de cierre y fundido a negro.

Todo el flujo de switches, diálogos y transferencias **ya funciona** en cuanto
lo cargues en el editor. Lo que falta es **arte**: los mapas tienen su capa de
tiles en blanco (0) a propósito, para no asumir nombres de archivos de tileset
que no existen en tu instalación.

## Cómo integrarlo (5 minutos)

1. Abre RPG Maker MZ → **Nuevo Proyecto**. Dale el nombre que prefieras (p. ej. `ElIncalDemo`). Esto genera automáticamente `js/`, `img/`, `audio/`, `index.html` y un `data/` con la base de datos por defecto.
2. Cierra el proyecto en el editor (para que no sobrescriba tus archivos al guardar).
3. **Reemplaza** la carpeta `data/` de tu proyecto nuevo por la carpeta `data/` de este directorio (haz una copia de seguridad de la original antes, por si acaso).
4. Vuelve a abrir el proyecto en RPG Maker MZ.
5. En la base de datos (F9) → pestaña **Tilesets**, asigna un tileset del RTP (o tuyo) a "Tileset Subsuelo (placeholder)" y ajusta los flags de paso si hace falta.
6. Abre cada mapa (Mapa 1 a 4) y pinta los tiles de suelo/paredes con el tileset ya asignado — ahora mismo están vacíos.
7. Juega con F5. El flujo narrativo (diálogos, patrulla, transferencias, final) ya debería funcionar de principio a fin.

## Notas y límites conocidos

- **Sin arte propio de "El Incal":** los personajes usan los sprites/retratos
  `Actor1` genéricos del RTP como marcador de posición. Sustitúyelos por arte
  propio inspirado en la estética (no copies viñetas del cómic).
- **Sin sonido:** no se incluyeron comandos de música/SE porque preferí no
  adivinar nombres de pista; los puntos naturales para añadir `Play BGM` /
  `Play SE` están marcados con comentarios (`108`/`408`) en los eventos de
  Mapa 3 y Mapa 4.
- **Sigilo simplificado:** el Agente usa detección por colisión directa
  ("Event Touch"), no un cono de visión real. Es una base funcional; si
  luego quieres un sigilo más elaborado, se puede sumar un plugin JS.
- **Base de datos de combate:** Classes/Skills/States son válidos pero no
  están balanceados — el demo no incluye batallas.
- `gen_mz_project.py` es el script Python que generó estos JSON; puedes
  editarlo y volver a ejecutarlo (`python3 gen_mz_project.py`) si quieres
  regenerar los archivos tras cambiar textos, mapas o switches.
