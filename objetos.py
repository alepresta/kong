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

# =========================================================================
#  NUEVO: KONG REDISEÑADO COMO GORILA
# =========================================================================
# =========================================================================
#  KONG REDISEÑADO - GORILA CON BRAZOS LEVANTADOS (COMO COLGANDO)
# =========================================================================
# =========================================================================
#  KONG ESTILO DONKEY KONG CON BRAZOS LEVANTADOS (COMO COLGANDO DE RAMA)
# =========================================================================
class KongCervecero(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor, nivel=1):
        super().__init__()
        self.gestor = gestor
        self.nivel = nivel
        self.rect = pygame.Rect(x, y, 110, 120)  # Tamaño más grande y proporcional a DK
        
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

        # Frames de animación
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
        """Dibuja a Donkey Kong con brazos levantados (postura de colgar de rama)"""
        surf = pygame.Surface((180, 160), pygame.SRCALPHA)
        x, y = 35, 20

        # === SOMBRA ===
        pygame.draw.ellipse(surf, (0, 0, 0, 100), (x + 5, y + 115, 95, 22))

        # === CUERPO ===
        # Torso musculoso
        pygame.draw.ellipse(surf, (45, 28, 18), (x + 18, y + 55, 78, 68))   # Pelaje base oscuro
        pygame.draw.ellipse(surf, (65, 42, 28), (x + 23, y + 58, 68, 58))   # Pelaje medio
        
        # Barriga más clara
        pygame.draw.ellipse(surf, (130, 85, 55), (x + 32, y + 68, 48, 45))

        # === CORBATA ROJA ICÓNICA ===
        tie_points = [(x+48, y+72), (x+38, y+88), (x+50, y+102), (x+62, y+88), (x+53, y+72)]
        pygame.draw.polygon(surf, (200, 10, 10), tie_points)
        pygame.draw.circle(surf, (180, 0, 0), (x + 50, y + 82), 11)  # Nudo
        
        # Letras "DK"
        pygame.draw.line(surf, (255, 255, 255), (x + 44, y + 78), (x + 44, y + 87), 3)
        pygame.draw.line(surf, (255, 255, 255), (x + 55, y + 78), (x + 55, y + 87), 3)
        pygame.draw.line(surf, (255, 255, 255), (x + 55, y + 82), (x + 59, y + 82), 3)

        # === BRAZOS (SIEMPRE LEVANTADOS, COMO COLGANDO DE RAMA) ===
        color_brazo = (45, 28, 18)
        color_mano = (60, 38, 25)

        # Brazo izquierdo (siempre levantado)
        # En rugido, ligeramente más arriba
        izq_y = y + 22 if estado == 'roar' else y + 28
        pygame.draw.line(surf, color_brazo, (x + 25, y + 65), (x + 18, izq_y), 24)
        pygame.draw.circle(surf, color_mano, (x + 18, izq_y), 14)
        # Dedos colgando
        for d in [-6, 0, 6]:
            pygame.draw.circle(surf, color_mano, (x + 16 + d, izq_y + 3), 5)

        # Brazo derecho (varía según estado)
        if estado == 'throw':
            # Brazo extendido hacia adelante para lanzar
            pygame.draw.line(surf, color_brazo, (x + 85, y + 65), (x + 135, y + 58), 24)
            pygame.draw.circle(surf, color_mano, (x + 135, y + 58), 14)
            pygame.draw.circle(surf, (35, 22, 15), (x + 140, y + 56), 11)  # Puño
            # Barril en la mano (para el frame de lanzamiento)
            bx = x + 130
            by = y + 45
            pygame.draw.rect(surf, (80, 55, 30), (bx, by, 18, 24))
            pygame.draw.rect(surf, (140, 100, 60), (bx+2, by+2, 14, 20))
            pygame.draw.ellipse(surf, (180, 150, 80), (bx, by-2, 18, 6))
            pygame.draw.ellipse(surf, (200, 180, 100), (bx+2, by, 14, 4))
            pygame.draw.rect(surf, (220, 200, 100), (bx+3, by+6, 12, 3))
            pygame.draw.rect(surf, (220, 200, 100), (bx+3, by+14, 12, 3))
        else:
            # Brazo derecho levantado (postura normal)
            der_y = y + 22 if estado == 'roar' else y + 28
            pygame.draw.line(surf, color_brazo, (x + 85, y + 65), (x + 95, der_y), 24)
            pygame.draw.circle(surf, color_mano, (x + 95, der_y), 14)
            # Dedos colgando
            for d in [-6, 0, 6]:
                pygame.draw.circle(surf, color_mano, (x + 93 + d, der_y + 3), 5)

        # === PIERNAS ===
        pygame.draw.ellipse(surf, (45, 28, 18), (x + 25, y + 110, 30, 38))
        pygame.draw.ellipse(surf, (45, 28, 18), (x + 58, y + 110, 30, 38))
        pygame.draw.ellipse(surf, (65, 42, 28), (x + 29, y + 115, 22, 28))
        pygame.draw.ellipse(surf, (65, 42, 28), (x + 62, y + 115, 22, 28))

        # === CABEZA ===
        # Cabeza base
        pygame.draw.circle(surf, (55, 35, 22), (x + 55, y + 38), 42)
        # Frente prominente
        pygame.draw.ellipse(surf, (55, 35, 22), (x + 28, y + 18, 54, 32))

        # Hocico
        pygame.draw.ellipse(surf, (80, 55, 38), (x + 33, y + 42, 46, 28))
        
        # === OREJAS ===
        pygame.draw.circle(surf, (50, 32, 20), (x + 18, y + 32), 14)
        pygame.draw.circle(surf, (50, 32, 20), (x + 92, y + 32), 14)

        # === CEJAS ENFADADAS ===
        eyebrow_y = y + 23 if estado == 'roar' else y + 26
        pygame.draw.line(surf, (25, 15, 10), (x + 28, eyebrow_y - 3), (x + 48, eyebrow_y + 3), 8)
        pygame.draw.line(surf, (25, 15, 10), (x + 62, eyebrow_y + 3), (x + 82, eyebrow_y - 4), 8)

        # === OJOS ===
        ojo_y = 32
        if estado == 'roar':
            ojo_y += 2

        pygame.draw.ellipse(surf, (255, 245, 210), (x + 36, y + ojo_y, 14, 12))
        pygame.draw.ellipse(surf, (255, 245, 210), (x + 64, y + ojo_y, 14, 12))

        # Pupilas (miran al jugador)
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

        # === NARIZ ===
        pygame.draw.ellipse(surf, (45, 28, 18), (x + 46, y + 48, 19, 11))
        pygame.draw.circle(surf, (25, 15, 10), (x + 50, y + 50), 3)
        pygame.draw.circle(surf, (25, 15, 10), (x + 60, y + 50), 3)

        # === BOCA ===
        if estado == 'roar':
            pygame.draw.ellipse(surf, (30, 12, 8), (x + 37, y + 58, 36, 20))
            # Dientes
            for i in range(5):
                pygame.draw.rect(surf, (255, 250, 230), (x + 40 + i*6, y + 58, 4, 9))
        else:
            pygame.draw.arc(surf, (30, 12, 8), (x + 37, y + 57, 34, 16), 0.2, math.pi - 0.3, 6)

        # === PELO DE LA CABEZA ===
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

        # Rebote en límites
        if self.rect.x > self.x_inicial + self.rango_movimiento:
            self.rect.x = self.x_inicial + self.rango_movimiento
            self.direccion = -1
        if self.rect.x < self.x_inicial - self.rango_movimiento:
            self.rect.x = self.x_inicial - self.rango_movimiento
            self.direccion = 1

        # Enfado
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
        """Lanza un barril desde la mano derecha levantada (posición de lanzamiento)"""
        cfg = DIFICULTAD_NIVEL.get(self.nivel, DIFICULTAD_NIVEL[5])
        vel_mult = cfg['vel_barril'] / 2.0

        # Posición de la mano derecha en el frame de lanzamiento (según dirección)
        if self.direccion == 1:
            # Mirando a la derecha: la mano derecha extendida está en x + 135, y + 58 (ver dibujo)
            mano_x = self.rect.x + 135 - 9  # centro del barril
            mano_y = self.rect.y + 58 - 12   # ajuste para que el barril salga de la mano
        else:
            # Mirando a la izquierda: invertir coordenadas
            mano_x = self.rect.x + self.rect.width - 135 - 9
            mano_y = self.rect.y + 58 - 12

        barril = BarrilCerveza(mano_x, mano_y, self.gestor, es_item=False, vel_mult=vel_mult)
        barril.vel_x = (4.2 * vel_mult) * self.direccion
        barril.vel_y = -4.5  # sale con impulso hacia arriba, típico de DK
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
        
        # Partículas de rugido
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






