"""
KONG ARGENTINO - PODER MATE
"""
import pygame
import random
import math
from config import *

class PoderMate(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, TAMANO_PODER[0], TAMANO_PODER[1])
        self.anim_frame = 0

    def update(self):
        self.anim_frame += 1

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y
        off = int(math.sin(self.anim_frame * 0.12) * 5)
        if self.anim_frame % 20 < 10:
            alpha = 80
            radio = 20
        else:
            alpha = 30
            radio = 14
        glow = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (0, 255, 0, alpha), (radio, radio), radio)
        pantalla.blit(glow, (x + 8 - radio, y + 8 + off - radio))
        pygame.draw.rect(pantalla, (60, 140, 60), (x + 1, y + 2 + off, 22, 20))
        pygame.draw.rect(pantalla, (80, 180, 80), (x + 3, y + 4 + off, 18, 16))
        pygame.draw.rect(pantalla, (100, 200, 100), (x + 4, y + 5 + off, 16, 6))
        pygame.draw.ellipse(pantalla, (150, 100, 50), (x + 6, y + off, 12, 6))
        pygame.draw.ellipse(pantalla, (180, 130, 70), (x + 7, y + 1 + off, 10, 4))
        pygame.draw.line(pantalla, (180, 130, 70), (x + 14, y + off), (x + 20, y - 6 + off), 3)
        pygame.draw.circle(pantalla, (200, 150, 80), (x + 20, y - 6 + off), 3)
        for i in range(3):
            pygame.draw.circle(pantalla, (100, 70, 30), 
                             (x + 8 + i * 5, y + 4 + off + i * 2), 2)


