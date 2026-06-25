"""
KONG ARGENTINO - PRINCESA
"""
import pygame
import random
import math
from config import *

class Princesa(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, TAMANO_PRINCESA[0], TAMANO_PRINCESA[1])
        self.anim_frame = 0
        self.ondeo = 0
        # --- NUEVO: Copa del Mundo ---
        self.tiene_copa = True  # Siempre la tiene al llegar al nivel final

    def update(self):
        self.anim_frame += 1
        self.ondeo = int(math.sin(self.anim_frame * 0.08) * 4)

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y
        o = self.ondeo
        self.gestor.dibujar_sombra(pantalla, x + 16, y + 38, 28, 8, alpha=60)
        pygame.draw.rect(pantalla, (200, 220, 255), (x + 4, y + 12 + o, 24, 20))
        pygame.draw.rect(pantalla, (180, 200, 235), (x + 6, y + 14 + o, 20, 16))
        for i in range(3):
            px = x + 2 + i * 8
            py = y + 26 + o + i * 2
            pygame.draw.ellipse(pantalla, (200, 220, 255), (px, py, 24 - i * 4, 8 - i))
            pygame.draw.ellipse(pantalla, (180, 200, 235), (px + 2, py + 1, 20 - i * 4, 6 - i))
        pygame.draw.rect(pantalla, (255, 215, 0), (x + 10, y + 20 + o, 12, 4))
        pygame.draw.rect(pantalla, (255, 220, 200), (x, y + 16 + o, 4, 12))
        pygame.draw.rect(pantalla, (255, 220, 200), (x + 28, y + 16 + o, 4, 12))
        pygame.draw.circle(pantalla, (255, 220, 200), (x + 2, y + 28 + o), 3)
        pygame.draw.circle(pantalla, (255, 220, 200), (x + 30, y + 28 + o), 3)
        pygame.draw.circle(pantalla, (255, 220, 200), (x + 16, y + 8 + o), 10)
        pygame.draw.ellipse(pantalla, (80, 50, 30), (x + 4, y - 2 + o, 24, 12))
        pygame.draw.ellipse(pantalla, (100, 70, 50), (x + 6, y - 1 + o, 20, 10))
        pygame.draw.ellipse(pantalla, (80, 50, 30), (x + 22, y - 4 + o, 10, 6))
        pygame.draw.ellipse(pantalla, (80, 50, 30), (x + 26, y - 2 + o, 8, 8))
        pygame.draw.rect(pantalla, (255, 215, 0), (x + 6, y - 2 + o, 20, 4))
        for i, px in enumerate([x + 8, x + 13, x + 18, x + 23]):
            alt = 6 if i % 2 == 0 else 4
            pygame.draw.polygon(pantalla, (255, 215, 0), 
                               [(px, y - 2 + o), (px + 2, y - 4 - alt + o), (px + 4, y - 2 + o)])
        pygame.draw.circle(pantalla, (255, 100, 100), (x + 10, y - 2 + o), 2)
        pygame.draw.circle(pantalla, (100, 100, 255), (x + 16, y - 3 + o), 2)
        pygame.draw.circle(pantalla, (100, 255, 100), (x + 22, y - 2 + o), 2)
        if self.anim_frame % 60 < 50:
            pygame.draw.circle(pantalla, (255, 255, 255), (x + 12, y + 6 + o), 4)
            pygame.draw.circle(pantalla, (255, 255, 255), (x + 20, y + 6 + o), 4)
            pygame.draw.circle(pantalla, (50, 50, 150), (x + 13, y + 7 + o), 2)
            pygame.draw.circle(pantalla, (50, 50, 150), (x + 21, y + 7 + o), 2)
            pygame.draw.circle(pantalla, (255, 255, 255), (x + 12, y + 5 + o), 1)
            pygame.draw.circle(pantalla, (255, 255, 255), (x + 20, y + 5 + o), 1)
        else:
            pygame.draw.line(pantalla, (50, 50, 150), (x + 9, y + 7 + o), (x + 15, y + 7 + o), 2)
            pygame.draw.line(pantalla, (50, 50, 150), (x + 17, y + 7 + o), (x + 23, y + 7 + o), 2)
        for ex in [12, 20]:
            pygame.draw.line(pantalla, (50, 50, 150), (x + ex - 2, y + 5 + o), (x + ex - 1, y + 3 + o), 1)
            pygame.draw.line(pantalla, (50, 50, 150), (x + ex + 2, y + 5 + o), (x + ex + 3, y + 3 + o), 1)
        pygame.draw.arc(pantalla, (200, 50, 50), (x + 11, y + 10 + o, 10, 6), 0, math.pi, 2)
        pygame.draw.arc(pantalla, (220, 80, 80), (x + 11, y + 11 + o, 10, 4), 0, math.pi, 1)
        if self.anim_frame % 90 < 40:
            self.gestor.dibujar_texto(pantalla, "¡AYUDA!", 14, COLORES['rojo'], 
                                      x + 34, y + 2 + o, sombra=True)
            heart_y = y - 10 + o + int(math.sin(self.anim_frame * 0.1) * 3)
            pygame.draw.polygon(pantalla, (255, 100, 100),
                               [(x + 30, heart_y), (x + 27, heart_y - 4), 
                                (x + 27, heart_y - 8), (x + 30, heart_y - 10),
                                (x + 33, heart_y - 8), (x + 33, heart_y - 4), 
                                (x + 30, heart_y)])

        # ─── COPA DEL MUNDO ──────────────────────────────────────────────
        if self.tiene_copa:
            # La copa se dibuja en la mano derecha (posición ajustada)
            copa_x = x + 28  # mano derecha
            copa_y = y + 10 + o
            self.gestor.dibujar_copa_mundo(pantalla, copa_x, copa_y, escala=0.45)

            # Resplandor
            for r in range(12, 0, -3):
                alpha = 30 - r * 2
                pygame.draw.circle(pantalla, (255, 215, 0, alpha), 
                                  (int(copa_x + 8), int(copa_y + 12)), r)

            # Cuerpo de la copa
            pygame.draw.ellipse(pantalla, (210, 180, 50), (copa_x + 2, copa_y + 4, 12, 16))
            pygame.draw.ellipse(pantalla, (255, 215, 0), (copa_x + 3, copa_y + 5, 10, 14))
            # Base
            pygame.draw.ellipse(pantalla, (180, 150, 40), (copa_x, copa_y + 18, 16, 6))
            pygame.draw.ellipse(pantalla, (255, 215, 0), (copa_x + 1, copa_y + 19, 14, 4))
            # Asas
            pygame.draw.arc(pantalla, (255, 215, 0), (copa_x - 2, copa_y + 6, 6, 12), 0, math.pi/2, 2)
            pygame.draw.arc(pantalla, (255, 215, 0), (copa_x + 12, copa_y + 6, 6, 12), math.pi/2, math.pi, 2)
            # Copa superior (globo)
            pygame.draw.circle(pantalla, (255, 215, 0), (copa_x + 8, copa_y + 4), 7)
            pygame.draw.circle(pantalla, (255, 220, 50), (copa_x + 8, copa_y + 4), 5)
            # Brillo
            pygame.draw.circle(pantalla, (255, 255, 255, 80), (copa_x + 6, copa_y + 2), 3)


