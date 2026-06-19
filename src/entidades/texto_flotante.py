"""
KONG ARGENTINO - TEXTO FLOTANTE v2.0
"""
import pygame
import math
from constantes import COLORES, MAX_PARTICULAS

class TextoFlotante:
    def __init__(self, texto, x, y, color, tamaño=22):
        self.texto = texto
        self.x = float(x)
        self.y = float(y)
        self.y_inicio = float(y)
        self.color = color
        self.tamaño = tamaño
        self.vida = 75
        self.vida_max = 75
        self.escala = 1.3

    def update(self):
        t = 1.0 - (self.vida / self.vida_max)
        self.y = self.y_inicio - (t * t * 60)
        self.escala = max(1.0, 1.3 - t * 0.4)
        self.vida -= 1

    def dibujar(self, pantalla, gestor):
        if self.vida <= 0:
            return
        alpha = min(1.0, self.vida / (self.vida_max * 0.35)) if self.vida < self.vida_max * 0.35 else 1.0
        col = (int(self.color[0]*alpha), int(self.color[1]*alpha), int(self.color[2]*alpha))
        tam = int(self.tamaño * self.escala)
        tam = max(10, min(tam, 48))
        gestor.dibujar_texto(pantalla, self.texto, tam, col,
                             int(self.x), int(self.y), centro=True, sombra=True)
