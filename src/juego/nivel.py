# src/juego/nivel.py
"""KONG ARGENTINO - Creación de nivel"""
import pygame
import sys
import os
import random
import math
import pickle
from constantes import *
from entidades import (
    Argentino, BorrachoIA, Plataforma, Escalera,
    BarrilCerveza, PoderMate, Princesa, KongCervecero,
    HinchaArgentina, HinchaViejoTambor,
    HinchaBorrachin, HinchaRandom, HinchaConBengala,
    HinchaGemelos, HinchaAbuela, HinchaBorrachito,
)
from niveles.generador import generar_layout_nivel

class NivelMixin:
    def crear_nivel(self):
        self.plataformas = []
        self.escaleras = []
        self.barriles = []
        self.poderes = []
        self.cervezas = []
        self.textos_flotantes = []

        plat_data, esc_data, cerv_pos, mates_pos, hincha_pos, hincha_viejo_pos = generar_layout_nivel(self.nivel)

        for (x, y, w) in plat_data:
            self.plataformas.append(Plataforma(x, y, w, self.gestor))
        for (x, y, h) in esc_data:
            self.escaleras.append(Escalera(x, y, h, self.gestor))
        for (x, y) in cerv_pos:
            self.cervezas.append(BarrilCerveza(x, y, self.gestor, es_item=True))
        for (x, y) in mates_pos:
            self.poderes.append(PoderMate(x, y, self.gestor))

        Y_KONG = 80
        self.kong = KongCervecero(ANCHO//2 - 60, Y_KONG, self.gestor, self.nivel)
        self.gestor.kong = self.kong
        self.princesa = Princesa(ANCHO//2 + 50, Y_KONG, self.gestor)
        self.argentino = Argentino(100, ALTO - 70, self.gestor)
        self.argentino.personaje = self.personaje_actual
        self.gestor.argentino = self.argentino
        self.borracho = BorrachoIA(300, ALTO - 70, self.gestor)
        self._crear_hinchada(hincha_pos, hincha_viejo_pos)

        self.gestor._fondo_cache.pop(self.nivel, None)

    def _crear_hinchada(self, hincha_pos, hincha_viejo_pos):
        def limitar_pos(pos):
            x = max(20, min(ANCHO - 60, int(pos[0])))
            y = max(80, min(ALTO - 80, int(pos[1])))
            return x, y

        def generar_posiciones(base, cantidad):
            base_x, base_y = base
            candidatas = [
                (base_x, base_y),
                (ANCHO // 2 - 16, ALTO - 120),
                (hincha_viejo_pos if hincha_viejo_pos else (ANCHO // 2 + 50, ALTO - 140)),
                (base_x + 120, base_y + 20),
                (base_x - 120, base_y + 10),
                (ANCHO // 2 + 180, ALTO - 200),
                (ANCHO // 2 - 200, ALTO - 210),
                (ANCHO // 2 + 240, ALTO - 280),
                (ANCHO // 2 - 250, ALTO - 300),
                (ANCHO // 2, ALTO - 260),
            ]

            if cantidad > len(candidatas):
                extra = cantidad - len(candidatas)
                for i in range(extra):
                    ang = (math.pi * 2 * i) / max(extra, 1)
                    rx = int((ANCHO // 2) + math.cos(ang) * 230)
                    ry = int((ALTO - 220) + math.sin(ang) * 110)
                    candidatas.append((rx, ry))

            return [limitar_pos(pos) for pos in candidatas[:cantidad]]

        base_x, base_y = hincha_pos
        tipos = [
            HinchaBorrachito,
            HinchaArgentina,
            HinchaViejoTambor,
            HinchaRandom,
            HinchaConBengala,
            HinchaGemelos,
            HinchaAbuela,
            HinchaBorrachin,
        ]

        posiciones = generar_posiciones((base_x, base_y), len(tipos))

        # Ajuste manual de posiciones especiales.
        if len(posiciones) >= 5:
            posiciones[2] = (ANCHO // 2 + 210, ALTO - 340)  # HinchaViejoTambor (3er piso)
            posiciones[4] = (ANCHO // 2 - 210, ALTO - 280)  # HinchaConBengala

        self.hinchada = []
        for tipo, pos in zip(tipos, posiciones):
            self.hinchada.append(tipo(pos[0], pos[1], self.gestor))

        self.hincha = self.hinchada[0] if self.hinchada else None

    # ──────────────────────── HELPERS ────────────────────────────── #

