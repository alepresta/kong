"""
KONG ARGENTINO - GESTOR DE GRÁFICOS v3 (Mejorado)
Creado por Apresta para Prestalabs
"""
import pygame
import math
import random
from constantes import *
from sonidos import GeneradorSonidos

class GestorGraficos:
    def __init__(self):
        self.generador_sonidos = GeneradorSonidos()
        self._fondo_cache = None
        self._fondo_nivel = -1
        self._estrellas = []
        self._nubes = []
        self._generar_estrellas()
        self._generar_nubes()
        
    def _generar_estrellas(self):
        rng = random.Random(42)
        self._estrellas = []
        for _ in range(150):
            self._estrellas.append({
                'x': rng.randint(0, ANCHO),
                'y': rng.randint(0, ALTO // 2),
                'tam': rng.randint(1, 3),
                'brillo': rng.randint(100, 255),
                'vel': rng.uniform(0.5, 2.0)
            })
    
    def _generar_nubes(self):
        self._nubes = []
        for i in range(8):
            self._nubes.append({
                'x': random.randint(-200, ANCHO),
                'y': random.randint(20, ALTO // 3),
                'w': random.randint(80, 200),
                'h': random.randint(30, 60),
                'vel': random.uniform(0.2, 0.8)
            })

    def dibujar_texto(self, pantalla, texto, tamaño, color, x, y, centro=False, sombra=False):
        fuente = pygame.font.SysFont("comicsansms", tamaño, bold=True)
        if sombra:
            sombra_surf = fuente.render(texto, True, COLORES['negro'])
            ox = x - sombra_surf.get_width()//2 if centro else x
            pantalla.blit(sombra_surf, (ox+3, y+3))
        superficie = fuente.render(texto, True, color)
        if centro:
            x = x - superficie.get_width() // 2
        pantalla.blit(superficie, (x, y))
        return superficie.get_width()

    def dibujar_boton(self, pantalla, x, y, texto, ancho, alto, activo=False):
        color_base = COLORES['verde'] if activo else COLORES['azul']
        color_borde = COLORES['oro'] if activo else COLORES['celeste']
        # Sombra del botón
        pygame.draw.rect(pantalla, COLORES['negro'], (x+3, y+3, ancho, alto))
        pygame.draw.rect(pantalla, color_base, (x, y, ancho, alto))
        # Degradado
        for i in range(10):
            pygame.draw.rect(pantalla, (min(255, color_base[0]+i*5), 
                                      min(255, color_base[1]+i*5), 
                                      min(255, color_base[2]+i*5)), 
                           (x+2, y+2+i*3, ancho-4, 3))
        pygame.draw.rect(pantalla, color_borde, (x, y, ancho, alto), 3)
        self.dibujar_texto(pantalla, texto, 26, COLORES['blanco'], 
                          x + ancho//2, y + alto//2 - 10, centro=True)

    def dibujar_sombra(self, pantalla, x, y, ancho, alto, alpha=80):
        """Dibuja una sombra elíptica debajo de un objeto"""
        sombra = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, alpha), (0, 0, ancho, alto))
        pantalla.blit(sombra, (x - ancho//2, y - alto//2))

    def dibujar_plataforma(self, pantalla, x, y, ancho):
        """Plataforma con textura de madera mejorada"""
        # Sombra
        pygame.draw.rect(pantalla, (40, 30, 20, 80), (x+3, y+5, ancho, 8))
        
        # Base de madera
        pygame.draw.rect(pantalla, (101, 67, 33), (x, y, ancho, 25))
        pygame.draw.rect(pantalla, (130, 90, 50), (x, y, ancho, 10))
        
        # Borde superior
        pygame.draw.rect(pantalla, (180, 130, 70), (x, y, ancho, 3))
        
        # Vetas de madera
        for i in range(0, ancho, 25):
            # Veta principal
            veta_y = y + 5 + (i % 15)
            pygame.draw.line(pantalla, (80, 50, 25), 
                           (x + i, veta_y), (x + i + 20, veta_y + 4), 2)
            # Veta secundaria
            if i % 50 < 25:
                pygame.draw.line(pantalla, (70, 40, 20), 
                               (x + i + 10, veta_y - 5), (x + i + 25, veta_y - 2), 1)
        
        # Clavos
        for i in range(3, ancho - 3, ancho // 6):
            pygame.draw.circle(pantalla, (60, 40, 20), (x + i, y + 20), 3)
            pygame.draw.circle(pantalla, (160, 120, 70), (x + i, y + 19), 2)
        
        # Reflejo
        pygame.draw.rect(pantalla, (255, 255, 255, 20), (x + 5, y + 2, ancho - 10, 3))

    def _generar_fondo(self, nivel):
        """Genera el fondo cacheado con detalles mejorados"""
        surf = pygame.Surface((ANCHO, ALTO))
        
        # Colores de fondo por nivel
        fondos = [
            (135, 206, 235),  # Cielo claro (nivel 1)
            (200, 150, 80),   # Atardecer (nivel 2)
            (25, 25, 80),     # Noche (nivel 3)
            (80, 20, 20),     # Tormenta (nivel 4)
            (20, 10, 40),     # Noche estrellada (nivel 5)
        ]
        
        base = fondos[min(nivel-1, len(fondos)-1)]
        
        # Degradado vertical mejorado
        for i in range(ALTO):
            factor = i / ALTO
            r = int(base[0] * (1 - factor * 0.6))
            g = int(base[1] * (1 - factor * 0.5))
            b = int(base[2] * (1 - factor * 0.4))
            pygame.draw.line(surf, (r, g, b), (0, i), (ANCHO, i))
        
        # Elementos según nivel
        if nivel <= 2:
            # Nubes detalladas
            for nube in self._nubes:
                x, y, w, h = nube['x'], nube['y'], nube['w'], nube['h']
                # Nube con múltiples círculos
                color_nube = (255, 255, 255, 200)
                pygame.draw.ellipse(surf, (240, 240, 240), (x, y, w, h))
                pygame.draw.ellipse(surf, (245, 245, 245), (x + w//4, y - h//3, w//2, h))
                pygame.draw.ellipse(surf, (250, 250, 250), (x + w//3, y + h//4, w//3, h//2))
            
            # Sol con brillo
            if nivel == 1:
                # Rayos de sol
                for ang in range(0, 360, 30):
                    rad = math.radians(ang)
                    x1 = 750 + math.cos(rad) * 50
                    y1 = 60 + math.sin(rad) * 50
                    x2 = 750 + math.cos(rad) * 70
                    y2 = 60 + math.sin(rad) * 70
                    pygame.draw.line(surf, (255, 220, 100, 50), (x1, y1), (x2, y2), 4)
                pygame.draw.circle(surf, (255, 230, 150), (750, 60), 40)
                pygame.draw.circle(surf, (255, 200, 50), (750, 60), 30)
        
        else:
            # Estrellas parpadeantes
            for estrella in self._estrellas:
                brillo = int(estrella['brillo'] * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.001 * estrella['vel'])))
                pygame.draw.circle(surf, (brillo, brillo, brillo), 
                                 (int(estrella['x']), int(estrella['y'])), estrella['tam'])
            
            # Luna detallada
            if nivel >= 3:
                # Resplandor
                for r in range(60, 0, -10):
                    alpha = int(30 * (r / 60))
                    pygame.draw.circle(surf, (255, 255, 200, alpha), (800, 70), r)
                
                pygame.draw.circle(surf, (240, 240, 220), (800, 70), 50)
                pygame.draw.circle(surf, (220, 220, 200), (800, 70), 45)
                # Cráteres
                for cx, cy, cr in [(790, 60, 10), (810, 85, 8), (820, 60, 6), (785, 80, 5)]:
                    pygame.draw.circle(surf, (200, 200, 180), (cx, cy), cr)
                    pygame.draw.circle(surf, (230, 230, 210), (cx-2, cy-2), cr-2)
        
        # Línea del horizonte
        pygame.draw.line(surf, (50, 40, 30), (0, ALTO-40), (ANCHO, ALTO-40), 3)
        
        return surf

    def dibujar_fondo(self, pantalla, nivel=1):
        if self._fondo_nivel != nivel:
            self._fondo_cache = self._generar_fondo(nivel)
            self._fondo_nivel = nivel
        pantalla.blit(self._fondo_cache, (0, 0))

    def dibujar_corazon(self, pantalla, x, y):
        """Corazón estilizado"""
        # Sombra
        pygame.draw.polygon(pantalla, (100, 0, 0, 100),
            [(x+1, y+1), (x-7, y-4), (x-7, y-11), (x+1, y-15),
             (x+9, y-11), (x+9, y-4), (x+1, y+1)])
        # Corazón
        pygame.draw.polygon(pantalla, COLORES['rojo'],
            [(x, y), (x-8, y-5), (x-8, y-12), (x, y-16),
             (x+8, y-12), (x+8, y-5), (x, y)])
        # Brillo
        pygame.draw.circle(pantalla, (255, 150, 150), (x-3, y-10), 3)

    def dibujar_menu(self, pantalla):
        self.dibujar_fondo(pantalla, 1)
        t = pygame.time.get_ticks()
        
        # Título con efecto de sombra y brillo
        off = int(math.sin(t * 0.003) * 5)
        
        # Sombra del título
        self.dibujar_texto(pantalla, NOMBRE_JUEGO, 70, COLORES['negro'],
                           ANCHO//2+3, 58+off, centro=True)
        self.dibujar_texto(pantalla, NOMBRE_JUEGO, 70, COLORES['rojo'],
                           ANCHO//2, 55+off, centro=True)
        
        # Subtítulo con destello
        col = COLORES['oro'] if (t // 500) % 2 == 0 else COLORES['amarillo']
        self.dibujar_texto(pantalla, "KONG CERVEZERO", 32, col,
                           ANCHO//2, 120, centro=True, sombra=True)
        self.dibujar_texto(pantalla, f"v{VERSION}", 16, COLORES['gris'],
                           ANCHO//2, 155, centro=True)

        # Marco translúcido con borde decorativo
        marco_surf = pygame.Surface((540, 350), pygame.SRCALPHA)
        marco_surf.fill((0, 0, 0, 160))
        pantalla.blit(marco_surf, (ANCHO//2 - 270, 175))
        pygame.draw.rect(pantalla, COLORES['oro'], (ANCHO//2-270, 175, 540, 350), 3)
        # Esquinas decorativas
        for cx, cy in [(ANCHO//2-270, 175), (ANCHO//2+270, 175), 
                       (ANCHO//2-270, 525), (ANCHO//2+270, 525)]:
            pygame.draw.rect(pantalla, COLORES['oro'], (cx-10, cy-10, 20, 20), 3)

        self.dibujar_texto(pantalla, "🎮 CONTROLES", 26, COLORES['amarillo'], 
                          ANCHO//2, 190, centro=True)
        
        instrucciones = [
            ("A / D  o  ← / →", "Moverse"),
            ("W / ↑",            "Subir escalera"),
            ("S / ↓",            "Bajar escalera"),
            ("ESPACIO",          "Saltar"),
            ("P",                "Pausa"),
            ("ESC",              "Volver al menú"),
        ]
        for i, (tecla, desc) in enumerate(instrucciones):
            y_pos = 225 + i*32
            self.dibujar_texto(pantalla, tecla, 20, COLORES['amarillo'], 
                              ANCHO//2 - 210, y_pos)
            self.dibujar_texto(pantalla, "→", 20, COLORES['celeste'], 
                              ANCHO//2 - 50, y_pos)
            self.dibujar_texto(pantalla, desc, 20, COLORES['blanco'], 
                              ANCHO//2 - 20, y_pos)

        self.dibujar_texto(pantalla, "🎯 OBJETIVO", 24, COLORES['oro'], 
                          ANCHO//2, 425, centro=True)
        self.dibujar_texto(pantalla, "Recogé cervezas • Tomá mates para ser invencible", 18,
                           COLORES['blanco'], ANCHO//2, 455, centro=True)
        self.dibujar_texto(pantalla, "¡Rescatá a la princesa del KONG CERVEZERO!", 18,
                           COLORES['celeste'], ANCHO//2, 480, centro=True)

    def reproducir_sonido(self, nombre):
        self.generador_sonidos.reproducir(nombre)