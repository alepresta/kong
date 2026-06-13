"""
PRESTALABS-PLAY - GESTOR DE GRÁFICOS
"""
import pygame
import os
from constantes import IMAGENES, COLORES, TAMANO_MARIO, TAMANO_BARRIL, TAMANO_MONEDA, TAMANO_MARTILLO, TAMANO_DONKEY, TAMANO_PAULINE, ANCHO, ALTO, NOMBRE_JUEGO
from sonidos import GeneradorSonidos

class GestorGraficos:
    def __init__(self):
        self.imagenes = {}
        self.cargar_imagenes()
        self.generador_sonidos = GeneradorSonidos()
        self.volumen = 0.5
    
    def cargar_imagenes(self):
        print("\n=== CARGANDO IMÁGENES ===")
        for nombre, ruta in IMAGENES.items():
            try:
                if os.path.exists(ruta):
                    img = pygame.image.load(ruta)
                    self.imagenes[nombre] = img
                    print(f"  ✓ {nombre}")
                else:
                    print(f"  - {nombre} (usando color sólido)")
                    self.imagenes[nombre] = None
            except Exception as e:
                print(f"  - {nombre} (error)")
                self.imagenes[nombre] = None
        print("========================\n")
    
    def get_imagen(self, nombre, escala=None):
        img = self.imagenes.get(nombre)
        if img and escala:
            return pygame.transform.scale(img, escala)
        return img
    
    def dibujar_texto(self, pantalla, texto, tamaño, color, x, y, centro=False):
        fuente = pygame.font.SysFont("comicsansms", tamaño)
        superficie = fuente.render(texto, True, color)
        if centro:
            x = x - superficie.get_width() // 2
        pantalla.blit(superficie, (x, y))
        return superficie.get_width()
    
    def dibujar_boton(self, pantalla, x, y, texto, ancho, alto, activo=False):
        color_fondo = COLORES['verde'] if activo else COLORES['azul']
        pygame.draw.rect(pantalla, color_fondo, (x, y, ancho, alto))
        pygame.draw.rect(pantalla, COLORES['blanco'], (x, y, ancho, alto), 2)
        self.dibujar_texto(pantalla, texto, 24, COLORES['blanco'], x + ancho//2, y + alto//2 - 10, centro=True)
    
    def dibujar_mario(self, pantalla, x, y, direccion, tiene_martillo, invencible, esta_saltando=False):
        if invencible > 0 and (invencible // 5) % 2 == 0:
            return
        
        if self.imagenes.get('mario_right') is None:
            color = COLORES['rojo']
            pygame.draw.rect(pantalla, color, (x, y, TAMANO_MARIO[0], TAMANO_MARIO[1]))
            if direccion == 1:
                pygame.draw.circle(pantalla, COLORES['blanco'], (x + 18, y + 6), 3)
                pygame.draw.circle(pantalla, COLORES['negro'], (x + 18, y + 6), 1)
            else:
                pygame.draw.circle(pantalla, COLORES['blanco'], (x + 6, y + 6), 3)
                pygame.draw.circle(pantalla, COLORES['negro'], (x + 6, y + 6), 1)
            if tiene_martillo:
                if direccion == 1:
                    pygame.draw.rect(pantalla, (150, 150, 150), (x + 20, y + 8, 8, 8))
                else:
                    pygame.draw.rect(pantalla, (150, 150, 150), (x - 4, y + 8, 8, 8))
            return
        
        if direccion == 1:
            img = self.get_imagen('mario_right', TAMANO_MARIO)
        else:
            img = self.get_imagen('mario_left', TAMANO_MARIO)
        if img:
            pantalla.blit(img, (x, y))
        
        if tiene_martillo:
            martillo_img = self.get_imagen('martillo', TAMANO_MARTILLO)
            if martillo_img:
                if direccion == 1:
                    pantalla.blit(martillo_img, (x + TAMANO_MARIO[0] - 5, y + 8))
                else:
                    pantalla.blit(martillo_img, (x - 12, y + 8))
    
    def dibujar_plataforma(self, pantalla, x, y, ancho):
        pygame.draw.rect(pantalla, (101, 67, 33), (x, y, ancho, 25))
        pygame.draw.rect(pantalla, (255, 215, 0), (x, y, ancho, 3))
        for i in range(0, ancho, 40):
            pygame.draw.rect(pantalla, (139, 69, 19), (x + i, y + 5, 20, 15))
        pygame.draw.rect(pantalla, (50, 30, 20), (x, y + 22, ancho, 3))
    
    def dibujar_escalera(self, pantalla, x, y, alto):
        pygame.draw.rect(pantalla, COLORES['marrón_claro'], (x, y, 12, alto))
        for i in range(0, alto, 12):
            pygame.draw.rect(pantalla, COLORES['marrón'], (x, y + i, 12, 3))
    
    def dibujar_moneda(self, pantalla, x, y, frame):
        pygame.draw.circle(pantalla, COLORES['oro'], (x + 7, y + 7), 7)
        pygame.draw.circle(pantalla, COLORES['amarillo'], (x + 7, y + 7), 5)
    
    def dibujar_barril(self, pantalla, x, y):
        pygame.draw.rect(pantalla, COLORES['marrón'], (x, y, TAMANO_BARRIL[0], TAMANO_BARRIL[1]))
        pygame.draw.rect(pantalla, COLORES['negro'], (x, y, TAMANO_BARRIL[0], TAMANO_BARRIL[1]), 2)
        pygame.draw.rect(pantalla, COLORES['gris'], (x + 2, y + 5, TAMANO_BARRIL[0] - 4, TAMANO_BARRIL[1] - 6))
    
    def dibujar_fondo(self, pantalla):
        for i in range(ALTO):
            color = (135 - i // 10, 206 - i // 15, 235 - i // 20)
            if color[0] < 0:
                color = (0, color[1], color[2])
            pygame.draw.line(pantalla, color, (0, i), (ANCHO, i))
        pygame.draw.ellipse(pantalla, COLORES['blanco'], (100, 50, 100, 50))
        pygame.draw.ellipse(pantalla, COLORES['blanco'], (700, 80, 120, 60))
        pygame.draw.ellipse(pantalla, COLORES['blanco'], (400, 30, 80, 40))
        pygame.draw.ellipse(pantalla, COLORES['blanco'], (850, 40, 90, 45))
        pygame.draw.circle(pantalla, COLORES['amarillo'], (750, 60), 35)
    
    def dibujar_corazon(self, pantalla, x, y):
        pygame.draw.polygon(pantalla, COLORES['rojo'], 
            [(x, y), (x - 8, y - 5), (x - 8, y - 12), (x, y - 16),
             (x + 8, y - 12), (x + 8, y - 5), (x, y)])
    
    def dibujar_pauline(self, pantalla, x, y):
        pygame.draw.rect(pantalla, COLORES['amarillo'], (x, y, TAMANO_PAULINE[0], TAMANO_PAULINE[1]))
        pygame.draw.rect(pantalla, COLORES['rojo'], (x, y, TAMANO_PAULINE[0], 8))
    
    def reproducir_sonido(self, nombre):
        return self.generador_sonidos.reproducir(nombre)
    
    def dibujar_menu(self, pantalla, puntuacion=None):
        self.dibujar_fondo(pantalla)
        self.dibujar_texto(pantalla, NOMBRE_JUEGO, 60, COLORES['rojo'], ANCHO//2, 80, centro=True)
        self.dibujar_texto(pantalla, "DONKEY KONG ARCADE", 30, COLORES['amarillo'], ANCHO//2, 140, centro=True)
        if puntuacion is not None:
            self.dibujar_texto(pantalla, f"SCORE: {puntuacion}", 36, COLORES['oro'], ANCHO//2, 250, centro=True)
        marco = pygame.Rect(ANCHO//2 - 250, 300, 500, 280)
        pygame.draw.rect(pantalla, (0, 0, 0, 128), marco, 3)
        self.dibujar_texto(pantalla, "INSTRUCCIONES:", 24, COLORES['amarillo'], ANCHO//2, 340, centro=True)
        self.dibujar_texto(pantalla, "A / D  o  ← / →  : Moverse", 20, COLORES['blanco'], ANCHO//2, 380, centro=True)
        self.dibujar_texto(pantalla, "W / ↑ : Subir escalera", 20, COLORES['blanco'], ANCHO//2, 410, centro=True)
        self.dibujar_texto(pantalla, "S / ↓ : Bajar escalera", 20, COLORES['blanco'], ANCHO//2, 440, centro=True)
        self.dibujar_texto(pantalla, "ESPACIO : Saltar", 20, COLORES['blanco'], ANCHO//2, 470, centro=True)
        self.dibujar_texto(pantalla, "P : Pausa  |  Q : Salir", 20, COLORES['blanco'], ANCHO//2, 500, centro=True)
        self.dibujar_texto(pantalla, "R : Reiniciar", 20, COLORES['blanco'], ANCHO//2, 530, centro=True)