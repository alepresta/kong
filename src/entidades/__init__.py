# src/entidades/__init__.py
"""
KONG ARGENTINO - Entidades del Juego
Cada clase tiene su propio archivo.
"""
# En escritorio "import pygame" expone pygame.sprite/font/mixer. En pygbag/wasm
# no estan disponibles, asi que: (1) se intentan importar y (2) si falta sprite
# (que solo se usa como clase base, sin Groups), se instala un shim minimo.
import pygame

for _sub in ("font", "mixer", "sprite"):
    try:
        __import__("pygame." + _sub)
    except Exception:
        pass

if not hasattr(pygame, "sprite"):
    import sys as _sys
    import types as _types
    _spr = _types.ModuleType("pygame.sprite")

    class Sprite:
        """Sprite minimo: solo lo que el juego usa (herencia + super().__init__)."""
        def __init__(self, *groups):
            self._groups = []
        def add(self, *groups):
            pass
        def remove(self, *groups):
            pass
        def kill(self):
            pass
        def groups(self):
            return []
        def alive(self):
            return True
        def update(self, *args, **kwargs):
            pass

    _spr.Sprite = Sprite
    pygame.sprite = _spr
    _sys.modules["pygame.sprite"] = _spr

# Objetos de juego
from .plataforma import Plataforma
from .escalera import Escalera
from .barril_cerveza import BarrilCerveza
from .poder_mate import PoderMate
# Personajes
from .argentino import Argentino
from .borracho_ia import BorrachoIA
from .princesa import Princesa
from .kong import KongCervecero
from .hincha_borrachito import HinchaBorrachito
from .hincha_argentina import HinchaArgentina
from .hincha_viejo import HinchaViejoTambor
from .base_hincha_extra import _BaseHinchaExtra
from .hincha_borrachin import HinchaBorrachin
from .hincha_random import HinchaRandom
from .hincha_con_bengala import HinchaConBengala
from .hincha_gemelos import HinchaGemelos
from .hincha_abuela import HinchaAbuela
# Efectos
from .sistema_particulas import SistemaParticulas
from .texto_flotante import TextoFlotante
