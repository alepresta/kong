# src/juego/main.py
"""
KONG ARGENTINO v4.0 - JUEGO PRINCIPAL
Mejoras v4.0:
- High score persistente en archivo
- Estado 'victoria_final' con pantalla especial
- Camera shake al recibir golpe
- Flash de pantalla al golpe / game over
- Detección de barril saltado → bonus de puntos
- Control de volumen con [ ] en cualquier momento
- ESC en game_over/victoria vuelve al menú directamente
- Pausa muestra controles resumidos
- Performance: tick() del gestor centralizado

Mejoras v4.1:
- Ataque en 4 direcciones (arriba, abajo, izquierda, derecha)
- Brazo de ataque más largo
- Salto más alto y caída más lenta
- Puede golpear a Kong, hinchas y borracho
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
    HinchaBorrachito, SistemaParticulas, TextoFlotante
)
from niveles.generador import generar_layout_nivel


class KongArgentino:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(f"{NOMBRE_JUEGO} - v{VERSION}")

        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.clock = pygame.time.Clock()
        self.gestor = GestorGraficos()
        self.particulas = SistemaParticulas(self.gestor)
        # Asignar la lista de partículas y el sistema al gestor
        self.gestor.particulas = self.particulas.particulas
        self.gestor.sistema_particulas = self.particulas
        self.textos_flotantes = []

        self.estado = "menu"
        self.nivel = 1
        self.puntuacion = 0
        self.high_score = self._cargar_high_score()
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
        # Tiempo de pantalla de victoria/game over antes de aceptar input
        self._tiempo_resultado = 0
        self.crear_nivel()

    # ──────────────────────── PERSISTENCIA ────────────────────────── #

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

    # ──────────────────────── NIVEL ──────────────────────────────── #

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
        self.kong = KongCervecero(ANCHO//2 - 60, Y_KONG, self.gestor, self.nivel)
        self.gestor.kong = self.kong
        self.princesa = Princesa(ANCHO//2 + 50, Y_KONG, self.gestor)
        self.argentino = Argentino(100, ALTO - 70, self.gestor)
        self.gestor.argentino = self.argentino
        self.borracho = BorrachoIA(300, ALTO - 70, self.gestor)
        self.hincha = HinchaBorrachito(hincha_pos[0], hincha_pos[1], self.gestor)

        # Invalidar caché de fondo si cambia nivel
        self.gestor._fondo_cache.pop(self.nivel, None)

    # ──────────────────────── HELPERS ────────────────────────────── #

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

    def _otorgar_puntos(self, puntos, x, y, color=None, texto=None):
        multi = max(1, self.argentino.combo)
        total = puntos * multi
        self.puntuacion += total
        lbl = texto or (f"+{total}" if multi == 1 else f"+{total} x{multi}!")
        self.texto_flotante(lbl, x, y, color or COLORES['amarillo'],
                            tamaño=18 + min(multi * 2, 10))

    def _golpear_kong(self):
        """Función para golpear a Kong"""
        self.gestor.iniciar_shake(10, 4)
        self.gestor.iniciar_flash((255, 200, 50), 6)
        self.emitir(self.kong.rect.centerx, self.kong.rect.centery,
                    COLORES['oro'], 20, 'explosion')
        self.gestor.reproducir_sonido('golpe')
        
        # Kong se enoja más
        self.kong.tiempo_enojado = max(self.kong.tiempo_enojado, 40)
        
        # Puntos por golpear a Kong
        self._otorgar_puntos(100, self.kong.rect.centerx, self.kong.rect.top,
                             COLORES['oro'], texto="👊 ¡GOLPE A KONG! +100")
        self.texto_flotante("💢 ¡KONG ENOJADO!", self.kong.rect.centerx, 
                            self.kong.rect.top - 20, COLORES['rojo'], 24)

    def _golpear_borracho(self):
        """Función para golpear al borracho"""
        self.emitir(self.borracho.rect.centerx, self.borracho.rect.centery,
                    COLORES['amarillo'], 15, 'golpe')
        self.gestor.reproducir_sonido('golpe')
        
        # El borracho pierde nivel de borrachera y puede caer
        self.borracho.nivel_borrachera = max(0, self.borracho.nivel_borrachera - 2)
        self.borracho.estado = "buscando"
        self.borracho.tiempo_estado = 30
        
        # Puntos por golpear al borracho
        self._otorgar_puntos(30, self.borracho.rect.centerx, self.borracho.rect.top,
                             COLORES['celeste'], texto="👊 ¡GOLPE AL BORRACHO! +30")
        
        # Si el borracho tiene mucha borrachera, se tambalea más
        if self.borracho.nivel_borrachera >= 6:
            self.borracho.vel_x = random.choice([-4, -3, 3, 4])
            self.borracho.vel_y = -3
            self.texto_flotante("🍺 ¡BORRACHO TAMBALEANDO!", 
                               self.borracho.rect.centerx, 
                               self.borracho.rect.top - 20, 
                               COLORES['naranja'], 20)

    # ──────────────────────── HUD ────────────────────────────────── #

    def dibujar_hud(self):
        # Barra superior semitransparente
        hud = pygame.Surface((ANCHO, 70), pygame.SRCALPHA)
        for i in range(70):
            alpha = 185 - i * 2
            pygame.draw.line(hud, (0, 0, 0, max(0, alpha)), (0, i), (ANCHO, i))
        self.pantalla.blit(hud, (0, 0))
        pygame.draw.line(self.pantalla, COLORES['oro'], (0, 69), (ANCHO, 69), 2)

        self.gestor.dibujar_texto(self.pantalla, f"PUNTOS: {self.puntuacion:06d}", 26,
                                   COLORES['amarillo'], 15, 8, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"NIVEL: {self.nivel}", 24,
                                   COLORES['blanco'], 15, 38, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"MEJOR: {self.high_score:06d}", 20,
                                   COLORES['oro'], ANCHO//2, 10, centro=True, sombra=True)

        # Vidas como corazones
        for i in range(min(self.argentino.vidas, 9)):
            self.gestor.dibujar_corazon(self.pantalla, 30 + i * 34, ALTO - 30)

        # Hint de controles
        self.gestor.dibujar_texto(self.pantalla, "ESPACIO: Atacar (↑↓←→)  [ ]: Volumen", 13,
                                   COLORES['gris'], ANCHO//2 - 150, ALTO - 22)

        # Barra de mate power
        if self.argentino.tiene_poder:
            t_seg = (self.argentino.tiempo_poder // FPS) + 1
            pct = self.argentino.tiempo_poder / TIEMPO_PODER
            col = COLORES['verde'] if pct > 0.3 else COLORES['rojo']
            # Parpadea cuando queda poco
            if pct < 0.2 and (self._frame_global // 8) % 2 == 0:
                self.gestor.reproducir_sonido('poder_acabando')
            self.gestor.dibujar_texto(self.pantalla, f"🧉 MATE {t_seg}s", 22, col,
                                       ANCHO - 152, 8, sombra=True)
            ancho_b = int(130 * pct)
            pygame.draw.rect(self.pantalla, COLORES['negro'], (ANCHO-152, 38, 130, 14))
            pygame.draw.rect(self.pantalla, COLORES['verde_oscuro'], (ANCHO-150, 40, 126, 10))
            pygame.draw.rect(self.pantalla, col, (ANCHO-150, 40, ancho_b, 10))
            pygame.draw.rect(self.pantalla, COLORES['blanco'], (ANCHO-152, 38, 130, 14), 2)

        # Combo
        if self.argentino.combo >= 2:
            colores_combo = [COLORES['amarillo'], COLORES['naranja'], 
                             COLORES['rojo'], COLORES['violeta'], COLORES['oro']]
            col = colores_combo[min(self.argentino.combo - 2, 4)]
            # Pulso de tamaño
            tam = 28 + int(math.sin(self._frame_global * 0.3) * 3)
            self.gestor.dibujar_texto(self.pantalla, f"🔥 COMBO x{self.argentino.combo}! 🔥", tam,
                                       col, ANCHO//2, 36, centro=True, sombra=True)

        # Barra de borrachera
        if self.borracho.nivel_borrachera > 0:
            bx = ANCHO - 170
            self.gestor.dibujar_texto(self.pantalla, "🍺 BORRACHERA:", 14, COLORES['blanco'], 
                                      bx, ALTO - 50)
            ab = int(90 * self.borracho.nivel_borrachera / 10)
            pygame.draw.rect(self.pantalla, COLORES['negro'], (bx, ALTO - 32, 90, 12))
            col_b = COLORES['verde'] if self.borracho.nivel_borrachera < 5 else COLORES['rojo']
            pygame.draw.rect(self.pantalla, col_b, (bx, ALTO - 32, ab, 12))
            pygame.draw.rect(self.pantalla, COLORES['blanco'], (bx, ALTO - 32, 90, 12), 1)

        # Watermark
        self.gestor.dibujar_texto(self.pantalla, NOMBRE_JUEGO, 13, COLORES['gris_oscuro'], 
                                  ANCHO-142, ALTO-18)

    # ──────────────────────── DIBUJAR ────────────────────────────── #

    def dibujar(self):
        ox, oy = self.gestor.get_shake()
        # Aplicamos shake al blit principal desplazando todo
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
        if self.hincha:
            self.hincha.dibujar(surf_juego)

        self.particulas.dibujar(surf_juego)
        self.dibujar_textos()

        self.pantalla.blit(surf_juego, (ox, oy))
        self.dibujar_hud()
        self.gestor.aplicar_flash(self.pantalla)

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
        return start_rect, exit_rect

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
        self.gestor.dibujar_texto(self.pantalla, "🎉 ¡NIVEL COMPLETADO! 🎉", 52, col,
                                   ANCHO//2, ALTO//2 - 110, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"PUNTOS: {self.puntuacion:06d}", 34,
                                   COLORES['blanco'], ANCHO//2, ALTO//2 - 40, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"Nivel {self.nivel + 1} te espera...", 26,
                                   COLORES['celeste'], ANCHO//2, ALTO//2 + 20, centro=True)
        self.gestor.dibujar_texto(self.pantalla, "R  siguiente nivel  |  ESC  menú", 24,
                                   COLORES['blanco'], ANCHO//2, ALTO//2 + 80, centro=True)
        self.particulas.dibujar(self.pantalla)

    def dibujar_victoria_final(self):
        self.gestor.dibujar_fondo(self.pantalla, 5)
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 155))
        self.pantalla.blit(s, (0, 0))

        t = self._frame_global
        # Titulo pulsante
        scale = 1.0 + 0.04 * math.sin(t * 0.06)
        tam = int(58 * scale)
        col_cycle = [COLORES['oro'], COLORES['amarillo'], COLORES['celeste'], COLORES['blanco']]
        col = col_cycle[(t // 20) % 4]
        self.gestor.dibujar_texto(self.pantalla, "🏆 ¡GANASTE! 🏆", tam, col,
                                   ANCHO//2, ALTO//2 - 140, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, "¡RESCATASTE A LA PRINCESA!", 36,
                                   COLORES['blanco'], ANCHO//2, ALTO//2 - 70, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, f"PUNTUACIÓN FINAL: {self.puntuacion:06d}", 30,
                                   COLORES['oro'], ANCHO//2, ALTO//2 - 10, centro=True, sombra=True)
        if self.puntuacion >= self.high_score:
            self.gestor.dibujar_texto(self.pantalla, "🏆 ¡NUEVO RÉCORD HISTÓRICO! 🏆", 28,
                                       COLORES['amarillo'], ANCHO//2, ALTO//2 + 36, centro=True, sombra=True)
        self.gestor.dibujar_texto(self.pantalla, "ESC  menú principal", 24,
                                   COLORES['blanco'], ANCHO//2, ALTO//2 + 90, centro=True)
        self.particulas.dibujar(self.pantalla)

    # ──────────────────────── ESTADOS ────────────────────────────── #

    def reiniciar_juego(self):
        self.nivel = 1
        self.puntuacion = 0
        self.crear_nivel()
        self.estado = "jugando"
        self._tiempo_resultado = 0

    def siguiente_nivel(self):
        self.nivel += 1
        if self.nivel > 5:
            self.estado = "victoria_final"
            if self.puntuacion > self.high_score:
                self.high_score = self.puntuacion
                self._guardar_high_score()
                self.gestor.reproducir_sonido('record')
            else:
                self.gestor.reproducir_sonido('victoria_final')
            # Fuegos artificiales
            for _ in range(60):
                self.emitir(random.randint(0, ANCHO), random.randint(0, ALTO // 2),
                             random.choice([COLORES['oro'], COLORES['celeste'],
                                            COLORES['blanco'], COLORES['amarillo'],
                                            COLORES['rosa'], COLORES['naranja']]),
                             8, 'fuego_artificial')
            return
        self.puntuacion += PUNTUACION_POR_NIVEL * self.nivel
        self.crear_nivel()
        self.estado = "jugando"
        self._tiempo_resultado = 0

    # ──────────────────────── UPDATE ─────────────────────────────── #

    def _update_juego(self):
        self.argentino.update(self.plataformas, self.escaleras)
        self.borracho.update(self.plataformas, self.escaleras, self.barriles)
        if self.hincha:
            self.hincha.update()
        self.princesa.update()
        self.kong.update(self.plataformas)

        dist_kong = math.hypot(self.argentino.rect.x - self.kong.rect.x,
                               self.argentino.rect.y - self.kong.rect.y)
        self.kong.set_mario_cerca(dist_kong < 250)

        cfg = DIFICULTAD_NIVEL.get(self.nivel, DIFICULTAD_NIVEL[5])

        # Lanzar barriles
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

            # Detección de salto sobre barril (bonus sin poder)
            if (not self.argentino.tiene_poder
                    and self.argentino.vel_y > 0
                    and not self.argentino.en_suelo
                    and self.argentino.rect.bottom <= b.rect.top + 10
                    and abs(self.argentino.rect.centerx - b.rect.centerx) < 28):
                self._otorgar_puntos(PUNTUACION_POR_BARRIL_SALTADO,
                                      b.rect.centerx, b.rect.top - 10,
                                      COLORES['cyan'], texto="¡SALTO! +25")
                self.gestor.reproducir_sonido('barril_saltado')

            # Colisión jugador - barril
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

            # Borracho toma barril
            if self.borracho.rect.colliderect(b.rect):
                self.borracho.beber_barril()
                self.barriles.remove(b)
                self.emitir(b.rect.centerx, b.rect.centery, COLORES['amarillo'], 10, 'explosion')
                self._otorgar_puntos(50, b.rect.centerx, b.rect.top, COLORES['celeste'],
                                      texto="🍺 +50 (Borracho!)")
                continue

            # Barril sale de la pantalla
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

        # ── SISTEMA DE ATAQUE MEJORADO ──
        # Golpear con el ataque activo
        if self.argentino.ataque_activo:
            ataque_rect = self.argentino.ataque_rect
            
            # Golpear al Kong
            if ataque_rect.colliderect(self.kong.rect):
                self._golpear_kong()
            
            # Golpear al borracho
            if ataque_rect.colliderect(self.borracho.rect):
                self._golpear_borracho()
            
            # Golpear al hincha
            if self.hincha and ataque_rect.colliderect(self.hincha.rect):
                hx, hy, htop = self.hincha.rect.centerx, self.hincha.rect.centery, self.hincha.rect.top
                murio = self.hincha.recibir_golpe()
                self.emitir(hx, hy, COLORES['rojo'], 15, 'golpe')
                self.gestor.reproducir_sonido('hincha_golpe')
                self._otorgar_puntos(50, hx, htop, COLORES['celeste'], texto="💥 ¡GOLPE AL HINCHA! +50")
                if murio:
                    self.texto_flotante("🇦🇷 ¡HINCHA ELIMINADO! +200", hx, htop - 20,
                                        COLORES['oro'], 28)
                    self._otorgar_puntos(200, hx, htop, COLORES['oro'])
                    self.emitir(hx, hy, COLORES['amarillo'], 30, 'fuego_artificial')
                    self.hincha = None

        # ── Colisión jugador - Kong (sin ataque) ──
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

    def run(self):
        while True:
            self.clock.tick(FPS)
            self._frame_global += 1
            self._tiempo_resultado += 1
            self.gestor.tick()   # actualiza shake, flash, etc.

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._guardar_high_score()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    key = event.key

                    # Volumen global (en cualquier estado)
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

                    # R solo acepta input pasados 30 frames (evita skip accidental)
                    if key == pygame.K_r and self._tiempo_resultado > 30:
                        if self.estado == "game_over":
                            self.reiniciar_juego()
                        elif self.estado == "victoria":
                            self.siguiente_nivel()

                    if key == pygame.K_q and self.estado == "menu":
                        self._guardar_high_score()
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and self.estado == "menu":
                    mx, my = pygame.mouse.get_pos()
                    start_rect = pygame.Rect(ANCHO//2 - 120, 548, 240, 55)
                    exit_rect  = pygame.Rect(ANCHO//2 - 120, 616, 240, 55)
                    if start_rect.collidepoint(mx, my):
                        self.reiniciar_juego()
                    elif exit_rect.collidepoint(mx, my):
                        self._guardar_high_score()
                        pygame.quit()
                        sys.exit()

            # ── Actualizar partículas ──
            self.particulas.actualizar()
            self.actualizar_textos()

            # ── Render según estado ──
            if self.estado == "menu":
                self.pantalla.fill((0, 0, 0))
                self.dibujar_menu()

            elif self.estado == "game_over":
                self.dibujar_game_over()

            elif self.estado == "victoria":
                self.dibujar_victoria()

            elif self.estado == "victoria_final":
                self.dibujar_victoria_final()
                # Fuegos artificiales continuos en victoria final
                if self._frame_global % 18 == 0:
                    self.emitir(random.randint(50, ANCHO-50),
                                random.randint(50, ALTO//2),
                                random.choice([COLORES['oro'], COLORES['celeste'],
                                               COLORES['blanco'], COLORES['amarillo'],
                                               COLORES['rosa'], COLORES['naranja']]),
                                10, 'fuego_artificial')

            elif self.estado == "jugando":
                if not self.pausa:
                    self._update_juego()
                self.dibujar()

            pygame.display.flip()