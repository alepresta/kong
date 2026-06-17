"""
KONG ARGENTINO - CLASES DE JUGADORES v3.1
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
        self.golpe_anim = 0  # Animación de golpe
        self.vel_max = 8

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

    def add_combo(self):
        self.combo = min(self.combo + 1, MULTIPLICADOR_COMBO_MAX)
        self.tiempo_combo = TIEMPO_COMBO

    def get_multiplicador(self):
        return self.combo

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

        # Dirección
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.direccion = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.direccion = 1

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
        
        # Si está en escalera y presiona arriba/abajo, se mueve verticalmente
        if self.en_escalera and (subir or bajar):
            # Alinear al centro de la escalera
            if self.escalera_actual:
                self.rect.centerx = self.escalera_actual.x_visual + 6
            
            # Movimiento vertical
            if subir:
                self.rect.y -= VELOCIDAD_JUGADOR_ESCALERA
                # Límite superior
                if self.rect.top < self.escalera_actual.y_visual - 5:
                    self.rect.top = self.escalera_actual.y_visual - 5
            if bajar:
                self.rect.y += VELOCIDAD_JUGADOR_ESCALERA
                # Límite inferior
                if self.rect.bottom > self.escalera_actual.y_visual + self.escalera_actual.alto_visual + 10:
                    self.rect.bottom = self.escalera_actual.y_visual + self.escalera_actual.alto_visual + 10
            
            # Si está en escalera y salta, sale de la escalera
            if teclas[pygame.K_SPACE] and not self.salto_presionado:
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
        # Velocidad horizontal con aceleración
        target_vel_x = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            target_vel_x = -VELOCIDAD_JUGADOR
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            target_vel_x = VELOCIDAD_JUGADOR
        
        # Aceleración suave
        self.vel_x += (target_vel_x - self.vel_x) * 0.25
        
        # Si está en escalera y no presiona arriba/abajo, puede moverse horizontalmente
        if self.en_escalera and not (subir or bajar):
            # Permitir movimiento horizontal pero manteniendo posición en escalera
            pass

        # Movimiento horizontal
        self.rect.x += self.vel_x
        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                    self.vel_x = 0
                elif self.vel_x < 0:
                    self.rect.left = p.rect.right
                    self.vel_x = 0

        # Gravedad y salto
        self.vel_y += GRAVEDAD
        if self.vel_y > 12:
            self.vel_y = 12
        
        # Salto
        if teclas[pygame.K_SPACE] and self.en_suelo and not self.salto_presionado:
            self.vel_y = SALTO
            self.en_suelo = False
            self.gestor.reproducir_sonido('salto')
            self.salto_presionado = True
        elif not teclas[pygame.K_SPACE]:
            self.salto_presionado = False

        # Movimiento vertical
        self.rect.y += self.vel_y

        # Colisiones con plataformas (suelo y techo)
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

        # Límites de pantalla
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
        
        # Invencibilidad
        if self.invencible > 0:
            self.invencible -= 1

        # Huellas de polvo
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
        # Si está invencible, parpadea
        if self.invencible > 0 and (self.invencible // 4) % 2 == 0:
            return

        x, y = self.rect.x, self.rect.y
        d = self.direccion
        
        # Efecto de golpe (temblor)
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

        # --- CUERPO ---
        # Camiseta argentina
        pygame.draw.rect(pantalla, COLORES['celeste'], (x, y + 12 + offset_y, 32, 20))
        pygame.draw.rect(pantalla, COLORES['blanco'], (x, y + 16 + offset_y, 32, 6))
        pygame.draw.rect(pantalla, COLORES['celeste'], (x, y + 20 + offset_y, 32, 4))
        
        # Cuello
        pygame.draw.rect(pantalla, (220, 200, 180), (x + 12, y + 10 + offset_y, 8, 4))
        
        # Brazos
        if abs(self.vel_x) > 1:
            brazo_off = int(math.sin(self.anim_frame * 0.4) * 3)
        else:
            brazo_off = 0
        
        # Brazo izquierdo
        pygame.draw.rect(pantalla, (220, 200, 180), (x - 4, y + 14 + offset_y + brazo_off, 6, 14))
        pygame.draw.circle(pantalla, (220, 200, 180), (x - 1, y + 28 + offset_y + brazo_off), 4)
        
        # Brazo derecho
        pygame.draw.rect(pantalla, (220, 200, 180), (x + 30, y + 14 + offset_y - brazo_off, 6, 14))
        pygame.draw.circle(pantalla, (220, 200, 180), (x + 33, y + 28 + offset_y - brazo_off), 4)

        # --- CABEZA ---
        # Cara
        pygame.draw.circle(pantalla, (255, 215, 180), (x + 16, y + 8 + offset_y), 10)
        
        # Pelo
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
        if self.vel_y < -3:
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

        # Detección de escalera
        self.en_escalera = False
        self.escalera_actual = None
        for e in escaleras:
            if self.rect.colliderect(e.rect_deteccion):
                self.en_escalera = True
                self.escalera_actual = e
                break

        # Subir escalera si está cerca de una y hay barril arriba
        if self.en_escalera and self.escalera_actual:
            # Buscar barriles arriba
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