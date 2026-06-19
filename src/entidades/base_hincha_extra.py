"""
KONG ARGENTINO - BASE HINCHA EXTRA
"""
import math
import random
import pygame
from constantes import COLORES
from .hincha_borrachito import HinchaBorrachito

class _BaseHinchaExtra(HinchaBorrachito):
    nombre_hincha = "Hincha"
    etiqueta_puntos = "🍺 +30 (Hincha)"
    puntos_barril = 30

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = 32
        self.rect.height = 40
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
        if hasattr(self, 'nivel_borrachera') and random.random() < 0.01:
            self.nivel_borrachera = min(10, self.nivel_borrachera + 1)
        if not self.gritando and self.anim_frame % 150 == 0 and random.random() < 0.6:
            self.gritando = True
            self.tiempo_texto = 60
            self.texto_grito = random.choice(self.textos_canto)

    def recibir_golpe(self):
        return super().recibir_golpe()

    def _dibujar_cuerpo_base(self, pantalla, x, y, remera=None, franja=None, pantalon=None, piel=None, radio=8):
        remera = remera or self.color_remera
        franja = franja or self.color_franja
        pantalon = pantalon or self.color_pantalon
        piel = piel or self.color_piel
        paso = int(math.sin(self.anim_frame * 0.25) * 2)

        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 24, 8)
        pygame.draw.rect(pantalla, remera, (x + 2, y + 12, 16, 18), border_radius=3)
        pygame.draw.rect(pantalla, COLORES['blanco'], (x + 2, y + 16, 16, 4))
        pygame.draw.rect(pantalla, franja, (x + 2, y + 20, 16, 3))
        pygame.draw.circle(pantalla, piel, (x + 10, y + 8), radio)
        pygame.draw.rect(pantalla, pantalon, (x + 4 + paso, y + 30, 4, 8))
        pygame.draw.rect(pantalla, pantalon, (x + 12 - paso, y + 30, 4, 8))

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

    def dibujar(self, pantalla):
        # Mantener el estilo visual del HinchaBorrachito original del juego.
        super().dibujar(pantalla)
        x, y = self.rect.x, self.rect.y + self.offset_y
        self._dibujar_bandera_argentina(pantalla, x, y, lado=self.direccion)


