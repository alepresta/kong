# src/juego/estados.py
"""KONG ARGENTINO - Gestión de estados y update"""
import pygame
import sys
import os
import random
import math
import pickle
from constantes import *

class EstadosMixin:
    def reiniciar_juego(self):
        self.nivel = 1
        self.puntuacion = 0
        self.crear_nivel()
        self.estado = "jugando"
        self._tiempo_resultado = 0

    def siguiente_nivel(self):
        self.nivel += 1
        if self.nivel > 6:
            self.estado = "victoria_final"
            if self.puntuacion > self.high_score:
                self.high_score = self.puntuacion
                self._guardar_high_score()
                self.gestor.reproducir_sonido('record')
            else:
                self.gestor.reproducir_sonido('victoria_final')
            for _ in range(80):
                self.emitir(random.randint(0, ANCHO), random.randint(0, ALTO // 2),
                             random.choice([COLORES['oro'], COLORES['celeste'],
                                            COLORES['blanco'], COLORES['amarillo'],
                                            COLORES['rosa'], COLORES['naranja']]),
                             6, 'fuego_artificial')
            return
        self.puntuacion += PUNTUACION_POR_NIVEL * self.nivel
        self.crear_nivel()
        self.estado = "jugando"
        self._tiempo_resultado = 0

    # ──────────────────────── UPDATE ─────────────────────────────── #

    def _update_juego(self):
        self.argentino.update(self.plataformas, self.escaleras)
        self.borracho.update(self.plataformas, self.escaleras, self.barriles)
        for hincha in self.hinchada:
            hincha.update(self.plataformas, self.escaleras, self.barriles)
        
        self.princesa.update()
        self.kong.update(self.plataformas)

        dist_kong = math.hypot(self.argentino.rect.x - self.kong.rect.x,
                               self.argentino.rect.y - self.kong.rect.y)
        self.kong.set_mario_cerca(dist_kong < 250)

        cfg = DIFICULTAD_NIVEL.get(self.nivel, DIFICULTAD_NIVEL[5])

        if (self.kong.tiempo_barril > self.kong.get_tiempo_barril()
                and len(self.barriles) < cfg['max_barriles']):
            barril = self.kong.lanzar_barril()
            self.barriles.append(barril)
            self.kong.tiempo_barril = 0

        # ── Actualizar barriles ──
        for b in self.barriles[:]:
            b.update(self.plataformas, self.escaleras)
            
            if hasattr(b, 'eliminar') and b.eliminar:
                self.emitir(b.rect.centerx, b.rect.centery, COLORES['marron'], 12, 'explosion')
                self.emitir(b.rect.centerx, b.rect.centery, COLORES['amarillo'], 6, 'chispa')
                self.barriles.remove(b)
                continue

            if (not self.argentino.tiene_poder
                    and self.argentino.vel_y > 0
                    and not self.argentino.en_suelo
                    and self.argentino.rect.bottom <= b.rect.top + 10
                    and abs(self.argentino.rect.centerx - b.rect.centerx) < 28):
                self._otorgar_puntos(PUNTUACION_POR_BARRIL_SALTADO,
                                      b.rect.centerx, b.rect.top - 10,
                                      COLORES['cyan'], texto="¡SALTO! +25")
                self.gestor.reproducir_sonido('barril_saltado')

            if self.argentino.rect.colliderect(b.rect):
                if self.argentino.tiene_poder:
                    self._otorgar_puntos(PUNTUACION_POR_BARRIL_ROTO,
                                          b.rect.centerx, b.rect.top,
                                          COLORES['verde'])
                    self.barriles.remove(b)
                    self.emitir(b.rect.centerx, b.rect.centery, COLORES['verde'], 15, 'explosion')
                    self.emitir(b.rect.centerx, b.rect.centery, COLORES['amarillo'], 8, 'chispa')
                    self.gestor.reproducir_sonido('golpe')
                else:
                    if self.argentino.golpear():
                        self.gestor.iniciar_shake(SHAKE_DURACION, SHAKE_INTENSIDAD)
                        self.gestor.iniciar_flash((220, 0, 0), 10)
                        self.emitir(self.argentino.rect.centerx, self.argentino.rect.centery,
                                    COLORES['rojo'], 20, 'golpe')
                        self.gestor.reproducir_sonido('golpe_fuerte')
                        self.texto_flotante("💥 ¡AY! 💥", self.argentino.rect.centerx,
                                            self.argentino.rect.top, COLORES['rojo'], 30)
                        if self.argentino.vidas <= 0:
                            self._game_over()
                        else:
                            self.argentino.respawn(100, ALTO - 70)
                    if b in self.barriles:
                        self.barriles.remove(b)
                continue

            if self.borracho.rect.colliderect(b.rect):
                self.borracho.beber_barril()
                self.barriles.remove(b)
                self.emitir(b.rect.centerx, b.rect.centery, COLORES['amarillo'], 10, 'explosion')
                self._otorgar_puntos(50, b.rect.centerx, b.rect.top, COLORES['celeste'],
                                      texto="🍺 +50 (Borracho!)")
                continue

            barril_consumido = False
            for hincha in self.hinchada:
                if self._hincha_colisiona_rect(hincha, b.rect):
                    hincha.beber_barril()
                    if b in self.barriles:
                        self.barriles.remove(b)
                    self.emitir(b.rect.centerx, b.rect.centery, COLORES['amarillo'], 10, 'explosion')
                    puntos_hincha = getattr(hincha, 'puntos_barril', 30)
                    texto_hincha = getattr(hincha, 'etiqueta_puntos', "🍺 +30 (Hincha)")
                    self._otorgar_puntos(puntos_hincha, b.rect.centerx, b.rect.top, COLORES['celeste'],
                                         texto=texto_hincha)
                    barril_consumido = True
                    break
            if barril_consumido:
                continue

            if b.rect.y > ALTO + 60 or b.rect.x < -60 or b.rect.x > ANCHO + 60:
                self.barriles.remove(b)
                continue

        # ── Cervezas ──
        for c in self.cervezas[:]:
            if self.argentino.rect.colliderect(c.rect):
                self.argentino.add_combo()
                self._otorgar_puntos(PUNTUACION_POR_CERVEZA,
                                      c.rect.centerx, c.rect.top,
                                      COLORES['amarillo'])
                self.cervezas.remove(c)
                self.gestor.reproducir_sonido('moneda')
                self.emitir(c.rect.centerx, c.rect.centery, COLORES['amarillo'], 8, 'estrella')
                if self.argentino.combo >= 5:
                    self.gestor.reproducir_sonido('combo_x5')
                    self.emitir(c.rect.centerx, c.rect.centery, COLORES['oro'], 18, 'combo')
                elif self.argentino.combo >= 3:
                    self.gestor.reproducir_sonido('combo')
                    self.emitir(c.rect.centerx, c.rect.centery, COLORES['oro'], 12, 'combo')

        # ── Poderes ──
        for p in self.poderes[:]:
            if self.argentino.rect.colliderect(p.rect):
                self.argentino.tiene_poder = True
                self.argentino.tiempo_poder = TIEMPO_PODER
                self.poderes.remove(p)
                self.gestor.reproducir_sonido('martillo')
                self.emitir(p.rect.centerx, p.rect.centery, COLORES['verde'], 22, 'combo')
                self.gestor.iniciar_flash((0, 200, 0), 8)
                self.texto_flotante("🧉 ¡MATE POWER! 🧉", p.rect.centerx, p.rect.top - 10,
                                    COLORES['verde'], 28)

        # ── ATAQUE ──
        if self.argentino.ataque_activo:
            ataque_rect = self.argentino.ataque_rect
            
            if ataque_rect.colliderect(self.kong.rect):
                self._golpear_kong()
            
            if ataque_rect.colliderect(self.borracho.rect):
                self._golpear_borracho()
            
            for hincha in self.hinchada:
                if self._hincha_colisiona_rect(hincha, ataque_rect):
                    self._golpear_hincha(hincha)
                    break

        # ── Colisión jugador - Kong ──
        if self.argentino.rect.colliderect(self.kong.rect):
            if not self.argentino.tiene_poder and not self.argentino.ataque_activo:
                if self.argentino.golpear():
                    self.gestor.iniciar_shake(SHAKE_DURACION + 5, SHAKE_INTENSIDAD + 2)
                    self.gestor.iniciar_flash((220, 0, 0), 14)
                    self.emitir(self.argentino.rect.centerx, self.argentino.rect.centery,
                                COLORES['rojo'], 20, 'golpe')
                    self.gestor.reproducir_sonido('golpe_fuerte')
                    if self.argentino.vidas <= 0:
                        self._game_over()
                    else:
                        self.argentino.respawn(100, ALTO - 70)

        # ── Victoria ──
        if self.argentino.rect.colliderect(self.princesa.rect):
            self.estado = "victoria"
            self._tiempo_resultado = 0
            self.gestor.reproducir_sonido('nivel')
            if self.puntuacion > self.high_score:
                self.high_score = self.puntuacion
                self._guardar_high_score()
            for _ in range(80):
                self.emitir(random.randint(0, ANCHO), random.randint(0, ALTO // 2),
                             random.choice([COLORES['oro'], COLORES['celeste'],
                                            COLORES['blanco'], COLORES['amarillo'],
                                            COLORES['rosa']]),
                             6, 'fuego_artificial')

    def _game_over(self):
        self.estado = "game_over"
        self._tiempo_resultado = 0
        if self.puntuacion > self.high_score:
            self.high_score = self.puntuacion
            self._guardar_high_score()
            self.gestor.reproducir_sonido('record')
        else:
            self.gestor.reproducir_sonido('game_over')
        self.gestor.iniciar_flash((255, 0, 0), 20)
        self.gestor.iniciar_shake(30, 8)

    # ──────────────────────── LOOP PRINCIPAL ─────────────────────── #

