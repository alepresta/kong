"""
KONG ARGENTINO - KONG CERVECERO
"""
import pygame
import random
import math
from constantes import *

from .barril_cerveza import BarrilCerveza

class KongCervecero(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor, nivel=1):
        super().__init__()
        self.gestor = gestor
        self.nivel = nivel
        self.rect = pygame.Rect(x, y, 110, 120)
        self.tiempo_barril = 0
        self.enojado = False
        self.tiempo_enojado = 0
        self.direccion = 1
        self.x_inicial = x
        self.rango_movimiento = 200
        self.anim_frame = 0
        self.rugido_frame = 0
        self.shake_x = 0
        self.shake_y = 0
        cfg = DIFICULTAD_NIVEL.get(nivel, DIFICULTAD_NIVEL[5])
        self.vel_x = cfg['vel_kong']
        self.tiempo_entre_barriles = 0
        self.frames_idle = []
        self.frames_roar = []
        self.frames_throw = []
        self._generar_frames()

    def _generar_frames(self):
        for i in range(6):
            self.frames_idle.append(self._dibujar_kong(i, 'idle'))
            self.frames_roar.append(self._dibujar_kong(i, 'roar'))
            self.frames_throw.append(self._dibujar_kong(i, 'throw'))

    def _dibujar_kong(self, frame, estado):
        surf = pygame.Surface((180, 160), pygame.SRCALPHA)
        x, y = 35, 20
        pygame.draw.ellipse(surf, (0, 0, 0, 100), (x + 5, y + 115, 95, 22))
        pygame.draw.ellipse(surf, (45, 28, 18), (x + 18, y + 55, 78, 68))
        pygame.draw.ellipse(surf, (65, 42, 28), (x + 23, y + 58, 68, 58))
        pygame.draw.ellipse(surf, (130, 85, 55), (x + 32, y + 68, 48, 45))
        tie_points = [(x+48, y+72), (x+38, y+88), (x+50, y+102), (x+62, y+88), (x+53, y+72)]
        pygame.draw.polygon(surf, (200, 10, 10), tie_points)
        pygame.draw.circle(surf, (180, 0, 0), (x + 50, y + 82), 11)
        pygame.draw.line(surf, (255, 255, 255), (x + 44, y + 78), (x + 44, y + 87), 3)
        pygame.draw.line(surf, (255, 255, 255), (x + 55, y + 78), (x + 55, y + 87), 3)
        pygame.draw.line(surf, (255, 255, 255), (x + 55, y + 82), (x + 59, y + 82), 3)
        color_brazo = (45, 28, 18)
        color_mano = (60, 38, 25)
        izq_y = y + 22 if estado == 'roar' else y + 28
        pygame.draw.line(surf, color_brazo, (x + 25, y + 65), (x + 18, izq_y), 24)
        pygame.draw.circle(surf, color_mano, (x + 18, izq_y), 14)
        for d in [-6, 0, 6]:
            pygame.draw.circle(surf, color_mano, (x + 16 + d, izq_y + 3), 5)
        if estado == 'throw':
            pygame.draw.line(surf, color_brazo, (x + 85, y + 65), (x + 135, y + 58), 24)
            pygame.draw.circle(surf, color_mano, (x + 135, y + 58), 14)
            pygame.draw.circle(surf, (35, 22, 15), (x + 140, y + 56), 11)
            bx = x + 130
            by = y + 45
            pygame.draw.rect(surf, (80, 55, 30), (bx, by, 18, 24))
            pygame.draw.rect(surf, (140, 100, 60), (bx+2, by+2, 14, 20))
            pygame.draw.ellipse(surf, (180, 150, 80), (bx, by-2, 18, 6))
            pygame.draw.ellipse(surf, (200, 180, 100), (bx+2, by, 14, 4))
            pygame.draw.rect(surf, (220, 200, 100), (bx+3, by+6, 12, 3))
            pygame.draw.rect(surf, (220, 200, 100), (bx+3, by+14, 12, 3))
        else:
            der_y = y + 22 if estado == 'roar' else y + 28
            pygame.draw.line(surf, color_brazo, (x + 85, y + 65), (x + 95, der_y), 24)
            pygame.draw.circle(surf, color_mano, (x + 95, der_y), 14)
            for d in [-6, 0, 6]:
                pygame.draw.circle(surf, color_mano, (x + 93 + d, der_y + 3), 5)
        pygame.draw.ellipse(surf, (45, 28, 18), (x + 25, y + 110, 30, 38))
        pygame.draw.ellipse(surf, (45, 28, 18), (x + 58, y + 110, 30, 38))
        pygame.draw.ellipse(surf, (65, 42, 28), (x + 29, y + 115, 22, 28))
        pygame.draw.ellipse(surf, (65, 42, 28), (x + 62, y + 115, 22, 28))
        pygame.draw.circle(surf, (55, 35, 22), (x + 55, y + 38), 42)
        pygame.draw.ellipse(surf, (55, 35, 22), (x + 28, y + 18, 54, 32))
        pygame.draw.ellipse(surf, (80, 55, 38), (x + 33, y + 42, 46, 28))
        pygame.draw.circle(surf, (50, 32, 20), (x + 18, y + 32), 14)
        pygame.draw.circle(surf, (50, 32, 20), (x + 92, y + 32), 14)
        eyebrow_y = y + 23 if estado == 'roar' else y + 26
        pygame.draw.line(surf, (25, 15, 10), (x + 28, eyebrow_y - 3), (x + 48, eyebrow_y + 3), 8)
        pygame.draw.line(surf, (25, 15, 10), (x + 62, eyebrow_y + 3), (x + 82, eyebrow_y - 4), 8)
        ojo_y = 32
        if estado == 'roar':
            ojo_y += 2
        pygame.draw.ellipse(surf, (255, 245, 210), (x + 36, y + ojo_y, 14, 12))
        pygame.draw.ellipse(surf, (255, 245, 210), (x + 64, y + ojo_y, 14, 12))
        if hasattr(self.gestor, 'argentino') and self.gestor.argentino:
            dx = self.gestor.argentino.rect.centerx - (self.rect.x + 55)
            dy = self.gestor.argentino.rect.centery - (self.rect.y + 38)
            ang = math.atan2(dy, dx)
            dist = min(2.8, math.hypot(dx, dy) * 0.013)
        else:
            ang, dist = 0, 0
        px1 = x + 42 + math.cos(ang) * dist * 3.5
        py1 = y + ojo_y + 6 + math.sin(ang) * dist * 3.5
        px2 = x + 70 + math.cos(ang) * dist * 3.5
        py2 = y + ojo_y + 6 + math.sin(ang) * dist * 3.5
        pygame.draw.circle(surf, (30, 18, 12), (int(px1), int(py1)), 4.5)
        pygame.draw.circle(surf, (30, 18, 12), (int(px2), int(py2)), 4.5)
        pygame.draw.ellipse(surf, (45, 28, 18), (x + 46, y + 48, 19, 11))
        pygame.draw.circle(surf, (25, 15, 10), (x + 50, y + 50), 3)
        pygame.draw.circle(surf, (25, 15, 10), (x + 60, y + 50), 3)
        if estado == 'roar':
            pygame.draw.ellipse(surf, (30, 12, 8), (x + 37, y + 58, 36, 20))
            for i in range(5):
                pygame.draw.rect(surf, (255, 250, 230), (x + 40 + i*6, y + 58, 4, 9))
        else:
            pygame.draw.arc(surf, (30, 12, 8), (x + 37, y + 57, 34, 16), 0.2, math.pi - 0.3, 6)
        for i in range(11):
            ang = math.radians(i * 33 + frame * 12)
            px = x + 55 + math.cos(ang) * 39
            py = y + 14 + math.sin(ang) * 19
            pygame.draw.line(surf, (38, 24, 16), (px, py), (px + math.cos(ang)*9, py - 7), 5)
        return surf

    def update(self, plataformas):
        self.anim_frame += 1
        self.tiempo_barril += 1
        self.rect.x += self.vel_x * self.direccion
        if self.rect.x > self.x_inicial + self.rango_movimiento:
            self.rect.x = self.x_inicial + self.rango_movimiento
            self.direccion = -1
        if self.rect.x < self.x_inicial - self.rango_movimiento:
            self.rect.x = self.x_inicial - self.rango_movimiento
            self.direccion = 1
        if self.tiempo_enojado > 0:
            self.tiempo_enojado -= 1
            self.enojado = True
            self.shake_x = random.randint(-3, 3)
            self.shake_y = random.randint(-2, 2)
        else:
            self.enojado = False
            self.shake_x = 0
            self.shake_y = 0
        if self.rugido_frame > 0:
            self.rugido_frame -= 1

    def lanzar_barril(self):
        cfg = DIFICULTAD_NIVEL.get(self.nivel, DIFICULTAD_NIVEL[5])
        vel_mult = cfg['vel_barril'] / 2.0
        if self.direccion == 1:
            mano_x = self.rect.x + 135 - 9
            mano_y = self.rect.y + 58 - 12
        else:
            mano_x = self.rect.x + self.rect.width - 135 - 9
            mano_y = self.rect.y + 58 - 12
        barril = BarrilCerveza(mano_x, mano_y, self.gestor, es_item=False, vel_mult=vel_mult)
        barril.vel_x = (4.2 * vel_mult) * self.direccion
        barril.vel_y = -2
        return barril

    def set_mario_cerca(self, cerca):
        if cerca and not self.enojado:
            self.tiempo_enojado = 70
            self.rugido_frame = 65

    def get_tiempo_barril(self):
        cfg = DIFICULTAD_NIVEL.get(self.nivel, DIFICULTAD_NIVEL[5])
        base = cfg['cadencia']
        return int(base * 0.75) if self.enojado else base

    def dibujar(self, pantalla):
        x = self.rect.x + self.shake_x
        y = self.rect.y + self.shake_y
        t = pygame.time.get_ticks()
        frame_idx = (t // 180) % 6
        if self.rugido_frame > 0:
            frame = self.frames_roar[frame_idx]
        elif self.tiempo_barril > self.get_tiempo_barril() - 25:
            frame = self.frames_throw[frame_idx]
        else:
            frame = self.frames_idle[frame_idx]
        if self.direccion == -1:
            frame = pygame.transform.flip(frame, True, False)
        pantalla.blit(frame, (x - 35, y - 18))
        if self.rugido_frame > 0 and self.rugido_frame % 8 < 4:
            for _ in range(4):
                self.gestor.particulas.append({
                    'x': x + random.randint(55, 95),
                    'y': y + random.randint(25, 55),
                    'vx': random.uniform(1.5, 5),
                    'vy': random.uniform(-3, 2),
                    'vida': 18,
                    'vida_max': 18,
                    'color': (220, 140, 40),
                    'tam': random.randint(3, 6)
                })


# src/entidades/objetos.py - Modificar la clase HinchaBorrachito (sin cambios relevantes)

