# src/entidades/hincha_argentina.py - VERSIÓN MEJORADA
"""
KONG ARGENTINO - HINCHA ARGENTINA v2.0 (MEJORADA)
Creado por Apresta para Prestalabs

Personaje femenino hincha con:
- Canto frecuente "Argentina Argentina"
- Bandera con animación mejorada
- Sube y baja escaleras más rápido
- Persigue al jugador si está cerca
- Suelta estrellas y confeti
- Se tambalea pero no se cae (más divertida)
"""

import pygame
import random
import math
from constantes import ANCHO, ALTO, COLORES, GRAVEDAD, MULTIPLICADOR_GRAVEDAD_BORRACHO
from constantes import VEL_MAX_CAIDA_BORRACHO, TIEMPO_PEGADO_TECHO

class HinchaArgentina(pygame.sprite.Sprite):
    """Hincha argentina femenina con bandera y cánticos - Versión mejorada"""
    
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, 32, 42)
        
        # Estado de animación
        self.anim_frame = 0
        self.offset_y = 0
        self.direccion = 1
        
        # Estado de movimiento
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.gravedad = 0.4
        self.vel_subida = 2.8   # más rápido
        self.vel_bajada = 2.8
        
        # Estado de escalera
        self.en_escalera = False
        self.escalera_actual = None
        self.subiendo = False
        self.bajando = False
        
        # Borrachera (nunca se cae, solo se tambalea)
        self.nivel_borrachera = random.randint(2, 5)
        self.estado = "subiendo"
        self.tiempo_estado = 0
        
        # Canto (más frecuente)
        self.cantando = False
        self.tiempo_canto = 0
        self.texto_canto = ""
        self.canciones = [
            "🇦🇷 ARGENTINA ARGENTINA 🇦🇷",
            "🇦🇷 VAMOS ARGENTINA 🇦🇷",
            "🇦🇷 DALE CAMPEÓN 🇦🇷",
            "🇦🇷 LA COPA ESTÁ EN CASA 🇦🇷",
            "🇦🇷 MESSI MESSI 🇦🇷",
            "🇦🇷 ¡¡¡ARGENTINA!!! 🇦🇷",
            "🏆 SOY ARGENTINO 🏆",
            "🇦🇷 VAMO VAMO ARGENTINA 🇦🇷"
        ]
        
        # Bandera (más grande)
        self.bandera = self._crear_bandera()
        self.bandera_visible = True
        self.bandera_anim = 0
        
        # Comportamiento
        self.altura_maxima = y - random.randint(100, 250)  # menos altura para que se vea más
        self.altura_minima = min(ALTO - 80, y + random.randint(30, 100))
        
        # Pegado al techo (desactivado para que no se pegue)
        self.pegado_techo = False
        self.tiempo_pegado_techo = 0
        self.frames_pegado_techo = 10  # reducido
        self.vel_max = VEL_MAX_CAIDA_BORRACHO
        
        # Contador de partículas
        self.contador_particulas = 0
        
        # Iniciar con un canto
        self._iniciar_canto()
    
    def _crear_bandera(self):
        """Crea la superficie de la bandera argentina (más grande)"""
        bandera = pygame.Surface((56, 36), pygame.SRCALPHA)
        
        # Fondo celeste y blanco
        bandera.fill(COLORES['celeste'])
        pygame.draw.rect(bandera, COLORES['blanco'], (0, 11, 56, 14))
        
        # Sol (más detallado)
        centro = (28, 18)
        for i in range(12):
            ang = i * 3.14159 / 6
            x1 = centro[0] + math.cos(ang) * 9
            y1 = centro[1] + math.sin(ang) * 9
            x2 = centro[0] + math.cos(ang) * 16
            y2 = centro[1] + math.sin(ang) * 16
            pygame.draw.line(bandera, COLORES['amarillo'], (x1, y1), (x2, y2), 2)
        pygame.draw.circle(bandera, COLORES['amarillo'], centro, 8)
        pygame.draw.circle(bandera, (255, 240, 100), centro, 5)
        
        # Olas de la bandera (más pronunciadas)
        for i in range(7):
            ox = i * 8
            pygame.draw.arc(bandera, (100, 180, 210, 100), (ox, 0, 14, 36), 0, 3.14, 2)
        
        return bandera
    
    def _iniciar_canto(self):
        """Inicia un canto aleatorio (más frecuente)"""
        if random.random() < 0.6:  # 60% de chance
            self.cantando = True
            self.tiempo_canto = random.randint(50, 120)
            self.texto_canto = random.choice(self.canciones)
    
    def update(self, plataformas, escaleras, barriles):
        """Actualiza el estado del personaje"""
        self.anim_frame += 1
        self.bandera_anim += 1
        self.offset_y = math.sin(self.anim_frame * 0.1) * 2 if not self.en_suelo else 0
        
        # Actualizar canto
        if self.cantando:
            self.tiempo_canto -= 1
            if self.tiempo_canto <= 0:
                self.cantando = False
                self.texto_canto = ""
                if random.random() < 0.5:
                    self._iniciar_canto()
        else:
            if self.anim_frame % 80 == 0 and random.random() < 0.6:
                self._iniciar_canto()
        
        # --- DETECCIÓN DE ESCALERA ---
        self.en_escalera = False
        self.escalera_actual = None
        for e in escaleras:
            if self.rect.colliderect(e.rect_deteccion):
                self.en_escalera = True
                self.escalera_actual = e
                break
        
        # --- COMPORTAMIENTO PRINCIPAL ---
        if self.estado == "subiendo":
            self._comportamiento_subiendo(plataformas, escaleras)
        elif self.estado == "bajando":
            self._comportamiento_bajando(plataformas, escaleras)
        elif self.estado == "celebrando":
            self._comportamiento_celebrando()
        else:
            self._comportamiento_subiendo(plataformas, escaleras)
        
        # --- INTERACCIÓN CON JUGADOR (persecución) ---
        if self.gestor.argentino:
            dx = self.gestor.argentino.rect.x - self.rect.x
            dy = self.gestor.argentino.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            if dist < 250 and dist > 50:
                # Persigue al jugador
                if abs(dx) > 20 and not self.en_escalera:
                    self.vel_x = 1.5 if dx > 0 else -1.5
                    self.direccion = 1 if dx > 0 else -1
                # Si el jugador está arriba, intenta subir
                if dy < -50 and self.en_suelo and random.random() < 0.05:
                    self.vel_y = -5  # salta para alcanzarlo
        
        # --- MOVIMIENTO FÍSICO ---
        self._aplicar_fisica(plataformas)
        
        # --- LÍMITES ---
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = abs(self.vel_x)
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
            self.vel_x = -abs(self.vel_x)
        
        # Si se cae, respawn en la parte superior
        if self.rect.y > ALTO + 50:
            self.rect.y = 50
            self.rect.x = random.randint(50, ANCHO - 50)
            self.vel_y = 0
            self.estado = "subiendo"
            self._iniciar_canto()
    
    def _comportamiento_subiendo(self, plataformas, escaleras):
        """Comportamiento: subir escaleras (más rápido)"""
        self.tiempo_estado += 1
        
        # Buscar escalera más cercana
        if escaleras and not self.en_escalera:
            escalera_cercana = min(escaleras, key=lambda e: abs(e.rect_deteccion.x - self.rect.x))
            if abs(escalera_cercana.rect_deteccion.x - self.rect.x) < 250:
                if self.rect.x < escalera_cercana.rect_deteccion.x - 10:
                    self.vel_x = 2.0 + self.nivel_borrachera * 0.1
                    self.direccion = 1
                elif self.rect.x > escalera_cercana.rect_deteccion.x + 10:
                    self.vel_x = -2.0 - self.nivel_borrachera * 0.1
                    self.direccion = -1
                else:
                    self.vel_x = 0
        
        if self.en_escalera and self.escalera_actual:
            self.rect.centerx = self.escalera_actual.x_visual + 6
            self.rect.y -= self.vel_subida
            self.vel_y = 0
            self.subiendo = True
            self.bajando = False
            
            if self.rect.top <= self.escalera_actual.y_visual + 5:
                if self.rect.y < self.altura_maxima:
                    self.rect.y = self.altura_maxima
                    self.estado = "bajando"
                    self.tiempo_estado = 0
                    self._iniciar_canto()
                else:
                    self.estado = "celebrando"
                    self.tiempo_estado = 0
        
        # Tambalear si borracha
        if self.nivel_borrachera >= 4 and random.random() < 0.03:
            self.vel_x += random.choice([-0.8, 0.8])
    
    def _comportamiento_bajando(self, plataformas, escaleras):
        """Comportamiento: bajar escaleras (más rápido)"""
        self.tiempo_estado += 1
        
        if escaleras and not self.en_escalera:
            escalera_cercana = min(escaleras, key=lambda e: abs(e.rect_deteccion.x - self.rect.x))
            if abs(escalera_cercana.rect_deteccion.x - self.rect.x) < 300:
                if self.rect.x < escalera_cercana.rect_deteccion.x - 10:
                    self.vel_x = 2.0 + self.nivel_borrachera * 0.1
                elif self.rect.x > escalera_cercana.rect_deteccion.x + 10:
                    self.vel_x = -2.0 - self.nivel_borrachera * 0.1
                else:
                    self.vel_x = 0
        
        if self.en_escalera and self.escalera_actual:
            self.rect.centerx = self.escalera_actual.x_visual + 6
            self.rect.y += self.vel_bajada
            self.vel_y = 0
            self.subiendo = False
            self.bajando = True
            
            if self.rect.bottom >= self.escalera_actual.y_visual + self.escalera_actual.alto_visual - 5:
                if self.rect.y > ALTO - 150:
                    self.estado = "celebrando"
                    self.tiempo_estado = 0
                    self._iniciar_canto()
                else:
                    self.estado = "subiendo"
                    self.tiempo_estado = 0
    
    def _comportamiento_celebrando(self):
        """Comportamiento: celebrar y cantar (con salto y partículas)"""
        self.tiempo_estado += 1
        self.vel_x = 0
        
        if self.tiempo_estado % 25 == 0:
            self.direccion = -self.direccion
        
        # Salto de celebración
        if self.en_suelo and self.tiempo_estado % 25 == 0 and random.random() < 0.5:
            self.vel_y = -5 - self.nivel_borrachera * 0.15
            self.en_suelo = False
        
        # Cantar más seguido
        if self.tiempo_estado % 15 == 0 and random.random() < 0.7:
            self._iniciar_canto()
        
        # Partículas de celebración (confeti/estrellas)
        self.contador_particulas += 1
        if self.contador_particulas % 5 == 0 and self.gestor.sistema_particulas:
            for _ in range(2):
                self.gestor.sistema_particulas.emitir(
                    self.rect.centerx + random.randint(-30, 30),
                    self.rect.top - 10 + random.randint(-10, 10),
                    random.choice([COLORES['celeste'], COLORES['blanco'], 
                                   COLORES['amarillo'], COLORES['oro']]),
                    2, 'estrella'
                )
        
        # Volver a subir
        if self.tiempo_estado > random.randint(70, 150):
            self.estado = "subiendo"
            self.tiempo_estado = 0
            self.altura_maxima = random.randint(50, 250)
    
    def _aplicar_fisica(self, plataformas):
        """Aplica física de movimiento y gravedad"""
        if self.en_escalera and (self.subiendo or self.bajando):
            return
        
        self.vel_y += self.gravedad * (1 + self.nivel_borrachera * 0.02)
        if self.vel_y > self.vel_max:
            self.vel_y = self.vel_max
        
        self.rect.x += self.vel_x
        self.vel_x *= 0.92
        
        old_y = self.rect.y
        
        if self.pegado_techo:
            self.tiempo_pegado_techo -= 1
            if self.tiempo_pegado_techo <= 0:
                self.pegado_techo = False
                self.vel_y = 0
        else:
            self.rect.y += self.vel_y
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
    
    def beber_barril(self):
        """Beber un barril (aumenta borrachera pero no se cae)"""
        self.nivel_borrachera = min(10, self.nivel_borrachera + 1)
        self.gestor.reproducir_sonido('beber')
        
        # Efecto visual
        if self.gestor and hasattr(self.gestor, 'sistema_particulas'):
            self.gestor.sistema_particulas.emitir(
                self.rect.centerx, self.rect.top,
                COLORES['amarillo'], 5, 'estrella'
            )
        
        # Si llega a nivel alto, se tambalea mucho y suelta partículas
        if self.nivel_borrachera >= 7:
            self.vel_x = random.choice([-2, -1, 1, 2]) * 1.5
            self.texto_canto = "🥴 ¡VAMO ARGENTINA! 🥴"
            self.cantando = True
            self.tiempo_canto = 40
            # Muchas partículas
            if self.gestor.sistema_particulas:
                for _ in range(10):
                    self.gestor.sistema_particulas.emitir(
                        self.rect.centerx + random.randint(-20, 20),
                        self.rect.top + random.randint(-10, 10),
                        random.choice([COLORES['amarillo'], COLORES['naranja']]),
                        3, 'chispa'
                    )
    
    def dibujar(self, pantalla):
        """Dibuja el personaje en pantalla"""
        x, y = self.rect.x, self.rect.y
        
        # Sombra
        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 30, 8)
        
        # --- EFECTO DE BORRACHERA (tambaleo) ---
        if self.nivel_borrachera >= 3:
            wobble = math.sin(self.anim_frame * 0.2) * (self.nivel_borrachera / 3)
            x += wobble
            if self.nivel_borrachera >= 6:
                wobble2 = math.sin(self.anim_frame * 0.12) * 2
                y += wobble2
        
        # --- BANDERA (más grande y con más onda) ---
        if self.bandera_visible:
            flag_x = x - 14 if self.direccion == 1 else x + 30
            flag_y = y - 8 + math.sin(self.bandera_anim * 0.12) * 4
            
            flag_surf = pygame.transform.rotate(
                self.bandera,
                math.sin(self.bandera_anim * 0.1) * 10
            )
            pantalla.blit(flag_surf, (flag_x, flag_y))
        
        # --- CUERPO (camiseta argentina) ---
        pygame.draw.rect(pantalla, COLORES['celeste'], (int(x + 4), int(y + 14), 24, 18))
        pygame.draw.rect(pantalla, COLORES['blanco'], (int(x + 4), int(y + 18), 24, 4))
        pygame.draw.rect(pantalla, COLORES['celeste'], (int(x + 4), int(y + 22), 24, 4))
        pygame.draw.rect(pantalla, COLORES['blanco'], (int(x + 4), int(y + 26), 24, 4))
        
        # Número 10
        self.gestor.dibujar_texto(pantalla, "10", 12, (0, 0, 0), 
                                  int(x + 16), int(y + 16), centro=True)
        
        # Falda
        for i in range(3):
            fx = int(x + 4 + i * 10)
            fl = 6 + i * 2
            pygame.draw.polygon(pantalla, (100, 180, 220),
                               [(fx, int(y + 32)), (fx + 6, int(y + 32 + fl)), (fx + 10, int(y + 32))])
        
        # --- CABEZA ---
        pygame.draw.circle(pantalla, (255, 220, 200), (int(x + 16), int(y + 10)), 11)
        
        # Pelo
        for i in range(-6, 7, 2):
            px = int(x + 16 + i)
            py = int(y + 8 + abs(i) * 0.5)
            pygame.draw.line(pantalla, (60, 40, 30), 
                           (px, py - 8), (px + i * 0.5, py + 12), 2)
        
        # Coleta
        cola_ang = math.sin(self.anim_frame * 0.18) * 4
        cola_x = int(x + 28 if self.direccion == 1 else x - 2)
        cola_y = int(y + 14)
        pygame.draw.ellipse(pantalla, (60, 40, 30), 
                           (cola_x - 4, cola_y - 2 + cola_ang, 10, 14))
        pygame.draw.line(pantalla, (60, 40, 30), 
                        (cola_x, cola_y + cola_ang), 
                        (cola_x + (2 if self.direccion == 1 else -2), cola_y + 12 + cola_ang), 3)
        
        # Ojos
        ojo_off = 3 if self.direccion == 1 else -3
        if self.cantando:
            pygame.draw.line(pantalla, (0, 0, 0), 
                           (int(x + 10 + ojo_off), int(y + 8)), 
                           (int(x + 14 + ojo_off), int(y + 8)), 2)
            pygame.draw.line(pantalla, (0, 0, 0), 
                           (int(x + 18 + ojo_off), int(y + 8)), 
                           (int(x + 22 + ojo_off), int(y + 8)), 2)
        else:
            pygame.draw.circle(pantalla, (255, 255, 255), (int(x + 12 + ojo_off), int(y + 8)), 4)
            pygame.draw.circle(pantalla, (255, 255, 255), (int(x + 20 + ojo_off), int(y + 8)), 4)
            pygame.draw.circle(pantalla, (50, 30, 20), (int(x + 13 + ojo_off), int(y + 9)), 2)
            pygame.draw.circle(pantalla, (50, 30, 20), (int(x + 21 + ojo_off), int(y + 9)), 2)
            pygame.draw.circle(pantalla, (255, 255, 255), (int(x + 12 + ojo_off), int(y + 7)), 1)
            pygame.draw.circle(pantalla, (255, 255, 255), (int(x + 20 + ojo_off), int(y + 7)), 1)
        
        # Ceja
        ceja_y = int(y + 4)
        pygame.draw.line(pantalla, (40, 30, 20),
                       (int(x + 8 + ojo_off), ceja_y),
                       (int(x + 16 + ojo_off), ceja_y - 1), 2)
        pygame.draw.line(pantalla, (40, 30, 20),
                       (int(x + 16 + ojo_off), ceja_y - 1),
                       (int(x + 24 + ojo_off), ceja_y), 2)
        
        # Boca
        if self.cantando:
            pygame.draw.ellipse(pantalla, (200, 50, 50), 
                              (int(x + 11), int(y + 13), 10, 7))
            pygame.draw.rect(pantalla, (255, 255, 255),
                           (int(x + 12), int(y + 13), 4, 3))
            pygame.draw.rect(pantalla, (255, 255, 255),
                           (int(x + 17), int(y + 13), 4, 3))
        else:
            pygame.draw.arc(pantalla, (200, 50, 50),
                          (int(x + 10), int(y + 12), 12, 7), 0, math.pi, 2)
        
        # Sonrojo
        if self.nivel_borrachera >= 3:
            pygame.draw.circle(pantalla, (255, 150, 150, 100),
                             (int(x + 6 + ojo_off), int(y + 12)), 4)
            pygame.draw.circle(pantalla, (255, 150, 150, 100),
                             (int(x + 26 + ojo_off), int(y + 12)), 4)
        
        # --- BRAZOS ---
        if self.estado == "celebrando":
            brazo_off = math.sin(self.anim_frame * 0.25) * 5
            pygame.draw.line(pantalla, (255, 220, 200),
                           (int(x + 4), int(y + 18)),
                           (int(x - 4), int(y + 4 + brazo_off)), 4)
            pygame.draw.line(pantalla, (255, 220, 200),
                           (int(x + 28), int(y + 18)),
                           (int(x + 36), int(y + 4 - brazo_off)), 4)
        else:
            brazo_off = math.sin(self.anim_frame * 0.15) * 2 if abs(self.vel_x) > 1 else 0
            pygame.draw.line(pantalla, (255, 220, 200),
                           (int(x + 4), int(y + 18)),
                           (int(x - 2), int(y + 28 + brazo_off)), 4)
            pygame.draw.line(pantalla, (255, 220, 200),
                           (int(x + 28), int(y + 18)),
                           (int(x + 34), int(y + 28 - brazo_off)), 4)
        
        # --- PIERNAS ---
        leg_off = math.sin(self.anim_frame * 0.25) * 3 if abs(self.vel_x) > 1 else 0
        pygame.draw.rect(pantalla, (30, 60, 140),
                        (int(x + 4), int(y + 34), 8, 8 + leg_off))
        pygame.draw.rect(pantalla, (30, 60, 140),
                        (int(x + 20), int(y + 34), 8, 8 - leg_off))
        
        # Zapatillas
        pygame.draw.rect(pantalla, (255, 255, 255),
                        (int(x + 2), int(y + 42 + leg_off), 12, 4))
        pygame.draw.rect(pantalla, (255, 255, 255),
                        (int(x + 18), int(y + 42 - leg_off), 12, 4))
        pygame.draw.rect(pantalla, COLORES['celeste'],
                        (int(x + 3), int(y + 43 + leg_off), 4, 2))
        pygame.draw.rect(pantalla, COLORES['celeste'],
                        (int(x + 19), int(y + 43 - leg_off), 4, 2))
        
        # --- TEXTO DE CANTO (con efecto pulsante) ---
        if self.cantando and self.texto_canto:
            escala = 1.0 + 0.1 * math.sin(self.anim_frame * 0.12)
            tam = int(18 * escala)
            
            self.gestor.dibujar_texto(
                pantalla, self.texto_canto, tam, (0, 0, 0),
                int(x + 16), int(y - 35), centro=True
            )
            col = COLORES['amarillo'] if self.anim_frame % 20 < 10 else COLORES['blanco']
            self.gestor.dibujar_texto(
                pantalla, self.texto_canto, tam, col,
                int(x + 16), int(y - 37), centro=True
            )
        
        # --- EFECTO DE BORRACHERA (estrellas alrededor) ---
        if self.nivel_borrachera >= 5:
            for i in range(3):
                ang = self.anim_frame * 0.06 + i * 2.1
                sx = x + 16 + math.cos(ang) * (18 + self.nivel_borrachera)
                sy = y + 16 + math.sin(ang) * (14 + self.nivel_borrachera)
                alpha = 150 + int(math.sin(self.anim_frame * 0.12 + i) * 80)
                pygame.draw.circle(pantalla, (255, 200, 50, alpha),
                                  (int(sx), int(sy)), 2)
        
        # --- INDICADOR DE BORRACHERA ---
        if self.nivel_borrachera > 0:
            bar_x = int(x)
            bar_y = int(y - 10)
            ancho_b = int(32 * (self.nivel_borrachera / 10))
            pygame.draw.rect(pantalla, COLORES['negro'], (bar_x, bar_y, 32, 4))
            col_b = COLORES['verde'] if self.nivel_borrachera < 5 else COLORES['naranja']
            if self.nivel_borrachera >= 8:
                col_b = COLORES['rojo']
            pygame.draw.rect(pantalla, col_b, (bar_x, bar_y, ancho_b, 4))
            pygame.draw.rect(pantalla, COLORES['blanco'], (bar_x, bar_y, 32, 4), 1)