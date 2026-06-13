"""
PRESTALABS-PLAY - OBJETOS DEL JUEGO
"""
import pygame
import random
from constantes import VELOCIDAD_BARRILES, PUNTUACION_POR_MONEDA, ANCHO, ALTO, TAMANO_BARRIL

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
        self.alto = alto
        self.rect = pygame.Rect(x, y, 12, alto)
    
    def dibujar(self, pantalla):
        self.gestor.dibujar_escalera(pantalla, self.rect.x, self.rect.y, self.alto)

class Barril(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_x, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, TAMANO_BARRIL[0], TAMANO_BARRIL[1])
        self.vel_x = vel_x  # Velocidad horizontal (positiva derecha, negativa izquierda)
        self.vel_y = 4      # Velocidad inicial hacia abajo
        self.gravedad = 0.4
    
    def update(self, plataformas, escaleras):
        # Aplicar gravedad
        self.vel_y += self.gravedad
        if self.vel_y > 10:
            self.vel_y = 10
        
        # Movimiento
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Colisión con plataformas
        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = -2  # Rebote pequeño
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 2
        
        # Colisión con escaleras (caen por escaleras)
        for e in escaleras:
            if self.rect.colliderect(e.rect) and self.vel_y == 0:
                self.rect.y += 3
        
        # Eliminar si sale de la pantalla
        if self.rect.y > ALTO or self.rect.x < -50 or self.rect.x > ANCHO + 50:
            self.kill()
    
    def dibujar(self, pantalla):
        self.gestor.dibujar_barril(pantalla, self.rect.x, self.rect.y)

class Martillo(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, 16, 16)
    
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (150, 150, 150), self.rect)
        pygame.draw.rect(pantalla, (139, 69, 19), (self.rect.x + 9, self.rect.y, 7, 10))

