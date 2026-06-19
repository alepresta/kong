"""
KONG ARGENTINO - hinchas_extra.py (re-exportación)
Cada personaje ahora tiene su propio archivo.
"""
from .base_hincha_extra import _BaseHinchaExtra
from .hincha_borrachin import HinchaBorrachin
from .hincha_random import HinchaRandom
from .hincha_con_bengala import HinchaConBengala
from .hincha_gemelos import HinchaGemelos
from .hincha_abuela import HinchaAbuela

__all__ = [
    '_BaseHinchaExtra',
    'HinchaBorrachin',
    'HinchaRandom',
    'HinchaConBengala',
    'HinchaGemelos',
    'HinchaAbuela',
]
