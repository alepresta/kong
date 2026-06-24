# KONG ARGENTINO — Estado de la versión web (pygbag/wasm)

> Documento de continuación. Última actualización: 2026-06-24. Commit de referencia: `74eedaf`.

## 1. Objetivo y estado actual

Portar el juego (pygame) al navegador con **pygbag 0.9.3** en GitHub Codespaces, puerto **8002**.

Pedido original (3 cosas):
1. **Sonidos** → ✅ funcionando (algunos se escuchan; ver "Pendientes").
2. **Responsive** → ✅ confirmado por el usuario.
3. **Velocidad normal** (estaba en cámara lenta) → ✅ confirmado por el usuario.

Estado del usuario al cierre: *"funciona mal pero funciona, y algunos sonidos se escuchan"*. Es decir: **jugable y con audio**, pero quedan detalles por pulir.

URL pública (puerto 8002 PÚBLICO):
`https://musical-space-engine-v69xq7546rj2wg6r-8002.app.github.dev/`

## 2. Reglas / restricciones IMPORTANTES

- ❌ **NO tocar el arte ni la lógica de los personajes** en `src/entidades/*.py`. El usuario fue muy claro con esto. Solo se permiten cambios de infra/build/compatibilidad/sonido.
- 🗣️ Responder siempre en **español**.
- ❌ **NO usar `run-web.sh`** para el build final: ese script desactiva la feature `snd` (`data-os="gui"`), dejando el juego **mudo**. El build se hace **manual** (ver sección 4) para mantener `snd` activo.
- ❌ **NO usar numpy.** El wheel pyodide de numpy (12 MB) **rompe el driver de video SDL** en wasm: `pygame.error: The video driver did not add any displays`. Por eso el audio se generó en **Python puro**.

## 3. Arquitectura de la solución (qué se cambió y por qué)

### `src/main.py` — entry point web
- pygbag hace **análisis estático de los imports top-level** del archivo de entrada para decidir qué wheels precargar. Por eso `import pygame` va arriba de todo.
- **NO** importar numpy aquí (rompe el display).
- `main()` async: importa `KongArgentino`, lo instancia y hace `await juego.run_web()`. Todo dentro de try/except que loguea a la consola del navegador con `_log`/`_err` (prefijo `[KONG]`).

### `src/juego/main.py` — clase `KongArgentino`
- `_ES_WEB = sys.platform == "emscripten"`.
- **Orden de init crítico en wasm** (`__init__`): primero `pygame.init()`, **luego `display.set_mode()`**, y **después** `pygame.mixer.init()`. Si el mixer se abre antes del display, SDL rompe el driver de video.
- `_frame_step()`: en web usa `self.clock.tick()` (sin FPS) porque el navegador ya pacea a ~60fps vía `requestAnimationFrame`; usar `tick(FPS)` bloqueante producía **cámara lenta** (doble espera). Este es el fix de velocidad.
- `run_web()`: bucle async con `await asyncio.sleep(0)` por frame + logs de diagnóstico `[KONG]`.

### `src/sonidos.py` — `GeneradorSonidos` (audio en Python puro)
- **Sin numpy.** Usa `math`, `random`, `array`.
- Lee el formato real del mixer con `pygame.mixer.get_init()` (en la práctica **44100 Hz, 2 canales**) y genera a esa frecuencia. ⚠️ **No hardcodear 22050**: `pygame.mixer.Sound(buffer=...)` interpreta los bytes al formato actual del mixer; si generás a otra frecuencia, el pitch/velocidad sale mal.
- `_to_sound(mono)`: convierte muestras float [-1..1] a int16 intercalado estéreo y devuelve `pygame.mixer.Sound(buffer=arr.tobytes())`.
- Métodos generadores reescritos en Python puro (misma matemática que la versión numpy): `_tono` (sine/square/saw/triangle + envolventes fade/attack/pluck), `_ruido` (low-pass opcional), `_glissando` (fase acumulada), `_chord`. Helpers `_fade_in`/`_fade_out`.
- **Las 20 definiciones de sonidos en `_generar_todos` se conservaron EXACTAS** (frecuencias, duración, volumen, forma, envolvente). No cambiar cuáles existen ni sus parámetros.
- Log de diagnóstico: `[KONG-SND]` (`_snd_log`). Al arrancar imprime `sonidos generados: 20`.

### `src/entidades/__init__.py` — shim de `pygame.sprite`
- En pygame-ce wasm **falta `pygame.sprite`**. Se instala un `Sprite` mínimo (init/add/remove/kill/groups/alive/update) en `sys.modules`. **No romper esto.**

## 4. Flujo de build + deploy (manual, mantiene `snd`)

