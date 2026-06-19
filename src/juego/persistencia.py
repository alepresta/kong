# src/juego/persistencia.py
"""KONG ARGENTINO - Persistencia (high score, perfil)"""
import pygame
import sys
import os
import random
import math
import pickle
from constantes import *

class PersistenciaMixin:
    def _cargar_high_score(self):
        try:
            if os.path.exists(ARCHIVO_HIGHSCORE):
                with open(ARCHIVO_HIGHSCORE, 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return 0

    def _guardar_high_score(self):
        try:
            with open(ARCHIVO_HIGHSCORE, 'wb') as f:
                pickle.dump(self.high_score, f)
        except Exception:
            pass

    def _cargar_perfil(self):
        try:
            if os.path.exists(ARCHIVO_PERFIL):
                with open(ARCHIVO_PERFIL, 'rb') as f:
                    data = pickle.load(f)
                    idx = int(data.get('indice_perfil', 0))
                    self.indice_perfil = idx % len(self.perfiles_jugador)
        except Exception:
            self.indice_perfil = 0
        self._aplicar_perfil_actual()

    def _guardar_perfil(self):
        try:
            with open(ARCHIVO_PERFIL, 'wb') as f:
                pickle.dump({'indice_perfil': self.indice_perfil}, f)
        except Exception:
            pass

    def _aplicar_perfil_actual(self):
        perfil = self.perfiles_jugador[self.indice_perfil]
        self.nombre_jugador = perfil['nombre']
        self.personaje_actual = perfil['personaje']

    def _cambiar_perfil(self, delta):
        self.indice_perfil = (self.indice_perfil + delta) % len(self.perfiles_jugador)
        self._aplicar_perfil_actual()
        self._guardar_perfil()

    # ──────────────────────── NIVEL ──────────────────────────────── #

