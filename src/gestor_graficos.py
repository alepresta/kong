# src/gestor_graficos.py
"""
KONG ARGENTINO - GESTOR DE GRÁFICOS v4.0
Mejoras v4.0:
- Fuentes cacheadas (no recrear en cada frame → gran mejora de performance)
- Fondo animado: nubes que se mueven en tiempo real
- Camera shake integrado
- Nuevo método: dibujar_barras_laterales (decoración HUD)
- Función de flash de pantalla para golpes
- Estrellas twinkle mejoradas
"""
import pygame
import math
import random
from constantes import *
from sonidos import GeneradorSonidos

class GestorGraficos:
    def __init__(self):
        self.generador_sonidos = GeneradorSonidos()
        self._fondo_cache = {}       # dict nivel → Surface estática
        self._fuente_cache = {}      # dict (familia, tamaño, bold) → Font
        self._estrellas = []
        self._nubes = []
        self._generar_estrellas()
        self._generar_nubes()
        
        # Referencias a entidades
        self.argentino = None
        self.kong = None
        self.particulas = []  # Lista de partículas (referencia)
        self.sistema_particulas = None  # Objeto SistemaParticulas
        
        # Camera shake
        self._shake_dur = 0
        self._shake_int = 0
        self._shake_off = (0, 0)

        # Flash de pantalla (al recibir golpe)
        self._flash_dur = 0
        self._flash_color = (255, 0, 0)

        # Tiempo global para animaciones
        self._t = 0

    # ──────────────────────── UTILIDADES ────────────────────────── #

    def tick(self):
        """Llamar una vez por frame en main"""
        self._t += 1
        if self._shake_dur > 0:
            self._shake_dur -= 1
            i = self._shake_int
            self._shake_off = (random.randint(-i, i), random.randint(-i, i))
        else:
            self._shake_off = (0, 0)
        if self._flash_dur > 0:
            self._flash_dur -= 1

    def iniciar_shake(self, duracion=None, intensidad=None):
        self._shake_dur = duracion or SHAKE_DURACION
        self._shake_int = intensidad or SHAKE_INTENSIDAD

    def iniciar_flash(self, color=(255, 60, 60), duracion=8):
        self._flash_dur = duracion
        self._flash_color = color

    def get_shake(self):
        return self._shake_off

    # ──────────────────────── FUENTES ────────────────────────────── #

    def _get_fuente(self, tamaño, bold=True, familia="comicsansms"):
        key = (familia, tamaño, bold)
        if key not in self._fuente_cache:
            self._fuente_cache[key] = pygame.font.SysFont(familia, tamaño, bold=bold)
        return self._fuente_cache[key]

    def dibujar_texto(self, pantalla, texto, tamaño, color, x, y,
                      centro=False, sombra=False, bold=True, familia="comicsansms"):
        fuente = self._get_fuente(tamaño, bold, familia)
        if sombra:
            sombra_surf = fuente.render(texto, True, COLORES['negro'])
            ox = x - sombra_surf.get_width()//2 if centro else x
            pantalla.blit(sombra_surf, (ox+2, y+2))
        superficie = fuente.render(texto, True, color)
        if centro:
            x = x - superficie.get_width() // 2
        pantalla.blit(superficie, (x, y))
        return superficie.get_width()

    # ──────────────────────── FONDO ──────────────────────────────── #

    def _generar_estrellas(self):
        rng = random.Random(42)
        self._estrellas = []
        for _ in range(160):
            self._estrellas.append({
                'x': rng.randint(0, ANCHO),
                'y': rng.randint(0, ALTO // 2),
                'tam': rng.randint(1, 3),
                'brillo': rng.randint(80, 255),
                'vel': rng.uniform(0.4, 2.2),
                'fase': rng.uniform(0, math.pi * 2),
            })
    
    def _generar_nubes(self):
        self._nubes = []
        for _ in range(10):
            self._nubes.append({
                'x': random.randint(-200, ANCHO + 100),
                'y': random.randint(20, ALTO // 3),
                'w': random.randint(80, 220),
                'h': random.randint(28, 65),
                'vel': random.uniform(0.15, 0.55),
                'alpha': random.randint(160, 240),
            })

    def _actualizar_nubes(self):
        for nube in self._nubes:
            nube['x'] += nube['vel']
            if nube['x'] > ANCHO + 250:
                nube['x'] = -250
                nube['y'] = random.randint(20, ALTO // 3)
                nube['w'] = random.randint(80, 220)

    def _generar_fondo_base(self, nivel):
        """Genera la superficie estática de fondo (sin nubes ni estrellas animadas)."""
        surf = pygame.Surface((ANCHO, ALTO))
        fondos = [
            (135, 206, 235),
            (200, 150, 80),
            (25, 25, 80),
            (80, 20, 20),
            (20, 10, 40),
        ]
        base = fondos[min(nivel-1, len(fondos)-1)]
        for i in range(ALTO):
            factor = i / ALTO
            r = int(base[0] * (1 - factor * 0.6))
            g = int(base[1] * (1 - factor * 0.5))
            b = int(base[2] * (1 - factor * 0.4))
            pygame.draw.line(surf, (r, g, b), (0, i), (ANCHO, i))

        # Sol / luna fijos
        if nivel == 1:
            for ang in range(0, 360, 30):
                rad = math.radians(ang)
                x1 = 750 + math.cos(rad) * 50
                y1 = 60 + math.sin(rad) * 50
                x2 = 750 + math.cos(rad) * 70
                y2 = 60 + math.sin(rad) * 70
                pygame.draw.line(surf, (255, 220, 100), (int(x1), int(y1)), (int(x2), int(y2)), 4)
            pygame.draw.circle(surf, (255, 230, 150), (750, 60), 40)
            pygame.draw.circle(surf, (255, 200, 50), (750, 60), 30)
        elif nivel >= 3:
            pygame.draw.circle(surf, (240, 240, 220), (800, 70), 50)
            pygame.draw.circle(surf, (220, 220, 200), (800, 70), 45)
            for cx, cy, cr in [(790, 60, 10), (810, 85, 8), (820, 60, 6), (785, 80, 5)]:
                pygame.draw.circle(surf, (200, 200, 180), (cx, cy), cr)

        # Suelo
        pygame.draw.line(surf, (50, 40, 30), (0, ALTO-40), (ANCHO, ALTO-40), 3)
        return surf

    def dibujar_fondo(self, pantalla, nivel=1):
        # Generamos fondo estático solo si no existe
        if nivel not in self._fondo_cache:
            self._fondo_cache[nivel] = self._generar_fondo_base(nivel)

        pantalla.blit(self._fondo_cache[nivel], (0, 0))

        t = self._t
        # Nubes animadas (niveles diurnos)
        if nivel <= 2:
            self._actualizar_nubes()
            for nube in self._nubes:
                x, y, w, h = int(nube['x']), int(nube['y']), nube['w'], nube['h']
                # Dibujamos nubes directamente (sin SRCALPHA para performance)
                pygame.draw.ellipse(pantalla, (230, 230, 230), (x, y, w, h))
                pygame.draw.ellipse(pantalla, (245, 245, 245), (x + w//4, y - h//3, w//2, h))
                pygame.draw.ellipse(pantalla, (255, 255, 255), (x + w//3, y + h//4, w//3, h//2))

        # Estrellas twinkle (niveles nocturnos)
        if nivel >= 3:
            for est in self._estrellas:
                brillo = int(est['brillo'] * (0.6 + 0.4 * math.sin(t * 0.04 * est['vel'] + est['fase'])))
                brillo = max(60, min(255, brillo))
                pygame.draw.circle(pantalla, (brillo, brillo, brillo),
                                   (est['x'], est['y']), est['tam'])

    def aplicar_flash(self, pantalla):
        """Superpone un flash semitransparente de color sobre la pantalla"""
        if self._flash_dur > 0:
            alpha = int(120 * (self._flash_dur / 10))
            flash_surf = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            flash_surf.fill((*self._flash_color, alpha))
            pantalla.blit(flash_surf, (0, 0))

    # ──────────────────────── HUD ────────────────────────────────── #

    def dibujar_boton(self, pantalla, x, y, texto, ancho, alto, activo=False):
        color_base = COLORES['verde'] if activo else COLORES['azul']
        color_borde = COLORES['oro'] if activo else COLORES['celeste']
        pygame.draw.rect(pantalla, COLORES['negro'], (x+3, y+3, ancho, alto))
        pygame.draw.rect(pantalla, color_base, (x, y, ancho, alto))
        for i in range(10):
            pygame.draw.rect(pantalla, (min(255, color_base[0]+i*5), 
                                      min(255, color_base[1]+i*5), 
                                      min(255, color_base[2]+i*5)), 
                           (x+2, y+2+i*3, ancho-4, 3))
        pygame.draw.rect(pantalla, color_borde, (x, y, ancho, alto), 3)
        # Efecto glow en hover
        if activo:
            glow_surf = pygame.Surface((ancho + 8, alto + 8), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*color_borde, 60), (0, 0, ancho+8, alto+8), border_radius=4)
            pantalla.blit(glow_surf, (x-4, y-4))
        self.dibujar_texto(pantalla, texto, 26, COLORES['blanco'], 
                          x + ancho//2, y + alto//2 - 10, centro=True)

    def dibujar_sombra(self, pantalla, x, y, ancho, alto, alpha=80):
        sombra = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, alpha), (0, 0, ancho, alto))
        pantalla.blit(sombra, (x - ancho//2, y - alto//2))

    def dibujar_corazon(self, pantalla, x, y):
        pygame.draw.polygon(pantalla, (100, 0, 0),
            [(x+1, y+1), (x-7, y-4), (x-7, y-11), (x+1, y-15),
             (x+9, y-11), (x+9, y-4), (x+1, y+1)])
        pygame.draw.polygon(pantalla, COLORES['rojo'],
            [(x, y), (x-8, y-5), (x-8, y-12), (x, y-16),
             (x+8, y-12), (x+8, y-5), (x, y)])
        pygame.draw.circle(pantalla, (255, 150, 150), (x-3, y-10), 3)

    # ──────────────────────── PLATAFORMAS ────────────────────────── #

    def dibujar_plataforma(self, pantalla, x, y, ancho):
        """Plataforma estilo tronco de jungla con madera, musgo y hojas"""
        pygame.draw.rect(pantalla, (40, 30, 20), (x+4, y+6, ancho, 10))
        pygame.draw.rect(pantalla, (70, 45, 25), (x, y, ancho, 28))
        pygame.draw.rect(pantalla, (95, 65, 40), (x, y, ancho, 14))
        
        for i in range(0, ancho, 20):
            vx = x + i + (i % 15)
            pygame.draw.line(pantalla, (50, 30, 15), (vx, y+6), (vx+15, y+18), 2)
        
        for i in range(15, ancho-10, 40):
            pygame.draw.ellipse(pantalla, (50, 35, 20), (x+i-5, y-2, 12, 32), 2)
        
        for i in range(0, ancho, 12):
            if i % 25 < 12:
                pygame.draw.ellipse(pantalla, (50, 120, 30), (x+i-4, y-3, 12, 8))
                pygame.draw.ellipse(pantalla, (70, 140, 40), (x+i+2, y-1, 10, 6))
        
        for i in range(6, ancho-6, 30):
            if i % 40 < 20:
                pygame.draw.line(pantalla, (40, 80, 20), (x+i, y+28), (x+i+4, y+38), 2)
                pygame.draw.ellipse(pantalla, (60, 140, 40), (x+i-4, y+32, 12, 8))

    # ──────────────────────── MENÚ ───────────────────────────────── #

    def dibujar_menu(self, pantalla):
        self.dibujar_fondo(pantalla, 1)
        t = self._t
        off = int(math.sin(t * 0.04) * 6)

        # Título con doble sombra
        self.dibujar_texto(pantalla, NOMBRE_JUEGO, 70, (80, 0, 0),
                           ANCHO//2+5, 60+off, centro=True)
        self.dibujar_texto(pantalla, NOMBRE_JUEGO, 70, COLORES['negro'],
                           ANCHO//2+2, 57+off, centro=True)
        self.dibujar_texto(pantalla, NOMBRE_JUEGO, 70, COLORES['rojo'],
                           ANCHO//2, 55+off, centro=True)

        col = COLORES['oro'] if (t // 30) % 2 == 0 else COLORES['amarillo']
        self.dibujar_texto(pantalla, "KONG CERVEZERO", 32, col,
                           ANCHO//2, 128, centro=True, sombra=True)
        self.dibujar_texto(pantalla, f"v{VERSION}", 16, COLORES['gris'],
                           ANCHO//2, 162, centro=True)

        # Panel de instrucciones con borde degradado
        marco_surf = pygame.Surface((560, 360), pygame.SRCALPHA)
        marco_surf.fill((0, 0, 0, 150))
        pantalla.blit(marco_surf, (ANCHO//2 - 280, 178))
        pygame.draw.rect(pantalla, COLORES['oro'], (ANCHO//2-280, 178, 560, 360), 3)
        for cx, cy in [(ANCHO//2-280, 178), (ANCHO//2+280, 178), 
                       (ANCHO//2-280, 538), (ANCHO//2+280, 538)]:
            pygame.draw.rect(pantalla, COLORES['oro'], (cx-10, cy-10, 20, 20), 3)

        self.dibujar_texto(pantalla, "🎮 CONTROLES", 26, COLORES['amarillo'], 
                          ANCHO//2, 192, centro=True)
        instrucciones = [
            ("A / D  o  ← / →", "Moverse"),
            ("W / ↑",            "Subir escalera / Saltar"),
            ("S / ↓",            "Bajar escalera"),
            ("ESPACIO",          "Atacar (↑↓←→ + ESPACIO)"),
            ("P",                "Pausar"),
            ("ESC",              "Volver al menú"),
        ]
        for i, (tecla, desc) in enumerate(instrucciones):
            y_pos = 218 + i*38
            self.dibujar_texto(pantalla, tecla, 20, COLORES['amarillo'], 
                              ANCHO//2 - 225, y_pos)
            self.dibujar_texto(pantalla, "→", 20, COLORES['celeste'], 
                              ANCHO//2 - 65, y_pos)
            self.dibujar_texto(pantalla, desc, 20, COLORES['blanco'], 
                              ANCHO//2 - 40, y_pos)

        self.dibujar_texto(pantalla, "🎯 OBJETIVO", 24, COLORES['oro'], 
                          ANCHO//2, 438, centro=True)
        self.dibujar_texto(pantalla, "Recogé cervezas • Tomá mates para ser invencible", 18,
                           COLORES['blanco'], ANCHO//2, 466, centro=True)
        self.dibujar_texto(pantalla, "¡Rescatá a la princesa del KONG CERVEZERO!", 18,
                           COLORES['celeste'], ANCHO//2, 490, centro=True)

    def reproducir_sonido(self, nombre):
        self.generador_sonidos.reproducir(nombre)