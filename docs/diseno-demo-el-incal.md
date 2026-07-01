# Demo "El Incal" — Documento de Diseño Narrativo
### Adaptación no comercial para RPG Maker VX Ace

> Nota sobre derechos: *El Incal* es una obra de Alejandro Jodorowsky (guion) y Jean Giraud "Mœbius" (dibujo), publicada originalmente por Les Humanoïdes Associés. Este documento es una **adaptación de fan, sin fines comerciales**, pensada como ejercicio de diseño de juego. No incluye ni reproduce arte, texto o assets originales del cómic: todo el material visual (tilesets, sprites, ilustraciones) deberá crearse desde cero o encargarse a artistas, inspirándose libremente en la estética sin copiar viñetas. Si en algún momento se plantea distribuir el demo públicamente, conviene revisar la política de fan-works y, si hace falta, contactar a los titulares de derechos.

---

## 1. Visión del proyecto

Un demo corto (20–40 minutos de juego) que adapta el **arranque de "La Casta de los Metabarones"... perdón, de *El Incal*: Clase R"**: la caída de John Difool desde el Suelo Oficial hasta el Subsuelo de Terra-21, su encuentro con el Incal, y su huida de la Tecno-Tecnocracia y de los Berg. El objetivo del demo es transmitir el tono del cómic (sci-fi psicodélica, sátira burocrática, misticismo) usando los sistemas nativos de RPG Maker VX Ace: exploración top-down, diálogos con retratos, eventos con interruptores/variables y alguna mecánica ligera de sigilo/huida en vez de combate tradicional.

**Pilares de diseño:**
- **Narrativa por encima del combate.** El demo prioriza diálogo, exploración y decisiones pequeñas sobre peleas.
- **Verticalidad social como level design.** Terra-21 está estratificada en niveles (Clase R en el fondo, burócratas y aristócratas arriba); el mapa del demo debe reflejar esa jerarquía aunque sea en 2D top-down.
- **Tono agridulce y absurdo.** Humor negro burocrático + momentos de asombro cósmico (el Incal).

---

## 2. Alcance del demo

Cubre el equivalente al **Capítulo 1 de "La Casta de los Meta-Barones"**... corrección: al **arco inicial del tomo 1 de El Incal**:

1. **Prólogo — Piso 0, cuarto de Difool.** Introducción del personaje, su vida como detective clase R degradado, tono de miseria burocrática.
2. **La persecución.** Agentes de la Tecno-Tecnocracia (o los Berg) irrumpen buscando el objeto que Difool robó sin saberlo: el **Incal Oscuro** (o una primera visión del Incal de Luz, a elección narrativa).
3. **La caída.** Secuencia de huida vertical: Difool cae por el "pozo" de Terra-21, pasando brevemente por distintos estratos sociales (transición de mapas con distinto tono visual).
4. **El encuentro con el Incal.** Escena clave: el objeto se activa, primera visión mística, gancho para "continuará" (fin del demo).

El demo **no** incluye: sistema de combate por turnos (se puede omitir o reducir a una única secuencia de "huida" sin batalla formal), subida de nivel, ni el resto de la trama (Animah, Aghora, los Meta-Barones, etc.) — quedan para una hipotética Parte 2.

---

## 3. Personajes del demo

| Personaje | Rol | Notas de diseño |
|---|---|---|
| **John Difool** | Protagonista jugable | Detective Clase R degradado. Cobarde, cínico, con chispazos de lucidez. Retrato con expresión "cansado/sarcástico" por defecto. |
| **Deepo** | Compañero (loro-consciencia) | Comenta la acción, sirve de exposición y humor. Puede implementarse como *event* que sigue al jugador (Follower) con diálogos aleatorios. |
| **El Incal** | MacGuffin / entidad | No es un personaje jugable; es un ítem de evento clave que al final del demo cobra "vida" (cambia de sprite/brillo, dispara la escena final). |
| **Agente Tecno** (genérico) | Antagonista menor | Enemigo tipo "patrulla" que persigue a Difool en la secuencia de huida; su detección activa un *game over* narrativo o reinicio del tramo, no una batalla. |
| **Vecina del piso 0** | NPC de color | Da una pista/objeto opcional y ambienta la miseria del subsuelo. |

---

## 4. Mundo y ambientación (mapas del demo)

Terra-21 se representa como una **torre invertida de estratos**, del suelo miserable (abajo) al lujo aristocrático (arriba). Para el demo usamos 4 mapas conectados verticalmente:

1. **Mapa 1 — Cuarto de Difool (Piso 0, Subsuelo).**
   Interior pequeño, cutre, iluminación verdosa/amarillenta. Objetos interactivos: cama, terminal de mensajes, ventana con vista a los túneles.
2. **Mapa 2 — Pasillo/Túneles del Subsuelo.**
   Zona de sigilo: el jugador debe evitar la línea de visión de una patrulla mientras huye hacia el pozo de ventilación.
3. **Mapa 3 — El Pozo (secuencia de caída).**
   Mapa vertical "de paso", con scroll y eventos automáticos que muestran fragmentos de los otros estratos sociales (comerciantes, sacerdotes tecnócratas, aristócratas) como *parallax* o mapas de fondo breves — más cinemática que jugable.
4. **Mapa 4 — Fondo del Pozo / Cámara del Incal.**
   Escenario onírico/luminoso, contraste fuerte con los mapas anteriores. Aquí ocurre el clímax y el corte a negro final ("Fin de la demo — Continuará").

