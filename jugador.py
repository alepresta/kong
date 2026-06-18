"""
KONG ARGENTINO - CLASES DE JUGADORES v3.2
Creado por Apresta para Prestalabs
"""
import pygame
import random
import math
from constantes import *

class Argentino(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, TAMANO_JUGADOR[0], TAMANO_JUGADOR[1])
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.vidas = VIDAS
        self.invencible = 0
        self.tiene_poder = False
        self.tiempo_poder = 0
        self.direccion = 1
        self.respawneando = False
        self.tiempo_respawn = 0
        self.anim_frame = 0
        self.en_escalera = False
        self.escalera_actual = None
        self.combo = 0
        self.tiempo_combo = 0
        self.huellas = []
        self.offset_y = 0
        self.salto_presionado = False
        self.golpe_anim = 0
        self.vel_max = 8
        
        # --- NUEVO: Sistema de ataque ---
        self.ataque_activo = False
        self.tiempo_ataque = 0
        self.ataque_cooldown = 0
        self.ataque_rect = pygame.Rect(0, 0, 40, 40)  # Hitbox del ataque
        
        # Animación de ataque
        self.animacion_ataque = 0

    def respawn(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.respawneando = True
        self.tiempo_respawn = TIEMPO_RESPAWN
        self.invencible = INVENCIBILIDAD_DESPUES_GOLPE
        self.combo = 0
        self.tiempo_combo = 0
        self.golpe_anim = 20
        self.ataque_activo = False
        self.ataque_cooldown = 0

    def add_combo(self):
        self.combo = min(self.combo + 1, MULTIPLICADOR_COMBO_MAX)
        self.tiempo_combo = TIEMPO_COMBO

    def get_multiplicador(self):
        return self.combo

    def get_ataque_rect(self):
        """Devuelve el rectángulo de ataque en la dirección del jugador"""
        if self.direccion == 1:
            return pygame.Rect(
                self.rect.right,
                self.rect.y + 5,
                DISTANCIA_ATAQUE,
                self.rect.height - 10
            )
        else:
            return pygame.Rect(
                self.rect.left - DISTANCIA_ATAQUE,
                self.rect.y + 5,
                DISTANCIA_ATAQUE,
                self.rect.height - 10
            )

    def atacar(self):
        """Ejecuta un ataque si está disponible"""
        if self.ataque_cooldown <= 0 and not self.respawneando:
            self.ataque_activo = True
            self.tiempo_ataque = TIEMPO_ATAQUE
            self.ataque_cooldown = 30  # Cooldown de medio segundo
            self.animacion_ataque = 15
            self.gestor.reproducir_sonido('golpe')
            self.ataque_rect = self.get_ataque_rect()
            return True
        return False

    def update(self, plataformas, escaleras):
        teclas = pygame.key.get_pressed()
        self.anim_frame += 1
        self.offset_y = math.sin(self.anim_frame * 0.1) * 2 if not self.en_suelo else 0
        
        # Animación de golpe
        if self.golpe_anim > 0:
            self.golpe_anim -= 1

        # Decaimiento del combo
        if self.tiempo_combo > 0:
            self.tiempo_combo -= 1
            if self.tiempo_combo <= 0:
                self.combo = 0

        if self.respawneando:
            self.tiempo_respawn -= 1
            if self.tiempo_respawn <= 0:
                self.respawneando = False
            return

        # --- SISTEMA DE ATAQUE ---
        if self.ataque_activo:
            self.tiempo_ataque -= 1
            self.ataque_rect = self.get_ataque_rect()
            if self.tiempo_ataque <= 0:
                self.ataque_activo = False
        
        if self.ataque_cooldown > 0:
            self.ataque_cooldown -= 1
        
        # Animación de ataque
        if self.animacion_ataque > 0:
            self.animacion_ataque -= 1

        # --- CONTROLES ---
        # Dirección
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.direccion = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.direccion = 1

        # ATAQUE CON ESPACIO + DIRECCIÓN (o tecla dedicada)
        ataque_presionado = teclas[pygame.K_SPACE] and (teclas[pygame.K_LEFT] or teclas[pygame.K_a] or teclas[pygame.K_RIGHT] or teclas[pygame.K_d])
        ataque_tecla = teclas[pygame.K_z] or teclas[pygame.K_x]  # Teclas Z o X para atacar
        
        if (ataque_presionado or ataque_tecla) and not self.respawneando:
            self.atacar()

        # --- DETECCIÓN DE ESCALERA ---
        self.en_escalera = False
        self.escalera_actual = None
        
        for e in escaleras:
            if self.rect.colliderect(e.rect_deteccion):
                self.en_escalera = True
                self.escalera_actual = e
                break

        # --- COMPORTAMIENTO EN ESCALERA ---
        subir = teclas[pygame.K_UP] or teclas[pygame.K_w]
        bajar = teclas[pygame.K_DOWN] or teclas[pygame.K_s]
        
        if self.en_escalera and (subir or bajar):
            if self.escalera_actual:
                self.rect.centerx = self.escalera_actual.x_visual + 6
            
            if subir:
                self.rect.y -= VELOCIDAD_JUGADOR_ESCALERA
                if self.rect.top < self.escalera_actual.y_visual - 5:
                    self.rect.top = self.escalera_actual.y_visual - 5
            if bajar:
                self.rect.y += VELOCIDAD_JUGADOR_ESCALERA
                if self.rect.bottom > self.escalera_actual.y_visual + self.escalera_actual.alto_visual + 10:
                    self.rect.bottom = self.escalera_actual.y_visual + self.escalera_actual.alto_visual + 10
            
            if teclas[pygame.K_SPACE] and not self.salto_presionado and not (teclas[pygame.K_LEFT] or teclas[pygame.K_a] or teclas[pygame.K_RIGHT] or teclas[pygame.K_d]):
                self.vel_y = SALTO_ESCALERA
                self.en_suelo = False
                self.en_escalera = False
                self.gestor.reproducir_sonido('salto')
                self.salto_presionado = True
            elif not teclas[pygame.K_SPACE]:
                self.salto_presionado = False
            
            self.vel_x = 0
            self.vel_y = 0
            return

        # --- MOVIMIENTO NORMAL ---
        target_vel_x = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            target_vel_x = -VELOCIDAD_JUGADOR
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            target_vel_x = VELOCIDAD_JUGADOR
        
        self.vel_x += (target_vel_x - self.vel_x) * 0.25

        self.rect.x += self.vel_x
        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                    self.vel_x = 0
                elif self.vel_x < 0:
                    self.rect.left = p.rect.right
                    self.vel_x = 0

        # Gravedad y salto (SALTO NORMAL con SPACE solo, sin dirección)
        self.vel_y += GRAVEDAD
        if self.vel_y > 12:
            self.vel_y = 12
        
        # Salto - SOLO con SPACE, sin dirección (para no confundir con ataque)
        if teclas[pygame.K_SPACE] and self.en_suelo and not self.salto_presionado:
            # Verificar que no está atacando con dirección
            if not (teclas[pygame.K_LEFT] or teclas[pygame.K_a] or teclas[pygame.K_RIGHT] or teclas[pygame.K_d]):
                self.vel_y = SALTO
                self.en_suelo = False
                self.gestor.reproducir_sonido('salto')
                self.salto_presionado = True
        elif not teclas[pygame.K_SPACE]:
            self.salto_presionado = False

        self.rect.y += self.vel_y

        self.en_suelo = False
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
            self.vel_x = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
            self.vel_x = 0
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
            self.vel_y = 0
            self.en_suelo = True
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0

        # Poder
        if self.tiene_poder:
            self.tiempo_poder -= 1
            if self.tiempo_poder <= 0:
                self.tiene_poder = False
                self.gestor.reproducir_sonido('peligro')
        
        if self.invencible > 0:
            self.invencible -= 1

        # Huellas
        if abs(self.vel_x) > 2 and self.en_suelo and self.anim_frame % 5 == 0:
            self.huellas.append({'x': self.rect.centerx, 'y': self.rect.bottom, 'vida': 15})
        for h in self.huellas[:]:
            h['vida'] -= 1
            if h['vida'] <= 0:
                self.huellas.remove(h)

    def golpear(self):
        if self.invencible <= 0 and not self.tiene_poder and not self.respawneando:
            self.vidas -= 1
            self.invencible = INVENCIBILIDAD_DESPUES_GOLPE
            self.combo = 0
            self.golpe_anim = 15
            self.gestor.reproducir_sonido('golpe')
            return True
        return False

    def dibujar(self, pantalla):
        if self.invencible > 0 and (self.invencible // 4) % 2 == 0:
            return

        x, y = self.rect.x, self.rect.y
        d = self.direccion
        
        # Efecto de golpe
        shake_x = random.randint(-2, 2) if self.golpe_anim > 0 else 0
        shake_y = random.randint(-2, 2) if self.golpe_anim > 0 else 0
        x += shake_x
        y += shake_y

        # Sombra
        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 30, 10)
        
        # Huellas
        for h in self.huellas:
            alpha = h['vida'] / 15
            c = int(alpha * 80)
            pygame.draw.circle(pantalla, (c, c, c), (h['x'], h['y'] + 2), 3)

        leg_off = int(math.sin(self.anim_frame * 0.3) * 4) if abs(self.vel_x) > 1 else 0
        offset_y = self.offset_y + shake_y

        # --- DIBUJAR ATAQUE (efecto visual) ---
        if self.ataque_activo or self.animacion_ataque > 0:
            # Línea de ataque (golpe)
            if d == 1:
                start_x = x + 32
                end_x = x + 32 + DISTANCIA_ATAQUE
            else:
                start_x = x
                end_x = x - DISTANCIA_ATAQUE
            
            # Efecto de "slash"
            for i in range(3):
                offset = i * 4 - 4
                alpha = 150 - i * 40
                pygame.draw.line(
                    pantalla,
                    (255, 255, 255, alpha),
                    (start_x, y + 19 + offset_y + offset),
                    (end_x, y + 19 + offset_y - offset),
                    max(2, 6 - i)
                )
            
            # Círculo de impacto
            pygame.draw.circle(
                pantalla,
                (255, 200, 50, 100),
                (end_x, y + 19 + offset_y),
                8 + self.animacion_ataque // 3
            )

        # --- CUERPO ---
        pygame.draw.rect(pantalla, COLORES['celeste'], (x, y + 12 + offset_y, 32, 20))
        pygame.draw.rect(pantalla, COLORES['blanco'], (x, y + 16 + offset_y, 32, 6))
        pygame.draw.rect(pantalla, COLORES['celeste'], (x, y + 20 + offset_y, 32, 4))
        
        # Cuello
        pygame.draw.rect(pantalla, (220, 200, 180), (x + 12, y + 10 + offset_y, 8, 4))
        
        # Brazos (con animación de ataque)
        if self.ataque_activo or self.animacion_ataque > 0:
            # Brazo extendido para ataque
            if d == 1:
                pygame.draw.rect(pantalla, (220, 200, 180), (x + 28, y + 12 + offset_y - 4, 16, 6))
                pygame.draw.circle(pantalla, (220, 200, 180), (x + 44, y + 13 + offset_y), 5)
                # Puño
                pygame.draw.circle(pantalla, (200, 180, 160), (x + 46, y + 13 + offset_y), 4)
            else:
                pygame.draw.rect(pantalla, (220, 200, 180), (x - 12, y + 12 + offset_y - 4, 16, 6))
                pygame.draw.circle(pantalla, (220, 200, 180), (x - 12, y + 13 + offset_y), 5)
                pygame.draw.circle(pantalla, (200, 180, 160), (x - 14, y + 13 + offset_y), 4)
            
            # Brazo trasero
            pygame.draw.rect(pantalla, (220, 200, 180), (x - 4, y + 14 + offset_y, 6, 14))
            pygame.draw.circle(pantalla, (220, 200, 180), (x - 1, y + 28 + offset_y), 4)
        else:
            # Brazos normales
            if abs(self.vel_x) > 1:
                brazo_off = int(math.sin(self.anim_frame * 0.4) * 3)
            else:
                brazo_off = 0
            
            pygame.draw.rect(pantalla, (220, 200, 180), (x - 4, y + 14 + offset_y + brazo_off, 6, 14))
            pygame.draw.circle(pantalla, (220, 200, 180), (x - 1, y + 28 + offset_y + brazo_off), 4)
            pygame.draw.rect(pantalla, (220, 200, 180), (x + 30, y + 14 + offset_y - brazo_off, 6, 14))
            pygame.draw.circle(pantalla, (220, 200, 180), (x + 33, y + 28 + offset_y - brazo_off), 4)

        # --- CABEZA ---
        pygame.draw.circle(pantalla, (255, 215, 180), (x + 16, y + 8 + offset_y), 10)
        pygame.draw.ellipse(pantalla, (30, 30, 30), (x + 6, y - 2 + offset_y, 20, 10))
        pygame.draw.ellipse(pantalla, (50, 50, 50), (x + 8, y - 4 + offset_y, 16, 8))
        
        # Gorra
        pygame.draw.ellipse(pantalla, COLORES['celeste'], (x + 2, y - 4 + offset_y, 28, 10))
        pygame.draw.rect(pantalla, COLORES['celeste'], (x + 2, y - 1 + offset_y, 28, 5))
        pygame.draw.rect(pantalla, COLORES['blanco'], (x + 3, y - 3 + offset_y, 26, 4))
        visera_off = 3 if d == 1 else -3
        pygame.draw.polygon(pantalla, (40, 40, 40), 
                           [(x + 6 + visera_off, y - 3 + offset_y),
                            (x + 12 + visera_off, y - 8 + offset_y),
                            (x + 26 + visera_off, y - 3 + offset_y),
                            (x + 22 + visera_off, y - 1 + offset_y)])

        # Ojos
        ojo_x = 2 if d == 1 else -2
        pygame.draw.circle(pantalla, COLORES['blanco'], (x + 12 + ojo_x, y + 6 + offset_y), 4)
        pygame.draw.circle(pantalla, COLORES['blanco'], (x + 20 + ojo_x, y + 6 + offset_y), 4)
        pygame.draw.circle(pantalla, COLORES['negro'], (x + 13 + ojo_x, y + 7 + offset_y), 2)
        pygame.draw.circle(pantalla, COLORES['negro'], (x + 21 + ojo_x, y + 7 + offset_y), 2)
        pygame.draw.circle(pantalla, COLORES['blanco'], (x + 12 + ojo_x, y + 5 + offset_y), 1)
        pygame.draw.circle(pantalla, COLORES['blanco'], (x + 20 + ojo_x, y + 5 + offset_y), 1)

        # Boca
        if self.ataque_activo or self.animacion_ataque > 0:
            # Grito de ataque
            pygame.draw.ellipse(pantalla, (200, 50, 50), (x + 12, y + 10 + offset_y, 8, 6))
            pygame.draw.ellipse(pantalla, (200, 80, 80), (x + 13, y + 11 + offset_y, 6, 4))
        elif self.vel_y < -3:
            pygame.draw.ellipse(pantalla, COLORES['negro'], (x + 12, y + 10 + offset_y, 8, 5))
            pygame.draw.ellipse(pantalla, (200, 100, 100), (x + 13, y + 11 + offset_y, 6, 3))
        else:
            pygame.draw.arc(pantalla, COLORES['negro'], (x + 10, y + 9 + offset_y, 12, 6), 0, math.pi, 2)

        # --- PIERNAS ---
        pygame.draw.rect(pantalla, (30, 60, 140), (x + 4, y + 32 + offset_y, 8, 6 + leg_off))
        pygame.draw.rect(pantalla, (30, 60, 140), (x + 20, y + 32 + offset_y, 8, 6 - leg_off))
        
        # Zapatillas
        pygame.draw.rect(pantalla, (40, 40, 40), (x + 2, y + 38 + leg_off + offset_y, 12, 4))
        pygame.draw.rect(pantalla, (40, 40, 40), (x + 18, y + 38 - leg_off + offset_y, 12, 4))
        pygame.draw.rect(pantalla, (200, 200, 200), (x + 3, y + 40 + leg_off + offset_y, 10, 2))
        pygame.draw.rect(pantalla, (200, 200, 200), (x + 19, y + 40 - leg_off + offset_y, 10, 2))

        # --- MATE POWER ---
        if self.tiene_poder:
            glow = pygame.Surface((40, 40), pygame.SRCALPHA)
            if self.anim_frame % 20 < 10:
                alpha = 100
            else:
                alpha = 40
            pygame.draw.circle(glow, (0, 255, 0, alpha), (20, 20), 18)
            pantalla.blit(glow, (x - 4, y + 8 + offset_y))
            
            pygame.draw.rect(pantalla, (60, 120, 60), (x + 24, y + 18 + offset_y, 8, 12))
            pygame.draw.circle(pantalla, (100, 160, 100), (x + 28, y + 18 + offset_y), 5)
            pygame.draw.circle(pantalla, (150, 100, 50), (x + 28, y + 20 + offset_y), 3)
            pygame.draw.line(pantalla, (180, 130, 70), (x + 30, y + 18 + offset_y), (x + 34, y + 14 + offset_y), 2)

        # --- COMBO BADGE ---
        if self.combo >= 2:
            colores = [COLORES['amarillo'], COLORES['naranja'], 
                      COLORES['rojo'], COLORES['violeta'], COLORES['oro']]
            col = colores[min(self.combo - 2, 4)]
            pygame.draw.circle(pantalla, COLORES['negro'], (x + 38, y + 2), 14)
            pygame.draw.circle(pantalla, col, (x + 36, y), 12)
            self.gestor.dibujar_texto(pantalla, f"x{self.combo}", 14, COLORES['blanco'],
                                      x + 36, y - 2, centro=True)

        # --- Indicador de ataque (cooldown) ---
        if self.ataque_cooldown > 0:
            # Pequeña barra de cooldown
            cooldown_bar = 30 - self.ataque_cooldown
            bar_width = 20
            pygame.draw.rect(pantalla, COLORES['negro'], (x + 6, y - 8, bar_width, 4))
            pygame.draw.rect(pantalla, COLORES['amarillo'], (x + 6, y - 8, cooldown_bar * bar_width // 30, 4))


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

        self.vel_y += GRAVEDAD
        if self.vel_y > 12:
            self.vel_y = 12

        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)

        self.en_suelo = False
        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vel_y >= 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.en_suelo = True
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0

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
            self.vel_y = SALTO // 2

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