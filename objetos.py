"""
KONG ARGENTINO - OBJETOS DEL JUEGO v3.1
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
        # Sombra
        pygame.draw.rect(pantalla, (40, 30, 20, 60), (self.x_visual + 2, self.y_visual + 4, 16, self.alto_visual))
        
        # Barandas
        for i in range(0, self.alto_visual, 12):
            pygame.draw.rect(pantalla, (150, 100, 60), (self.x_visual - 2, self.y_visual + i, 20, 2))
            pygame.draw.rect(pantalla, (200, 150, 100), (self.x_visual - 2, self.y_visual + i, 20, 1))
        
        # Postes
        pygame.draw.rect(pantalla, (101, 67, 33), (self.x_visual - 2, self.y_visual, 4, self.alto_visual))
        pygame.draw.rect(pantalla, (101, 67, 33), (self.x_visual + 14, self.y_visual, 4, self.alto_visual))
        pygame.draw.rect(pantalla, (130, 90, 50), (self.x_visual - 2, self.y_visual, 4, 3))
        pygame.draw.rect(pantalla, (130, 90, 50), (self.x_visual + 14, self.y_visual, 4, 3))
        
        # Escalones
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
        self.bounces = 0
        self.estado = "normal"  # normal, rodando, explotando
        
        # Crear frames de rotación (8 direcciones)
        self.frames = []
        self._generar_frames_barril()

        if not es_item:
            self.vel_x = random.choice([-1, 1]) * (2.0 * vel_mult)
            self.vel_y = -2  # Empieza con impulso hacia arriba
            self.gravedad = 0.5
            self.bounces = 0
            self.max_bounces = 8
            self.rotacion_vel = 4 * (1 if self.vel_x > 0 else -1)
        else:
            self.vel_x = 0
            self.vel_y = 0

    def _generar_frames_barril(self):
        """Genera 8 frames de rotación para el barril"""
        for i in range(8):
            surf = pygame.Surface((TAMANO_BARRIL[0], TAMANO_BARRIL[1]), pygame.SRCALPHA)
            ang = i * 45
            
            # Cuerpo del barril
            cx, cy = 16, 16
            pygame.draw.ellipse(surf, (101, 67, 33), (2, 4, 28, 24))
            pygame.draw.ellipse(surf, (130, 90, 50), (4, 6, 24, 20))
            
            # Aros metálicos
            if i % 2 == 0:
                pygame.draw.ellipse(surf, (180, 160, 80), (2, 8, 28, 6), 2)
                pygame.draw.ellipse(surf, (180, 160, 80), (2, 18, 28, 6), 2)
            else:
                pygame.draw.ellipse(surf, (180, 160, 80), (2, 6, 28, 6), 2)
                pygame.draw.ellipse(surf, (180, 160, 80), (2, 20, 28, 6), 2)
            
            # Aro central
            pygame.draw.ellipse(surf, (200, 180, 100), (2, 13, 28, 6), 2)
            
            # Vetas de madera
            for v in range(3):
                vx = 6 + v * 8 + (i * 2) % 6
                vy = 8 + v * 5
                pygame.draw.line(surf, (80, 50, 25), (vx, vy), (vx + 6, vy + 8), 1)
            
            # Reflejo
            pygame.draw.ellipse(surf, (255, 255, 255, 30), (6, 5, 10, 8))
            pygame.draw.ellipse(surf, (255, 255, 255, 60), (10, 5, 6, 4))
            
            # Sombra interior
            pygame.draw.ellipse(surf, (40, 30, 20, 30), (2, 20, 28, 8))
            
            # Rotar
            rot = pygame.transform.rotate(surf, ang)
            self.frames.append(rot)

    def update(self, plataformas, escaleras):
        self.anim_frame += 1
        
        if not self.es_item:
            # Rotación
            self.angulo = (self.angulo + self.rotacion_vel) % 360
            
            # Gravedad
            self.vel_y += self.gravedad
            if self.vel_y > 12:
                self.vel_y = 12

            self.rect.x += int(self.vel_x)
            self.rect.y += int(self.vel_y)

            # Colisiones con plataformas
            for p in plataformas:
                if self.rect.colliderect(p.rect):
                    if self.vel_y > 0:
                        # Rebote en el suelo
                        self.rect.bottom = p.rect.top
                        self.vel_y = -abs(self.vel_y) * 0.6
                        self.bounces += 1
                        
                        # Efecto de partículas al rebotar
                        if self.bounces < self.max_bounces:
                            for _ in range(3):
                                self.gestor.particulas.append({
                                    'x': self.rect.centerx + random.randint(-5, 5),
                                    'y': self.rect.bottom,
                                    'vx': random.uniform(-1.5, 1.5),
                                    'vy': random.uniform(-3, -0.5),
                                    'vida': 10,
                                    'vida_max': 10,
                                    'color': (150, 100, 60),
                                    'tam': random.randint(2, 4)
                                })
                    elif self.vel_y < 0:
                        # Rebote en el techo
                        self.rect.top = p.rect.bottom
                        self.vel_y = abs(self.vel_y) * 0.5

            # Colisiones con escaleras (pueden rodar sobre ellas)
            for e in escaleras:
                if self.rect.colliderect(e.rect_deteccion):
                    # Si está en una escalera, reduce la gravedad
                    self.vel_y *= 0.98

            # Límites laterales
            if self.rect.left <= 0:
                self.rect.left = 0
                self.vel_x = abs(self.vel_x)
                self.rotacion_vel = abs(self.rotacion_vel)
            if self.rect.right >= ANCHO:
                self.rect.right = ANCHO
                self.vel_x = -abs(self.vel_x)
                self.rotacion_vel = -abs(self.rotacion_vel)

            # Si rebota demasiado, se detiene
            if self.bounces >= self.max_bounces:
                self.vel_y = 0
                if abs(self.vel_x) < 0.5:
                    self.vel_x = 0

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y
        
        if self.es_item:
            # Cerveza coleccionable con animación flotante
            off = int(math.sin(self.anim_frame * 0.1) * 4)
            
            # Brillo
            if self.anim_frame % 30 < 15:
                pygame.draw.circle(pantalla, (255, 220, 100, 30), (x + 10, y + 8 + off), 12)
            
            # Cuerpo
            pygame.draw.rect(pantalla, (101, 67, 33), (x + 2, y + 2 + off, 16, 16))
            pygame.draw.rect(pantalla, (130, 90, 50), (x + 3, y + 3 + off, 14, 14))
            
            # Etiqueta
            pygame.draw.rect(pantalla, (200, 180, 100), (x + 4, y + 4 + off, 12, 12), 1)
            pygame.draw.rect(pantalla, (255, 220, 50), (x + 5, y + 7 + off, 10, 2))
            pygame.draw.rect(pantalla, (255, 220, 50), (x + 5, y + 10 + off, 10, 2))
            
            # Espuma
            pygame.draw.ellipse(pantalla, (240, 230, 200), (x + 3, y - 2 + off, 12, 5))
            pygame.draw.ellipse(pantalla, (200, 190, 160), (x + 5, y - 1 + off, 8, 3))
            
            # Brillo
            pygame.draw.ellipse(pantalla, (255, 255, 255, 40), (x + 4, y + 3 + off, 5, 4))
        else:
            # Sombra del barril
            self.gestor.dibujar_sombra(pantalla, x + 16, y + 32, 30, 8, alpha=60)
            
            # Barril con rotación
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
        
        # Glow pulsante
        if self.anim_frame % 20 < 10:
            alpha = 80
            radio = 20
        else:
            alpha = 30
            radio = 14
        glow = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (0, 255, 0, alpha), (radio, radio), radio)
        pantalla.blit(glow, (x + 8 - radio, y + 8 + off - radio))
        
        # Cuerpo del mate
        pygame.draw.rect(pantalla, (60, 140, 60), (x + 1, y + 2 + off, 22, 20))
        pygame.draw.rect(pantalla, (80, 180, 80), (x + 3, y + 4 + off, 18, 16))
        pygame.draw.rect(pantalla, (100, 200, 100), (x + 4, y + 5 + off, 16, 6))
        
        # Boca del mate
        pygame.draw.ellipse(pantalla, (150, 100, 50), (x + 6, y + off, 12, 6))
        pygame.draw.ellipse(pantalla, (180, 130, 70), (x + 7, y + 1 + off, 10, 4))
        
        # Bombilla
        pygame.draw.line(pantalla, (180, 130, 70), (x + 14, y + off), (x + 20, y - 6 + off), 3)
        pygame.draw.circle(pantalla, (200, 150, 80), (x + 20, y - 6 + off), 3)
        
        # Yerba
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

    def update(self):
        self.anim_frame += 1
        self.ondeo = int(math.sin(self.anim_frame * 0.08) * 4)

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y
        o = self.ondeo
        
        self.gestor.dibujar_sombra(pantalla, x + 16, y + 38, 28, 8, alpha=60)
        
        # --- VESTIDO ---
        pygame.draw.rect(pantalla, (200, 220, 255), (x + 4, y + 12 + o, 24, 20))
        pygame.draw.rect(pantalla, (180, 200, 235), (x + 6, y + 14 + o, 20, 16))
        
        for i in range(3):
            px = x + 2 + i * 8
            py = y + 26 + o + i * 2
            pygame.draw.ellipse(pantalla, (200, 220, 255), (px, py, 24 - i * 4, 8 - i))
            pygame.draw.ellipse(pantalla, (180, 200, 235), (px + 2, py + 1, 20 - i * 4, 6 - i))
        
        pygame.draw.rect(pantalla, (255, 215, 0), (x + 10, y + 20 + o, 12, 4))
        
        # Brazos
        pygame.draw.rect(pantalla, (255, 220, 200), (x, y + 16 + o, 4, 12))
        pygame.draw.rect(pantalla, (255, 220, 200), (x + 28, y + 16 + o, 4, 12))
        pygame.draw.circle(pantalla, (255, 220, 200), (x + 2, y + 28 + o), 3)
        pygame.draw.circle(pantalla, (255, 220, 200), (x + 30, y + 28 + o), 3)
        
        # --- CABEZA ---
        pygame.draw.circle(pantalla, (255, 220, 200), (x + 16, y + 8 + o), 10)
        
        # Cabello
        pygame.draw.ellipse(pantalla, (80, 50, 30), (x + 4, y - 2 + o, 24, 12))
        pygame.draw.ellipse(pantalla, (100, 70, 50), (x + 6, y - 1 + o, 20, 10))
        
        # Moño
        pygame.draw.ellipse(pantalla, (80, 50, 30), (x + 22, y - 4 + o, 10, 6))
        pygame.draw.ellipse(pantalla, (80, 50, 30), (x + 26, y - 2 + o, 8, 8))
        
        # --- CORONA ---
        pygame.draw.rect(pantalla, (255, 215, 0), (x + 6, y - 2 + o, 20, 4))
        for i, px in enumerate([x + 8, x + 13, x + 18, x + 23]):
            alt = 6 if i % 2 == 0 else 4
            pygame.draw.polygon(pantalla, (255, 215, 0), 
                               [(px, y - 2 + o), (px + 2, y - 4 - alt + o), (px + 4, y - 2 + o)])
        pygame.draw.circle(pantalla, (255, 100, 100), (x + 10, y - 2 + o), 2)
        pygame.draw.circle(pantalla, (100, 100, 255), (x + 16, y - 3 + o), 2)
        pygame.draw.circle(pantalla, (100, 255, 100), (x + 22, y - 2 + o), 2)
        
        # --- OJOS ---
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
        
        # Pestañas
        for ex in [12, 20]:
            pygame.draw.line(pantalla, (50, 50, 150), (x + ex - 2, y + 5 + o), (x + ex - 1, y + 3 + o), 1)
            pygame.draw.line(pantalla, (50, 50, 150), (x + ex + 2, y + 5 + o), (x + ex + 3, y + 3 + o), 1)
        
        # --- BOCA ---
        pygame.draw.arc(pantalla, (200, 50, 50), (x + 11, y + 10 + o, 10, 6), 0, math.pi, 2)
        pygame.draw.arc(pantalla, (220, 80, 80), (x + 11, y + 11 + o, 10, 4), 0, math.pi, 1)
        
        # --- MENSAJE DE AYUDA ---
        if self.anim_frame % 90 < 40:
            self.gestor.dibujar_texto(pantalla, "¡AYUDA!", 14, COLORES['rojo'], 
                                      x + 34, y + 2 + o, sombra=True)
            heart_y = y - 10 + o + int(math.sin(self.anim_frame * 0.1) * 3)
            pygame.draw.polygon(pantalla, (255, 100, 100),
                               [(x + 30, heart_y), (x + 27, heart_y - 4), 
                                (x + 27, heart_y - 8), (x + 30, heart_y - 10),
                                (x + 33, heart_y - 8), (x + 33, heart_y - 4), 
                                (x + 30, heart_y)])

class KongCervecero(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor, nivel=1):
        super().__init__()
        self.gestor = gestor
        self.nivel = nivel
        self.rect = pygame.Rect(x, y, TAMANO_KONG[0], TAMANO_KONG[1])
        self.tiempo_barril = 0
        self.enojado = False
        self.tiempo_enojado = 0
        self.direccion = 1
        cfg = DIFICULTAD_NIVEL.get(nivel, DIFICULTAD_NIVEL[5])
        self.vel_x = cfg['vel_kong']
        self.x_inicial = x
        self.rango_movimiento = 180
        self.anim_frame = 0
        self.rugido_frame = 0
        self.shake_x = 0
        self.shake_y = 0
        self.tiempo_entre_barriles = 0
        
        # Generar frames de animación
        self.frames_idle = []
        self.frames_roar = []
        self.frames_throw = []
        self._generar_frames()

    def _generar_frames(self):
        for i in range(6):
            surf = self._dibujar_kong(i, 'idle')
            self.frames_idle.append(surf)
            surf = self._dibujar_kong(i, 'roar')
            self.frames_roar.append(surf)
            surf = self._dibujar_kong(i, 'throw')
            self.frames_throw.append(surf)

    def _dibujar_kong(self, frame, estado):
        surf = pygame.Surface((TAMANO_KONG[0] + 30, TAMANO_KONG[1] + 30), pygame.SRCALPHA)
        x, y = 15, 15
        
        # --- SOMBRA ---
        pygame.draw.ellipse(surf, (0, 0, 0, 60), (x + 5, y + 65, 70, 15))
        
        # --- CUERPO ---
        pygame.draw.ellipse(surf, (60, 40, 30), (x + 15, y + 35, 50, 40))
        pygame.draw.ellipse(surf, (80, 55, 40), (x + 18, y + 38, 44, 34))
        
        for px in range(6):
            for py in range(4):
                if (px + py) % 2 == 0:
                    pygame.draw.circle(surf, (100, 70, 50), 
                                     (x + 28 + px * 5, y + 42 + py * 6), 2)
        
        # --- BRAZOS ---
        if estado == 'throw':
            brazo_off = -10
        elif estado == 'roar':
            brazo_off = -5
        else:
            brazo_off = int(math.sin(frame * 0.5) * 2)
        
        pygame.draw.line(surf, (70, 45, 35), 
                        (x + 20, y + 40), (x - 5 + brazo_off, y + 55), 12)
        pygame.draw.circle(surf, (80, 55, 40), (x - 5 + brazo_off, y + 55), 7)
        for d in [-3, 0, 3]:
            pygame.draw.circle(surf, (80, 55, 40), (x - 8 + brazo_off + d, y + 58), 3)
        
        if estado == 'throw':
            brazo_off2 = 15
            botella_off = 10
        elif estado == 'roar':
            brazo_off2 = 5
            botella_off = 5
        else:
            brazo_off2 = int(math.sin(frame * 0.5 + 1) * 2)
            botella_off = 0
        
        pygame.draw.line(surf, (70, 45, 35), 
                        (x + 60, y + 40), (x + 85 + brazo_off2, y + 45), 12)
        pygame.draw.circle(surf, (80, 55, 40), (x + 85 + brazo_off2, y + 45), 7)
        
        bx = x + 80 + brazo_off2 + botella_off
        by = y + 35
        pygame.draw.rect(surf, (60, 40, 20), (bx, by, 12, 20))
        pygame.draw.rect(surf, (200, 180, 100), (bx, by, 12, 20), 1)
        pygame.draw.ellipse(surf, (200, 180, 100), (bx - 1, by - 4, 14, 8))
        pygame.draw.ellipse(surf, (150, 130, 70), (bx + 2, by - 2, 8, 4))
        pygame.draw.rect(surf, (255, 220, 50), (bx + 2, by + 6, 8, 4))
        pygame.draw.rect(surf, (255, 220, 50), (bx + 2, by + 12, 8, 4))
        
        # --- CABEZA ---
        if estado == 'roar':
            boca_off = 8
            boca_abierta = True
        else:
            boca_off = 0
            boca_abierta = False
        
        pygame.draw.circle(surf, (70, 45, 35), (x + 40, y + 22), 25)
        pygame.draw.circle(surf, (90, 60, 45), (x + 40, y + 24), 22)
        
        if boca_abierta:
            pygame.draw.ellipse(surf, (60, 35, 25), (x + 28, y + 30, 24, 16))
            pygame.draw.ellipse(surf, (80, 50, 35), (x + 30, y + 32, 20, 12))
        else:
            pygame.draw.ellipse(surf, (60, 35, 25), (x + 28, y + 30, 24, 8))
        
        if boca_abierta:
            pygame.draw.ellipse(surf, (200, 50, 50), (x + 32, y + 34, 16, 10))
            for d in range(4):
                pygame.draw.rect(surf, (255, 255, 255), (x + 34 + d * 4, y + 34, 3, 4))
                pygame.draw.rect(surf, (255, 255, 255), (x + 34 + d * 4, y + 38, 3, 4))
            pygame.draw.polygon(surf, (255, 255, 255), 
                               [(x + 30, y + 32), (x + 33, y + 38), (x + 36, y + 32)])
            pygame.draw.polygon(surf, (255, 255, 255), 
                               [(x + 50, y + 32), (x + 53, y + 38), (x + 56, y + 32)])
        else:
            pygame.draw.arc(surf, (100, 60, 40), (x + 32, y + 32, 16, 8), 0, math.pi, 2)
        
        # --- OREJAS ---
        for ox in [8, 56]:
            pygame.draw.circle(surf, (60, 35, 25), (x + ox, y + 10), 10)
            pygame.draw.circle(surf, (90, 60, 45), (x + ox, y + 12), 7)
            pygame.draw.circle(surf, (80, 50, 35), (x + ox, y + 13), 4)
        
        # --- OJOS ---
        ojo_y = 18 + boca_off // 2
        pygame.draw.circle(surf, (255, 255, 255), (x + 32, y + ojo_y), 8)
        pygame.draw.circle(surf, (255, 255, 255), (x + 48, y + ojo_y), 8)
        
        if self.gestor.argentino:
            dx = self.gestor.argentino.rect.centerx - (self.rect.x + 40)
            dy = self.gestor.argentino.rect.centery - (self.rect.y + 40)
            ang = math.atan2(dy, dx)
            dist = min(3, math.hypot(dx, dy) * 0.01)
            px1 = x + 32 + math.cos(ang) * dist * 2
            py1 = y + ojo_y + math.sin(ang) * dist * 2
            px2 = x + 48 + math.cos(ang) * dist * 2
            py2 = y + ojo_y + math.sin(ang) * dist * 2
        else:
            px1, py1 = x + 33, y + ojo_y
            px2, py2 = x + 49, y + ojo_y
        
        if self.enojado:
            color_iris = (200, 50, 50)
        else:
            color_iris = (100, 80, 50)
        pygame.draw.circle(surf, color_iris, (int(px1), int(py1)), 4)
        pygame.draw.circle(surf, color_iris, (int(px2), int(py2)), 4)
        
        pygame.draw.circle(surf, (20, 20, 20), (int(px1 + 1), int(py1 + 1)), 2)
        pygame.draw.circle(surf, (20, 20, 20), (int(px2 + 1), int(py2 + 1)), 2)
        
        pygame.draw.circle(surf, (255, 255, 255), (int(px1 - 1), int(py1 - 2)), 1)
        pygame.draw.circle(surf, (255, 255, 255), (int(px2 - 1), int(py2 - 2)), 1)
        
        # --- CEJAS ---
        if self.enojado:
            pygame.draw.line(surf, (30, 30, 30), (x + 24, y + 12 + boca_off//2), 
                           (x + 36, y + 16 + boca_off//2), 3)
            pygame.draw.line(surf, (30, 30, 30), (x + 44, y + 16 + boca_off//2), 
                           (x + 56, y + 12 + boca_off//2), 3)
        else:
            pygame.draw.line(surf, (30, 30, 30), (x + 26, y + 14 + boca_off//2), 
                           (x + 36, y + 12 + boca_off//2), 2)
            pygame.draw.line(surf, (30, 30, 30), (x + 44, y + 12 + boca_off//2), 
                           (x + 54, y + 14 + boca_off//2), 2)
        
        # --- VELLO FACIAL ---
        for fx, fy in [(x + 20, y + 30), (x + 60, y + 30), (x + 25, y + 35), (x + 55, y + 35)]:
            pygame.draw.line(surf, (50, 30, 20), (fx, fy), (fx + 2, fy + 4), 1)
        
        # --- EXPRESIÓN DE RUGIDO ---
        if estado == 'roar':
            for i in range(3):
                ang = math.radians(30 + i * 20)
                lx = x + 70 + math.cos(ang) * 10
                ly = y + 20 + math.sin(ang) * 10
                pygame.draw.line(surf, (200, 100, 50), (lx, ly), 
                               (lx + math.cos(ang) * 15, ly + math.sin(ang) * 15), 2)
            pygame.draw.line(surf, (200, 100, 50), (x + 70, y + 35), (x + 85, y + 38), 2)
            pygame.draw.line(surf, (200, 100, 50), (x + 70, y + 40), (x + 82, y + 44), 2)
        
        return surf

    def update(self, plataformas):
        self.anim_frame += 1
        self.tiempo_barril += 1
        
        # Movimiento horizontal
        self.rect.x += self.vel_x * self.direccion
        
        if self.enojado:
            self.shake_x = random.randint(-2, 2)
            self.shake_y = random.randint(-2, 2)
        else:
            self.shake_x = 0
            self.shake_y = 0

        if self.rect.x > self.x_inicial + self.rango_movimiento:
            self.rect.x = self.x_inicial + self.rango_movimiento
            self.direccion = -1
        if self.rect.x < self.x_inicial - self.rango_movimiento:
            self.rect.x = self.x_inicial - self.rango_movimiento
            self.direccion = 1

        if self.tiempo_enojado > 0:
            self.tiempo_enojado -= 1
            self.enojado = True
        else:
            self.enojado = False

        if self.rugido_frame > 0:
            self.rugido_frame -= 1

    def lanzar_barril(self):
        cfg = DIFICULTAD_NIVEL.get(self.nivel, DIFICULTAD_NIVEL[5])
        vel_mult = cfg['vel_barril'] / 2.0
        barril = BarrilCerveza(self.rect.centerx - 16, self.rect.bottom - 10,
                               self.gestor, es_item=False, vel_mult=vel_mult)
        barril.vel_x = (3 * vel_mult) * self.direccion
        barril.vel_y = -4  # Lanzado hacia arriba
        return barril

    def set_mario_cerca(self, cerca):
        if cerca and not self.enojado:
            self.tiempo_enojado = 60
            self.rugido_frame = 60

    def get_tiempo_barril(self):
        cfg = DIFICULTAD_NIVEL.get(self.nivel, DIFICULTAD_NIVEL[5])
        # Si está enojado, lanza más rápido
        base = cfg['cadencia']
        if self.enojado:
            base = int(base * 0.7)
        return base

    def dibujar(self, pantalla):
        x, y = self.rect.x + self.shake_x, self.rect.y + self.shake_y
        
        t = pygame.time.get_ticks()
        frame_idx = (t // 200) % len(self.frames_idle)
        
        if self.rugido_frame > 0:
            frame = self.frames_roar[frame_idx % len(self.frames_roar)]
        elif self.tiempo_barril > self.get_tiempo_barril() - 20:
            frame = self.frames_throw[frame_idx % len(self.frames_throw)]
        else:
            frame = self.frames_idle[frame_idx % len(self.frames_idle)]
        
        if self.direccion == -1:
            frame = pygame.transform.flip(frame, True, False)
        
        pantalla.blit(frame, (x - 15, y - 10))
        
        # Partículas de rugido
        if self.rugido_frame > 0 and self.rugido_frame % 10 < 5:
            for _ in range(3):
                self.gestor.particulas.append({
                    'x': x + random.randint(50, 80),
                    'y': y + random.randint(20, 40),
                    'vx': random.uniform(1, 4),
                    'vy': random.uniform(-2, 2),
                    'vida': 15,
                    'vida_max': 15,
                    'color': (200, 150, 50),
                    'tam': random.randint(2, 5)
                })