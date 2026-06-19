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
        self.color_remera = COLORES['celeste']
        self.color_franja = COLORES['blanco']
        self.color_pantalon = (30, 60, 140)
        self.color_piel = (255, 220, 200)
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

    def _dibujar_cuerpo_base(self, pantalla, x, y, remera=None, franja=None, pantalon=None, piel=None, radio=8):
        remera = remera or self.color_remera
        franja = franja or self.color_franja
        pantalon = pantalon or self.color_pantalon
        piel = piel or self.color_piel

        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 24, 8)
        pygame.draw.rect(pantalla, remera, (x + 2, y + 12, 16, 18))
        pygame.draw.rect(pantalla, franja, (x + 2, y + 18, 16, 4))
        pygame.draw.circle(pantalla, piel, (x + 10, y + 8), radio)
        pygame.draw.rect(pantalla, pantalon, (x + 4, y + 30, 4, 8))
        pygame.draw.rect(pantalla, pantalon, (x + 12, y + 30, 4, 8))

        if self.gritando and self.tiempo_texto > 0:
            self.gestor.dibujar_texto(
                pantalla,
                self.texto_grito,
                13,
                COLORES['amarillo'],
                self.rect.centerx,
                y - 22,
                centro=True,
            )


class HinchaBorrachin(_BaseHinchaExtra):
    nombre_hincha = "Hincha Borrachin"
    etiqueta_puntos = "🍻 +35 (Borrachin)"
    puntos_barril = 35

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
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
        x = self.rect.x
        y = self.rect.y + self.offset_y + int(math.sin(self.anim_frame * 0.3) * 2)
        self._dibujar_cuerpo_base(pantalla, x, y)
        pygame.draw.rect(pantalla, (120, 70, 30), (x + 15, y + 20, 6, 10), border_radius=2)
        pygame.draw.rect(pantalla, (240, 200, 120), (x + 16, y + 18, 4, 3), border_radius=1)
        pygame.draw.circle(pantalla, (220, 90, 90), (x + 7, y + 8), 1)
        pygame.draw.circle(pantalla, (220, 90, 90), (x + 13, y + 8), 1)


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
            COLORES['rojo'],
            COLORES['naranja'],
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
        x, y = self.rect.x, self.rect.y + self.offset_y
        self._dibujar_cuerpo_base(
            pantalla,
            x,
            y,
            remera=self.color_remera,
            franja=COLORES['blanco'],
            pantalon=self.color_pantalon,
        )
        if self.accesorio == "gorra":
            pygame.draw.rect(pantalla, (40, 40, 40), (x + 4, y + 1, 12, 4), border_radius=2)
            pygame.draw.rect(pantalla, (40, 40, 40), (x + 12, y + 4, 6, 2), border_radius=1)
        elif self.accesorio == "vincha":
            pygame.draw.rect(pantalla, (255, 215, 0), (x + 3, y + 5, 14, 2))
        else:
            pygame.draw.rect(pantalla, (60, 40, 25), (x + 8, y + 11, 5, 2), border_radius=1)


class HinchaConBengala(_BaseHinchaExtra):
    nombre_hincha = "Hincha Con Bengala"
    etiqueta_puntos = "🔥 +35 (Bengala)"
    puntos_barril = 35

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.color_remera = (120, 30, 30)
        self.color_franja = (240, 180, 80)
        self.color_pantalon = (40, 30, 20)
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
        x, y = self.rect.x, self.rect.y + self.offset_y
        glow = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 120, 0, 70), (18, 18), 18)
        pantalla.blit(glow, (x + 18, y - 20))
        self._dibujar_cuerpo_base(pantalla, x, y)
        x, y = self.rect.x, self.rect.y + self.offset_y
        pygame.draw.line(pantalla, (180, 180, 180), (x + 30, y + 10), (x + 34, y - 4), 2)
        pygame.draw.circle(pantalla, COLORES['naranja'], (x + 34, y - 4), 4)
        pygame.draw.circle(pantalla, COLORES['amarillo'], (x + 34, y - 4), 2)


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
        x, y = self.rect.x, self.rect.y + self.offset_y
        self._dibujar_cuerpo_base(pantalla, x, y, radio=7)
        x, y = self.rect.x, self.rect.y + self.offset_y
        pygame.draw.circle(pantalla, (210, 210, 210), (x + 10, y + 2), 5)
        pygame.draw.circle(pantalla, (180, 180, 180), (x + 14, y + 3), 3)
        pygame.draw.rect(pantalla, (190, 150, 200), (x + 0, y + 14, 20, 8), border_radius=4)
        pygame.draw.circle(pantalla, COLORES['gris'], (x + 6, y + 22), 6)
        pygame.draw.line(pantalla, COLORES['marron_claro'], (x + 12, y + 20), (x + 16, y + 10), 2)
        if self.anim_frame % 20 < 10:
            pygame.draw.circle(pantalla, COLORES['amarillo'], (x + 6, y + 22), 2)
