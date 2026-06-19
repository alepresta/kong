"""
KONG ARGENTINO - HinchaGemelos
"""
import math
import random
import pygame
from constantes import COLORES
from .base_hincha_extra import _BaseHinchaExtra

class HinchaGemelos(_BaseHinchaExtra):
    nombre_hincha = "Hincha Gemelos"
    etiqueta_puntos = "👫 +40 (Gemelos)"
    puntos_barril = 40

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = 20
        self.rect.height = 40
        self.rect_derecho = pygame.Rect(x + 20, y, 20, self.rect.height)
        self._offset_gemelo = 20
        self.textos_canto = [
            "Cantamos los dos",
            "Dale dale dale",
            "Messi Messi",
        ]

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        bamboleo = int(math.sin(self.anim_frame * 0.22) * 2)
        self.rect_derecho.x = self.rect.x + self._offset_gemelo + bamboleo
        self.rect_derecho.y = self.rect.y

    def iter_rects(self):
        return [self.rect, self.rect_derecho]

    def beber_barril(self):
        super().beber_barril()
        self.nivel_borrachera = min(10, self.nivel_borrachera + 1)

    def recibir_golpe(self):
        self.estado = "golpeado"
        self.tiempo_estado = 75
        self.vel_x = random.choice([-3, -2, 2, 3])
        self.nivel_borrachera = max(0, self.nivel_borrachera - 1)
        self.gritando = True
        self.tiempo_texto = 35
        self.texto_grito = "¡AU, LOS GEMELOS!"
        return False

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y + self.offset_y
        x2, y2 = self.rect_derecho.x, self.rect_derecho.y + self.offset_y
        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 24, 8)
        self.gestor.dibujar_sombra(pantalla, self.rect_derecho.centerx, self.rect_derecho.bottom, 24, 8)
        for bx, by in ((x, y), (x2, y2)):
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx + 2, by + 12, 16, 18), border_radius=3)
            pygame.draw.rect(pantalla, COLORES['blanco'], (bx + 2, by + 16, 16, 4))
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx + 2, by + 20, 16, 3))
            pygame.draw.circle(pantalla, (255, 220, 200), (bx + 10, by + 8), 8)
            pygame.draw.rect(pantalla, (30, 60, 140), (bx + 4, by + 30, 4, 8))
            pygame.draw.rect(pantalla, (30, 60, 140), (bx + 12, by + 30, 4, 8))
            pygame.draw.circle(pantalla, (35, 35, 55), (bx + 7, by + 8), 1)
            pygame.draw.circle(pantalla, (35, 35, 55), (bx + 13, by + 8), 1)
            pygame.draw.arc(pantalla, (160, 60, 60), (bx + 7, by + 10, 6, 4), 0, math.pi, 1)
        self._dibujar_bandera_argentina(pantalla, x2, y2, lado=1)
        if self.gritando and self.tiempo_texto > 0:
            cx = (self.rect.centerx + self.rect_derecho.centerx) // 2
            cy = min(y, y2) - 24
            self.gestor.dibujar_texto(pantalla, self.texto_grito, 14, COLORES['amarillo'], cx, cy, centro=True)


