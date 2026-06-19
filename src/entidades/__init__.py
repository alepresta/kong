# src/entidades/__init__.py
"""
KONG ARGENTINO - Entidades del Juego
Cada clase tiene su propio archivo.
"""
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
