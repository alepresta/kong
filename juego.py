"""
PRESTALABS-PLAY - DONKEY KONG ARCADE EDITION
"""
import pygame
import sys
import random
from constantes import *
from gestor_graficos import GestorGraficos
from jugador import Mario
from objetos import Plataforma, Escalera, Barril, Martillo, Moneda, DonkeyKong, Pauline

class PrestaLabsPlay:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(f"{NOMBRE_JUEGO} - Donkey Kong v{VERSION}")
        
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.clock = pygame.time.Clock()
        self.gestor = GestorGraficos()
        
        self.estado = "menu"
        self.nivel = 1
        self.puntuacion = 0
        self.pausa = False
        
        self.particulas = []
        self.efecto_tiempo = 0
        self.plataformas = []
        self.escaleras = []
        self.barriles = []
        self.martillos = []
        self.monedas = []
        self.mario = None
        self.donkey_kong = None
        self.pauline = None
        
        self.crear_nivel()
    
    def crear_nivel(self):
        self.plataformas = []
        self.escaleras = []
        self.barriles = []
        self.martillos = []
        self.monedas = []
        
        suelo = Plataforma(0, ALTO - 40, ANCHO, self.gestor)
        self.plataformas.append(suelo)
        
        niveles_plataformas = [
            (80, ALTO - 120, 180), (320, ALTO - 120, 180), (560, ALTO - 120, 180), (800, ALTO - 120, 150),
            (150, ALTO - 220, 150), (400, ALTO - 220, 150), (650, ALTO - 220, 150),
            (100, ALTO - 320, 140), (350, ALTO - 320, 140), (600, ALTO - 320, 140), (850, ALTO - 320, 120),
            (200, ALTO - 420, 130), (500, ALTO - 420, 130),
            (300, ALTO - 520, 120), (580, ALTO - 520, 120),
        ]
        
        for x, y, ancho in niveles_plataformas:
            self.plataformas.append(Plataforma(x, y, ancho, self.gestor))
        
        plataforma_dk = Plataforma(100, 160, 825, self.gestor)
        self.plataformas.append(plataforma_dk)
        
        conexiones = [
            (130, ALTO - 120, 85), (400, ALTO - 120, 85), (680, ALTO - 120, 85),
            (220, ALTO - 220, 105), (470, ALTO - 220, 105), (720, ALTO - 220, 105),
            (170, ALTO - 320, 105), (420, ALTO - 320, 105), (670, ALTO - 320, 105), (920, ALTO - 320, 105),
            (270, ALTO - 420, 105), (570, ALTO - 420, 105),
            (360, ALTO - 520, 105), (640, ALTO - 520, 105),
            (ANCHO//2 - 30, 160, 400),
        ]
        
        for x, y, alto in conexiones:
            self.escaleras.append(Escalera(x, y, alto, self.gestor))
        
        posiciones_monedas = [
            (120, ALTO - 140), (180, ALTO - 140), (360, ALTO - 140), (420, ALTO - 140),
            (600, ALTO - 140), (660, ALTO - 140), (840, ALTO - 140),
            (190, ALTO - 240), (250, ALTO - 240), (440, ALTO - 240), (500, ALTO - 240),
            (690, ALTO - 240), (750, ALTO - 240),
            (140, ALTO - 340), (200, ALTO - 340), (390, ALTO - 340), (450, ALTO - 340),
            (640, ALTO - 340), (700, ALTO - 340), (890, ALTO - 340),
            (240, ALTO - 440), (300, ALTO - 440), (540, ALTO - 440), (600, ALTO - 440),
            (340, ALTO - 540), (400, ALTO - 540), (620, ALTO - 540), (680, ALTO - 540),
        ]
        
        for x, y in posiciones_monedas:
            self.monedas.append(Moneda(x, y, self.gestor))
        
        self.martillos.append(Martillo(200, ALTO - 140, self.gestor))
        self.martillos.append(Martillo(600, ALTO - 340, self.gestor))
        
        Y_PLATAFORMA_DK = 160
        ALTO_MARIO = 24
        ALTO_DONKEY = 50
        ALTO_PAULINE = 28
        
        Y_MARIO = ALTO - 65
        Y_DONKEY = Y_PLATAFORMA_DK - ALTO_DONKEY
        Y_PAULINE = Y_PLATAFORMA_DK - ALTO_PAULINE
        
        self.mario = Mario(100, Y_MARIO, self.gestor)
        self.donkey_kong = DonkeyKong(ANCHO//2 - 40, 160, self.gestor)
        self.pauline = Pauline(ANCHO//2 + 60, Y_PAULINE, self.gestor)
    
    def crear_particula(self, x, y, color):
        self.particulas.append({'x': x, 'y': y, 'vx': random.uniform(-2, 2), 'vy': random.uniform(-5, -1), 'vida': 20, 'color': color})
    
    def actualizar_particulas(self):
        for p in self.particulas[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.3
            p['vida'] -= 1
            if p['vida'] <= 0:
                self.particulas.remove(p)
    
    def dibujar_particulas(self):
        for p in self.particulas:
            alpha = p['vida'] / 20
            size = int(3 * alpha)
            if size > 0:
                pygame.draw.circle(self.pantalla, p['color'], (int(p['x']), int(p['y'])), size)
    
    def dibujar_hud(self):
        self.gestor.dibujar_texto(self.pantalla, f"SCORE: {self.puntuacion}", 28, (0, 0, 0), 15, 15)
        self.gestor.dibujar_texto(self.pantalla, f"LEVEL: {self.nivel}", 28, (0, 0, 0), 15, 50)
        for i in range(min(self.mario.vidas, 9)):
            self.gestor.dibujar_corazon(self.pantalla, 30 + i * 30, ALTO - 30)
        if self.mario.tiene_martillo:
            tiempo = (self.mario.tiempo_martillo // 60) + 1
            self.gestor.dibujar_texto(self.pantalla, f"HAMMER: {tiempo}s", 20, (255, 215, 0), ANCHO - 120, 15)
        self.gestor.dibujar_texto(self.pantalla, NOMBRE_JUEGO, 16, (100, 100, 100), ANCHO - 110, ALTO - 20)
    
    def dibujar(self):
        self.gestor.dibujar_fondo(self.pantalla)
        for p in self.plataformas:
            p.dibujar(self.pantalla)
        for e in self.escaleras:
            e.dibujar(self.pantalla)
        for m in self.monedas:
            m.dibujar(self.pantalla)
        for b in self.barriles:
            b.dibujar(self.pantalla)
        for m in self.martillos:
            m.dibujar(self.pantalla)
        self.donkey_kong.dibujar(self.pantalla)
        self.pauline.dibujar(self.pantalla)
        self.mario.dibujar(self.pantalla)
        self.dibujar_particulas()
        self.dibujar_hud()
        if self.pausa:
            s = pygame.Surface((ANCHO, ALTO))
            s.set_alpha(180)
            s.fill((0, 0, 0))
            self.pantalla.blit(s, (0, 0))
            self.gestor.dibujar_texto(self.pantalla, "PAUSA", 72, (255, 255, 255), ANCHO//2, ALTO//2 - 50, centro=True)
            self.gestor.dibujar_texto(self.pantalla, "Presiona P para continuar", 28, (255, 255, 255), ANCHO//2, ALTO//2 + 30, centro=True)
            self.gestor.dibujar_texto(self.pantalla, "Presiona Q para salir", 28, (255, 255, 255), ANCHO//2, ALTO//2 + 70, centro=True)
    
    def dibujar_menu(self):
        self.gestor.dibujar_menu(self.pantalla)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        start_rect = pygame.Rect(ANCHO//2 - 100, 400, 200, 50)
        start_hover = start_rect.collidepoint(mouse_x, mouse_y)
        self.gestor.dibujar_boton(self.pantalla, start_rect.x, start_rect.y, "INICIAR", 200, 50, start_hover)
        exit_rect = pygame.Rect(ANCHO//2 - 100, 470, 200, 50)
        exit_hover = exit_rect.collidepoint(mouse_x, mouse_y)
        self.gestor.dibujar_boton(self.pantalla, exit_rect.x, exit_rect.y, "SALIR", 200, 50, exit_hover)
        return start_rect, exit_rect
    
    def dibujar_game_over(self):
        s = pygame.Surface((ANCHO, ALTO))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        self.pantalla.blit(s, (0, 0))
        self.gestor.dibujar_texto(self.pantalla, "GAME OVER", 64, (255, 0, 0), ANCHO//2, ALTO//2 - 80, centro=True)
        self.gestor.dibujar_texto(self.pantalla, f"SCORE FINAL: {self.puntuacion}", 36, (255, 215, 0), ANCHO//2, ALTO//2, centro=True)
        self.gestor.dibujar_texto(self.pantalla, "Presiona R para reiniciar", 28, (255, 255, 255), ANCHO//2, ALTO//2 + 80, centro=True)
        self.gestor.dibujar_texto(self.pantalla, "Presiona Q para salir", 28, (255, 255, 255), ANCHO//2, ALTO//2 + 120, centro=True)
    
    def dibujar_victoria(self):
        s = pygame.Surface((ANCHO, ALTO))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        self.pantalla.blit(s, (0, 0))
        self.gestor.dibujar_texto(self.pantalla, "¡NIVEL COMPLETADO!", 48, (255, 215, 0), ANCHO//2, ALTO//2 - 80, centro=True)
        self.gestor.dibujar_texto(self.pantalla, f"PUNTUACIÓN: {self.puntuacion}", 32, (255, 255, 255), ANCHO//2, ALTO//2 - 20, centro=True)
        self.gestor.dibujar_texto(self.pantalla, "Presiona R para siguiente nivel", 28, (255, 255, 255), ANCHO//2, ALTO//2 + 50, centro=True)
        self.gestor.dibujar_texto(self.pantalla, "Presiona Q para salir", 28, (255, 255, 255), ANCHO//2, ALTO//2 + 90, centro=True)
    
    def reiniciar_juego(self):
        self.nivel = 1
        self.puntuacion = 0
        self.crear_nivel()
        self.estado = "jugando"
    
    def siguiente_nivel(self):
        self.nivel += 1
        self.puntuacion += PUNTUACION_POR_NIVEL * self.nivel
        self.crear_nivel()
        self.estado = "jugando"
        self.efecto_tiempo = 30
    
    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_p and self.estado == "jugando":
                        self.pausa = not self.pausa
                    if event.key == pygame.K_r:
                        if self.estado == "game_over":
                            self.reiniciar_juego()
                        elif self.estado == "victoria":
                            self.siguiente_nivel()
                    if event.key == pygame.K_ESCAPE:
                        self.estado = "menu"
                if event.type == pygame.MOUSEBUTTONDOWN and self.estado == "menu":
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    start_rect = pygame.Rect(ANCHO//2 - 100, 400, 200, 50)
                    exit_rect = pygame.Rect(ANCHO//2 - 100, 470, 200, 50)
                    if start_rect.collidepoint(mouse_x, mouse_y):
                        self.reiniciar_juego()
                        self.estado = "jugando"
                    elif exit_rect.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        sys.exit()
            
            self.actualizar_particulas()
            
            if self.estado == "menu":
                self.pantalla.fill((0, 0, 0))
                start_rect, exit_rect = self.dibujar_menu()
                pygame.display.flip()
                continue
            elif self.estado == "game_over":
                self.dibujar_game_over()
                pygame.display.flip()
                continue
            elif self.estado == "victoria":
                self.dibujar_victoria()
                pygame.display.flip()
                if self.efecto_tiempo > 0:
                    self.efecto_tiempo -= 1
                continue
            elif self.estado == "jugando" and not self.pausa:
                self.mario.update(self.plataformas, self.escaleras)
                for moneda in self.monedas:
                    moneda.update()
                self.pauline.update()
                
                distancia = abs(self.mario.rect.x - self.donkey_kong.rect.x)
                self.donkey_kong.set_mario_cerca(distancia < 200)
                self.donkey_kong.update(self.plataformas)
                
                # En el método run(), dentro del loop de juego:
                tiempo_espera = self.donkey_kong.get_tiempo_barril()
                if self.donkey_kong.tiempo_barril > tiempo_espera:
                    # Lanzar barril en la dirección que mira Donkey Kong
                    barril = self.donkey_kong.lanzar_barril()
                    self.barriles.append(barril)
                    self.donkey_kong.tiempo_barril = 0
                
                for barril in self.barriles[:]:
                    barril.update(self.plataformas, self.escaleras)
                    if barril.rect.y > ALTO:
                        self.barriles.remove(barril)
                
                for moneda in self.monedas[:]:
                    if self.mario.rect.colliderect(moneda.rect):
                        self.puntuacion += moneda.valor
                        self.monedas.remove(moneda)
                        self.gestor.reproducir_sonido('moneda')
                        self.crear_particula(moneda.rect.centerx, moneda.rect.centery, (255, 215, 0))
                
                for martillo in self.martillos[:]:
                    if self.mario.rect.colliderect(martillo.rect):
                        self.mario.tiene_martillo = True
                        self.mario.tiempo_martillo = TIEMPO_MARTILLO
                        self.martillos.remove(martillo)
                        self.gestor.reproducir_sonido('martillo')
                        self.crear_particula(martillo.rect.centerx, martillo.rect.centery, (150, 150, 150))
                
                for barril in self.barriles[:]:
                    if self.mario.rect.colliderect(barril.rect):
                        if self.mario.tiene_martillo:
                            self.puntuacion += PUNTUACION_POR_BARRIL_ROTO
                            self.barriles.remove(barril)
                            self.crear_particula(barril.rect.centerx, barril.rect.centery, (139, 69, 19))
                        else:
                            if self.mario.golpear():
                                self.crear_particula(self.mario.rect.centerx, self.mario.rect.centery, (255, 0, 0))
                                if self.mario.vidas <= 0:
                                    self.estado = "game_over"
                                else:
                                    self.mario.respawn(100, ALTO - 65)
                            self.barriles.remove(barril)
                
                if (self.mario.rect.colliderect(self.donkey_kong.rect) or 
                    self.mario.rect.colliderect(self.pauline.rect)):
                    self.estado = "victoria"
                    self.gestor.reproducir_sonido('victoria')
                    for _ in range(50):
                        self.crear_particula(random.randint(0, ANCHO), random.randint(0, ALTO), (255, 215, 0))
            
            self.dibujar()
            pygame.display.flip()

if __name__ == "__main__":
    print(f"""
    ╔══════════════════════════════════════╗
    ║      PRESTALABS-PLAY v{VERSION}       ║
    ║         DONKEY KONG ARCADE           ║
    ╠══════════════════════════════════════╣
    ║  ¡Rescata a Pauline de Donkey Kong!  ║
    ╚══════════════════════════════════════╝
    """)
    juego = PrestaLabsPlay()
    juego.run()