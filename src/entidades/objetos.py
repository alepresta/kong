"""
KONG ARGENTINO - objetos.py (re-exportación)
Cada clase tiene su propio archivo.
"""
from .plataforma import Plataforma
from .escalera import Escalera
from .barril_cerveza import BarrilCerveza
from .poder_mate import PoderMate
from .princesa import Princesa
from .kong import KongCervecero  # noqa (kong importa barril_cerveza, no objetos)
from .hincha_borrachito import HinchaBorrachito

__all__ = ['Plataforma', 'Escalera', 'BarrilCerveza', 'PoderMate',
           'Princesa', 'KongCervecero', 'HinchaBorrachito']
