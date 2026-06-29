"""
KONG ARGENTINO - Controles táctiles para móvil
"""
import pygame
import math
from constantes import *

class ControlTactil:
    """Gestiona los controles táctiles para dispositivos móviles"""
    
    def __init__(self):
        # Joystick virtual (lado izquierdo)
        self.joystick_activo = False
        self.joystick_id = None
        self.joystick_centro_x = 150
        self.joystick_centro_y = ALTO - 150
        self.joystick_radio = 80
        self.joystick_posicion = (0, 0)  # (x, y) relativo al centro (-1 a 1)
        
        # Botones (lado derecho)
        self.boton_salto = {
            'rect': pygame.Rect(ANCHO - 200, ALTO - 120, 80, 80),
            'activo': False,
            'color': (100, 200, 100),
            'texto': '🦘'
        }
        self.boton_ataque = {
            'rect': pygame.Rect(ANCHO - 100, ALTO - 120, 80, 80),
            'activo': False,
            'color': (200, 100, 100),
            'texto': '💥'
        }
        
        # Estado de teclas simuladas
        self.teclas = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_SPACE: False,
        }
        
        # Zona muerta del joystick
        self.zona_muerta = 0.15
        
    def procesar_evento(self, event):
        """Procesa eventos táctiles y actualiza el estado"""
        if event.type == pygame.FINGERDOWN:
            self._handle_finger_down(event)
        elif event.type == pygame.FINGERUP:
            self._handle_finger_up(event)
        elif event.type == pygame.FINGERMOTION:
            self._handle_finger_motion(event)
            
    def _handle_finger_down(self, event):
        """Maneja el inicio de un toque"""
        touch_id = event.finger_id
        x = event.x * ANCHO
        y = event.y * ALTO
        
        # Verificar si toca el joystick (lado izquierdo)
        if x < ANCHO // 2:
            dist = math.sqrt((x - self.joystick_centro_x)**2 + **(y - self.joystick_centro_y)2)
            if dist <= self.joystick_radio:
                self.joystick_activo = True
                self.joystick_id = touch_id
                self._actualizar_joystick(x, y)
                
        # Verificar si toca los botones (lado derecho)
        elif x >= ANCHO // 2:
            if self.boton_salto['rect'].collidepoint(x, y):
                self.boton_salto['activo'] = True
                self.teclas[pygame.K_SPACE] = True
            elif self.boton_ataque['rect'].collidepoint(x, y):
                self.boton_ataque['activo'] = True
                self.teclas[pygame.K_SPACE] = True  # Atacar también con espacio
                
    def _handle_finger_up(self, event):
        """Maneja el fin de un toque"""
        touch_id = event.finger_id
        x = event.x * ANCHO
        y = event.y * ALTO
        
        # Liberar joystick
        if self.joystick_activo and self.joystick_id == touch_id:
            self.joystick_activo = False
            self.joystick_id = None
            self.joystick_posicion = (0, 0)
            self.teclas[pygame.K_LEFT] = False
            self.teclas[pygame.K_RIGHT] = False
            self.teclas[pygame.K_UP] = False
            self.teclas[pygame.K_DOWN] = False
            
        # Liberar botones
        if self.boton_salto['activo']:
            self.boton_salto['activo'] = False
            self.teclas[pygame.K_SPACE] = False
            
        if self.boton_ataque['activo']:
            self.boton_ataque['activo'] = False
            self.teclas[pygame.K_SPACE] = False
            
    def _handle_finger_motion(self, event):
        """Maneja el movimiento de un toque"""
        if self.joystick_activo and event.finger_id == self.joystick_id:
            x = event.x * ANCHO
            y = event.y * ALTO
            self._actualizar_joystick(x, y)
            
    def _actualizar_joystick(self, x, y):
        """Actualiza la posición del joystick y las teclas simuladas"""
        dx = x - self.joystick_centro_x
        dy = y - self.joystick_centro_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        # Normalizar a [-1, 1]
        if dist > 0:
            max_dist = min(dist, self.joystick_radio)
            nx = (dx / dist) * (max_dist / self.joystick_radio)
            ny = (dy / dist) * (max_dist / self.joystick_radio)
        else:
            nx, ny = 0, 0
            
        self.joystick_posicion = (nx, ny)
        
        # Aplicar zona muerta
        abs_x = abs(nx)
        abs_y = abs(ny)
        
        # Actualizar teclas basadas en la dirección del joystick
        self.teclas[pygame.K_LEFT] = nx < -self.zona_muerta
        self.teclas[pygame.K_RIGHT] = nx > self.zona_muerta
        self.teclas[pygame.K_UP] = ny < -self.zona_muerta
        self.teclas[pygame.K_DOWN] = ny > self.zona_muerta
        
    def get_teclas(self):
        """Devuelve el diccionario de teclas simuladas"""
        return self.teclas
    
    def dibujar(self, pantalla):
        """Dibuja los controles táctiles en pantalla"""
        # Dibujar joystick
        alpha = 150
        base_surface = pygame.Surface((self.joystick_radio * 2, self.joystick_radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(base_surface, (50, 50, 50, alpha), 
                          (self.joystick_radio, self.joystick_radio), 
                          self.joystick_radio, 3)
        
        # Círculo interior (posición actual)
        if self.joystick_activo:
            offset_x = self.joystick_posicion[0] * self.joystick_radio
            offset_y = self.joystick_posicion[1] * self.joystick_radio
            pygame.draw.circle(base_surface, (100, 150, 255, alpha),
                              (self.joystick_radio + offset_x, self.joystick_radio + offset_y),
                              30)
        else:
            pygame.draw.circle(base_surface, (100, 150, 255, alpha // 2),
                              (self.joystick_radio, self.joystick_radio),
                              30)
        
        pantalla.blit(base_surface, (self.joystick_centro_x - self.joystick_radio,
                                     self.joystick_centro_y - self.joystick_radio))
        
        # Dibujar botones
        for boton in [self.boton_salto, self.boton_ataque]:
            color = boton['color']
            if boton['activo']:
                # Efecto de presionado
                color = tuple(min(255, c + 50) for c in color)
                pygame.draw.circle(pantalla, color, boton['rect'].center, 45)
            
            pygame.draw.circle(pantalla, color, boton['rect'].center, 40, 3)
            pygame.draw.circle(pantalla, color, boton['rect'].center, 35)
            
            # Texto del botón
            font = pygame.font.Font(None, 40)
            texto = font.render(boton['texto'], True, (255, 255, 255))
            texto_rect = texto.get_rect(center=boton['rect'].center)
            pantalla.blit(texto, texto_rect)
        
        # Instrucciones (solo si no hay toque activo)
        if not self.joystick_activo and not self.boton_salto['activo'] and not self.boton_ataque['activo']:
            font = pygame.font.Font(None, 24)
            instr = font.render("Joystick: Mover | Botones: Saltar/Atacar", True, (150, 150, 150))
            instr_rect = instr.get_rect(center=(ANCHO // 2, ALTO - 30))
            pantalla.blit(instr, instr_rect)
