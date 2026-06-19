"""
KONG ARGENTINO - HINCHA BORRACHITO
"""
import pygame
import random
import math
from constantes import *

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