"""
KONG ARGENTINO - HinchaAbuela
"""
import math
import random
import pygame
from constantes import COLORES
from .base_hincha_extra import _BaseHinchaExtra

class HinchaAbuela(_BaseHinchaExtra):
    nombre_hincha = "Hincha Abuela"
    etiqueta_puntos = "🥘 +30 (Abuela)"
    puntos_barril = 30

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = 34
        self.rect.height = 46
        self.color_remera = (145, 95, 165)
        self.color_franja = (215, 190, 230)
        self.color_pantalon = (70, 60, 90)
        self.color_piel = (245, 215, 190)
        self.textos_canto = [
            "Traje la cacerola",
            "Vamos mis nietos",
            "La copa se queda",
        ]

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        if self.gestor.sistema_particulas and self.anim_frame % 12 == 0 and random.random() < 0.4:
            self.gestor.sistema_particulas.emitir(
                self.rect.centerx + random.randint(-6, 6),
                self.rect.top,
                COLORES['blanco'],
                1,
                'estrella',
            )

    def dibujar(self, pantalla):
        super().dibujar(pantalla)
        x, y = self.rect.x, self.rect.y + self.offset_y

        # Convertir sprite base en abuela: pelo canoso, chal, falda, cacerola.
        pygame.draw.rect(pantalla, (180, 140, 200), (x + 2, y + 12, 28, 7), border_radius=3)
        pygame.draw.rect(pantalla, (120, 80, 145), (x + 5, y + 26, 22, 16), border_radius=4)
        pygame.draw.circle(pantalla, (215, 215, 215), (x + 16, y + 2), 7)
        pygame.draw.circle(pantalla, (180, 180, 180), (x + 23, y + 5), 4)
        pygame.draw.circle(pantalla, COLORES['gris'], (x + 4, y + 24), 6)
        pygame.draw.circle(pantalla, (200, 200, 200), (x + 4, y + 24), 3)
        pygame.draw.line(pantalla, COLORES['marron_claro'], (x + 11, y + 20), (x + 18, y + 9), 2)
        pygame.draw.circle(pantalla, COLORES['marron_claro'], (x + 18, y + 9), 2)
        pygame.draw.line(pantalla, (130, 90, 55), (x + 28, y + 14), (x + 28, y + 37), 2)
        pygame.draw.arc(pantalla, (130, 90, 55), (x + 25, y + 11, 6, 6), math.pi / 2, math.pi * 1.6, 2)
        if self.anim_frame % 20 < 10:
            pygame.draw.circle(pantalla, COLORES['amarillo'], (x + 4, y + 24), 2)
