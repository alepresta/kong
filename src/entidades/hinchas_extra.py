"""
KONG ARGENTINO - HINCHAS EXTRA
Variantes adicionales de hinchada para completar el roster del diseno.
"""

import math
import random
import pygame

from constantes import COLORES
from .objetos import HinchaBorrachito


class _BaseHinchaExtra(HinchaBorrachito):
    nombre_hincha = "Hincha"
    etiqueta_puntos = "🍺 +30 (Hincha)"
    puntos_barril = 30

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.textos_canto = [
            "Vamo' Argentina",
            "Messi, Messi",
            "La copa esta en casa",
        ]

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        if not self.gritando and self.anim_frame % 240 == 0 and random.random() < 0.35:
            self.gritando = True
            self.tiempo_texto = 50
            self.texto_grito = random.choice(self.textos_canto)

    def recibir_golpe(self):
        return super().recibir_golpe()


class HinchaBorrachin(_BaseHinchaExtra):
    nombre_hincha = "Hincha Borrachin"
    etiqueta_puntos = "🍻 +35 (Borrachin)"
    puntos_barril = 35

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.nivel_borrachera = random.randint(7, 9)
        self.textos_canto = [
            "No veo nada, pero vamos",
            "Messi te amo",
            "La copa, la copa",
        ]


class HinchaRandom(_BaseHinchaExtra):
    nombre_hincha = "Hincha Random"
    etiqueta_puntos = "🎲 +25 (Random)"
    puntos_barril = 25

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.color_remera = random.choice([
            COLORES['celeste'],
            COLORES['azul'],
            COLORES['blanco'],
        ])

    def dibujar(self, pantalla):
        super().dibujar(pantalla)
        x, y = self.rect.x, self.rect.y + self.offset_y
        pygame.draw.rect(pantalla, self.color_remera, (x + 6, y + 18, 20, 8), 2)


class HinchaConBengala(_BaseHinchaExtra):
    nombre_hincha = "Hincha Con Bengala"
    etiqueta_puntos = "🔥 +35 (Bengala)"
    puntos_barril = 35

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.textos_canto = [
            "Bengala y carnaval",
            "Argentina nomas",
            "Dale campeon",
        ]

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        if self.gestor.sistema_particulas and self.anim_frame % 6 == 0:
            self.gestor.sistema_particulas.emitir(
                self.rect.centerx + 12,
                self.rect.top - 5,
                random.choice([COLORES['naranja'], COLORES['rojo'], COLORES['amarillo']]),
                1,
                'chispa',
            )

    def dibujar(self, pantalla):
        super().dibujar(pantalla)
        x, y = self.rect.x, self.rect.y + self.offset_y
        pygame.draw.line(pantalla, (180, 180, 180), (x + 30, y + 10), (x + 34, y - 4), 2)
        pygame.draw.circle(pantalla, COLORES['naranja'], (x + 34, y - 4), 4)


class HinchaGemelos(_BaseHinchaExtra):
    nombre_hincha = "Hincha Gemelos"
    etiqueta_puntos = "👫 +40 (Gemelos)"
    puntos_barril = 40

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = 20
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
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx + 2, by + 12, 16, 18))
            pygame.draw.rect(pantalla, COLORES['blanco'], (bx + 2, by + 18, 16, 4))
            pygame.draw.circle(pantalla, (255, 220, 200), (bx + 10, by + 8), 8)
            pygame.draw.rect(pantalla, (30, 60, 140), (bx + 4, by + 30, 4, 8))
            pygame.draw.rect(pantalla, (30, 60, 140), (bx + 12, by + 30, 4, 8))
        if self.gritando and self.tiempo_texto > 0:
            cx = (self.rect.centerx + self.rect_derecho.centerx) // 2
            cy = min(y, y2) - 24
            self.gestor.dibujar_texto(pantalla, self.texto_grito, 14, COLORES['amarillo'], cx, cy, centro=True)


class HinchaAbuela(_BaseHinchaExtra):
    nombre_hincha = "Hincha Abuela"
    etiqueta_puntos = "🥘 +30 (Abuela)"
    puntos_barril = 30

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
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
        pygame.draw.circle(pantalla, COLORES['gris'], (x + 6, y + 22), 6)
        pygame.draw.line(pantalla, COLORES['marron_claro'], (x + 12, y + 20), (x + 16, y + 10), 2)
        if self.anim_frame % 20 < 10:
            pygame.draw.circle(pantalla, COLORES['amarillo'], (x + 6, y + 22), 2)
