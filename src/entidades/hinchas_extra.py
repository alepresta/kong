"""
KONG ARGENTINO - HINCHAS EXTRA
Variantes adicionales de hinchada para completar el roster del diseno.
"""

import math
import random
import pygame

from constantes import COLORES
from .objetos import HinchaBorrachito


class _BaseHinchaExtra(HinchaBorrachito):
    nombre_hincha = "Hincha"
    etiqueta_puntos = "🍺 +30 (Hincha)"
    puntos_barril = 30

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = 32
        self.rect.height = 40
        self.color_remera = COLORES['celeste']
        self.color_franja = COLORES['blanco']
        self.color_pantalon = (30, 60, 140)
        self.color_piel = (255, 220, 200)
        self.textos_canto = [
            "Vamo' Argentina",
            "Messi, Messi",
            "La copa esta en casa",
        ]

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        if not self.gritando and self.anim_frame % 240 == 0 and random.random() < 0.35:
            self.gritando = True
            self.tiempo_texto = 50
            self.texto_grito = random.choice(self.textos_canto)

    def recibir_golpe(self):
        return super().recibir_golpe()

    def _dibujar_cuerpo_base(self, pantalla, x, y, remera=None, franja=None, pantalon=None, piel=None, radio=8):
        remera = remera or self.color_remera
        franja = franja or self.color_franja
        pantalon = pantalon or self.color_pantalon
        piel = piel or self.color_piel
        paso = int(math.sin(self.anim_frame * 0.25) * 2)

        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 24, 8)
        pygame.draw.rect(pantalla, remera, (x + 2, y + 12, 16, 18), border_radius=3)
        pygame.draw.rect(pantalla, COLORES['blanco'], (x + 2, y + 16, 16, 4))
        pygame.draw.rect(pantalla, franja, (x + 2, y + 20, 16, 3))
        pygame.draw.circle(pantalla, piel, (x + 10, y + 8), radio)
        pygame.draw.rect(pantalla, pantalon, (x + 4 + paso, y + 30, 4, 8))
        pygame.draw.rect(pantalla, pantalon, (x + 12 - paso, y + 30, 4, 8))

        self._dibujar_rostro(pantalla, x, y)
        self._dibujar_bandera_argentina(pantalla, x, y)

        if self.gritando and self.tiempo_texto > 0:
            self.gestor.dibujar_texto(
                pantalla,
                self.texto_grito,
                13,
                COLORES['amarillo'],
                self.rect.centerx,
                y - 22,
                centro=True,
            )

    def _dibujar_rostro(self, pantalla, x, y):
        pygame.draw.circle(pantalla, (35, 35, 55), (x + 7, y + 8), 1)
        pygame.draw.circle(pantalla, (35, 35, 55), (x + 13, y + 8), 1)
        pygame.draw.line(pantalla, (60, 35, 25), (x + 5, y + 6), (x + 8, y + 5), 1)
        pygame.draw.line(pantalla, (60, 35, 25), (x + 12, y + 5), (x + 15, y + 6), 1)
        pygame.draw.arc(pantalla, (160, 60, 60), (x + 7, y + 10, 6, 4), 0, math.pi, 1)

    def _dibujar_bandera_argentina(self, pantalla, x, y, lado=1):
        asta_x = x + (19 if lado >= 0 else 1)
        asta_y = y + 8
        pygame.draw.line(pantalla, (170, 140, 90), (asta_x, asta_y), (asta_x, asta_y + 15), 2)

        flag_w = 10
        dir_mult = 1 if lado >= 0 else -1
        bx = asta_x + dir_mult
        by = asta_y + 1
        if lado >= 0:
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx, by, flag_w, 2))
            pygame.draw.rect(pantalla, COLORES['blanco'], (bx, by + 2, flag_w, 2))
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx, by + 4, flag_w, 2))
            pygame.draw.circle(pantalla, COLORES['amarillo'], (bx + 5, by + 3), 1)
        else:
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx - flag_w, by, flag_w, 2))
            pygame.draw.rect(pantalla, COLORES['blanco'], (bx - flag_w, by + 2, flag_w, 2))
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx - flag_w, by + 4, flag_w, 2))
            pygame.draw.circle(pantalla, COLORES['amarillo'], (bx - 5, by + 3), 1)

    def dibujar(self, pantalla):
        # Mantener el estilo visual del HinchaBorrachito original del juego.
        super().dibujar(pantalla)
        x, y = self.rect.x, self.rect.y + self.offset_y
        self._dibujar_bandera_argentina(pantalla, x, y, lado=self.direccion)


