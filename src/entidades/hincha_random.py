"""
KONG ARGENTINO - HinchaRandom
"""
import math
import random
import pygame
from constantes import COLORES
from .base_hincha_extra import _BaseHinchaExtra

class HinchaRandom(_BaseHinchaExtra):
    nombre_hincha = "Hincha Random"
    etiqueta_puntos = "🎲 +25 (Random)"
    puntos_barril = 25

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = random.choice([30, 32, 34])
        self.rect.height = random.choice([38, 40, 42])
        self.color_remera = random.choice([
            COLORES['celeste'],
            COLORES['azul'],
            COLORES['blanco'],
        ])
        self.color_pantalon = random.choice([
            (30, 60, 140),
            (40, 40, 40),
            (70, 30, 20),
        ])
        self.accesorio = random.choice(["gorra", "vincha", "bigote"])

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        if self.anim_frame % 90 == 0 and random.random() < 0.4:
            self.direccion *= -1

    def dibujar(self, pantalla):
        super().dibujar(pantalla)
        x, y = self.rect.x, self.rect.y + self.offset_y
        # Variar remera sobre el sprite base para mantener lenguaje visual común.
        pygame.draw.rect(pantalla, self.color_remera, (x + 2, y + 14, 28, 6), border_radius=2)
        if self.accesorio == "gorra":
            pygame.draw.rect(pantalla, (40, 40, 40), (x + 8, y - 3, 16, 4), border_radius=2)
            pygame.draw.rect(pantalla, (40, 40, 40), (x + 20, y, 7, 2), border_radius=1)
        elif self.accesorio == "vincha":
            pygame.draw.rect(pantalla, (255, 215, 0), (x + 8, y + 6, 16, 2))
        else:
            pygame.draw.rect(pantalla, (60, 40, 25), (x + 14, y + 16, 6, 2), border_radius=1)


