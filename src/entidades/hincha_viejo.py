# src/entidades/hincha_viejo.py
"""
KONG ARGENTINO - HINCHA VIEJO CON TAMBOR
Creado por Apresta para Prestalabs

Personaje veterano: barba blanca, camiseta argentina, tambor de hinchada.
- Sube y baja escaleras
- Busca barriles de Kong para beber
- Canta canciones del mundial al agarrar un barril
- Se tambalea según su nivel de borrachera
"""

import pygame
import math
import random
from config import ANCHO, ALTO, COLORES, GRAVEDAD, MULTIPLICADOR_GRAVEDAD_BORRACHO
from config import VEL_MAX_CAIDA_BORRACHO, TIEMPO_PEGADO_TECHO


class HinchaViejoTambor(pygame.sprite.Sprite):
    def __init__(self, x, y, gestor):
        super().__init__()
        self.gestor = gestor
        self.rect = pygame.Rect(x, y, 34, 44)

        # Estado de movimiento
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.direccion = 1
        self.anim_frame = 0
        self.offset_y = 0

        # Escaleras
        self.en_escalera = False
        self.escalera_actual = None
        self.subiendo = False
        self.bajando = False
        self.vel_subida = 2.6   # velocidad al subir
        self.vel_bajada = 2.6

        # Borrachera
        self.nivel_borrachera = random.randint(2, 5)
        self.estado = "tocando"        # "buscando", "tocando", "celebrando"
        self.tiempo_estado = 0
        self.ancla_x = x
        self.ancla_y = min(y, 90)
        self.modo_fijo_arriba = True

        # Búsqueda de barriles
        self.tiempo_idle = 0

        # Canto
        self.cantando = False
        self.tiempo_canto = 0
        self.texto_canto = ""
        self.canciones = [
            "🇦🇷 VAMOS ARGENTINA 🇦🇷",
            "🇦🇷 DALE CAMPEÓN 🇦🇷",
            "🇦🇷 LA COPA ESTÁ EN CASA 🇦🇷",
            "🇦🇷 MESSI MESSI 🇦🇷",
            "🏆 SOY ARGENTINO 🏆",
            "🇦🇷 VAMO VAMO ARGENTINA 🇦🇷",
            "🎵 ARGENTINA, ARGENTINA 🎵",
            "🇦🇷 ¡VAMOS CARAJO! 🇦🇷"
        ]

        # Física
        self.pegado_techo = False
        self.tiempo_pegado_techo = 0
        self.frames_pegado_techo = TIEMPO_PEGADO_TECHO
        self.vel_max = VEL_MAX_CAIDA_BORRACHO

        # Partículas de celebración
        self.contador_particulas = 0

        # Iniciar con un canto
        self._iniciar_canto()

    def _iniciar_canto(self):
        """Inicia un canto aleatorio (frecuencia media)"""
        if random.random() < 0.5:
            self.cantando = True
            self.tiempo_canto = random.randint(60, 150)
            self.texto_canto = random.choice(self.canciones)

    def update(self, plataformas, escaleras, barriles):
        self.anim_frame += 1
        self.offset_y = math.sin(self.anim_frame * 0.1) * 2 if not self.en_suelo else 0

        # Actualizar canto
        if self.cantando:
            self.tiempo_canto -= 1
            if self.tiempo_canto <= 0:
                self.cantando = False
                self.texto_canto = ""
                if random.random() < 0.4:
                    self._iniciar_canto()
        else:
            if self.anim_frame % 70 == 0 and random.random() < 0.55:
                self._iniciar_canto()

        # Modo fijo arriba: no camina, solo rebota y toca el bombo
        if self.modo_fijo_arriba:
            self.en_escalera = False
            self.escalera_actual = None
            self.subiendo = False
            self.bajando = False
            self.vel_x = 0
            self.vel_y = 0
            self.en_suelo = True
            self.rect.x = self.ancla_x
            if self.estado == "celebrando":
                salto = int(abs(math.sin(self.anim_frame * 0.28)) * 11)
                self.rect.y = self.ancla_y - salto
            else:
                salto = int(abs(math.sin(self.anim_frame * 0.18)) * 4)
                self.rect.y = self.ancla_y - salto
                self.estado = "tocando"
            self.tiempo_estado = max(self.tiempo_estado - 1, 0)
            if self.tiempo_estado <= 0:
                self.estado = "tocando"
                self.tiempo_estado = 0
            return

        # Detección de escalera
        self.en_escalera = False
        self.escalera_actual = None
        for e in escaleras:
            if self.rect.colliderect(e.rect_deteccion):
                self.en_escalera = True
                self.escalera_actual = e
                break

        # --- COMPORTAMIENTO SEGÚN ESTADO ---
        if self.estado == "buscando":
            self._comportamiento_buscando(plataformas, escaleras, barriles)
        elif self.estado == "tocando":
            self._comportamiento_tocando()
        elif self.estado == "celebrando":
            self._comportamiento_celebrando()
        else:
            self._comportamiento_buscando(plataformas, escaleras, barriles)

        # --- MOVIMIENTO FÍSICO ---
        self._aplicar_fisica(plataformas)

        # Límites laterales
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
            self.estado = "buscando"
            self._iniciar_canto()

    # --- COMPORTAMIENTOS ---

    def _comportamiento_buscando(self, plataformas, escaleras, barriles):
        """Busca barriles y se mueve hacia ellos, subiendo escaleras si es necesario"""
        self.tiempo_estado += 1

        # Si hay barriles, orientarse al más cercano
        if barriles and self.tiempo_idle <= 0:
            barril_cercano = min(barriles, key=lambda b: math.hypot(b.rect.x - self.rect.x,
                                                                    b.rect.y - self.rect.y))
            dx = barril_cercano.rect.x - self.rect.x
            dy = barril_cercano.rect.y - self.rect.y
            dist = math.hypot(dx, dy)

            if dist > 30:
                # Moverse horizontalmente
                spd = min(2.5 + self.nivel_borrachera // 3, 4.0)
                if abs(dx) > 15:
                    self.vel_x = spd * (1 if dx > 0 else -1)
                    self.direccion = 1 if dx > 0 else -1
                else:
                    self.vel_x = 0

                # Si el barril está en una plataforma superior, buscar escalera
                if dy < -50 and self.en_suelo and not self.en_escalera:
                    # Buscar escalera cercana
                    escalera_cercana = None
                    for e in escaleras:
                        if abs(e.rect_deteccion.x - self.rect.x) < 300:
                            if escalera_cercana is None or abs(e.rect_deteccion.x - self.rect.x) < abs(escalera_cercana.rect_deteccion.x - self.rect.x):
                                escalera_cercana = e
                    if escalera_cercana:
                        # Moverse hacia la escalera
                        dx_e = escalera_cercana.rect_deteccion.x - self.rect.x
                        if abs(dx_e) > 10:
                            self.vel_x = 2.0 * (1 if dx_e > 0 else -1)
                        else:
                            self.vel_x = 0
                        # Subir escalera si colisiona
                        if self.rect.colliderect(escalera_cercana.rect_deteccion):
                            self.en_escalera = True
                            self.escalera_actual = escalera_cercana
                            self.subiendo = True
                            self.bajando = False
                            self.rect.centerx = escalera_cercana.x_visual + 6
                            self.rect.y -= self.vel_subida
                            self.vel_y = 0
            else:
                # Cerca del barril, intentar atraparlo (la colisión se maneja en el bucle principal)
                self.vel_x = 0

        # Si no hay barriles o está idle, se mueve aleatoriamente
        else:
            if self.tiempo_idle <= 0:
                self.vel_x = random.choice([-1.5, -0.5, 0.5, 1.5])
                self.tiempo_idle = random.randint(30, 90)
            else:
                self.tiempo_idle -= 1

        # Tambalear si borracho
        if self.nivel_borrachera >= 4 and random.random() < 0.03:
            self.vel_x += random.choice([-0.8, 0.8])

        # Si está en escalera, subir o bajar según posición del barril
        if self.en_escalera and self.escalera_actual:
            # Buscar barril para decidir dirección
            if barriles:
                barril_cercano = min(barriles, key=lambda b: math.hypot(b.rect.x - self.rect.x,
                                                                        b.rect.y - self.rect.y))
                if barril_cercano.rect.y < self.rect.y - 30:
                    self.subiendo = True
                    self.bajando = False
                elif barril_cercano.rect.y > self.rect.y + 30:
                    self.subiendo = False
                    self.bajando = True
                else:
                    self.subiendo = False
                    self.bajando = False
            else:
                # Si no hay barriles, subir hasta la cima y bajar
                if self.rect.top > self.escalera_actual.y_visual + 20:
                    self.subiendo = True
                    self.bajando = False
                elif self.rect.bottom < self.escalera_actual.y_visual + self.escalera_actual.alto_visual - 20:
                    self.subiendo = False
                    self.bajando = True
                else:
                    self.subiendo = False
                    self.bajando = False

            if self.subiendo:
                self.rect.y -= self.vel_subida
                if self.rect.top < self.escalera_actual.y_visual - 5:
                    self.rect.top = self.escalera_actual.y_visual - 5
                    self.subiendo = False
            elif self.bajando:
                self.rect.y += self.vel_bajada
                if self.rect.bottom > self.escalera_actual.y_visual + self.escalera_actual.alto_visual + 10:
                    self.rect.bottom = self.escalera_actual.y_visual + self.escalera_actual.alto_visual + 10
                    self.bajando = False

            self.vel_y = 0
            return  # No aplicar gravedad mientras está en escalera

    def _comportamiento_tocando(self):
        """Se queda quieto tocando el tambor y cantando"""
        self.tiempo_estado -= 1
        self.vel_x = 0

        # Cada cierto tiempo suelta partículas de ritmo
        self.contador_particulas += 1
        if self.contador_particulas % 8 == 0 and self.gestor.sistema_particulas:
            self.gestor.sistema_particulas.emitir(
                self.rect.centerx + random.randint(-20, 20),
                self.rect.top + random.randint(-10, 10),
                random.choice([COLORES['celeste'], COLORES['blanco'], COLORES['amarillo']]),
                3, 'estrella'
            )

        # Cantar más seguido
        if self.tiempo_estado % 20 == 0:
            self._iniciar_canto()

        if self.tiempo_estado <= 0:
            self.estado = "buscando"
            self.tiempo_estado = 0

    def _comportamiento_celebrando(self):
        """Celebra después de beber un barril (salta y toca el tambor)"""
        self.tiempo_estado -= 1
        self.vel_x = 0

        if self.en_suelo and self.tiempo_estado % 15 == 0 and random.random() < 0.6:
            self.vel_y = -5 - self.nivel_borrachera * 0.15
            self.en_suelo = False

        # Partículas de celebración
        self.contador_particulas += 1
        if self.contador_particulas % 4 == 0 and self.gestor.sistema_particulas:
            self.gestor.sistema_particulas.emitir(
                self.rect.centerx + random.randint(-30, 30),
                self.rect.top - 10 + random.randint(-10, 10),
                random.choice([COLORES['celeste'], COLORES['blanco'], COLORES['oro']]),
                4, 'fuego_artificial'
            )

        if self.tiempo_estado <= 0:
            self.estado = "buscando"
            self.tiempo_estado = 0

    # --- FÍSICA ---

    def _aplicar_fisica(self, plataformas):
        """Aplica gravedad y colisiones con plataformas"""
        if self.en_escalera and (self.subiendo or self.bajando):
            return

        # Gravedad
        self.vel_y += GRAVEDAD * MULTIPLICADOR_GRAVEDAD_BORRACHO
        if self.vel_y > self.vel_max:
            self.vel_y = self.vel_max

        # Movimiento horizontal
        self.rect.x += self.vel_x
        self.vel_x *= 0.92

        # Movimiento vertical
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

    # --- INTERACCIÓN CON BARRILES ---

    def beber_barril(self):
        """Bebe un barril: aumenta borrachera, cambia a estado de celebración/tocar"""
        self.nivel_borrachera = min(10, self.nivel_borrachera + 2)
        self.gestor.reproducir_sonido('beber')

        # Efecto visual
        if self.gestor and hasattr(self.gestor, 'sistema_particulas'):
            self.gestor.sistema_particulas.emitir(
                self.rect.centerx, self.rect.top,
                COLORES['amarillo'], 10, 'combo'
            )

        # Cambiar estado a "tocando" o "celebrando"
        if random.random() < 0.6:
            self.estado = "tocando"
            self.tiempo_estado = random.randint(60, 120)
        else:
            self.estado = "celebrando"
            self.tiempo_estado = random.randint(40, 90)

        if self.modo_fijo_arriba:
            self.rect.x = self.ancla_x
            self.rect.y = self.ancla_y

        # Asegurar canto
        self.cantando = True
        self.tiempo_canto = 80
        self.texto_canto = random.choice([
            "🎵 ¡VAMOS ARGENTINA! 🎵",
            "🥁 ¡DALE CAMPEÓN! 🥁",
            "🇦🇷 ¡ARGENTINA, ARGENTINA! 🇦🇷",
            "🏆 ¡LA COPA ESTÁ EN CASA! 🏆"
        ])

        # Si la borrachera es muy alta, se tambalea mucho
        if self.nivel_borrachera >= 7:
            self.vel_x = random.choice([-2, -1, 1, 2]) * 1.5

    # --- DIBUJO ---

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y + self.offset_y
        x += self.vel_x * 0.5  # pequeño desplazamiento por inercia

        # Sombra
        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 32, 8)

        # --- EFECTO DE BORRACHERA (tambaleo) ---
        wobble_x = 0
        wobble_y = 0
        if self.nivel_borrachera >= 3:
            wobble_x = math.sin(self.anim_frame * 0.2) * (self.nivel_borrachera / 3)
            if self.nivel_borrachera >= 6:
                wobble_y = math.sin(self.anim_frame * 0.12) * 2
        x += wobble_x
        y += wobble_y

        # --- TAMBOR ---
        tambor_x = x + 28 if self.direccion == 1 else x - 12
        tambor_y = y + 18

        # Cuerpo del tambor (cilindro)
        pygame.draw.ellipse(pantalla, (180, 150, 120), (tambor_x, tambor_y, 14, 12))
        pygame.draw.rect(pantalla, (200, 170, 140), (tambor_x, tambor_y + 6, 14, 14))
        pygame.draw.ellipse(pantalla, (220, 200, 180), (tambor_x - 1, tambor_y + 18, 16, 6))
        # Parche superior
        pygame.draw.ellipse(pantalla, (240, 220, 200), (tambor_x + 2, tambor_y + 2, 10, 8))
        pygame.draw.circle(pantalla, (200, 180, 160), (tambor_x + 7, tambor_y + 6), 2)

        # Brazos (tocando el tambor o balanceándose)
        if self.estado == "tocando" or self.estado == "celebrando":
            # Movimiento de brazos para tocar
            brazo_off = math.sin(self.anim_frame * 0.3) * 4
            # Brazo derecho (tambor)
            pygame.draw.line(pantalla, (255, 220, 200),
                             (x + 26, y + 20),
                             (tambor_x + 10 + brazo_off, tambor_y + 4), 4)
            # Brazo izquierdo
            pygame.draw.line(pantalla, (255, 220, 200),
                             (x + 2, y + 20),
                             (x - 4, y + 16 - brazo_off), 4)
        else:
            # Brazos normales
            brazo_off = math.sin(self.anim_frame * 0.15) * 2 if abs(self.vel_x) > 1 else 0
            if self.direccion == 1:
                pygame.draw.line(pantalla, (255, 220, 200),
                                 (x + 26, y + 20),
                                 (x + 34, y + 28 + brazo_off), 4)
                pygame.draw.line(pantalla, (255, 220, 200),
                                 (x + 2, y + 20),
                                 (x - 4, y + 28 - brazo_off), 4)
            else:
                pygame.draw.line(pantalla, (255, 220, 200),
                                 (x + 2, y + 20),
                                 (x - 6, y + 28 + brazo_off), 4)
                pygame.draw.line(pantalla, (255, 220, 200),
                                 (x + 26, y + 20),
                                 (x + 32, y + 28 - brazo_off), 4)

        # --- CUERPO (camiseta argentina) ---
        pygame.draw.rect(pantalla, COLORES['celeste'], (int(x + 4), int(y + 14), 26, 22))
        # Franjas blancas
        for i in range(0, 26, 8):
            pygame.draw.rect(pantalla, COLORES['blanco'], (int(x + 4 + i), int(y + 14), 4, 22))
        pygame.draw.rect(pantalla, COLORES['blanco'], (int(x + 10), int(y + 12), 14, 6))  # cuello

        # Número 10
        self.gestor.dibujar_texto(pantalla, "10", 14, (0, 0, 0),
                                  int(x + 17), int(y + 18), centro=True)

        # --- PIERNAS ---
        leg_off = math.sin(self.anim_frame * 0.25) * 3 if abs(self.vel_x) > 1 else 0
        pygame.draw.rect(pantalla, (30, 60, 140), (int(x + 6), int(y + 36), 8, 8 + leg_off))
        pygame.draw.rect(pantalla, (30, 60, 140), (int(x + 20), int(y + 36), 8, 8 - leg_off))
        # Zapatos
        pygame.draw.rect(pantalla, (40, 40, 40), (int(x + 4), int(y + 44 + leg_off), 12, 4))
        pygame.draw.rect(pantalla, (40, 40, 40), (int(x + 18), int(y + 44 - leg_off), 12, 4))

        # --- CABEZA ---
        # Piel
        pygame.draw.circle(pantalla, (240, 220, 200), (int(x + 17), int(y + 8)), 12)

        # Pelo blanco (viejo)
        for i in range(-6, 7, 2):
            px = int(x + 17 + i * 0.8)
            py = int(y + 6 + abs(i) * 0.4)
            pygame.draw.line(pantalla, (220, 220, 220),
                             (px, py - 8), (px + i * 0.3, py + 6), 2)

        # Barba blanca
        for i in range(-5, 6, 2):
            bx = int(x + 17 + i * 1.2)
            by = int(y + 12 + abs(i) * 0.3)
            pygame.draw.line(pantalla, (240, 240, 240),
                             (bx, by), (bx + i * 0.2, by + 8 + abs(i) * 0.3), 3)

        # Ojos
        ojo_off = 3 if self.direccion == 1 else -3
        if self.cantando or self.estado in ("tocando", "celebrando"):
            # Ojos cerrados (cantando)
            pygame.draw.line(pantalla, (0, 0, 0),
                             (int(x + 11 + ojo_off), int(y + 7)),
                             (int(x + 15 + ojo_off), int(y + 7)), 2)
            pygame.draw.line(pantalla, (0, 0, 0),
                             (int(x + 19 + ojo_off), int(y + 7)),
                             (int(x + 23 + ojo_off), int(y + 7)), 2)
        else:
            pygame.draw.circle(pantalla, (255, 255, 255), (int(x + 13 + ojo_off), int(y + 6)), 4)
            pygame.draw.circle(pantalla, (255, 255, 255), (int(x + 21 + ojo_off), int(y + 6)), 4)
            pygame.draw.circle(pantalla, (50, 30, 20), (int(x + 14 + ojo_off), int(y + 7)), 2)
            pygame.draw.circle(pantalla, (50, 30, 20), (int(x + 22 + ojo_off), int(y + 7)), 2)
            pygame.draw.circle(pantalla, (255, 255, 255), (int(x + 13 + ojo_off), int(y + 5)), 1)
            pygame.draw.circle(pantalla, (255, 255, 255), (int(x + 21 + ojo_off), int(y + 5)), 1)

        # Ceja
        ceja_y = int(y + 2)
        pygame.draw.line(pantalla, (200, 200, 200),
                         (int(x + 9 + ojo_off), ceja_y),
                         (int(x + 17 + ojo_off), ceja_y - 1), 2)
        pygame.draw.line(pantalla, (200, 200, 200),
                         (int(x + 17 + ojo_off), ceja_y - 1),
                         (int(x + 25 + ojo_off), ceja_y), 2)

        # Boca
        if self.cantando or self.estado in ("tocando", "celebrando"):
            pygame.draw.ellipse(pantalla, (200, 50, 50),
                              (int(x + 12), int(y + 12), 10, 7))
            pygame.draw.rect(pantalla, (255, 255, 255),
                           (int(x + 13), int(y + 12), 4, 3))
            pygame.draw.rect(pantalla, (255, 255, 255),
                           (int(x + 18), int(y + 12), 4, 3))
        else:
            pygame.draw.arc(pantalla, (200, 50, 50),
                          (int(x + 11), int(y + 12), 12, 6), 0, math.pi, 2)

        # Sonrojo (borracho)
        if self.nivel_borrachera >= 3:
            pygame.draw.circle(pantalla, (255, 150, 150, 100),
                             (int(x + 7 + ojo_off), int(y + 11)), 4)
            pygame.draw.circle(pantalla, (255, 150, 150, 100),
                             (int(x + 27 + ojo_off), int(y + 11)), 4)

        # --- TEXTO DE CANTO ---
        if self.cantando and self.texto_canto:
            escala = 1.0 + 0.1 * math.sin(self.anim_frame * 0.12)
            tam = int(18 * escala)

            self.gestor.dibujar_texto(
                pantalla, self.texto_canto, tam, (0, 0, 0),
                int(x + 17), int(y - 32), centro=True
            )
            col = COLORES['amarillo'] if self.anim_frame % 20 < 10 else COLORES['blanco']
            self.gestor.dibujar_texto(
                pantalla, self.texto_canto, tam, col,
                int(x + 17), int(y - 34), centro=True
            )

        # --- INDICADOR DE BORRACHERA ---
        if self.nivel_borrachera > 0:
            bar_x = int(x)
            bar_y = int(y - 8)
            ancho_b = int(34 * (self.nivel_borrachera / 10))
            pygame.draw.rect(pantalla, COLORES['negro'], (bar_x, bar_y, 34, 4))
            col_b = COLORES['verde'] if self.nivel_borrachera < 5 else COLORES['naranja']
            if self.nivel_borrachera >= 8:
                col_b = COLORES['rojo']
            pygame.draw.rect(pantalla, col_b, (bar_x, bar_y, ancho_b, 4))
            pygame.draw.rect(pantalla, COLORES['blanco'], (bar_x, bar_y, 34, 4), 1)

        # --- ESTRELLAS DE BORRACHERA (efecto visual) ---
        if self.nivel_borrachera >= 5:
            for i in range(3):
                ang = self.anim_frame * 0.06 + i * 2.1
                sx = x + 17 + math.cos(ang) * (18 + self.nivel_borrachera)
                sy = y + 16 + math.sin(ang) * (14 + self.nivel_borrachera)
                alpha = 150 + int(math.sin(self.anim_frame * 0.12 + i) * 80)
                pygame.draw.circle(pantalla, (255, 200, 50, alpha),
                                  (int(sx), int(sy)), 2)