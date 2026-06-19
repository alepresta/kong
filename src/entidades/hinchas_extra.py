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
        pygame.draw.rect(pantalla, remera, (x + 2, y + 12, 16, 18), border_radius=3)
        pygame.draw.rect(pantalla, COLORES['blanco'], (x + 2, y + 16, 16, 4))
        pygame.draw.rect(pantalla, franja, (x + 2, y + 20, 16, 3))
        pygame.draw.circle(pantalla, piel, (x + 10, y + 8), radio)
        pygame.draw.rect(pantalla, pantalon, (x + 4, y + 30, 4, 8))
        pygame.draw.rect(pantalla, pantalon, (x + 12, y + 30, 4, 8))

        self._dibujar_rostro(pantalla, x, y)
        self._dibujar_bandera_argentina(pantalla, x, y)

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

    def _dibujar_rostro(self, pantalla, x, y):
        pygame.draw.circle(pantalla, (35, 35, 55), (x + 7, y + 8), 1)
        pygame.draw.circle(pantalla, (35, 35, 55), (x + 13, y + 8), 1)
        pygame.draw.line(pantalla, (60, 35, 25), (x + 5, y + 6), (x + 8, y + 5), 1)
        pygame.draw.line(pantalla, (60, 35, 25), (x + 12, y + 5), (x + 15, y + 6), 1)
        pygame.draw.arc(pantalla, (160, 60, 60), (x + 7, y + 10, 6, 4), 0, math.pi, 1)

    def _dibujar_bandera_argentina(self, pantalla, x, y, lado=1):
        asta_x = x + (19 if lado >= 0 else 1)
        asta_y = y + 8
        pygame.draw.line(pantalla, (170, 140, 90), (asta_x, asta_y), (asta_x, asta_y + 15), 2)

        flag_w = 10
        dir_mult = 1 if lado >= 0 else -1
        bx = asta_x + dir_mult
        by = asta_y + 1
        if lado >= 0:
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx, by, flag_w, 2))
            pygame.draw.rect(pantalla, COLORES['blanco'], (bx, by + 2, flag_w, 2))
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx, by + 4, flag_w, 2))
            pygame.draw.circle(pantalla, COLORES['amarillo'], (bx + 5, by + 3), 1)
        else:
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx - flag_w, by, flag_w, 2))
            pygame.draw.rect(pantalla, COLORES['blanco'], (bx - flag_w, by + 2, flag_w, 2))
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx - flag_w, by + 4, flag_w, 2))
            pygame.draw.circle(pantalla, COLORES['amarillo'], (bx - 5, by + 3), 1)


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
        self.color_remera = (70, 130, 170)
        self.color_franja = COLORES['blanco']
        self.color_pantalon = (35, 35, 55)
        self._arrodillado = False
        self.textos_canto = [
            "Bengala y carnaval",
            "Argentina nomas",
            "Dale campeon",
        ]

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        self._arrodillado = (self.anim_frame // 24) % 2 == 0
        if self.gestor.sistema_particulas and self.anim_frame % 6 == 0:
            origen_y = self.rect.top + (8 if self._arrodillado else -5)
            self.gestor.sistema_particulas.emitir(
                self.rect.centerx + 14,
                origen_y,
                random.choice([COLORES['naranja'], COLORES['rojo'], COLORES['amarillo']]),
                1,
                'chispa',
            )

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y + self.offset_y
        if self._arrodillado:
            y += 6

        glow = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 120, 0, 70), (18, 18), 18)
        pantalla.blit(glow, (x + 16, y - 20))
        self._dibujar_cuerpo_base(pantalla, x, y)

        # Rastas
        for i in range(6):
            dx = -2 + i * 3
            largo = 7 + (i % 2)
            pygame.draw.line(pantalla, (45, 28, 20), (x + 6 + dx, y + 2), (x + 5 + dx, y + 2 + largo), 2)

        # Posicion de arrodillado para lanzar bengala.
        if self._arrodillado:
            pygame.draw.rect(pantalla, self.color_pantalon, (x + 3, y + 31, 8, 5), border_radius=2)
            pygame.draw.rect(pantalla, self.color_pantalon, (x + 12, y + 31, 7, 4), border_radius=2)

        pygame.draw.line(pantalla, (180, 180, 180), (x + 18, y + 18), (x + 30, y + 10), 2)
        pygame.draw.circle(pantalla, COLORES['naranja'], (x + 32, y + 9), 4)
        pygame.draw.circle(pantalla, COLORES['amarillo'], (x + 32, y + 9), 2)
        pygame.draw.line(pantalla, (255, 140, 0), (x + 32, y + 9), (x + 37, y + 4), 1)
        pygame.draw.line(pantalla, (255, 220, 120), (x + 32, y + 9), (x + 38, y + 9), 1)


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
        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 24, 8)

        # Falda larga y poncho de abuela.
        pygame.draw.rect(pantalla, (120, 80, 145), (x + 3, y + 16, 14, 20), border_radius=4)
        pygame.draw.rect(pantalla, COLORES['blanco'], (x + 3, y + 21, 14, 3))
        pygame.draw.rect(pantalla, (185, 140, 200), (x + 1, y + 13, 18, 7), border_radius=4)

        # Cabeza y pelo canoso (rodete).
        pygame.draw.circle(pantalla, self.color_piel, (x + 10, y + 8), 7)
        pygame.draw.circle(pantalla, (215, 215, 215), (x + 10, y + 1), 5)
        pygame.draw.circle(pantalla, (180, 180, 180), (x + 15, y + 3), 3)
        pygame.draw.circle(pantalla, (35, 35, 55), (x + 8, y + 8), 1)
        pygame.draw.circle(pantalla, (35, 35, 55), (x + 12, y + 8), 1)
        pygame.draw.arc(pantalla, (140, 60, 70), (x + 7, y + 10, 6, 4), 0, math.pi, 1)

        # Cacerola y cuchara bien visibles.
        pygame.draw.circle(pantalla, COLORES['gris'], (x + 5, y + 24), 6)
        pygame.draw.circle(pantalla, (200, 200, 200), (x + 5, y + 24), 3)
        pygame.draw.line(pantalla, COLORES['marron_claro'], (x + 12, y + 21), (x + 18, y + 9), 2)
        pygame.draw.circle(pantalla, COLORES['marron_claro'], (x + 18, y + 9), 2)

        self._dibujar_bandera_argentina(pantalla, x, y, lado=-1)
        if self.anim_frame % 20 < 10:
            pygame.draw.circle(pantalla, COLORES['amarillo'], (x + 6, y + 22), 2)
