"""
KONG ARGENTINO - OBJETOS DEL JUEGO v3.2 (Barriles con física de rodadura)
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

class HinchaBorrachito(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, 32, 38)
        self.vidas = 5  # Más vidas para que no muera fácil
        self.anim_frame = 0
        self.offset_y = 0
        self.tiempo_grito = 0
        self.gritando = False
        self.texto_grito = ""
        self.tiempo_texto = 0
        
        # --- NUEVOS ATRIBUTOS PARA COMPORTAMIENTO ---
        self.estado = "buscando"  # "buscando", "golpeado", "tambaleando"
        self.tiempo_estado = 0
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.direccion = 1
        self.nivel_borrachera = 3  # Nivel inicial de borrachera
        self.plataforma_objetivo = None
        self.gravedad = 0.5
        self.barriles_agarrados = 0
        self.tiempo_idle = 0

    def update(self, plataformas=None, escaleras=None, barriles=None):
        self.anim_frame += 1
        self.offset_y = math.sin(self.anim_frame * 0.1) * 3
        self.tiempo_grito += 1
        
        # Grito aleatorio
        if self.tiempo_grito >= 180 and random.randint(0, 30) == 0:
            self.tiempo_grito = 0
            self.gritando = True
            self.tiempo_texto = 50
            
        if self.tiempo_texto > 0:
            self.tiempo_texto -= 1
            if self.tiempo_texto == 0:
                self.gritando = False
                
        # --- NUEVO: Manejo de estados ---
        if self.estado == "golpeado":
            self._actualizar_golpeado()
            return
        elif self.estado == "tambaleando":
            self._actualizar_tambaleando(plataformas)
            return
        else:  # buscando
            self._actualizar_buscando(plataformas, barriles)

    def _actualizar_buscando(self, plataformas, barriles):
        """Comportamiento normal: buscar barriles"""
        if plataformas is None:
            return
            
        # Aplicar gravedad
        self.vel_y += self.gravedad
        if self.vel_y > 8:
            self.vel_y = 8
            
        # Movimiento horizontal
        self.rect.x += self.vel_x
        
        # Buscar barril cercano
        if barriles and self.tiempo_idle <= 0:
            barril_cercano = min(barriles, key=lambda b: math.hypot(b.rect.x - self.rect.x, b.rect.y - self.rect.y))
            dx = barril_cercano.rect.x - self.rect.x
            
            if abs(dx) > 15:
                spd = 1.5 + self.nivel_borrachera // 3
                self.vel_x = spd * (1 if dx > 0 else -1)
                self.direccion = 1 if dx > 0 else -1
            else:
                self.vel_x = 0
                
            # Si está muy borracho, se tambalea
            if self.nivel_borrachera >= 5 and random.randint(0, 60) == 0:
                self.vel_x = random.choice([-3, -2, 0, 2, 3])
        elif self.tiempo_idle <= 0:
            self.tiempo_idle = random.randint(30, 90)
            self.vel_x = random.choice([-1.5, -0.5, 0.5, 1.5])
        else:
            self.tiempo_idle -= 1
        
        # Colisiones con plataformas
        self.rect.y += int(self.vel_y)
        self.en_suelo = False
        if plataformas:
            for p in plataformas:
                if self.rect.colliderect(p.rect):
                    if self.vel_y >= 0:
                        self.rect.bottom = p.rect.top
                        self.vel_y = 0
                        self.en_suelo = True
                    elif self.vel_y < 0:
                        self.rect.top = p.rect.bottom
                        self.vel_y = 0
        
        # Límites
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = abs(self.vel_x)
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
            self.vel_x = -abs(self.vel_x)
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
            self.vel_y = 0
            self.en_suelo = True

    def _actualizar_golpeado(self):
        """Estado cuando recibe un golpe - retrocede y se queda quieto"""
        self.tiempo_estado -= 1
        
        # Retroceder con impulso
        if self.tiempo_estado > 50:  # Primera fase: retroceder rápido
            retroceso = 8 if self.direccion == 1 else -8
            self.rect.x += retroceso
        else:
            # Frenar gradualmente
            self.vel_x *= 0.9
        
        # Pequeño rebote hacia arriba
        if self.tiempo_estado > 55:
            self.rect.y -= 2
        
        # Volver al estado normal
        if self.tiempo_estado <= 0:
            self.estado = "tambaleando"
            self.tiempo_estado = 40  # Tiempo de tambaleo
            self.vel_x = random.choice([-2, -1, 1, 2]) if random.random() > 0.3 else 0

    def _actualizar_tambaleando(self, plataformas):
        """Estado de tambaleo después del golpe"""
        self.tiempo_estado -= 1
        
        # Se mueve erráticamente
        if random.randint(0, 10) == 0:
            self.vel_x = random.choice([-2, -1, 0, 1, 2])
        
        # Aplicar movimiento
        if plataformas:
            self.rect.x += self.vel_x
            self.rect.y += int(self.vel_y)
            
            # Gravedad simple
            self.vel_y += self.gravedad
            if self.vel_y > 6:
                self.vel_y = 6
                
            self.en_suelo = False
            for p in plataformas:
                if self.rect.colliderect(p.rect):
                    if self.vel_y >= 0:
                        self.rect.bottom = p.rect.top
                        self.vel_y = 0
                        self.en_suelo = True
        
        # Volver a buscar
        if self.tiempo_estado <= 0:
            self.estado = "buscando"
            self.tiempo_estado = 0
            self.nivel_borrachera = max(0, self.nivel_borrachera - 1)  # Se despeja un poco

    def recibir_golpe(self):
        """Recibe un golpe - NO MUERE, solo retrocede"""
        # Efecto visual de golpe
        self.gritando = True
        self.tiempo_texto = 30
        self.texto_grito = "¡AY! 🍺"
        
        # Cambiar estado a golpeado
        self.estado = "golpeado"
        self.tiempo_estado = 70  # Frames de estado golpeado
        
        # Retroceder en dirección opuesta
        self.direccion = -self.direccion
        
        # Aumentar borrachera (se enoja y bebe más)
        self.nivel_borrachera = min(10, self.nivel_borrachera + 1)
        
        # No se reduce vida
        return False  # Nunca muere

    def beber_barril(self):
        """El hincha bebe un barril cuando lo encuentra"""
        self.nivel_borrachera = min(10, self.nivel_borrachera + 2)
        self.barriles_agarrados += 1
        self.gestor.reproducir_sonido('beber')
        
        # A veces se pone a celebrar
        if self.barriles_agarrados % 3 == 0:
            self.gritando = True
            self.tiempo_texto = 60
            self.texto_grito = "¡VAMO VAMO ARGENTINA! 🇦🇷"

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y + self.offset_y
        
        # Sombra
        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 28, 8)
        
        # Cuerpo (camiseta argentina)
        pygame.draw.rect(pantalla, (117, 190, 218), (x, y+12, 32, 22))
        for i in range(0, 32, 8):
            pygame.draw.rect(pantalla, (255, 255, 255), (x+i, y+12, 4, 22))
        pygame.draw.rect(pantalla, (255, 255, 255), (x+10, y+10, 12, 6))
        
        # Número
        self.gestor.dibujar_texto(pantalla, "10", 12, (0, 0, 0), x+12, y+18)
        
        # Cabeza
        pygame.draw.circle(pantalla, (255, 220, 200), (x+16, y+10), 12)
        pygame.draw.ellipse(pantalla, (30, 30, 30), (x+4, y-2, 24, 10))
        
        # Ojos (pueden estar entrecerrados si está borracho)
        if self.nivel_borrachera >= 6:
            # Ojos entrecerrados
            pygame.draw.line(pantalla, (0, 0, 0), (x+10, y+8), (x+14, y+8), 2)
            pygame.draw.line(pantalla, (0, 0, 0), (x+18, y+8), (x+22, y+8), 2)
        else:
            pygame.draw.circle(pantalla, (255, 255, 255), (x+12, y+8), 3)
            pygame.draw.circle(pantalla, (255, 255, 255), (x+20, y+8), 3)
            pygame.draw.circle(pantalla, (0, 0, 0), (x+13, y+9), 2)
            pygame.draw.circle(pantalla, (0, 0, 0), (x+21, y+9), 2)
        
        # Boca
        if self.gritando:
            pygame.draw.ellipse(pantalla, (200, 50, 50), (x+12, y+14, 8, 6))
        else:
            pygame.draw.arc(pantalla, (200, 50, 50), (x+10, y+14, 12, 6), 0, math.pi, 2)
        
        # Brazos
        if self.estado == "golpeado":
            # Brazos levantados (sorpresa)
            pygame.draw.rect(pantalla, (255, 220, 200), (x-4, y+2, 5, 12))
            pygame.draw.rect(pantalla, (255, 220, 200), (x+31, y+2, 5, 12))
            pygame.draw.circle(pantalla, (255, 220, 200), (x-2, y+2), 4)
            pygame.draw.circle(pantalla, (255, 220, 200), (x+34, y+2), 4)
        else:
            pygame.draw.rect(pantalla, (255, 220, 200), (x-4, y+14, 5, 14))
            pygame.draw.rect(pantalla, (255, 220, 200), (x+31, y+14, 5, 14))
        
        # Piernas
        leg_offset = int(math.sin(self.anim_frame * 0.15) * 3) if abs(self.vel_x) > 0.5 else 0
        pygame.draw.rect(pantalla, (30, 60, 140), (x+4, y+34, 8, 8 + leg_offset))
        pygame.draw.rect(pantalla, (30, 60, 140), (x+20, y+34, 8, 8 - leg_offset))
        pygame.draw.rect(pantalla, (40, 40, 40), (x+2, y+42 + leg_offset, 12, 4))
        pygame.draw.rect(pantalla, (40, 40, 40), (x+18, y+42 - leg_offset, 12, 4))
        
        # Barra de borrachera
        if self.nivel_borrachera > 0:
            ancho_b = int(32 * (self.nivel_borrachera / 10))
            pygame.draw.rect(pantalla, COLORES['negro'], (x, y-8, 32, 4))
            col_b = COLORES['verde'] if self.nivel_borrachera < 6 else COLORES['naranja']
            pygame.draw.rect(pantalla, col_b, (x, y-8, ancho_b, 4))
            pygame.draw.rect(pantalla, COLORES['blanco'], (x, y-8, 32, 4), 1)
        
        # Texto de grito
        if self.gritando and self.tiempo_texto > 0:
            textos = [
                "🇦🇷 VAMO VAMO ARGENTINA 🇦🇷",
                "¡VAMOS CARAJO! 🍺",
                "¡DALE DALE DALE! 🇦🇷",
                "¡AGUANTE ARGENTINA! 🏆",
                "¡AY! 🍺",
            ]
            if not hasattr(self, 'texto_grito') or self.texto_grito == "":
                self.texto_grito = random.choice(textos)
            
            self.gestor.dibujar_texto(pantalla, self.texto_grito, 16, (0,0,0), x+16, y-28, centro=True)
            self.gestor.dibujar_texto(pantalla, self.texto_grito, 16, COLORES['amarillo'], x+14, y-30, centro=True)
            
            # Partículas de celebración
            if self.anim_frame % 3 == 0:
                self.gestor.particulas.append({
                    'x': x + random.randint(-5, 37),
                    'y': y - 20 + random.randint(-5, 5),
                    'vx': random.uniform(-1.5, 1.5),
                    'vy': random.uniform(-3, -0.5),
                    'vida': 25,
                    'vida_max': 25,
                    'color': random.choice([COLORES['celeste'], COLORES['blanco'], COLORES['amarillo']]),
                    'tam': random.randint(2, 4)
                })
        
        # Indicador de estado
        if self.estado == "golpeado":
            # Efecto de "estrella" sobre la cabeza
            for i in range(3):
                ang = self.anim_frame * 0.3 + i * 2.1
                sx = x + 16 + math.cos(ang) * 18
                sy = y - 6 + math.sin(ang) * 10
                pygame.draw.circle(pantalla, (255, 200, 50), (int(sx), int(sy)), 2)