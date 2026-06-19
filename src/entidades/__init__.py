# src/entidades/__init__.py
"""
KONG ARGENTINO - Entidades del Juego
"""
from .jugador import Argentino, BorrachoIA
from .objetos import (
    Plataforma, Escalera, BarrilCerveza,
    PoderMate, Princesa, KongCervecero, HinchaBorrachito
)
from .particulas import SistemaParticulas, TextoFlotante
from .hincha_argentina import HinchaArgentina
from .hincha_viejo import HinchaViejoTambor   # <--- NUEVO
from .hinchas_extra import (
    HinchaBorrachin,
    HinchaRandom,
    HinchaConBengala,
    HinchaGemelos,
    HinchaAbuela,
)