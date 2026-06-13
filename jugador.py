"""
PRESTALABS-PLAY - CLASE JUGADOR (SIN REBOTE)
"""
import pygame
from constantes import VELOCIDAD_JUGADOR, GRAVEDAD, SALTO, ANCHO, ALTO

class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, 24, 24)
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.en_escalera = False
        self.vidas = 9
        self.invencible = 0
        self.tiene_martillo = False
        self.tiempo_martillo = 0
        self.direccion = 1
        self.respawneando = False
        self.tiempo_respawn = 0
        self.agarrando_escalera = False
        self.escalera_actual = None
    
    def respawn(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.respawneando = True
        self.tiempo_respawn = 30
        self.invencible = 60
    
    def update(self, plataformas, escaleras):
        teclas = pygame.key.get_pressed()
        
        if self.respawneando:
            self.tiempo_respawn -= 1
            if self.tiempo_respawn <= 0:
                self.respawneando = False
        
        # CAMBIAR DIRECCIÓN
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.direccion = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.direccion = 1
        
        # VERIFICAR ESCALERA
        self.en_escalera = False
        for e in escaleras:
            if self.rect.colliderect(e.rect):
                if abs(self.rect.centerx - e.rect.centerx) < 20:
                    self.en_escalera = True
                    self.escalera_actual = e
                    break
        
        # MOVIMIENTO EN ESCALERA
        if self.en_escalera and (teclas[pygame.K_UP] or teclas[pygame.K_w] or teclas[pygame.K_DOWN] or teclas[pygame.K_s]):
            self.vel_y = 0
            if teclas[pygame.K_UP] or teclas[pygame.K_w]:
                self.rect.y -= VELOCIDAD_JUGADOR
            if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
                self.rect.y += VELOCIDAD_JUGADOR
            if self.escalera_actual:
                self.rect.centerx = self.escalera_actual.rect.centerx
        else:
            # MOVIMIENTO HORIZONTAL
            self.vel_x = 0
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                self.vel_x = -VELOCIDAD_JUGADOR
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                self.vel_x = VELOCIDAD_JUGADOR
            
            # MOVER EN X
            self.rect.x += self.vel_x
            
            # COLISIÓN HORIZONTAL (SOLO DETENER, NO REBOTAR)
            for p in plataformas:
                if self.rect.colliderect(p.rect):
                    if self.vel_x > 0:
                        self.rect.right = p.rect.left
                        # NO invertir velocidad, solo detener
                    elif self.vel_x < 0:
                        self.rect.left = p.rect.right
                        # NO invertir velocidad, solo detener
            
            # GRAVEDAD
            self.vel_y += GRAVEDAD
            if self.vel_y > 10:
                self.vel_y = 10
            
            self.rect.y += self.vel_y
            
            # COLISIÓN VERTICAL
            self.en_suelo = False
            for p in plataformas:
                if self.rect.colliderect(p.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = p.rect.top
                        self.vel_y = 0
                        self.en_suelo = True
                    elif self.vel_y < 0:
                        self.rect.top = p.rect.bottom
                        self.vel_y = 0
            
            # SALTO
            if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w]) and self.en_suelo and not self.respawneando:
                self.vel_y = SALTO
                self.en_suelo = False
                self.gestor.reproducir_sonido('salto')
        
        # LÍMITES DE PANTALLA
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
            self.vel_y = 0
            self.en_suelo = True
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
        
        # MARTILLO
        if self.tiene_martillo:
            self.tiempo_martillo -= 1
            if self.tiempo_martillo <= 0:
                self.tiene_martillo = False
        
        # INVENCIBILIDAD
        if self.invencible > 0:
            self.invencible -= 1
    
    def golpear(self):
        if self.invencible <= 0 and not self.tiene_martillo and not self.respawneando:
            self.vidas -= 1
            self.invencible = 60
            return True
        return False
    
    def dibujar(self, pantalla):
        self.gestor.dibujar_mario(
            pantalla, self.rect.x, self.rect.y, 
            self.direccion, self.tiene_martillo, self.invencible,
            False
        )
"""
PRESTALABS-PLAY - CLASE JUGADOR
"""
import pygame
from constantes import VELOCIDAD_JUGADOR, GRAVEDAD, SALTO, ANCHO, ALTO

class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, 24, 24)
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.en_escalera = False
        self.vidas = 9
        self.invencible = 0
        self.tiene_martillo = False
        self.tiempo_martillo = 0
        self.direccion = 1
        self.respawneando = False
        self.tiempo_respawn = 0
        self.agarrando_escalera = False
        self.escalera_actual = None
    
    def respawn(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.respawneando = True
        self.tiempo_respawn = 30
        self.invencible = 60
    
    def update(self, plataformas, escaleras):
        teclas = pygame.key.get_pressed()
        
        if self.respawneando:
            self.tiempo_respawn -= 1
            if self.tiempo_respawn <= 0:
                self.respawneando = False
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.direccion = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.direccion = 1
        
        self.en_escalera = False
        for e in escaleras:
            if self.rect.colliderect(e.rect):
                if abs(self.rect.centerx - e.rect.centerx) < 20:
                    self.en_escalera = True
                    self.escalera_actual = e
                    break
        
        if self.en_escalera and (teclas[pygame.K_UP] or teclas[pygame.K_w] or teclas[pygame.K_DOWN] or teclas[pygame.K_s]):
            self.vel_y = 0
            if teclas[pygame.K_UP] or teclas[pygame.K_w]:
                self.rect.y -= VELOCIDAD_JUGADOR
            if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
                self.rect.y += VELOCIDAD_JUGADOR
            if self.escalera_actual:
                self.rect.centerx = self.escalera_actual.rect.centerx
        else:
            self.vel_x = 0
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                self.vel_x = -VELOCIDAD_JUGADOR
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                self.vel_x = VELOCIDAD_JUGADOR
            
            self.rect.x += self.vel_x
            for p in plataformas:
                if self.rect.colliderect(p.rect):
                    if self.vel_x > 0:
                        self.rect.right = p.rect.left
                    elif self.vel_x < 0:
                        self.rect.left = p.rect.right
            
            self.vel_y += GRAVEDAD
            if self.vel_y > 10:
                self.vel_y = 10
            self.rect.y += self.vel_y
            
            self.en_suelo = False
            for p in plataformas:
                if self.rect.colliderect(p.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = p.rect.top
                        self.vel_y = 0
                        self.en_suelo = True
                    elif self.vel_y < 0:
                        self.rect.top = p.rect.bottom
                        self.vel_y = 0
            
            if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w]) and self.en_suelo and not self.respawneando:
                self.vel_y = SALTO
                self.en_suelo = False
                self.gestor.reproducir_sonido('salto')
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
            self.vel_y = 0
            self.en_suelo = True
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
        
        if self.tiene_martillo:
            self.tiempo_martillo -= 1
            if self.tiempo_martillo <= 0:
                self.tiene_martillo = False
        
        if self.invencible > 0:
            self.invencible -= 1
    
    def golpear(self):
        if self.invencible <= 0 and not self.tiene_martillo and not self.respawneando:
            self.vidas -= 1
            self.invencible = 60
            return True
        return False
    
    def dibujar(self, pantalla):
        self.gestor.dibujar_mario(pantalla, self.rect.x, self.rect.y, self.direccion, self.tiene_martillo, self.invencible, False)