"""Entrada web para ejecutar KONG ARGENTINO en navegador (pygbag)."""
import asyncio

from juego.main import KongArgentino


async def main():
    juego = KongArgentino()
    await juego.run_web()


if __name__ == "__main__":
    asyncio.run(main())