class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, 14, 14)
        self.valor = PUNTUACION_POR_MONEDA
        self.frame = 0
    
    def update(self):
        self.frame = (self.frame + 1) % 25
    
    def dibujar(self, pantalla):
        frame_anim = (self.frame // 5) + 1
        self.gestor.dibujar_moneda(pantalla, self.rect.x, self.rect.y, frame_anim)

class Pauline(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, 22, 28)
        self.anim_frame = 0
    
    def update(self):
        self.anim_frame += 1
    
    def dibujar(self, pantalla):
        self.gestor.dibujar_pauline(pantalla, self.rect.x, self.rect.y)
        if self.anim_frame % 40 < 20:
            self.gestor.dibujar_texto(pantalla, "HELP!", 16, (255, 0, 0), self.rect.x + 25, self.rect.y + 5)

class DonkeyKong(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, 50, 50)
        self.tiempo_barril = 0
        self.enojado = False
        self.tiempo_enojado = 0
        self.direccion = 1  # 1 derecha, -1 izquierda
        self.vel_x = 1.5
        self.x_inicial = x
        self.rango_movimiento = 200
        self.anim_frame = 0
        
    def update(self, plataformas):
        self.anim_frame += 1
        self.rect.x += self.vel_x * self.direccion
        
        # Cambiar dirección en los límites
        if self.rect.x > self.x_inicial + self.rango_movimiento:
            self.rect.x = self.x_inicial + self.rango_movimiento
            self.direccion = -1
        if self.rect.x < self.x_inicial - self.rango_movimiento:
            self.rect.x = self.x_inicial - self.rango_movimiento
            self.direccion = 1
        
        self.tiempo_barril += 1
        
        if self.tiempo_enojado > 0:
            self.tiempo_enojado -= 1
            self.enojado = True
        else:
            self.enojado = False
    
    def lanzar_barril(self):
        """Lanza un barril en la dirección donde mira Donkey Kong"""
        # Velocidad horizontal: hacia donde mira (derecha o izquierda)
        # Velocidad vertical: hacia abajo
        vel_x = 3 * self.direccion  # 3 derecha, -3 izquierda
        vel_y = 4  # Velocidad inicial hacia abajo
        
        # Crear barril con la dirección
        barril = Barril(self.rect.centerx - 9, self.rect.bottom, vel_x, self.gestor)
        barril.vel_x = vel_x
        barril.vel_y = vel_y
        return barril
    
    def set_mario_cerca(self, cerca):
        if cerca:
            self.tiempo_enojado = 30
    
    def get_tiempo_barril(self):
        return 50 if self.enojado else 80
    
    def dibujar(self, pantalla):
        # Soga horizontal
        soga_y = self.rect.y - 25
        pygame.draw.line(pantalla, (80, 50, 20), 
                        (self.x_inicial - self.rango_movimiento - 30, soga_y), 
                        (self.x_inicial + self.rango_movimiento + 30, soga_y), 3)
        
        # Cuerda que sostiene al mono
        pygame.draw.line(pantalla, (80, 50, 20), 
                        (self.rect.centerx, soga_y), 
                        (self.rect.centerx, self.rect.y), 2)
        
        # Cuerpo del mono
        pygame.draw.ellipse(pantalla, (101, 67, 33), self.rect)
        
        # Cabeza
        pygame.draw.circle(pantalla, (139, 90, 43), (self.rect.centerx, self.rect.y + 15), 18)
        
        # Orejas
        pygame.draw.circle(pantalla, (139, 90, 43), (self.rect.centerx - 14, self.rect.y + 5), 10)
        pygame.draw.circle(pantalla, (139, 90, 43), (self.rect.centerx + 14, self.rect.y + 5), 10)
        pygame.draw.circle(pantalla, (160, 110, 60), (self.rect.centerx - 14, self.rect.y + 5), 6)
        pygame.draw.circle(pantalla, (160, 110, 60), (self.rect.centerx + 14, self.rect.y + 5), 6)
        
        # Brazos agarrando la cuerda
        pygame.draw.line(pantalla, (101, 67, 33), 
                        (self.rect.centerx, self.rect.y + 5),
                        (self.rect.centerx - 12, self.rect.y + 18), 4)
        pygame.draw.line(pantalla, (101, 67, 33),
                        (self.rect.centerx, self.rect.y + 5),
                        (self.rect.centerx + 12, self.rect.y + 18), 4)
        
        # Ojos (mirando hacia la dirección)
        if self.direccion == 1:  # Mirando derecha
            pygame.draw.circle(pantalla, (255, 255, 255), (self.rect.centerx + 10, self.rect.y + 12), 5)
            pygame.draw.circle(pantalla, (0, 0, 0), (self.rect.centerx + 11, self.rect.y + 12), 2)
            pygame.draw.circle(pantalla, (255, 255, 255), (self.rect.centerx - 2, self.rect.y + 12), 5)
            pygame.draw.circle(pantalla, (0, 0, 0), (self.rect.centerx - 1, self.rect.y + 12), 2)
        else:  # Mirando izquierda
            pygame.draw.circle(pantalla, (255, 255, 255), (self.rect.centerx + 2, self.rect.y + 12), 5)
            pygame.draw.circle(pantalla, (0, 0, 0), (self.rect.centerx + 3, self.rect.y + 12), 2)
            pygame.draw.circle(pantalla, (255, 255, 255), (self.rect.centerx - 10, self.rect.y + 12), 5)
            pygame.draw.circle(pantalla, (0, 0, 0), (self.rect.centerx - 9, self.rect.y + 12), 2)
        
        # Sonrisa
        pygame.draw.arc(pantalla, (0, 0, 0), (self.rect.centerx - 8, self.rect.y + 16, 16, 8), 0, 3.14, 2)
        
        # Cejas enojadas
        if self.enojado:
            pygame.draw.line(pantalla, (0, 0, 0), (self.rect.centerx - 8, self.rect.y + 8), 
                            (self.rect.centerx, self.rect.y + 10), 2)
            pygame.draw.line(pantalla, (0, 0, 0), (self.rect.centerx + 8, self.rect.y + 8), 
                            (self.rect.centerx, self.rect.y + 10), 2)
        
        # Piernas colgando
        pygame.draw.line(pantalla, (101, 67, 33), 
                        (self.rect.centerx - 10, self.rect.bottom - 5),
                        (self.rect.centerx - 15, self.rect.bottom + 10), 4)
        pygame.draw.line(pantalla, (101, 67, 33),
                        (self.rect.centerx + 10, self.rect.bottom - 5),
                        (self.rect.centerx + 15, self.rect.bottom + 10), 4)