class HinchaBorrachin(_BaseHinchaExtra):
    nombre_hincha = "Hincha Borrachin"
    etiqueta_puntos = "🍻 +35 (Borrachin)"
    puntos_barril = 35

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = 34
        self.rect.height = 42
        self.nivel_borrachera = random.randint(7, 9)
        self.color_remera = (190, 80, 70)
        self.color_franja = (250, 190, 120)
        self.color_pantalon = (65, 35, 20)
        self.textos_canto = [
            "No veo nada, pero vamos",
            "Messi te amo",
            "La copa, la copa",
        ]

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        if self.anim_frame % 50 == 0 and random.random() < 0.6:
            self.vel_x += random.choice([-1.2, -0.8, 0.8, 1.2])
            self.vel_x = max(-3.0, min(3.0, self.vel_x))

    def dibujar(self, pantalla):
        super().dibujar(pantalla)
        x, y = self.rect.x, self.rect.y + self.offset_y
        # Botella en mano y cara colorada.
        pygame.draw.rect(pantalla, (120, 70, 30), (x + 26, y + 20, 6, 11), border_radius=2)
        pygame.draw.rect(pantalla, (240, 200, 120), (x + 27, y + 18, 4, 3), border_radius=1)
        pygame.draw.circle(pantalla, (220, 90, 90), (x + 11, y + 12), 2)
        pygame.draw.circle(pantalla, (220, 90, 90), (x + 21, y + 12), 2)


class HinchaRandom(_BaseHinchaExtra):
    nombre_hincha = "Hincha Random"
    etiqueta_puntos = "🎲 +25 (Random)"
    puntos_barril = 25

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = random.choice([30, 32, 34])
        self.rect.height = random.choice([38, 40, 42])
        self.color_remera = random.choice([
            COLORES['celeste'],
            COLORES['azul'],
            COLORES['blanco'],
        ])
        self.color_pantalon = random.choice([
            (30, 60, 140),
            (40, 40, 40),
            (70, 30, 20),
        ])
        self.accesorio = random.choice(["gorra", "vincha", "bigote"])

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        if self.anim_frame % 90 == 0 and random.random() < 0.4:
            self.direccion *= -1

    def dibujar(self, pantalla):
        super().dibujar(pantalla)
        x, y = self.rect.x, self.rect.y + self.offset_y
        # Variar remera sobre el sprite base para mantener lenguaje visual común.
        pygame.draw.rect(pantalla, self.color_remera, (x + 2, y + 14, 28, 6), border_radius=2)
        if self.accesorio == "gorra":
            pygame.draw.rect(pantalla, (40, 40, 40), (x + 8, y - 3, 16, 4), border_radius=2)
            pygame.draw.rect(pantalla, (40, 40, 40), (x + 20, y, 7, 2), border_radius=1)
        elif self.accesorio == "vincha":
            pygame.draw.rect(pantalla, (255, 215, 0), (x + 8, y + 6, 16, 2))
        else:
            pygame.draw.rect(pantalla, (60, 40, 25), (x + 14, y + 16, 6, 2), border_radius=1)


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

        if self._arrodillado:
            self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 28, 8)
            # Cuerpo arrodillado
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
        else:
            super().dibujar(pantalla)

        # Cabeza pelada (sin pelo)

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


