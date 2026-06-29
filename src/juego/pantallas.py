# src/juego/pantallas.py
"""KONG ARGENTINO - Renderizado de pantallas"""
import pygame
import sys
import os
import random
import math
import pickle
from constantes import *

class PantallasMixin:
    def dibujar(self):
        ox, oy = self.gestor.get_shake()
        surf_juego = pygame.Surface((ANCHO, ALTO))
        self.gestor.dibujar_fondo(surf_juego, self.nivel)

        for p in self.plataformas:
            p.dibujar(surf_juego)
        for e in self.escaleras:
            e.dibujar(surf_juego)
        for c in self.cervezas:
            c.dibujar(surf_juego)
        for b in self.barriles:
            b.dibujar(surf_juego)
        for p in self.poderes:
            p.dibujar(surf_juego)

        self.kong.dibujar(surf_juego)
        self.princesa.dibujar(surf_juego)
        self.argentino.dibujar(surf_juego)
        self.borracho.dibujar(surf_juego)
        for hincha in self.hinchada:
            hincha.dibujar(surf_juego)

        self.particulas.dibujar(surf_juego)
        self.dibujar_textos()

        self.pantalla.blit(surf_juego, (ox, oy))
        self.dibujar_hud()
        self.gestor.aplicar_flash(self.pantalla)
        
        # Dibujar controles táctiles en modo juego
        self.controles_tactiles.dibujar(self.pantalla)

        if self.pausa:
            s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            s.fill((0, 0, 0, 175))
            self.pantalla.blit(s, (0, 0))
            self.gestor.dibujar_texto(self.pantalla, "⏸  PAUSA", 72, COLORES['blanco'],
                                       ANCHO//2, ALTO//2 - 60, centro=True, sombra=True)
            self.gestor.dibujar_texto(self.pantalla, "P  continuar  |  ESC  menú  |  [ ]  volumen",
                                       22, COLORES['amarillo'], ANCHO//2, ALTO//2 + 30, centro=True)
            vol = int(self.gestor.generador_sonidos.volumen_maestro * 100)
            self.gestor.dibujar_texto(self.pantalla, f"Volumen: {vol}%",
                                       20, COLORES['celeste'], ANCHO//2, ALTO//2 + 62, centro=True)

    def dibujar_menu(self):
        self.gestor.dibujar_menu(self.pantalla)
        mx, my = pygame.mouse.get_pos()

        start_rect = pygame.Rect(ANCHO//2 - 120, 548, 240, 55)
        exit_rect  = pygame.Rect(ANCHO//2 - 120, 616, 240, 55)
        self.gestor.dibujar_boton(self.pantalla, start_rect.x, start_rect.y,
                                   "▶  INICIAR", 240, 55, start_rect.collidepoint(mx, my))
        self.gestor.dibujar_boton(self.pantalla, exit_rect.x, exit_rect.y,
                                   "✖  SALIR",   240, 55, exit_rect.collidepoint(mx, my))
        if self.high_score > 0:
            self.gestor.dibujar_texto(self.pantalla, f"🏆 RÉCORD: {self.high_score:06d}", 22,
                                       COLORES['oro'], ANCHO//2, 682, centro=True, sombra=True)
        perfil = self.perfiles_jugador[self.indice_perfil]
        left_rect = pygame.Rect(ANCHO//2 - 180, 492, 40, 40)
        right_rect = pygame.Rect(ANCHO//2 + 140, 492, 40, 40)
        pygame.draw.rect(self.pantalla, COLORES['azul'], left_rect, border_radius=6)
        pygame.draw.rect(self.pantalla, COLORES['azul'], right_rect, border_radius=6)
        pygame.draw.rect(self.pantalla, COLORES['celeste'], left_rect, 2, border_radius=6)
        pygame.draw.rect(self.pantalla, COLORES['celeste'], right_rect, 2, border_radius=6)
        self.gestor.dibujar_texto(self.pantalla, "<", 28, COLORES['blanco'], left_rect.centerx - 6, left_rect.y + 3)
        self.gestor.dibujar_texto(self.pantalla, ">", 28, COLORES['blanco'], right_rect.centerx - 6, right_rect.y + 3)
        self.gestor.dibujar_texto(self.pantalla, "PERFIL", 16, COLORES['gris'], ANCHO//2, 470, centro=True)
        self.gestor.dibujar_texto(self.pantalla,
                                  f"{perfil['nombre']}  |  estilo: {perfil['personaje']}",
                                  20, COLORES['blanco'], ANCHO//2, 500, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla,
                                  "A/D o Flechas: cambiar perfil  |  ENTER: iniciar",
                                  14, COLORES['gris'], ANCHO//2, 530, centro=True)
        return start_rect, exit_rect, left_rect, right_rect

    def dibujar_game_over(self):
        self.gestor.dibujar_fondo(self.pantalla, self.nivel)
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 195))
        self.pantalla.blit(s, (0, 0))

        parpadeo = (self._frame_global // 20) % 2 == 0
        col = COLORES['rojo'] if parpadeo else (160, 0, 0)
        self.gestor.dibujar_texto(self.pantalla, "💀 GAME OVER 💀", 70, col,
                                   ANCHO//2, ALTO//2 - 120, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"PUNTOS: {self.puntuacion:06d}", 38,
                                   COLORES['oro'], ANCHO//2, ALTO//2 - 30, centro=True, sombra=True)
        if self.puntuacion >= self.high_score and self.high_score > 0:
            self.gestor.dibujar_texto(self.pantalla, "🏆 ¡NUEVO RÉCORD! 🏆", 30,
                                       COLORES['amarillo'], ANCHO//2, ALTO//2 + 22, centro=True, sombra=True)
        hint_col = COLORES['blanco'] if self._tiempo_resultado < 30 else COLORES['gris']
        self.gestor.dibujar_texto(self.pantalla, "R  reiniciar  |  ESC  menú", 26,
                                   hint_col, ANCHO//2, ALTO//2 + 90, centro=True)
        self.particulas.dibujar(self.pantalla)

    def dibujar_victoria(self):
        self.gestor.dibujar_fondo(self.pantalla, self.nivel)
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 170))
        self.pantalla.blit(s, (0, 0))

        t = self._frame_global
        col = COLORES['oro'] if (t // 15) % 2 == 0 else COLORES['amarillo']
        self.gestor.dibujar_texto(self.pantalla, "🎉 ¡RESCATASTE A PAULINE! 🎉", 50, col,
                                   ANCHO//2, ALTO//2 - 110, centro=True, sombra=True)

        # Escena corta de rescate para hacer visible el exito del nivel.
        px = ANCHO // 2
        py = ALTO // 2 + 25
        salto = int(math.sin(t * 0.08) * 5)
        self.princesa.rect.centerx = px - 40
        self.princesa.rect.centery = py + salto
        self.princesa.dibujar(self.pantalla)
        self.argentino.rect.centerx = px + 40
        self.argentino.rect.centery = py + salto
        self.argentino.dibujar(self.pantalla)
        self.gestor.dibujar_copa_mundo(self.pantalla, px, py - 45 + salto, escala=2.0)

        self.gestor.dibujar_texto(self.pantalla, f"PUNTOS: {self.puntuacion:06d}", 34,
                                   COLORES['blanco'], ANCHO//2, ALTO//2 - 85, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"Nivel {self.nivel + 1} te espera...", 26,
                                   COLORES['celeste'], ANCHO//2, ALTO//2 + 80, centro=True)
        self.gestor.dibujar_texto(self.pantalla, "Auto avance en 10s  |  R siguiente  |  ESC menú", 22,
                                   COLORES['blanco'], ANCHO//2, ALTO//2 + 125, centro=True)
        self.particulas.dibujar(self.pantalla)

    # ─── NUEVA VERSIÓN DE VICTORIA FINAL CON CELEBRACIÓN MUNDIALISTA ───
    def dibujar_victoria_final(self):
        # Fondo de estadio (gradas)
        self.gestor.dibujar_fondo(self.pantalla, 5)
        s_estadio = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        for i in range(0, ALTO//2, 10):
            color = (0, 100, 0) if (i//10) % 2 == 0 else (200, 180, 0)
            pygame.draw.rect(s_estadio, color, (0, i, ANCHO, 10))
        self.pantalla.blit(s_estadio, (0, 0))
        
        oscuro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        oscuro.fill((0, 0, 0, 150))
        self.pantalla.blit(oscuro, (0, 0))

        t = self._frame_global
        px = ANCHO // 2
        py = ALTO // 2 + 60
        salto = int(math.sin(t * 0.08) * 25)
        
        # Pauline (izquierda)
        self.princesa.rect.centerx = px - 45
        self.princesa.rect.centery = py + salto
        self.princesa.dibujar(self.pantalla)
        
        # Jugador (derecha)
        self.argentino.rect.centerx = px + 45
        self.argentino.rect.centery = py + salto
        self.argentino.dibujar(self.pantalla)
        
        # Copa del Mundo en el centro (más grande y con brillo)
        copa_x = px
        copa_y = py - 60 + salto  # Ajuste para subir la copa
        self.gestor.dibujar_copa_mundo(self.pantalla, copa_x, copa_y, escala=3.0)
        
        # Destello en la copa (animado)
        if t % 20 < 10:
            glow = pygame.Surface((120, 120), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 255, 200, 80), (60, 60), 60)
            self.pantalla.blit(glow, (copa_x - 60, copa_y - 80))
        else:
            glow = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 255, 200, 40), (40, 40), 40)
            self.pantalla.blit(glow, (copa_x - 40, copa_y - 60))
        
        # Textos épicos
        escala_tit = 1.0 + 0.05 * math.sin(t * 0.05)
        tam_tit = int(62 * escala_tit)
        col_tit = COLORES['oro'] if (t // 20) % 2 == 0 else COLORES['amarillo']
        self.gestor.dibujar_texto(self.pantalla, "🏆 ¡CAMPEONES DEL MUNDO! 🏆", tam_tit,
                                   col_tit, ANCHO//2, 80, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, "🇦🇷 ARGENTINA CAMPEÓN 🇦🇷", 40,
                                   COLORES['celeste'], ANCHO//2, 150, centro=True, sombra=True)
        frases = ["¡VAMOS CARAJO!", "¡LA COPA ESTÁ EN CASA!", "¡SOMOS CAMPEONES!", "¡DALE DALE!"]
        frase = frases[(t // 60) % len(frases)]
        self.gestor.dibujar_texto(self.pantalla, frase, 32,
                                   COLORES['blanco'], ANCHO//2, 210, centro=True, sombra=True)
        
        # Confeti y fuegos artificiales
        if t % 5 == 0:
            self.emitir(random.randint(0, ANCHO), random.randint(20, ALTO//2),
                         random.choice([COLORES['celeste'], COLORES['blanco'],
                                        COLORES['amarillo'], COLORES['oro'],
                                        COLORES['rosa'], COLORES['naranja']]),
                         8, 'fuego_artificial')
        if t % 12 == 0:
            for _ in range(10):
                self.emitir(random.randint(0, ANCHO), random.randint(20, ALTO//2),
                             random.choice([COLORES['celeste'], COLORES['blanco'],
                                            COLORES['amarillo'], COLORES['oro']]),
                             4, 'estrella')
        
        self.gestor.dibujar_texto(self.pantalla, "ESC  menú principal", 24,
                                   COLORES['blanco'], ANCHO//2, ALTO-50, centro=True, sombra=True)
        self.particulas.actualizar()
        self.particulas.dibujar(self.pantalla)

    # ──────────────────────── ESTADOS ────────────────────────────── #

