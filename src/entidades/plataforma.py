"""
KONG ARGENTINO - PLATAFORMA
"""
import pygame
import random
import math
from constantes import *

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, gestor):
        super().__init__()
        self.gestor = gestor
        self.ancho = ancho
        self.rect = pygame.Rect(x, y, ancho, 25)

    def dibujar(self, pantalla):
        self.gestor.dibujar_plataforma(pantalla, self.rect.x, self.rect.y, self.ancho)