```bash
# 1) Build (desde src/). NO borrar build/web con rm -rf: pygbag falla al crear src.apk.
cd /workspaces/kong/src
fuser -k 8002/tcp 2>/dev/null
mkdir -p build/web
pygbag --build --ume_block 0 --width 1024 --height 768 main.py

# 2) Parche responsive — RE-APLICAR DESPUÉS DE CADA BUILD (index.html se regenera)
python3 - <<'PY'
p = "build/web/index.html"
s = open(p, encoding="utf-8").read()
a = "            width: 100%;\n            height: 100%;\n            z-index: 5;"
b = "            width: 100%;\n            height: 100%;\n            object-fit: contain;\n            z-index: 5;"
if a in s: s = s.replace(a, b); print("object-fit OK")
elif "object-fit: contain" in s: print("object-fit ya estaba")
else: print("WARN patron no encontrado")
if "background-color:powderblue;" in s:
    s = s.replace("background-color:powderblue;", "background-color:#000000;"); print("bg OK")
open(p, "w", encoding="utf-8").write(s); print("responsive listo")
PY

# 3) Servir (puerto 8002 público)
cd /workspaces/kong/src/build/web
fuser -k 8002/tcp 2>/dev/null
python3 -m http.server 8002 --bind 0.0.0.0
```

Luego en el navegador: **Ctrl+Shift+R** (recarga forzada para evitar caché).

### Test rápido headless (escritorio, sin navegador)
```bash
cd /workspaces/kong/src
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python3 -c \
  "from juego.main import KongArgentino; j=KongArgentino(); j._frame_step(); print('OK', j.estado)"
# Debe imprimir: init: modo=python-puro mixer_init=(44100,...); sonidos generados: 20; OK menu
```

## 5. Diagnóstico en el navegador (Chrome DevTools → Console)

- `[KONG] ...` → ciclo de vida del entry/juego (arranque, frames, excepciones).
- `[KONG-SND] ...` → audio. Buscar `[KONG-SND] sonidos generados: 20`.
- Features esperadas en consola al cargar: `['vtx','snd','gui']` (si aparece solo `gui`, el build salió mudo → se usó run-web.sh por error).

## 6. Pendientes / próximos pasos (orden sugerido)

1. **Investigar el "funciona mal"**: pedir al usuario detalles concretos (¿qué sonidos NO suenan? ¿glitches visuales? ¿rendimiento/lag? ¿algo del gameplay?). Sin repro concreto no avanzar a ciegas.
2. **Audio**: confirmar que los 20 sonidos suenan. Posible causa de que "algunos" no se escuchen: solapamiento de canales (`pygame.mixer` tiene 8 canales por defecto) o sonidos muy cortos/silenciosos. Revisar `reproducir()` y considerar más canales (`pygame.mixer.set_num_channels`).
3. **`reproducir_con_pitch`** actualmente ignora el pitch (solo llama a `reproducir`). Si se quiere el efecto de combo con pitch, hay que regenerar el sonido a otra frecuencia (no hay pitchshift directo con buffers).
4. **Limpiar logs de debug** `[KONG]` / `[KONG-SND]` una vez estable (en `main.py`, `juego/main.py`, `sonidos.py`).
5. **Automatizar build+parche+serve**: crear un script alternativo a `run-web.sh` que mantenga `snd` y aplique el parche responsive automáticamente.

## 7. Lecciones aprendidas (no repetir errores)

- numpy en pygbag 0.9.3 **rompe el video** → usar Python puro para audio.
- `await asyncio.sleep(0)` **no** "despierta" el registro del driver de video; no sirve como workaround del problema de numpy.
- `pygame.mixer.Sound(buffer=...)` usa el formato **actual** del mixer → generar a `get_init()[0]`.
- Abrir el mixer **antes** del `set_mode` rompe el video en wasm → display primero, audio después.
- `clock.tick(FPS)` bloqueante en web = cámara lenta → en web usar `clock.tick()` sin argumento.
- `run-web.sh` desactiva `snd` (deja el juego mudo) → build manual.
- `rm -rf build/web` antes del build hace fallar a pygbag (`src.apk` no encontrado) → usar `mkdir -p build/web`.
- El `index.html` se **regenera** en cada build → re-aplicar el parche responsive siempre.

## 8. Archivos clave

| Archivo | Rol |
|---|---|
| `src/main.py` | Entry point web (pygbag). Logs `[KONG]`. |
| `src/juego/main.py` | Clase `KongArgentino`: orden de init, `_frame_step`, `run_web`. |
| `src/sonidos.py` | Audio procedural en Python puro. Logs `[KONG-SND]`. |
| `src/entidades/__init__.py` | Shim de `pygame.sprite` para wasm. |
| `src/gestor_graficos.py` | Gráficos + `reproducir_sonido`. Fuente web. |
| `src/build/web/index.html` | Harness generado (parche responsive tras cada build). |
| `run-web.sh` | ⚠️ Desactiva `snd`. NO usar para el build final. |
