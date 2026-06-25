"""
KONG ARGENTINO - ESCALERA
"""
import pygame
import random
import math
from config import *

class Escalera(pygame.sprite.Sprite):
    def __init__(self, x, y, alto, gestor):
        super().__init__()
        self.gestor = gestor
        self.alto_visual = alto
        self.x_visual = x
        self.y_visual = y
        det_x = x - 8
        det_ancho = 32
        det_y = y - 10
        det_alto = alto + 20
        self.rect_deteccion = pygame.Rect(det_x, det_y, det_ancho, det_alto)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (40, 30, 20, 60), (self.x_visual + 2, self.y_visual + 4, 16, self.alto_visual))
        for i in range(0, self.alto_visual, 12):
            pygame.draw.rect(pantalla, (150, 100, 60), (self.x_visual - 2, self.y_visual + i, 20, 2))
            pygame.draw.rect(pantalla, (200, 150, 100), (self.x_visual - 2, self.y_visual + i, 20, 1))
        pygame.draw.rect(pantalla, (101, 67, 33), (self.x_visual - 2, self.y_visual, 4, self.alto_visual))
        pygame.draw.rect(pantalla, (101, 67, 33), (self.x_visual + 14, self.y_visual, 4, self.alto_visual))
        pygame.draw.rect(pantalla, (130, 90, 50), (self.x_visual - 2, self.y_visual, 4, 3))
        pygame.draw.rect(pantalla, (130, 90, 50), (self.x_visual + 14, self.y_visual, 4, 3))
        for i in range(0, self.alto_visual, 12):
            pygame.draw.rect(pantalla, (120, 80, 40), (self.x_visual, self.y_visual + i, 16, 3))
            pygame.draw.rect(pantalla, (160, 110, 60), (self.x_visual, self.y_visual + i, 16, 1))


