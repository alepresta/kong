"""
KONG ARGENTINO - BARRIL CERVEZA
"""
import pygame
import random
import math
from constantes import *

class BarrilCerveza(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor, es_item=False, vel_mult=1.0):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, TAMANO_BARRIL[0], TAMANO_BARRIL[1])
        self.es_item = es_item
        self.valor = PUNTUACION_POR_CERVEZA if es_item else 0
        self.anim_frame = 0
        self.angulo = 0
        self.shake_x = 0
        self.shake_y = 0
        self.eliminar = False

        self.frames = []
        self._generar_frames_barril()

        if not es_item:
            self.vel_x = random.choice([-1, 1]) * (2.0 * vel_mult)
            self.vel_y = 0
            self.gravedad = 0.4
            self.rotacion_vel = 4 * (1 if self.vel_x > 0 else -1)
            self.sobre_plataforma = False
            self.plataforma_actual = None
        else:
            self.vel_x = 0
            self.vel_y = 0
            self.sobre_plataforma = False
            self.plataforma_actual = None

    def _generar_frames_barril(self):
        for i in range(8):
            surf = pygame.Surface((TAMANO_BARRIL[0]+4, TAMANO_BARRIL[1]+4), pygame.SRCALPHA)
            ang = i * 45

            pygame.draw.ellipse(surf, (0, 0, 0, 60), (4, 24, 28, 8))
            pygame.draw.ellipse(surf, (80, 55, 30), (2, 4, 28, 24))
            pygame.draw.ellipse(surf, (110, 75, 45), (4, 6, 24, 20))

            pygame.draw.ellipse(surf, (180, 170, 150), (0, 6, 32, 8), 3)
            pygame.draw.ellipse(surf, (180, 170, 150), (0, 18, 32, 8), 3)
            pygame.draw.ellipse(surf, (200, 190, 170), (2, 13, 28, 6), 2)

            for v in range(4):
                vx = 5 + v * 7 + (i * 2) % 5
                vy = 8 + v * 4
                pygame.draw.line(surf, (60, 40, 20), (vx, vy), (vx+8, vy+10), 1)

            pygame.draw.rect(surf, (220, 200, 100), (6, 10, 20, 12))
            pygame.draw.rect(surf, (255, 220, 50), (8, 12, 16, 2))
            pygame.draw.rect(surf, (255, 220, 50), (8, 16, 16, 2))
            pygame.draw.circle(surf, (200, 100, 50), (16, 16), 3)

            pygame.draw.ellipse(surf, (255, 255, 255, 40), (6, 5, 10, 8))
            pygame.draw.ellipse(surf, (255, 255, 255, 70), (10, 5, 6, 4))

            rot = pygame.transform.rotate(surf, ang)
            self.frames.append(rot)

    def update(self, plataformas, escaleras):
        if self.es_item:
            self.anim_frame += 1
            return

        self.anim_frame += 1
        self.rect.x += self.vel_x

        if self.rect.x < -60 or self.rect.x > ANCHO + 60:
            self.eliminar = True
            return

        if not self.sobre_plataforma:
            self.vel_y += self.gravedad
            if self.vel_y > 12:
                self.vel_y = 12
        else:
            self.vel_y = 0

        self.rect.y += self.vel_y

        self.sobre_plataforma = False
        self.plataforma_actual = None

        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vel_y >= 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.sobre_plataforma = True
                    self.plataforma_actual = p
                    break

        if self.sobre_plataforma and self.plataforma_actual:
            p = self.plataforma_actual
            if self.vel_x > 0 and self.rect.right > p.rect.right:
                self.sobre_plataforma = False
                self.plataforma_actual = None
                self.vel_y = 1
            elif self.vel_x < 0 and self.rect.left < p.rect.left:
                self.sobre_plataforma = False
                self.plataforma_actual = None
                self.vel_y = 1

        if self.rect.y > ALTO + 60:
            self.eliminar = True
            return

        self.angulo = (self.angulo + self.rotacion_vel) % 360

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y

        if self.es_item:
            off = int(math.sin(self.anim_frame * 0.1) * 4)
            if self.anim_frame % 30 < 15:
                pygame.draw.circle(pantalla, (255, 220, 100, 30), (x + 10, y + 8 + off), 12)
            pygame.draw.rect(pantalla, (101, 67, 33), (x + 2, y + 2 + off, 16, 16))
            pygame.draw.rect(pantalla, (130, 90, 50), (x + 3, y + 3 + off, 14, 14))
            pygame.draw.rect(pantalla, (200, 180, 100), (x + 4, y + 4 + off, 12, 12), 1)
            pygame.draw.rect(pantalla, (255, 220, 50), (x + 5, y + 7 + off, 10, 2))
            pygame.draw.rect(pantalla, (255, 220, 50), (x + 5, y + 10 + off, 10, 2))
            pygame.draw.ellipse(pantalla, (240, 230, 200), (x + 3, y - 2 + off, 12, 5))
            pygame.draw.ellipse(pantalla, (200, 190, 160), (x + 5, y - 1 + off, 8, 3))
            pygame.draw.ellipse(pantalla, (255, 255, 255, 40), (x + 4, y + 3 + off, 5, 4))
        else:
            self.gestor.dibujar_sombra(pantalla, x + 16, y + 32, 30, 8, alpha=60)
            frame_idx = int((self.angulo / 45) % 8)
            frame = self.frames[frame_idx]
            pantalla.blit(frame, (x - 2, y - 2))