---

## 5. Sistemas y mecánicas (a nivel de diseño, sin código)

- **Diálogo con retratos:** usar el sistema estándar de *Show Text* con *faces* para Difool, Deepo y NPCs. Mantener frases cortas, ritmo tipo cómic (viñeta a viñeta).
- **Sigilo ligero (Mapa 2):** un evento "Agente" con *Move Route* en patrulla; un *Region* o *Switch* detecta si Difool entra en su campo de visión (puede simularse con un evento invisible que compruebe la posición relativa cada pocos frames). Si detecta al jugador → teletransporta a un punto de reinicio del tramo con una línea de diálogo ("Casi te atrapan...").
- **Caída/cinemática (Mapa 3):** secuencia de eventos automáticos (autorun), sin control del jugador, con *Scroll Map*, cambios de tinte de pantalla (*Tint Screen*) por cada estrato que se atraviesa, y texto ambiental breve.
- **Objeto de trama (Incal):** ítem gestionado por *Switch* global; en el Mapa 4 su recolección dispara la cinemática final (animación, cambio de música, mensaje de cierre).
- **Sin menú de combate:** el *Party* puede limitarse a Difool en solitario; el menú de batalla y las bases de datos de armas/enemigos no son necesarias para el demo, salvo un enemigo "decorativo" para la secuencia de sigilo si se prefiere mostrar un *Game Over* real en vez de reinicio silencioso.

*(Si más adelante quieres los scripts RGSS3 para el sigilo, el tinte progresivo o un sistema de diálogo estilizado tipo cómic, lo armamos en una pasada aparte — quedó fuera del alcance de este documento a petición tuya.)*

---

## 6. Guion escena por escena (borrador)

**Escena 1 — Cuarto de Difool**
> *(Difool, tumbado, mirando el techo)*
> **Difool:** Otro día en el paraíso... si por paraíso entendemos una lata de conservas con vistas al pozo.
> **Deepo:** *(desde su percha)* Squawk. Deberías levantarte. Debes dinero. Otra vez.
> **Difool:** Deepo, cállate o te vendo por piezas.

*(El jugador explora el cuarto; puede examinar 2-3 objetos con líneas de color. Un ruido en la puerta dispara la Escena 2.)*

**Escena 2 — Irrupción**
> *(Golpes en la puerta. Difool se sobresalta.)*
> **Voz (Agente):** ¡Tecno-Tecnocracia! ¡Abra en nombre del Orden Administrativo!
> **Difool:** *(para sí)* No he hecho nada... esta semana.

*(Transición automática al Mapa 2. Comienza la secuencia de sigilo.)*

**Escena 3 — Huida por los túneles**
> Jugable: el jugador guía a Difool evitando al Agente hasta el pozo de ventilación.
> Diálogo opcional con la Vecina: pista sobre un atajo, o un objeto (linterna) que ilumina el Mapa 4 más adelante.

**Escena 4 — La caída (cinemática)**
> Autorun: Difool cae por el pozo. Fragmentos visuales de los estratos sociales pasan a los lados (tintes de pantalla distintos: rojo institucional, dorado aristocrático, gris industrial). Deepo comenta cada uno con una línea sarcástica.

**Escena 5 — El Incal**
> *(Difool aterriza, aturdido, en un espacio luminoso. Un objeto extraño flota/brilla: el Incal.)*
> **Difool:** ¿Qué... qué es esto?
> **Deepo:** *(en voz baja, por primera vez sin sarcasmo)* Eso, Difool, es una pregunta que va a cambiarte la vida.

*(Fade to white/negro. Texto: "FIN DE LA DEMO — El Incal continuará." Música de cierre.)*

---

## 7. Tono visual y de audio (referencias, no assets)

- **Paleta subsuelo:** verdes sucios, amarillos institucionales, sombras duras — evocar burocracia decadente sin copiar el trazo de Mœbius.
- **Paleta cámara del Incal:** blancos, dorados, violetas — contraste deliberado con el resto del demo.
- **Música:** ambient/sintetizador retro-futurista para el subsuelo; un tema etéreo/coral para la escena final.
- **SFX:** pasos metálicos, alarmas burocráticas (sirenas suaves, no alarmas de acción), silencio total en la cámara del Incal antes del clímax.

---

## 8. Próximos pasos sugeridos

1. Crear el proyecto nuevo en RPG Maker VX Ace (`Archivo → Nuevo Proyecto`).
2. Montar los 4 mapas descritos en la sección 4 con los tilesets por defecto (o custom, respetando la paleta de la sección 7).
3. Dar de alta a Difool como Actor 1 (sin clase de combate relevante) y a Deepo como Event-follower.
4. Implementar la Escena 1 y 2 con eventos de página condicionada por Switches.
5. Implementar el tramo de sigilo del Mapa 2 (puede empezar como versión simplificada: un solo camino con un evento de patrulla).
6. Implementar la cinemática del Mapa 3 (autorun, Tint Screen, Scroll Map).
7. Cerrar con la Escena 5 en el Mapa 4 y la pantalla de fin de demo.
8. (Opcional, fuera de este documento) Pedir los scripts RGSS3 para pulir sigilo, transiciones y el "despertar" del Incal.

---

*Este documento cubre el diseño narrativo solicitado. Cuando quieras avanzar con el guion de eventos en formato copiable para el editor, los scripts RGSS3, o el plan detallado de mapas/tilesets, dímelo y lo preparamos como siguiente entrega.*
