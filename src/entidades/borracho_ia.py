"""
KONG ARGENTINO - BORRACHO IA
"""
import pygame
import random
import math
from config import *

class BorrachoIA(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, TAMANO_BORRACHO[0], TAMANO_BORRACHO[1])
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.vidas = 5
        self.direccion = 1
        self.estado = "buscando"
        self.tiempo_estado = 0
        self.nivel_borrachera = 0
        self.anim_frame = 0
        self.barriles_agarrados = 0
        self.plataforma_objetivo = None
        self.tiempo_idle = 0
        self.offset_y = 0
        self.en_escalera = False
        self.escalera_actual = None
        self.pegado_techo = False
        self.tiempo_pegado_techo = 0
        self.frames_pegado_techo = TIEMPO_PEGADO_TECHO
        self.vel_max = VEL_MAX_CAIDA_BORRACHO

    def update(self, plataformas, escaleras, barriles):
        self.anim_frame += 1
        self.offset_y = math.sin(self.anim_frame * 0.15) * 2 if not self.en_suelo else 0

        if self.tiempo_estado > 0:
            self.tiempo_estado -= 1
            if self.tiempo_estado <= 0:
                self.estado = "buscando"

        if self.tiempo_idle > 0:
            self.tiempo_idle -= 1

        if self.estado == "buscando":
            self._buscar_barril(barriles, plataformas)
        elif self.estado == "bebiendo":
            self._tambalear()
        elif self.estado == "celebrando":
            self.vel_x = 0

        self.en_escalera = False
        self.escalera_actual = None
        for e in escaleras:
            if self.rect.colliderect(e.rect_deteccion):
                self.en_escalera = True
                self.escalera_actual = e
                break

        if self.en_escalera and self.escalera_actual:
            barril_arriba = any(
                b.rect.y < self.rect.y - 50 
                for b in barriles
            )
            if barril_arriba and random.randint(0, 20) == 0:
                self.rect.centerx = self.escalera_actual.x_visual + 6
                self.rect.y -= 3
                self.vel_y = 0
                return

        # Movimiento horizontal
        self.rect.x += int(self.vel_x)
        
        # Gravedad
        self.vel_y += GRAVEDAD * MULTIPLICADOR_GRAVEDAD_BORRACHO
        if self.vel_y > self.vel_max:
            self.vel_y = self.vel_max
        
        old_y = self.rect.y
        
        # Pegado al techo
        if self.pegado_techo:
            self.tiempo_pegado_techo -= 1
            if self.tiempo_pegado_techo <= 0:
                self.pegado_techo = False
                self.vel_y = 0
        else:
            # Movimiento vertical
            self.rect.y += int(self.vel_y)
            
            self.en_suelo = False
            for p in plataformas:
                if self.rect.colliderect(p.rect):
                    if old_y + self.rect.height <= p.rect.top + 10:
                        self.rect.bottom = p.rect.top
                        self.vel_y = 0
                        self.en_suelo = True
                    elif old_y >= p.rect.bottom - 10:
                        self.rect.top = p.rect.bottom
                        self.vel_y = 0
                        self.pegado_techo = True
                        self.tiempo_pegado_techo = self.frames_pegado_techo
                    else:
                        if self.vel_y > 0:
                            self.rect.bottom = p.rect.top
                            self.vel_y = 0
                            self.en_suelo = True
                        elif self.vel_y < 0:
                            self.rect.top = p.rect.bottom
                            self.vel_y = 0
                            self.pegado_techo = True
                            self.tiempo_pegado_techo = self.frames_pegado_techo

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
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
            self.pegado_techo = True
            self.tiempo_pegado_techo = self.frames_pegado_techo

    def _buscar_barril(self, barriles, plataformas):
        if not barriles:
            if self.tiempo_idle <= 0:
                self.vel_x = random.choice([-1.5, -0.5, 0.5, 1.5])
                self.tiempo_idle = random.randint(30, 90)
            return

        barril_cercano = min(barriles, key=lambda b: math.hypot(b.rect.x - self.rect.x, b.rect.y - self.rect.y))
        dx = barril_cercano.rect.x - self.rect.x

        spd = min(VELOCIDAD_JUGADOR - 1, 3 + self.nivel_borrachera // 4)
        if abs(dx) > 10:
            self.vel_x = spd * (1 if dx > 0 else -1)
            self.direccion = 1 if dx > 0 else -1
        else:
            self.vel_x = 0

        if self.nivel_borrachera > 4 and random.randint(0, 40) == 0:
            self.vel_x = random.choice([-3, -2, 0, 2, 3])

    def beber_barril(self):
        self.nivel_borrachera = min(self.nivel_borrachera + 2, 10)
        self.estado = "bebiendo"
        self.tiempo_estado = 90
        self.barriles_agarrados += 1
        self.gestor.reproducir_sonido('beber')
        if self.barriles_agarrados % 3 == 0:
            self.estado = "celebrando"
            self.tiempo_estado = 60

    def _tambalear(self):
        intensidad = max(1, self.nivel_borrachera // 2)
        self.vel_x = random.choice(range(-intensidad - 1, intensidad + 2))
        if self.nivel_borrachera >= 7 and self.en_suelo and random.randint(0, 45) == 0:
            self.vel_y = SALTO * MULTIPLICADOR_SALTO

    def dibujar(self, pantalla):
        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 28, 8)
        
        x, y = self.rect.x, self.rect.y
        offset_x = 0
        if self.nivel_borrachera >= 5:
            offset_x = int(math.sin(self.anim_frame * 0.25) * (self.nivel_borrachera // 2))
        bx = x + offset_x
        
        pygame.draw.rect(pantalla, COLORES['blanco'], (bx, y + 8, 32, 24))
        pygame.draw.rect(pantalla, COLORES['celeste'], (bx, y + 8, 10, 24))
        pygame.draw.rect(pantalla, COLORES['celeste'], (bx + 22, y + 8, 10, 24))
        
        if self.nivel_borrachera >= 4:
            brazo_off = int(math.sin(self.anim_frame * 0.2) * 4)
        else:
            brazo_off = 0
        pygame.draw.rect(pantalla, (255, 200, 180), (bx - 4, y + 12 + brazo_off, 6, 12))
        pygame.draw.rect(pantalla, (255, 200, 180), (bx + 30, y + 12 - brazo_off, 6, 12))
        
        r = 255
        g = max(140, 220 - self.nivel_borrachera * 8)
        b = max(120, 180 - self.nivel_borrachera * 6)
        pygame.draw.circle(pantalla, (r, g, b), (bx + 16, y + 8), 10)
        
        if self.nivel_borrachera > 3:
            pygame.draw.arc(pantalla, COLORES['negro'], (bx + 8, y + 4, 6, 5), 0, math.pi, 2)
            pygame.draw.arc(pantalla, COLORES['negro'], (bx + 18, y + 4, 6, 5), 0, math.pi, 2)
            if self.nivel_borrachera >= 6 and self.anim_frame % 20 < 10:
                for sx, sy in [(bx + 26, y - 4), (bx + 32, y - 8)]:
                    pygame.draw.circle(pantalla, COLORES['amarillo'], (sx, sy), 3)
                    pygame.draw.circle(pantalla, COLORES['amarillo'], (sx - 2, sy + 1), 2)
                    pygame.draw.circle(pantalla, COLORES['amarillo'], (sx + 2, sy + 1), 2)
        else:
            pygame.draw.circle(pantalla, COLORES['negro'], (bx + 13, y + 7), 2)
            pygame.draw.circle(pantalla, COLORES['negro'], (bx + 19, y + 7), 2)
            pygame.draw.circle(pantalla, COLORES['blanco'], (bx + 12, y + 6), 1)
            pygame.draw.circle(pantalla, COLORES['blanco'], (bx + 18, y + 6), 1)
        
        if self.estado == "celebrando":
            pygame.draw.arc(pantalla, COLORES['rojo'], (bx + 10, y + 11, 12, 7), 0, math.pi, 2)
            self.gestor.dibujar_texto(pantalla, "¡OLE!", 16, COLORES['amarillo'], 
                                      bx + 32, y - 6, sombra=True)
        else:
            pygame.draw.arc(pantalla, COLORES['rojo'], (bx + 10, y + 12, 12, 6), math.pi, 0, 2)
        
        pygame.draw.circle(pantalla, (255, 150, 150), (bx + 6, y + 10), 4)
        pygame.draw.circle(pantalla, (255, 150, 150), (bx + 26, y + 10), 4)
        
        if self.nivel_borrachera > 0:
            pygame.draw.rect(pantalla, (60, 40, 20), (bx + 26, y + 14, 6, 14))
            pygame.draw.rect(pantalla, (200, 180, 100), (bx + 26, y + 14, 6, 14), 1)
            pygame.draw.ellipse(pantalla, (200, 180, 100), (bx + 24, y + 12, 10, 6))
            pygame.draw.ellipse(pantalla, (150, 130, 70), (bx + 26, y + 13, 6, 4))
        
        ancho_b = int(32 * (self.nivel_borrachera / 10))
        pygame.draw.rect(pantalla, COLORES['negro'], (x, y - 12, 32, 6))
        col_b = COLORES['verde'] if self.nivel_borrachera < 5 else COLORES['rojo']
        pygame.draw.rect(pantalla, col_b, (x, y - 12, ancho_b, 6))
        pygame.draw.rect(pantalla, COLORES['blanco'], (x, y - 12, 32, 6), 1)
        
        if self.estado == "bebiendo" and self.anim_frame % 20 < 10:
            self.gestor.dibujar_texto(pantalla, "🍺", 20, COLORES['amarillo'], bx + 40, y + 4)