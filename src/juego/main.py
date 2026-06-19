# src/juego/main.py
"""
KONG ARGENTINO v4.0 - JUEGO PRINCIPAL
"""
import pygame
import sys
import os
import random
import math
import pickle
from constantes import *
from gestor_graficos import GestorGraficos
from entidades import (
    Argentino, BorrachoIA, Plataforma, Escalera,
    BarrilCerveza, PoderMate, Princesa, KongCervecero,
    HinchaBorrachito, HinchaArgentina,
    HinchaViejoTambor,
    HinchaBorrachin, HinchaRandom, HinchaConBengala, HinchaGemelos, HinchaAbuela,
    SistemaParticulas, TextoFlotante
)
from niveles.generador import generar_layout_nivel


from juego.persistencia import PersistenciaMixin
from juego.nivel import NivelMixin
from juego.helpers import HelpersMixin
from juego.colisiones import ColisionesMixin
from juego.hud import HudMixin
from juego.pantallas import PantallasMixin
from juego.estados import EstadosMixin


class KongArgentino(
    PersistenciaMixin,
    NivelMixin,
    HelpersMixin,
    ColisionesMixin,
    HudMixin,
    PantallasMixin,
    EstadosMixin,
):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(f"{NOMBRE_JUEGO} - v{VERSION}")

        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.clock = pygame.time.Clock()
        self.gestor = GestorGraficos()
        self.particulas = SistemaParticulas(self.gestor)
        self.gestor.particulas = self.particulas.particulas
        self.gestor.sistema_particulas = self.particulas
        self.textos_flotantes = []

        self.estado = "menu"
        self.nivel = 1
        self.puntuacion = 0
        self.high_score = self._cargar_high_score()
        self.perfiles_jugador = [
            {"nombre": "Mario", "personaje": "mario"},
            {"nombre": "Pibe", "personaje": "hincha"},
        ]
        self.indice_perfil = 0
        self.nombre_jugador = NOMBRE_JUGADOR
        self.personaje_actual = "mario"
        self._cargar_perfil()
        self.pausa = False

        self.plataformas = []
        self.escaleras = []
        self.barriles = []
        self.poderes = []
        self.cervezas = []

        self.argentino = None
        self.borracho = None
        self.hincha = None
        self.hinchada = []
        self.kong = None
        self.princesa = None

        self._frame_global = 0
        self._tiempo_resultado = 0
        self.crear_nivel()

    # ──────────────────────── PERSISTENCIA ────────────────────────── #



    def run(self):
        while True:
            self.clock.tick(FPS)
            self._frame_global += 1
            self._tiempo_resultado += 1
            self.gestor.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._guardar_high_score()
                    self._guardar_perfil()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    key = event.key

                    if key == pygame.K_LEFTBRACKET:
                        self.gestor.generador_sonidos.set_volumen(
                            self.gestor.generador_sonidos.volumen_maestro - 0.1)
                    if key == pygame.K_RIGHTBRACKET:
                        self.gestor.generador_sonidos.set_volumen(
                            self.gestor.generador_sonidos.volumen_maestro + 0.1)

                    if key == pygame.K_ESCAPE:
                        if self.estado in ("jugando", "game_over", "victoria", "victoria_final"):
                            self.estado = "menu"
                            self.pausa = False

                    if key == pygame.K_p and self.estado == "jugando":
                        self.pausa = not self.pausa

                    if key == pygame.K_r and self._tiempo_resultado > 30:
                        if self.estado == "game_over":
                            self.reiniciar_juego()
                        elif self.estado == "victoria":
                            self.siguiente_nivel()

                    if key == pygame.K_q and self.estado == "menu":
                        self._guardar_high_score()
                        self._guardar_perfil()
                        pygame.quit()
                        sys.exit()

                    if self.estado == "menu" and key in (pygame.K_LEFT, pygame.K_a):
                        self._cambiar_perfil(-1)
                    if self.estado == "menu" and key in (pygame.K_RIGHT, pygame.K_d):
                        self._cambiar_perfil(1)
                    if self.estado == "menu" and key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.reiniciar_juego()

                if event.type == pygame.MOUSEBUTTONDOWN and self.estado == "menu":
                    mx, my = pygame.mouse.get_pos()
                    start_rect = pygame.Rect(ANCHO//2 - 120, 548, 240, 55)
                    exit_rect  = pygame.Rect(ANCHO//2 - 120, 616, 240, 55)
                    left_rect = pygame.Rect(ANCHO//2 - 180, 492, 40, 40)
                    right_rect = pygame.Rect(ANCHO//2 + 140, 492, 40, 40)
                    if start_rect.collidepoint(mx, my):
                        self.reiniciar_juego()
                    elif exit_rect.collidepoint(mx, my):
                        self._guardar_high_score()
                        self._guardar_perfil()
                        pygame.quit()
                        sys.exit()
                    elif left_rect.collidepoint(mx, my):
                        self._cambiar_perfil(-1)
                    elif right_rect.collidepoint(mx, my):
                        self._cambiar_perfil(1)

            self.particulas.actualizar()
            self.actualizar_textos()

            if self.estado == "menu":
                self.pantalla.fill((0, 0, 0))
                self.dibujar_menu()

            elif self.estado == "game_over":
                self.dibujar_game_over()

            elif self.estado == "victoria":
                self.dibujar_victoria()
                if self._tiempo_resultado >= DURACION_CELEBRACION_RESCATE:
                    self.siguiente_nivel()

            elif self.estado == "victoria_final":
                self.dibujar_victoria_final()

            elif self.estado == "jugando":
                if not self.pausa:
                    self._update_juego()
                self.dibujar()

            pygame.display.flip()