"""
KONG ARGENTINO - HinchaConBengala
"""
import math
import random
import pygame
from constantes import COLORES
from .base_hincha_extra import _BaseHinchaExtra

class HinchaConBengala(_BaseHinchaExtra):
    nombre_hincha = "Hincha Con Bengala"
    etiqueta_puntos = "🔥 +35 (Bengala)"
    puntos_barril = 35

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = 34
        self.rect.height = 41
        self.color_remera = (70, 130, 170)
        self.color_franja = COLORES['blanco']
        self.color_pantalon = (35, 35, 55)
        
        # Máquina de estados
        self._estado = 'quieto'  # quieto, caminando
        self._tiempo_estado = 0
        self._arrodillado = False
        self._bengala_viajando = False
        self._bengala_pos_x = 0
        self._bengala_pos_y = 0
        self._bengala_angulo = 0  # Rotación de la bengala
        
        self.textos_canto = [
            "Bengala y carnaval",
            "Argentina nomas",
            "Dale campeon",
        ]

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        
        # Contador del ciclo: 10 seg quieto + 25 seg caminando = 35 seg total
        # A 30fps: 300 + 750 = 1050 frames por ciclo
        ciclo_tiempo = self.anim_frame % 1050
        
        # Primeros 300 frames (10 segundos): quieto y lanza bengala
        if ciclo_tiempo < 300:
            self._estado = 'quieto'
            self._arrodillado = True
            self.vel_x = 0
            self.gritando = True
            self.tiempo_texto = 300
            self.texto_grito = "DALE BENGALA"
            
            # Lanza al final de los 10 segundos
            if ciclo_tiempo == 290:
                self._bengala_viajando = True
                self._bengala_pos_x = self.rect.centerx + 4
                self._bengala_pos_y = self.rect.top + 6
                if hasattr(self.gestor, 'iniciar_flash'):
                    self.gestor.iniciar_flash((255, 150, 0), 8)
                if hasattr(self.gestor, 'iniciar_shake'):
                    self.gestor.iniciar_shake(12, 3)
        
        # Siguientes 750 frames (25 segundos): caminando normalmente
        else:
            self._estado = 'caminando'
            self._arrodillado = False
            self.gritando = False
            self._bengala_viajando = False
        
        # Movimiento de la bengala cuando viaja
        if self._bengala_viajando:
            self._bengala_pos_x += 4
            self._bengala_pos_y -= 5
            self._bengala_angulo += 45  # Girar 45 grados por frame (cañita boladora)
            if self._bengala_pos_y < self.rect.top - 120:
                # Explosión final en el aire
                self._bengala_viajando = False
                if self.gestor.sistema_particulas:
                    ox = int(self._bengala_pos_x)
                    oy = int(self._bengala_pos_y)
                    # Explosión masiva
                    for _ in range(20):
                        ang = random.uniform(0, math.pi * 2)
                        dist = random.uniform(0, 40)
                        px = ox + math.cos(ang) * dist
                        py = oy + math.sin(ang) * dist
                        self.gestor.sistema_particulas.emitir(
                            int(px),
                            int(py),
                            random.choice([COLORES['naranja'], COLORES['rojo'], COLORES['amarillo'], (255, 200, 50)]),
                            5,
                            'fuego_artificial',
                        )
                    # Brillo de explosión
                    for _ in range(10):
                        self.gestor.sistema_particulas.emitir(
                            ox + random.randint(-20, 20),
                            oy + random.randint(-20, 20),
                            COLORES['gris'],
                            6,
                            'estrella',
                        )
        
        # Partículas de la bengala
        if self.gestor.sistema_particulas:
            if self._bengala_viajando:
                ox = int(self._bengala_pos_x)
                oy = int(self._bengala_pos_y)
                for _ in range(8):
                    self.gestor.sistema_particulas.emitir(
                        ox + random.randint(-6, 6),
                        oy + random.randint(-6, 6),
                        random.choice([COLORES['naranja'], COLORES['rojo'], COLORES['amarillo']]),
                        3,
                        'fuego_artificial',
                    )
                if self.anim_frame % 2 == 0:
                    self.gestor.sistema_particulas.emitir(
                        ox + random.randint(-8, 8),
                        oy + random.randint(-8, 8),
                        random.choice([COLORES['gris'], COLORES['blanco']]),
                        4,
                        'estrella',
                    )
            elif self._estado == 'quieto':
                # Partículas suaves mientras está quieto preparando
                ox = self.rect.centerx + 16
                oy = self.rect.top + 8
                if self.anim_frame % 8 == 0:
                    self.gestor.sistema_particulas.emitir(
                        ox + random.randint(-3, 3),
                        oy + random.randint(-3, 3),
                        COLORES['naranja'],
                        2,
                        'chispa',
                    )

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y + self.offset_y

        # Primero dibujamos el sprite base para conservar su cara original.
        super().dibujar(pantalla)

        if self._arrodillado:
            self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 28, 8)
            # Cuerpo arrodillado por encima del sprite base
            pygame.draw.rect(pantalla, (117, 190, 218), (x + 3, y + 16, 28, 20), border_radius=3)
            for i in range(2, 30, 8):
                pygame.draw.rect(pantalla, COLORES['blanco'], (x + i, y + 16, 4, 20))
            # Pierna de apoyo (levantada, rodilla arriba)
            pygame.draw.rect(pantalla, self.color_pantalon, (x + 8, y + 24, 6, 12), border_radius=2)
            pygame.draw.rect(pantalla, (40, 40, 40), (x + 7, y + 35, 8, 3), border_radius=1)
            # Pierna apoyada en el piso
            pygame.draw.rect(pantalla, self.color_pantalon, (x + 18, y + 32, 6, 5), border_radius=2)
            pygame.draw.rect(pantalla, (40, 40, 40), (x + 16, y + 36, 10, 2), border_radius=1)
            # Brazos apuntando a la bengala
            pygame.draw.line(pantalla, (255, 220, 200), (x + 31, y + 22), (x + 38, y + 14), 3)
            pygame.draw.circle(pantalla, (255, 220, 200), (x + 38, y + 14), 3)

        # Cubre solo el pelo superior del sprite base, sin tocar la cara
        pygame.draw.ellipse(pantalla, (255, 220, 200), (x + 5, y + 0, 22, 8))

        glow = pygame.Surface((56, 56), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 120, 0, 90), (28, 28), 24)
        pygame.draw.circle(glow, (255, 200, 120, 60), (28, 28), 16)
        pantalla.blit(glow, (x + 6, y - 30))

        if self._bengala_viajando:
            bx = int(self._bengala_pos_x)
            by = int(self._bengala_pos_y)
            
            # Dibujar cañita boladora girando (cilindro que rota)
            ang_rad = math.radians(self._bengala_angulo)
            
            # Cilindro de la cañita (que rota)
            # Base del cilindro (oscuro)
            p1x = int(bx + math.cos(ang_rad) * 6)
            p1y = int(by + math.sin(ang_rad) * 3)
            p2x = int(bx - math.cos(ang_rad) * 6)
            p2y = int(by - math.sin(ang_rad) * 3)
            pygame.draw.line(pantalla, (150, 30, 10), (p1x, p1y), (p2x, p2y), 5)
            
            # Parte superior brillante
            p3x = int(bx + math.cos(ang_rad + math.pi/2) * 5)
            p3y = int(by + math.sin(ang_rad + math.pi/2) * 5)
            pygame.draw.line(pantalla, (220, 100, 50), (p1x, p1y), (p3x, p3y), 3)
            
            # Punta de fuego en la punta
            punta_x = int(bx + math.cos(ang_rad + math.pi/4) * 10)
            punta_y = int(by + math.sin(ang_rad + math.pi/4) * 10)
            pygame.draw.circle(pantalla, (255, 150, 0), (punta_x, punta_y), 5)
            pygame.draw.circle(pantalla, (255, 220, 100), (punta_x, punta_y), 2)
            
            # Estelas de fuego mientras viaja
            for i in range(3):
                estela_x = bx + random.randint(-8, 8)
                estela_y = by + random.randint(-8, 8) + i * 10
                pygame.draw.circle(pantalla, (255, 100 + i*30, 50), (estela_x, estela_y), 3 - i)
            
            # Glow explosivo alrededor
            glow2 = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(glow2, (255, 120, 0, 140), (40, 40), 35)
            pygame.draw.circle(glow2, (255, 180, 80, 90), (40, 40), 20)
            pantalla.blit(glow2, (bx - 40, by - 40))
        else:
            # Bengala en mano (reposo)
            pygame.draw.line(pantalla, (180, 180, 180), (x + 26, y + 18), (x + 31, y + 8), 3)
            pygame.draw.rect(pantalla, (200, 50, 20), (x + 28, y + 4, 5, 10), border_radius=1)
            pygame.draw.circle(pantalla, COLORES['naranja'], (x + 32, y + 7), 6)
            pygame.draw.circle(pantalla, COLORES['amarillo'], (x + 32, y + 7), 3)
            pygame.draw.circle(pantalla, (255, 200, 100), (x + 32, y + 7), 1)
            # Líneas de fuego alrededor
            pygame.draw.line(pantalla, (255, 140, 0), (x + 32, y + 7), (x + 40, y - 2), 2)
            pygame.draw.line(pantalla, (255, 220, 120), (x + 32, y + 7), (x + 41, y + 5), 2)
            pygame.draw.line(pantalla, (255, 70, 0), (x + 32, y + 7), (x + 38, y + 12), 2)


