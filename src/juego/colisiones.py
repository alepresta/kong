# src/juego/colisiones.py
"""KONG ARGENTINO - Lógica de colisiones y ataques"""
import pygame
import sys
import os
import random
import math
import pickle
from config import *

class ColisionesMixin:
    def _golpear_kong(self):
        self.gestor.iniciar_shake(10, 4)
        self.gestor.iniciar_flash((255, 200, 50), 6)
        self.emitir(self.kong.rect.centerx, self.kong.rect.centery,
                    COLORES['oro'], 20, 'explosion')
        self.gestor.reproducir_sonido('golpe')
        self.kong.tiempo_enojado = max(self.kong.tiempo_enojado, 40)
        self._otorgar_puntos(100, self.kong.rect.centerx, self.kong.rect.top,
                             COLORES['oro'], texto="👊 ¡GOLPE A KONG! +100")
        self.texto_flotante("💢 ¡KONG ENOJADO!", self.kong.rect.centerx, 
                            self.kong.rect.top - 20, COLORES['rojo'], 24)

    def _golpear_borracho(self):
        self.emitir(self.borracho.rect.centerx, self.borracho.rect.centery,
                    COLORES['amarillo'], 15, 'golpe')
        self.gestor.reproducir_sonido('golpe')
        self.borracho.nivel_borrachera = max(0, self.borracho.nivel_borrachera - 2)
        self.borracho.estado = "buscando"
        self.borracho.tiempo_estado = 30
        self._otorgar_puntos(30, self.borracho.rect.centerx, self.borracho.rect.top,
                             COLORES['celeste'], texto="👊 ¡GOLPE AL BORRACHO! +30")
        if self.borracho.nivel_borrachera >= 6:
            self.borracho.vel_x = random.choice([-4, -3, 3, 4])
            self.borracho.vel_y = -3
            self.texto_flotante("🍺 ¡BORRACHO TAMBALEANDO!", 
                               self.borracho.rect.centerx, 
                               self.borracho.rect.top - 20, 
                               COLORES['naranja'], 20)

    def _golpear_hincha(self, hincha_obj):
        hx, hy, htop = hincha_obj.rect.centerx, hincha_obj.rect.centery, hincha_obj.rect.top
        if hasattr(hincha_obj, 'recibir_golpe'):
            hincha_obj.recibir_golpe()
        elif hasattr(hincha_obj, 'nivel_borrachera'):
            hincha_obj.nivel_borrachera = max(0, hincha_obj.nivel_borrachera - 1)
        self.emitir(hx, hy, COLORES['rojo'], 15, 'golpe')
        self.emitir(hx, hy, COLORES['amarillo'], 8, 'chispa')
        self.gestor.reproducir_sonido('hincha_golpe')
        self._otorgar_puntos(30, hx, htop, COLORES['celeste'], 
                             texto="👊 ¡GOLPE AL HINCHA! +30")
        if getattr(hincha_obj, 'nivel_borrachera', 0) >= 7:
            self.texto_flotante("🍺 ¡HINCHA RE BORRACHO!", hx, htop - 20,
                               COLORES['naranja'], 20)

    def _iter_hincha_rects(self, hincha_obj):
        if hasattr(hincha_obj, 'iter_rects'):
            return hincha_obj.iter_rects()
        return [hincha_obj.rect]

    def _hincha_colisiona_rect(self, hincha_obj, rect):
        for hrect in self._iter_hincha_rects(hincha_obj):
            if hrect.colliderect(rect):
                return True
        return False

    # ──────────────────────── HUD ────────────────────────────────── #