# =========================================================================
#  NUEVO: HINCHA BORRACHITO (compañero del borracho)
# =========================================================================
class HinchaBorrachito(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, 32, 38)  # tamaño similar al jugador
        self.vidas = 3
        self.anim_frame = 0
        self.offset_y = 0
        self.tiempo_grito = 0
        self.gritando = False
        self.texto_grito = ""
        self.tiempo_texto = 0

    def update(self):
        self.anim_frame += 1
        self.offset_y = math.sin(self.anim_frame * 0.1) * 3
        
        # Grito cada 2 segundos (120 frames)
        self.tiempo_grito += 1
        if self.tiempo_grito >= 120:
            self.tiempo_grito = 0
            self.gritando = True
            self.tiempo_texto = 40  # dura 40 frames visible
        
        if self.tiempo_texto > 0:
            self.tiempo_texto -= 1
            if self.tiempo_texto == 0:
                self.gritando = False

    def recibir_golpe(self):
        """Reduce vidas y devuelve True si murió"""
        self.vidas -= 1
        if self.vidas <= 0:
            return True
        return False

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y + self.offset_y
        # Sombra
        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 28, 8)

        # --- CAMISETA CELESTE Y BLANCA (como Argentina) ---
        pygame.draw.rect(pantalla, (117, 190, 218), (x, y+12, 32, 22))  # celeste
        # Franjas blancas
        for i in range(0, 32, 8):
            pygame.draw.rect(pantalla, (255, 255, 255), (x+i, y+12, 4, 22))
        # Cuello
        pygame.draw.rect(pantalla, (255, 255, 255), (x+10, y+10, 12, 6))
        # Número 10 (como Maradona/Messi)
        self.gestor.dibujar_texto(pantalla, "10", 12, (0, 0, 0), x+12, y+18)

        # --- CABEZA ---
        pygame.draw.circle(pantalla, (255, 220, 200), (x+16, y+10), 12)
        # Pelo negro (corto)
        pygame.draw.ellipse(pantalla, (30, 30, 30), (x+4, y-2, 24, 10))
        # Ojos
        pygame.draw.circle(pantalla, (255, 255, 255), (x+12, y+8), 3)
        pygame.draw.circle(pantalla, (255, 255, 255), (x+20, y+8), 3)
        pygame.draw.circle(pantalla, (0, 0, 0), (x+13, y+9), 2)
        pygame.draw.circle(pantalla, (0, 0, 0), (x+21, y+9), 2)
        # Boca (feliz o gritando)
        if self.gritando:
            pygame.draw.ellipse(pantalla, (200, 50, 50), (x+12, y+14, 8, 6))
        else:
            pygame.draw.arc(pantalla, (200, 50, 50), (x+10, y+14, 12, 6), 0, math.pi, 2)

        # --- BRAZOS (alzados si grita) ---
        if self.gritando:
            # Brazos arriba
            pygame.draw.rect(pantalla, (255, 220, 200), (x-4, y+6, 5, 12))
            pygame.draw.rect(pantalla, (255, 220, 200), (x+31, y+6, 5, 12))
            # Puños
            pygame.draw.circle(pantalla, (255, 220, 200), (x-2, y+6), 4)
            pygame.draw.circle(pantalla, (255, 220, 200), (x+34, y+6), 4)
        else:
            pygame.draw.rect(pantalla, (255, 220, 200), (x-4, y+14, 5, 14))
            pygame.draw.rect(pantalla, (255, 220, 200), (x+31, y+14, 5, 14))

        # --- PIERNAS ---
        pygame.draw.rect(pantalla, (30, 60, 140), (x+4, y+34, 8, 8))
        pygame.draw.rect(pantalla, (30, 60, 140), (x+20, y+34, 8, 8))
        # Zapatillas
        pygame.draw.rect(pantalla, (40, 40, 40), (x+2, y+40, 12, 4))
        pygame.draw.rect(pantalla, (40, 40, 40), (x+18, y+40, 12, 4))

        # --- TEXTO DE GRITO ---
        if self.gritando:
            # Texto "VAMO VAMO ARGENTINA" con sombra
            texto = "🇦🇷 VAMO VAMO ARGENTINA 🇦🇷"
            # Sombra
            self.gestor.dibujar_texto(pantalla, texto, 18, (0,0,0), x+16, y-30, centro=True)
            # Texto principal (amarillo con borde)
            self.gestor.dibujar_texto(pantalla, texto, 18, COLORES['amarillo'], x+14, y-32, centro=True)
            
            # Partículas de confeti (simulado)
            if self.anim_frame % 5 == 0:
                self.gestor.particulas.append({
                    'x': x + random.randint(-10, 40),
                    'y': y - 20,
                    'vx': random.uniform(-1, 1),
                    'vy': random.uniform(-2, 0),
                    'vida': 20,
                    'vida_max': 20,
                    'color': random.choice([COLORES['celeste'], COLORES['blanco'], COLORES['amarillo']]),
                    'tam': random.randint(2, 4)
                })

        # Barra de vidas (3 corazones pequeños)
        for i in range(self.vidas):
            pygame.draw.circle(pantalla, COLORES['rojo'], (x+6 + i*10, y+50), 4)
            pygame.draw.circle(pantalla, COLORES['blanco'], (x+6 + i*10, y+49), 2)