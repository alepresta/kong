"""
KONG ARGENTINO - HinchaBorrachin
"""
import math
import random
import pygame
from constantes import COLORES
from .base_hincha_extra import _BaseHinchaExtra

class HinchaBorrachin(_BaseHinchaExtra):
    nombre_hincha = "Hincha Borrachin"
    etiqueta_puntos = "🍻 +35 (Borrachin)"
    puntos_barril = 35

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = 34
        self.rect.height = 42
        self.nivel_borrachera = random.randint(7, 9)
        self.color_remera = (190, 80, 70)
        self.color_franja = (250, 190, 120)
        self.color_pantalon = (65, 35, 20)
        self.textos_canto = [
            "No veo nada, pero vamos",
            "Messi te amo",
            "La copa, la copa",
        ]

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        if self.anim_frame % 50 == 0 and random.random() < 0.6:
            self.vel_x += random.choice([-1.2, -0.8, 0.8, 1.2])
            self.vel_x = max(-3.0, min(3.0, self.vel_x))

    def dibujar(self, pantalla):
        super().dibujar(pantalla)
        x, y = self.rect.x, self.rect.y + self.offset_y
        # Botella en mano y cara colorada.
        pygame.draw.rect(pantalla, (120, 70, 30), (x + 26, y + 20, 6, 11), border_radius=2)
        pygame.draw.rect(pantalla, (240, 200, 120), (x + 27, y + 18, 4, 3), border_radius=1)
        pygame.draw.circle(pantalla, (220, 90, 90), (x + 11, y + 12), 2)
        pygame.draw.circle(pantalla, (220, 90, 90), (x + 21, y + 12), 2)