class HinchaGemelos(_BaseHinchaExtra):
    nombre_hincha = "Hincha Gemelos"
    etiqueta_puntos = "👫 +40 (Gemelos)"
    puntos_barril = 40

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = 20
        self.rect.height = 40
        self.rect_derecho = pygame.Rect(x + 20, y, 20, self.rect.height)
        self._offset_gemelo = 20
        self.textos_canto = [
            "Cantamos los dos",
            "Dale dale dale",
            "Messi Messi",
        ]

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        bamboleo = int(math.sin(self.anim_frame * 0.22) * 2)
        self.rect_derecho.x = self.rect.x + self._offset_gemelo + bamboleo
        self.rect_derecho.y = self.rect.y

    def iter_rects(self):
        return [self.rect, self.rect_derecho]

    def beber_barril(self):
        super().beber_barril()
        self.nivel_borrachera = min(10, self.nivel_borrachera + 1)

    def recibir_golpe(self):
        self.estado = "golpeado"
        self.tiempo_estado = 75
        self.vel_x = random.choice([-3, -2, 2, 3])
        self.nivel_borrachera = max(0, self.nivel_borrachera - 1)
        self.gritando = True
        self.tiempo_texto = 35
        self.texto_grito = "¡AU, LOS GEMELOS!"
        return False

    def dibujar(self, pantalla):
        x, y = self.rect.x, self.rect.y + self.offset_y
        x2, y2 = self.rect_derecho.x, self.rect_derecho.y + self.offset_y
        self.gestor.dibujar_sombra(pantalla, self.rect.centerx, self.rect.bottom, 24, 8)
        self.gestor.dibujar_sombra(pantalla, self.rect_derecho.centerx, self.rect_derecho.bottom, 24, 8)
        for bx, by in ((x, y), (x2, y2)):
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx + 2, by + 12, 16, 18), border_radius=3)
            pygame.draw.rect(pantalla, COLORES['blanco'], (bx + 2, by + 16, 16, 4))
            pygame.draw.rect(pantalla, COLORES['celeste'], (bx + 2, by + 20, 16, 3))
            pygame.draw.circle(pantalla, (255, 220, 200), (bx + 10, by + 8), 8)
            pygame.draw.rect(pantalla, (30, 60, 140), (bx + 4, by + 30, 4, 8))
            pygame.draw.rect(pantalla, (30, 60, 140), (bx + 12, by + 30, 4, 8))
            pygame.draw.circle(pantalla, (35, 35, 55), (bx + 7, by + 8), 1)
            pygame.draw.circle(pantalla, (35, 35, 55), (bx + 13, by + 8), 1)
            pygame.draw.arc(pantalla, (160, 60, 60), (bx + 7, by + 10, 6, 4), 0, math.pi, 1)
        self._dibujar_bandera_argentina(pantalla, x2, y2, lado=1)
        if self.gritando and self.tiempo_texto > 0:
            cx = (self.rect.centerx + self.rect_derecho.centerx) // 2
            cy = min(y, y2) - 24
            self.gestor.dibujar_texto(pantalla, self.texto_grito, 14, COLORES['amarillo'], cx, cy, centro=True)


class HinchaAbuela(_BaseHinchaExtra):
    nombre_hincha = "Hincha Abuela"
    etiqueta_puntos = "🥘 +30 (Abuela)"
    puntos_barril = 30

    def __init__(self, x, y, gestor):
        super().__init__(x, y, gestor)
        self.rect.width = 34
        self.rect.height = 46
        self.color_remera = (145, 95, 165)
        self.color_franja = (215, 190, 230)
        self.color_pantalon = (70, 60, 90)
        self.color_piel = (245, 215, 190)
        self.textos_canto = [
            "Traje la cacerola",
            "Vamos mis nietos",
            "La copa se queda",
        ]

    def update(self, plataformas=None, escaleras=None, barriles=None):
        super().update(plataformas, escaleras, barriles)
        if self.gestor.sistema_particulas and self.anim_frame % 12 == 0 and random.random() < 0.4:
            self.gestor.sistema_particulas.emitir(
                self.rect.centerx + random.randint(-6, 6),
                self.rect.top,
                COLORES['blanco'],
                1,
                'estrella',
            )

    def dibujar(self, pantalla):
        super().dibujar(pantalla)
        x, y = self.rect.x, self.rect.y + self.offset_y

        # Convertir sprite base en abuela: pelo canoso, chal, falda, cacerola.
        pygame.draw.rect(pantalla, (180, 140, 200), (x + 2, y + 12, 28, 7), border_radius=3)
        pygame.draw.rect(pantalla, (120, 80, 145), (x + 5, y + 26, 22, 16), border_radius=4)
        pygame.draw.circle(pantalla, (215, 215, 215), (x + 16, y + 2), 7)
        pygame.draw.circle(pantalla, (180, 180, 180), (x + 23, y + 5), 4)
        pygame.draw.circle(pantalla, COLORES['gris'], (x + 4, y + 24), 6)
        pygame.draw.circle(pantalla, (200, 200, 200), (x + 4, y + 24), 3)
        pygame.draw.line(pantalla, COLORES['marron_claro'], (x + 11, y + 20), (x + 18, y + 9), 2)
        pygame.draw.circle(pantalla, COLORES['marron_claro'], (x + 18, y + 9), 2)
        pygame.draw.line(pantalla, (130, 90, 55), (x + 28, y + 14), (x + 28, y + 37), 2)
        pygame.draw.arc(pantalla, (130, 90, 55), (x + 25, y + 11, 6, 6), math.pi / 2, math.pi * 1.6, 2)
        if self.anim_frame % 20 < 10:
            pygame.draw.circle(pantalla, COLORES['amarillo'], (x + 4, y + 24), 2)
