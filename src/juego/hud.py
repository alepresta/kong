# src/juego/hud.py
"""KONG ARGENTINO - HUD (heads-up display)"""
import pygame
import sys
import os
import random
import math
import pickle
from config import *

class HudMixin:
    def dibujar_hud(self):
        hud = pygame.Surface((ANCHO, 70), pygame.SRCALPHA)
        for i in range(70):
            alpha = 185 - i * 2
            pygame.draw.line(hud, (0, 0, 0, max(0, alpha)), (0, i), (ANCHO, i))
        self.pantalla.blit(hud, (0, 0))
        pygame.draw.line(self.pantalla, COLORES['oro'], (0, 69), (ANCHO, 69), 2)

        self.gestor.dibujar_texto(self.pantalla, f"PUNTOS: {self.puntuacion:06d}", 26,
                                   COLORES['amarillo'], 15, 8, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"NIVEL: {self.nivel}", 24,
                                   COLORES['blanco'], 15, 38, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"MEJOR: {self.high_score:06d}", 20,
                                   COLORES['oro'], ANCHO//2, 10, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"JUGADOR: {self.nombre_jugador}", 16,
                       COLORES['celeste'], ANCHO//2 + 210, 12, sombra=True)

        for i in range(min(self.argentino.vidas, 9)):
            self.gestor.dibujar_corazon(self.pantalla, 30 + i * 34, ALTO - 30)

        self.gestor.dibujar_texto(self.pantalla, "ESPACIO: Atacar (↑↓←→)  [ ]: Volumen", 13,
                                   COLORES['gris'], ANCHO//2 - 150, ALTO - 22)

        if self.argentino.tiene_poder:
            t_seg = (self.argentino.tiempo_poder // FPS) + 1
            pct = self.argentino.tiempo_poder / TIEMPO_PODER
            col = COLORES['verde'] if pct > 0.3 else COLORES['rojo']
            if pct < 0.2 and (self._frame_global // 8) % 2 == 0:
                self.gestor.reproducir_sonido('poder_acabando')
            self.gestor.dibujar_texto(self.pantalla, f"🧉 MATE {t_seg}s", 22, col,
                                       ANCHO - 152, 8, sombra=True)
            ancho_b = int(130 * pct)
            pygame.draw.rect(self.pantalla, COLORES['negro'], (ANCHO-152, 38, 130, 14))
            pygame.draw.rect(self.pantalla, COLORES['verde_oscuro'], (ANCHO-150, 40, 126, 10))
            pygame.draw.rect(self.pantalla, col, (ANCHO-150, 40, ancho_b, 10))
            pygame.draw.rect(self.pantalla, COLORES['blanco'], (ANCHO-152, 38, 130, 14), 2)

        if self.argentino.combo >= 2:
            colores_combo = [COLORES['amarillo'], COLORES['naranja'], 
                             COLORES['rojo'], COLORES['violeta'], COLORES['oro']]
            col = colores_combo[min(self.argentino.combo - 2, 4)]
            tam = 28 + int(math.sin(self._frame_global * 0.3) * 3)
            self.gestor.dibujar_texto(self.pantalla, f"🔥 COMBO x{self.argentino.combo}! 🔥", tam,
                                       col, ANCHO//2, 36, centro=True, sombra=True)

        if self.borracho.nivel_borrachera > 0:
            bx = ANCHO - 170
            self.gestor.dibujar_texto(self.pantalla, "🍺 BORRACHERA:", 14, COLORES['blanco'], 
                                      bx, ALTO - 50)
            ab = int(90 * self.borracho.nivel_borrachera / 10)
            pygame.draw.rect(self.pantalla, COLORES['negro'], (bx, ALTO - 32, 90, 12))
            col_b = COLORES['verde'] if self.borracho.nivel_borrachera < 5 else COLORES['rojo']
            pygame.draw.rect(self.pantalla, col_b, (bx, ALTO - 32, ab, 12))
            pygame.draw.rect(self.pantalla, COLORES['blanco'], (bx, ALTO - 32, 90, 12), 1)

        if self.hincha and self.hincha.nivel_borrachera > 0:
            bx = ANCHO - 170
            self.gestor.dibujar_texto(self.pantalla, "🍺 HINCHA:", 14, COLORES['blanco'], 
                                      bx, ALTO - 20)
            ab = int(90 * self.hincha.nivel_borrachera / 10)
            pygame.draw.rect(self.pantalla, COLORES['negro'], (bx, ALTO - 2, 90, 12))
            col_b = COLORES['verde'] if self.hincha.nivel_borrachera < 6 else COLORES['naranja']
            pygame.draw.rect(self.pantalla, col_b, (bx, ALTO - 2, ab, 12))
            pygame.draw.rect(self.pantalla, COLORES['blanco'], (bx, ALTO - 2, 90, 12), 1)

        self.gestor.dibujar_texto(self.pantalla, NOMBRE_JUEGO, 13, COLORES['gris_oscuro'], 
                                  ANCHO-142, ALTO-18)

    # ──────────────────────── DIBUJAR ────────────────────────────── #

