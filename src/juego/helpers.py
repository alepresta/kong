# src/juego/helpers.py
"""KONG ARGENTINO - Helpers de partículas y textos"""
import pygame
import sys
import os
import random
import math
import pickle
from config import *
from entidades import TextoFlotante

class HelpersMixin:
    def emitir(self, x, y, color, n=10, fuente='explosion'):
        self.particulas.emitir(x, y, color, n, fuente)

    def texto_flotante(self, texto, x, y, color, tamaño=22):
        self.textos_flotantes.append(TextoFlotante(texto, x, y, color, tamaño))

    def actualizar_textos(self):
        for t in self.textos_flotantes[:]:
            t.update()
            if t.vida <= 0:
                self.textos_flotantes.remove(t)

    def dibujar_textos(self):
        for t in self.textos_flotantes:
            t.dibujar(self.pantalla, self.gestor)

    def _otorgar_puntos(self, puntos, x, y, color=None, texto=None):
        multi = max(1, self.argentino.combo)
        total = puntos * multi
        self.puntuacion += total
        lbl = texto or (f"+{total}" if multi == 1 else f"+{total} x{multi}!")
        self.texto_flotante(lbl, x, y, color or COLORES['amarillo'],
                            tamaño=18 + min(multi * 2, 10))

