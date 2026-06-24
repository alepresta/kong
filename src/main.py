"""Entrada web para ejecutar KONG ARGENTINO en navegador (pygbag)."""
# IMPORTANTE: pygbag analiza el archivo de entrada para decidir que cargar.
# Importar pygame aqui (nivel superior) hace que pygbag inicialice el modulo
# pygame real (con init/sprite/font/mixer); sin esto queda un stub vacio.
# NOTA: NO importar numpy aqui. El wheel pyodide de numpy rompe el driver de
# video SDL en wasm ("video driver did not add any displays"); los sonidos se
# generan en Python puro (ver sonidos.py).
import pygame  # noqa: F401
import asyncio
import traceback


def _log(msg):
    """Envia un mensaje a la consola del navegador (Chrome DevTools)."""
    print(msg)
    try:
        import platform
        platform.window.console.log("[KONG] " + str(msg))
    except Exception:
        pass


def _err(msg):
    """Envia un error a la consola del navegador (Chrome DevTools)."""
    print(msg)
    try:
        import platform
        platform.window.console.error("[KONG] " + str(msg))
    except Exception:
        pass


async def main():
    _log("== INICIO main() ==")
    try:
        _log("Importando KongArgentino...")
        from juego.main import KongArgentino
        _log("Import OK. Creando instancia (init + crear_nivel)...")
        juego = KongArgentino()
        _log("Instancia creada OK. Estado inicial: " + str(getattr(juego, "estado", "?")))
        _log("Entrando al bucle run_web()...")
        await juego.run_web()
        _log("run_web() finalizo normalmente.")
    except Exception as e:
        _err("EXCEPCION EN ARRANQUE: " + repr(e))
        _err(traceback.format_exc())
        raise


if __name__ == "__main__":
    asyncio.run(main())
