"""
KONG ARGENTINO v3.2 - ¡Rescata a la princesa del Kong cervecero!
Creado por Apresta para Prestalabs
"""
import pygame
import sys
import random
import math
from constantes import *
from gestor_graficos import GestorGraficos
from jugador import Argentino, BorrachoIA
from objetos import Plataforma, Escalera, BarrilCerveza, PoderMate, Princesa, KongCervecero, HinchaBorrachito


# ─────────────────────────────────────────────────────────────────────────────
#  SISTEMA DE PARTÍCULAS
# ─────────────────────────────────────────────────────────────────────────────
class SistemaParticulas:
    def __init__(self, gestor):
        self.particulas = []
        self.gestor = gestor

    def emitir(self, x, y, color, n=8, fuente='explosion'):
        for _ in range(n):
            if fuente == 'explosion':
                vx = random.uniform(-4, 4)
                vy = random.uniform(-6, -1)
                vida = random.randint(20, 40)
                tam = random.randint(2, 6)
            elif fuente == 'combo':
                ang = random.uniform(0, math.pi * 2)
                spd = random.uniform(2, 6)
                vx = math.cos(ang) * spd
                vy = math.sin(ang) * spd - 3
                vida = random.randint(25, 50)
                tam = random.randint(3, 7)
            elif fuente == 'humo':
                vx = random.uniform(-1.5, 1.5)
                vy = random.uniform(-2.5, -0.5)
                vida = random.randint(15, 30)
                tam = random.randint(4, 10)
            elif fuente == 'estrella':
                ang = random.uniform(0, math.pi * 2)
                spd = random.uniform(1, 5)
                vx = math.cos(ang) * spd
                vy = math.sin(ang) * spd - 2
                vida = random.randint(30, 60)
                tam = random.randint(2, 5)
            elif fuente == 'polvo':
                vx = random.uniform(-2, 2)
                vy = random.uniform(-3, -0.5)
                vida = random.randint(10, 20)
                tam = random.randint(2, 5)
            elif fuente == 'golpe':
                ang = random.uniform(0, math.pi * 2)
                spd = random.uniform(1, 3)
                vx = math.cos(ang) * spd
                vy = math.sin(ang) * spd - 1
                vida = random.randint(10, 20)
                tam = random.randint(2, 4)
            elif fuente == 'ataque':
                ang = random.uniform(-math.pi/3, math.pi/3)
                spd = random.uniform(2, 6)
                vx = math.cos(ang) * spd
                vy = math.sin(ang) * spd - 2
                vida = random.randint(15, 25)
                tam = random.randint(3, 6)
            else:
                vx, vy, vida, tam = random.uniform(-2, 2), random.uniform(-3, -1), 20, 3
            self.particulas.append({
                'x': float(x), 'y': float(y),
                'vx': vx, 'vy': vy,
                'vida': vida, 'vida_max': vida,
                'color': color, 'tam': tam,
            })

    def actualizar(self):
        for p in self.particulas[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.15
            p['vx'] *= 0.98
            p['vida'] -= 1
            if p['vida'] <= 0:
                self.particulas.remove(p)

    def dibujar(self, pantalla):
        for p in self.particulas:
            alpha = p['vida'] / p['vida_max']
            tam = max(1, int(p['tam'] * alpha))
            c = p['color']
            col = (int(c[0]*alpha), int(c[1]*alpha), int(c[2]*alpha))
            pygame.draw.circle(pantalla, col, (int(p['x']), int(p['y'])), tam)


# ─────────────────────────────────────────────────────────────────────────────
#  TEXTOS FLOTANTES
# ─────────────────────────────────────────────────────────────────────────────
class TextoFlotante:
    def __init__(self, texto, x, y, color, tamaño=22):
        self.texto = texto
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.tamaño = tamaño
        self.vida = 60
        self.vida_max = 60

    def update(self):
        self.y -= 1.0
        self.vida -= 1

    def dibujar(self, pantalla, gestor):
        if self.vida <= 0:
            return
        alpha = self.vida / self.vida_max
        col = (int(self.color[0]*alpha), int(self.color[1]*alpha), int(self.color[2]*alpha))
        gestor.dibujar_texto(pantalla, self.texto, self.tamaño, col,
                             int(self.x), int(self.y), centro=True, sombra=True)


# ─────────────────────────────────────────────────────────────────────────────
#  GENERADOR DE NIVELES (con hincha)
# ─────────────────────────────────────────────────────────────────────────────
def generar_layout_nivel(nivel):
    """Devuelve (plataformas_data, escaleras_data, cervezas_pos, mates_pos, hincha_pos)"""
    plataformas = []
    escaleras = []

    # Suelo
    plataformas.append((0, ALTO - 40, ANCHO))

    layouts = [
        # Nivel 1
        {
            'p': [
                (80, ALTO-120, 180), (320, ALTO-120, 180), (560, ALTO-120, 180), (800, ALTO-120, 150),
                (150, ALTO-220, 150), (400, ALTO-220, 150), (650, ALTO-220, 150),
                (100, ALTO-320, 140), (350, ALTO-320, 140), (600, ALTO-320, 140), (850, ALTO-320, 120),
                (200, ALTO-420, 130), (500, ALTO-420, 130),
                (300, ALTO-520, 120), (580, ALTO-520, 120),
            ],
            'e': [
                (130, ALTO-120, 80), (400, ALTO-120, 80), (680, ALTO-120, 80),
                (220, ALTO-220, 100), (470, ALTO-220, 100), (720, ALTO-220, 100),
                (170, ALTO-320, 100), (420, ALTO-320, 100), (670, ALTO-320, 100), (920, ALTO-320, 100),
                (270, ALTO-420, 100), (570, ALTO-420, 100),
                (360, ALTO-520, 100), (640, ALTO-520, 100),
                (ANCHO//2-20, 260, 100),
            ],
            'hincha': (350, ALTO-520-30),
        },
        # Nivel 2
        {
            'p': [
                (60, ALTO-130, 160), (300, ALTO-130, 160), (580, ALTO-130, 160), (820, ALTO-130, 140),
                (130, ALTO-240, 140), (420, ALTO-240, 140), (700, ALTO-240, 140),
                (80, ALTO-350, 130), (380, ALTO-350, 130), (650, ALTO-350, 130), (880, ALTO-350, 110),
                (220, ALTO-460, 120), (540, ALTO-460, 120),
                (320, ALTO-560, 115), (600, ALTO-560, 115),
            ],
            'e': [
                (110, ALTO-130, 90), (370, ALTO-130, 90), (660, ALTO-130, 90),
                (200, ALTO-240, 110), (490, ALTO-240, 110), (760, ALTO-240, 110),
                (150, ALTO-350, 110), (450, ALTO-350, 110), (720, ALTO-350, 110), (940, ALTO-350, 110),
                (290, ALTO-460, 110), (600, ALTO-460, 110),
                (390, ALTO-560, 105), (660, ALTO-560, 105),
                (ANCHO//2-25, 255, 105),
            ],
            'hincha': (390, ALTO-560-30),
        },
        # Nivel 3
        {
            'p': [
                (50, ALTO-120, 150), (310, ALTO-150, 150), (560, ALTO-120, 150), (800, ALTO-150, 140),
                (130, ALTO-240, 140), (410, ALTO-260, 140), (660, ALTO-240, 140),
                (70, ALTO-360, 130), (360, ALTO-380, 130), (620, ALTO-360, 130), (860, ALTO-380, 120),
                (180, ALTO-480, 120), (500, ALTO-480, 120),
                (290, ALTO-580, 110), (580, ALTO-580, 110),
            ],
            'e': [
                (100, ALTO-120, 80), (380, ALTO-150, 80), (640, ALTO-120, 80),
                (200, ALTO-240, 120), (480, ALTO-260, 120), (730, ALTO-240, 120),
                (140, ALTO-360, 120), (430, ALTO-380, 120), (690, ALTO-360, 120), (920, ALTO-380, 120),
                (250, ALTO-480, 120), (560, ALTO-480, 120),
                (360, ALTO-580, 105), (640, ALTO-580, 105),
                (ANCHO//2-20, 250, 110),
            ],
            'hincha': (360, ALTO-580-30),
        },
        # Nivel 4
        {
            'p': [
                (60, ALTO-120, 130), (300, ALTO-120, 130), (520, ALTO-120, 130), (760, ALTO-120, 130),
                (160, ALTO-230, 120), (430, ALTO-230, 120), (680, ALTO-230, 120),
                (90, ALTO-340, 115), (370, ALTO-340, 115), (620, ALTO-340, 115), (880, ALTO-340, 110),
                (210, ALTO-450, 110), (540, ALTO-450, 110),
                (320, ALTO-560, 105), (600, ALTO-560, 105),
            ],
            'e': [
                (120, ALTO-120, 80), (370, ALTO-120, 80), (640, ALTO-120, 80),
                (230, ALTO-230, 110), (500, ALTO-230, 110), (750, ALTO-230, 110),
                (160, ALTO-340, 110), (440, ALTO-340, 110), (690, ALTO-340, 110), (950, ALTO-340, 110),
                (280, ALTO-450, 110), (610, ALTO-450, 110),
                (390, ALTO-560, 100), (660, ALTO-560, 100),
                (ANCHO//2-20, 250, 110),
            ],
            'hincha': (390, ALTO-560-30),
        },
        # Nivel 5
        {
            'p': [
                (40, ALTO-120, 110), (280, ALTO-120, 110), (490, ALTO-120, 110), (720, ALTO-120, 110), (890, ALTO-120, 100),
                (140, ALTO-235, 100), (400, ALTO-235, 100), (650, ALTO-235, 100),
                (80, ALTO-355, 95), (350, ALTO-355, 95), (600, ALTO-355, 95), (860, ALTO-355, 90),
                (200, ALTO-470, 90), (510, ALTO-470, 90),
                (310, ALTO-580, 85), (580, ALTO-580, 85),
            ],
            'e': [
                (90, ALTO-120, 80), (350, ALTO-120, 80), (580, ALTO-120, 80), (800, ALTO-120, 80),
                (210, ALTO-235, 115), (470, ALTO-235, 115), (720, ALTO-235, 115),
                (150, ALTO-355, 120), (420, ALTO-355, 120), (670, ALTO-355, 120), (930, ALTO-355, 120),
                (270, ALTO-470, 115), (570, ALTO-470, 115),
                (380, ALTO-580, 110), (640, ALTO-580, 110),
                (ANCHO//2-20, 248, 110),
            ],
            'hincha': (380, ALTO-580-30),
        },
    ]

    idx = min(nivel - 1, len(layouts) - 1)
    lay = layouts[idx]
    plataformas += lay['p']
    escaleras = lay['e']
    hincha_pos = lay.get('hincha', (ANCHO//2, ALTO-100))

    cervezas = []
    for (px, py, pw) in lay['p']:
        n = max(1, pw // 60)
        for i in range(n):
            cx = px + (i + 1) * pw // (n + 1)
            cervezas.append((cx, py - 20))

    mates = []
    if len(lay['p']) > 4:
        mates.append((lay['p'][2][0] + 30, lay['p'][2][1] - 20))
    if len(lay['p']) > 8:
        mates.append((lay['p'][6][0] + 30, lay['p'][6][1] - 20))

    return plataformas, escaleras, cervezas, mates, hincha_pos


# ─────────────────────────────────────────────────────────────────────────────
#  JUEGO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
class KongArgentino:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(f"{NOMBRE_JUEGO} - v{VERSION}")

        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.clock = pygame.time.Clock()
        self.gestor = GestorGraficos()
        self.gestor.argentino = None
        self.particulas = SistemaParticulas(self.gestor)
        self.gestor.particulas = self.particulas.particulas
        self.textos_flotantes = []

        self.estado = "menu"
        self.nivel = 1
        self.puntuacion = 0
        self.high_score = 0
        self.pausa = False

        self.plataformas = []
        self.escaleras = []
        self.barriles = []
        self.poderes = []
        self.cervezas = []

        self.argentino = None
        self.borracho = None
        self.hincha = None
        self.kong = None
        self.princesa = None

        self._frame_global = 0
        self.crear_nivel()

    # ── NIVEL ─────────────────────────────────────────────────────────────────
    def crear_nivel(self):
        self.plataformas = []
        self.escaleras = []
        self.barriles = []
        self.poderes = []
        self.cervezas = []
        self.textos_flotantes = []

        plat_data, esc_data, cerv_pos, mates_pos, hincha_pos = generar_layout_nivel(self.nivel)

        for (x, y, w) in plat_data:
            self.plataformas.append(Plataforma(x, y, w, self.gestor))
        for (x, y, h) in esc_data:
            self.escaleras.append(Escalera(x, y, h, self.gestor))
        for (x, y) in cerv_pos:
            self.cervezas.append(BarrilCerveza(x, y, self.gestor, es_item=True))
        for (x, y) in mates_pos:
            self.poderes.append(PoderMate(x, y, self.gestor))

        Y_KONG = 80
        Y_PRINCESA = 80
        self.kong = KongCervecero(ANCHO//2 - 60, Y_KONG, self.gestor, self.nivel)
        self.gestor.kong = self.kong
        self.princesa = Princesa(ANCHO//2 + 50, Y_PRINCESA, self.gestor)
        self.argentino = Argentino(100, ALTO - 70, self.gestor)
        self.gestor.argentino = self.argentino
        self.borracho = BorrachoIA(300, ALTO - 70, self.gestor)
        # Crear el hincha
        self.hincha = HinchaBorrachito(hincha_pos[0], hincha_pos[1], self.gestor)

    # ── PARTÍCULAS Y TEXTOS ───────────────────────────────────────────────────
    def emitir(self, x, y, color, n=10, fuente='explosion'):
        self.particulas.emitir(x, y, color, n, fuente)

    def texto_flotante(self, texto, x, y, color, tamaño=22):
        self.textos_flotantes.append(TextoFlotante(texto, x, y, color, tamaño))

    def actualizar_textos(self):
        for t in self.textos_flotantes[:]:
            t.update()
            if t.vida <= 0:
                self.textos_flotantes.remove(t)

    def dibujar_textos(self):
        for t in self.textos_flotantes:
            t.dibujar(self.pantalla, self.gestor)

    # ── HUD ───────────────────────────────────────────────────────────────────
    def dibujar_hud(self):
        hud = pygame.Surface((ANCHO, 70), pygame.SRCALPHA)
        for i in range(70):
            alpha = 180 - i
            pygame.draw.line(hud, (0, 0, 0, max(0, alpha)), (0, i), (ANCHO, i))
        self.pantalla.blit(hud, (0, 0))
        pygame.draw.line(self.pantalla, COLORES['oro'], (0, 69), (ANCHO, 69), 2)

        self.gestor.dibujar_texto(self.pantalla, f"PUNTOS: {self.puntuacion:06d}", 26,
                                   COLORES['amarillo'], 15, 8, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"NIVEL: {self.nivel}", 24,
                                   COLORES['blanco'], 15, 38, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"MEJOR: {self.high_score:06d}", 20,
                                   COLORES['oro'], ANCHO//2, 10, centro=True, sombra=True)

        for i in range(min(self.argentino.vidas, 9)):
            self.gestor.dibujar_corazon(self.pantalla, 30 + i * 34, ALTO - 30)

        # Controles en HUD
        self.gestor.dibujar_texto(self.pantalla, "Z/X: Atacar", 14, COLORES['gris'],
                                   ANCHO//2 - 100, ALTO - 25)

        if self.argentino.tiene_poder:
            t_seg = (self.argentino.tiempo_poder // FPS) + 1
            col = COLORES['verde'] if t_seg > 2 else COLORES['rojo']
            self.gestor.dibujar_texto(self.pantalla, f"🧉 MATE {t_seg}s", 22, col,
                                       ANCHO - 150, 8, sombra=True)
            ancho_b = int(130 * self.argentino.tiempo_poder / TIEMPO_PODER)
            pygame.draw.rect(self.pantalla, COLORES['negro'], (ANCHO-152, 38, 130, 14))
            pygame.draw.rect(self.pantalla, COLORES['verde_oscuro'], (ANCHO-150, 40, 126, 10))
            pygame.draw.rect(self.pantalla, COLORES['verde'], (ANCHO-150, 40, ancho_b, 10))
            pygame.draw.rect(self.pantalla, COLORES['blanco'], (ANCHO-152, 38, 130, 14), 2)

        if self.argentino.combo >= 2:
            colores = [COLORES['amarillo'], COLORES['naranja'], 
                       COLORES['rojo'], COLORES['violeta'], COLORES['oro']]
            col = colores[min(self.argentino.combo - 2, 4)]
            self.gestor.dibujar_texto(self.pantalla, f"🔥 COMBO x{self.argentino.combo}! 🔥", 28,
                                       col, ANCHO//2, 36, centro=True, sombra=True)

        if self.borracho.nivel_borrachera > 0:
            bx = ANCHO - 170
            self.gestor.dibujar_texto(self.pantalla, "🍺 BORRACHERA:", 14, COLORES['blanco'], 
                                      bx, ALTO - 50)
            ab = int(90 * self.borracho.nivel_borrachera / 10)
            pygame.draw.rect(self.pantalla, COLORES['negro'], (bx, ALTO - 32, 90, 12))
            col_b = COLORES['verde'] if self.borracho.nivel_borrachera < 5 else COLORES['rojo']
            pygame.draw.rect(self.pantalla, col_b, (bx, ALTO - 32, ab, 12))
            pygame.draw.rect(self.pantalla, COLORES['blanco'], (bx, ALTO - 32, 90, 12), 1)

        self.gestor.dibujar_texto(self.pantalla, NOMBRE_JUEGO, 14, COLORES['gris'], 
                                  ANCHO-140, ALTO-18)

    # ── DIBUJO ────────────────────────────────────────────────────────────────
    def dibujar(self):
        self.gestor.dibujar_fondo(self.pantalla, self.nivel)

        for p in self.plataformas:
            p.dibujar(self.pantalla)
        for e in self.escaleras:
            e.dibujar(self.pantalla)
        for c in self.cervezas:
            c.dibujar(self.pantalla)
        for b in self.barriles:
            b.dibujar(self.pantalla)
        for p in self.poderes:
            p.dibujar(self.pantalla)

        self.kong.dibujar(self.pantalla)
        self.princesa.dibujar(self.pantalla)
        self.argentino.dibujar(self.pantalla)
        self.borracho.dibujar(self.pantalla)
        if self.hincha:
            self.hincha.dibujar(self.pantalla)

        self.particulas.dibujar(self.pantalla)
        self.dibujar_textos()
        self.dibujar_hud()

        if self.pausa:
            s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            s.fill((0, 0, 0, 170))
            self.pantalla.blit(s, (0, 0))
            self.gestor.dibujar_texto(self.pantalla, "⏸  PAUSA", 72, COLORES['blanco'],
                                       ANCHO//2, ALTO//2 - 50, centro=True, sombra=True)
            self.gestor.dibujar_texto(self.pantalla, "P para continuar  |  ESC para salir al menú", 24,
                                       COLORES['amarillo'], ANCHO//2, ALTO//2 + 30, centro=True)

    # ── PANTALLAS ─────────────────────────────────────────────────────────────
    def dibujar_menu(self):
        self.gestor.dibujar_menu(self.pantalla)
        mx, my = pygame.mouse.get_pos()

        start_rect = pygame.Rect(ANCHO//2 - 120, 540, 240, 55)
        exit_rect = pygame.Rect(ANCHO//2 - 120, 608, 240, 55)
        self.gestor.dibujar_boton(self.pantalla, start_rect.x, start_rect.y,
                                   "▶  INICIAR", 240, 55, start_rect.collidepoint(mx, my))
        self.gestor.dibujar_boton(self.pantalla, exit_rect.x, exit_rect.y,
                                   "✖  SALIR", 240, 55, exit_rect.collidepoint(mx, my))
        if self.high_score > 0:
            self.gestor.dibujar_texto(self.pantalla, f"🏆 MEJOR PUNTAJE: {self.high_score:06d}", 22,
                                       COLORES['oro'], ANCHO//2, 630, centro=True, sombra=True)
        return start_rect, exit_rect

    def dibujar_game_over(self):
        self.gestor.dibujar_fondo(self.pantalla, self.nivel)
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 190))
        self.pantalla.blit(s, (0, 0))

        col = COLORES['rojo'] if (self._frame_global // 20) % 2 == 0 else (180, 0, 0)
        self.gestor.dibujar_texto(self.pantalla, "💀 GAME OVER 💀", 70, col,
                                   ANCHO//2, ALTO//2 - 110, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"PUNTOS: {self.puntuacion:06d}", 38,
                                   COLORES['oro'], ANCHO//2, ALTO//2 - 20, centro=True, sombra=True)
        if self.puntuacion >= self.high_score and self.high_score > 0:
            self.gestor.dibujar_texto(self.pantalla, "🏆 ¡NUEVO RÉCORD! 🏆", 28,
                                       COLORES['amarillo'], ANCHO//2, ALTO//2 + 30, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, "R  para reiniciar  |  ESC  para el menú", 26,
                                   COLORES['blanco'], ANCHO//2, ALTO//2 + 90, centro=True)

    def dibujar_victoria(self):
        self.gestor.dibujar_fondo(self.pantalla, self.nivel)
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 170))
        self.pantalla.blit(s, (0, 0))

        t = self._frame_global
        col = COLORES['oro'] if (t // 15) % 2 == 0 else COLORES['amarillo']
        self.gestor.dibujar_texto(self.pantalla, "🎉 ¡NIVEL COMPLETADO! 🎉", 52, col,
                                   ANCHO//2, ALTO//2 - 100, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"PUNTOS: {self.puntuacion:06d}", 34,
                                   COLORES['blanco'], ANCHO//2, ALTO//2 - 30, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"Nivel {self.nivel + 1} te espera...", 26,
                                   COLORES['celeste'], ANCHO//2, ALTO//2 + 30, centro=True)
        self.gestor.dibujar_texto(self.pantalla,
                                   "R  siguiente nivel  |  ESC  menú", 24,
                                   COLORES['blanco'], ANCHO//2, ALTO//2 + 90, centro=True)
        self.particulas.dibujar(self.pantalla)

    # ── LÓGICA ────────────────────────────────────────────────────────────────
    def reiniciar_juego(self):
        self.nivel = 1
        self.puntuacion = 0
        self.crear_nivel()
        self.estado = "jugando"

    def siguiente_nivel(self):
        self.nivel += 1
        if self.nivel > 5:
            self.estado = "victoria_final"
            return
        self.puntuacion += PUNTUACION_POR_NIVEL * self.nivel
        self.crear_nivel()
        self.estado = "jugando"

    def _otorgar_puntos(self, puntos, x, y, color=None, texto=None):
        multi = max(1, self.argentino.combo)
        total = puntos * multi
        self.puntuacion += total
        lbl = texto or (f"+{total}" if multi == 1 else f"+{total} x{multi}!")
        self.texto_flotante(lbl, x, y, color or COLORES['amarillo'],
                             tamaño=18 + min(multi * 2, 10))

    def _update_juego(self):
        self.argentino.update(self.plataformas, self.escaleras)
        self.borracho.update(self.plataformas, self.escaleras, self.barriles)
        if self.hincha:
            self.hincha.update()
        self.princesa.update()
        self.kong.update(self.plataformas)

        for pm in self.poderes:
            pm.update()

        dist_kong = math.hypot(self.argentino.rect.x - self.kong.rect.x,
                               self.argentino.rect.y - self.kong.rect.y)
        self.kong.set_mario_cerca(dist_kong < 250)

        cfg = DIFICULTAD_NIVEL.get(self.nivel, DIFICULTAD_NIVEL[5])
        if (self.kong.tiempo_barril > self.kong.get_tiempo_barril()
                and len(self.barriles) < cfg['max_barriles']):
            barril = self.kong.lanzar_barril()
            self.barriles.append(barril)
            self.kong.tiempo_barril = 0

        for b in self.barriles[:]:
            b.update(self.plataformas, self.escaleras)
            if b.rect.y > ALTO + 60 or b.rect.x < -60 or b.rect.x > ANCHO + 60:
                self.barriles.remove(b)

        # --- COLISIONES ---
        # Cervezas
        for c in self.cervezas[:]:
            if self.argentino.rect.colliderect(c.rect):
                self.argentino.add_combo()
                self._otorgar_puntos(PUNTUACION_POR_CERVEZA,
                                      c.rect.centerx, c.rect.top,
                                      COLORES['amarillo'])
                self.cervezas.remove(c)
                self.gestor.reproducir_sonido('moneda')
                self.emitir(c.rect.centerx, c.rect.centery, COLORES['amarillo'], 8, 'estrella')
                if self.argentino.combo >= 3:
                    self.gestor.reproducir_sonido('combo')
                    self.emitir(c.rect.centerx, c.rect.centery, COLORES['oro'], 15, 'combo')

        # Poderes
        for p in self.poderes[:]:
            if self.argentino.rect.colliderect(p.rect):
                self.argentino.tiene_poder = True
                self.argentino.tiempo_poder = TIEMPO_PODER
                self.poderes.remove(p)
                self.gestor.reproducir_sonido('martillo')
                self.emitir(p.rect.centerx, p.rect.centery, COLORES['verde'], 20, 'combo')
                self.texto_flotante("🧉 ¡MATE POWER! 🧉", p.rect.centerx, p.rect.top - 10,
                                    COLORES['verde'], 28)

        # ─── BARRILES VS JUGADOR (CON ATAQUE Y SALTO) ───
        for b in self.barriles[:]:
            # 1. Verificar si el jugador golpea el barril con ataque
            if self.argentino.ataque_activo and self.argentino.ataque_rect.colliderect(b.rect):
                self._otorgar_puntos(PUNTUACION_POR_BARRIL_ROTO,
                                      b.rect.centerx, b.rect.top,
                                      COLORES['naranja'])
                self.barriles.remove(b)
                self.emitir(b.rect.centerx, b.rect.centery, COLORES['marron'], 15, 'explosion')
                self.emitir(b.rect.centerx, b.rect.centery, COLORES['amarillo'], 10, 'ataque')
                self.gestor.reproducir_sonido('golpe')
                self.texto_flotante("💥 ¡BARRIL ROTO! 💥", b.rect.centerx, b.rect.top - 10,
                                    COLORES['naranja'], 24)
                continue

            # 2. Verificar si el jugador es golpeado por el barril
            if self.argentino.rect.colliderect(b.rect):
                if self.argentino.tiene_poder:
                    # Con poder, rompe el barril automáticamente
                    self._otorgar_puntos(PUNTUACION_POR_BARRIL_ROTO,
                                          b.rect.centerx, b.rect.top,
                                          COLORES['verde'])
                    self.barriles.remove(b)
                    self.emitir(b.rect.centerx, b.rect.centery, COLORES['verde'], 15, 'explosion')
                    self.gestor.reproducir_sonido('golpe')
                else:
                    # Golpe normal
                    if self.argentino.golpear():
                        self.emitir(self.argentino.rect.centerx, self.argentino.rect.centery,
                                    COLORES['rojo'], 20, 'golpe')
                        self.gestor.reproducir_sonido('golpe')
                        self.texto_flotante("💥 ¡AY! 💥", self.argentino.rect.centerx,
                                            self.argentino.rect.top, COLORES['rojo'], 30)
                        if self.argentino.vidas <= 0:
                            self.estado = "game_over"
                            if self.puntuacion > self.high_score:
                                self.high_score = self.puntuacion
                            self.gestor.reproducir_sonido('game_over')
                        else:
                            self.argentino.respawn(100, ALTO - 70)
                    if b in self.barriles:
                        self.barriles.remove(b)

        # Barriles contra borracho
        for b in self.barriles[:]:
            if self.borracho.rect.colliderect(b.rect):
                self.borracho.beber_barril()
                self.barriles.remove(b)
                self.emitir(b.rect.centerx, b.rect.centery, COLORES['amarillo'], 10, 'explosion')
                self._otorgar_puntos(50, b.rect.centerx, b.rect.top, COLORES['celeste'],
                                      texto="🍺 +50 (Borracho!)")

        # ─── ATAQUE DEL JUGADOR CONTRA EL HINCHA (CORREGIDO) ───
        if self.hincha and self.argentino.ataque_activo and self.argentino.ataque_rect.colliderect(self.hincha.rect):
            # Guardamos las coordenadas ANTES de que el objeto desaparezca
            hx = self.hincha.rect.centerx
            hy = self.hincha.rect.centery
            htop = self.hincha.rect.top

            murio = self.hincha.recibir_golpe()

            # Efectos visuales y sonido del golpe
            self.emitir(hx, hy, COLORES['rojo'], 15, 'golpe')
            self.gestor.reproducir_sonido('golpe')
            self._otorgar_puntos(50, hx, htop, COLORES['celeste'],
                                 texto="💥 ¡GOLPE AL HINCHA! +50")

            if murio:
                self.texto_flotante("🇦🇷 ¡HINCHA ELIMINADO! +200",
                                    hx, htop - 20,
                                    COLORES['oro'], 28)
                self._otorgar_puntos(200, hx, htop, COLORES['oro'])
                self.emitir(hx, hy, COLORES['amarillo'], 30, 'combo')
                self.hincha = None  # Ahora sí, después de usar las coordenadas

        # Colisión con Kong
        if self.argentino.rect.colliderect(self.kong.rect):
            if not self.argentino.tiene_poder:
                if self.argentino.golpear():
                    self.emitir(self.argentino.rect.centerx, self.argentino.rect.centery,
                                COLORES['rojo'], 20, 'golpe')
                    self.gestor.reproducir_sonido('peligro')
                    if self.argentino.vidas <= 0:
                        self.estado = "game_over"
                        if self.puntuacion > self.high_score:
                            self.high_score = self.puntuacion
                        self.gestor.reproducir_sonido('game_over')
                    else:
                        self.argentino.respawn(100, ALTO - 70)

        # Victoria
        if self.argentino.rect.colliderect(self.princesa.rect):
            self.estado = "victoria"
            self.gestor.reproducir_sonido('nivel')
            if self.puntuacion > self.high_score:
                self.high_score = self.puntuacion
            for _ in range(80):
                self.emitir(random.randint(0, ANCHO), random.randint(0, ALTO // 2),
                             random.choice([COLORES['oro'], COLORES['celeste'],
                                            COLORES['blanco'], COLORES['amarillo'],
                                            COLORES['rosa']]),
                             6, 'estrella')

    # ── LOOP PRINCIPAL ────────────────────────────────────────────────────────
    def run(self):
        while True:
            self.clock.tick(FPS)
            self._frame_global += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.estado == "jugando":
                            self.estado = "menu"
                        else:
                            self.estado = "menu"
                    if event.key == pygame.K_q and self.estado != "jugando":
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_p and self.estado == "jugando":
                        self.pausa = not self.pausa
                    if event.key == pygame.K_r:
                        if self.estado == "game_over":
                            self.reiniciar_juego()
                        elif self.estado == "victoria":
                            self.siguiente_nivel()

                if event.type == pygame.MOUSEBUTTONDOWN and self.estado == "menu":
                    mx, my = pygame.mouse.get_pos()
                    start_rect = pygame.Rect(ANCHO//2 - 120, 540, 240, 55)
                    exit_rect = pygame.Rect(ANCHO//2 - 120, 608, 240, 55)
                    if start_rect.collidepoint(mx, my):
                        self.reiniciar_juego()
                    elif exit_rect.collidepoint(mx, my):
                        pygame.quit()
                        sys.exit()

            self.particulas.actualizar()
            self.actualizar_textos()

            if self.estado == "menu":
                self.pantalla.fill((0, 0, 0))
                self.dibujar_menu()

            elif self.estado == "game_over":
                self.dibujar_game_over()
                self.particulas.dibujar(self.pantalla)

            elif self.estado == "victoria":
                self.dibujar_victoria()

            elif self.estado == "jugando":
                if not self.pausa:
                    self._update_juego()
                self.dibujar()

            pygame.display.flip()


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║          KONG ARGENTINO v3.2 - Gráficos Mejorados             ║
    ║                   Creado por Apresta                          ║
    ║                   para PRESTALABS                             ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║   ¡Rescata a la princesa del Kong Cervecero!                  ║
    ║                                                               ║
    ║   CONTROLES:                                                  ║
    ║   A/D o ←/→  : Moverse                                        ║
    ║   W/↑        : Subir escalera                                 ║
    ║   S/↓        : Bajar escalera                                 ║
    ║   ESPACIO    : Saltar                                         ║
    ║   Z o X      : Atacar (golpear barriles y hincha)             ║
    ║   P          : Pausar                                         ║
    ║   ESC        : Menú                                           ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    juego = KongArgentino()
    juego.run()