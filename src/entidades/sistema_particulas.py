"""
KONG ARGENTINO - SISTEMA DE PARTÍCULAS v2.0
"""
import pygame
import random
import math
from constantes import COLORES, MAX_PARTICULAS

class SistemaParticulas:
    def __init__(self, gestor):
        self.particulas = []
        self.gestor = gestor

    def emitir(self, x, y, color, n=8, fuente='explosion'):
        espacio = MAX_PARTICULAS - len(self.particulas)
        n = min(n, max(0, espacio))
        if n <= 0:
            return

        for _ in range(n):
            p = {'x': float(x), 'y': float(y), 'color': color,
                 'trail': [], 'forma': 'circulo'}

            if fuente == 'explosion':
                p.update(vx=random.uniform(-4.5, 4.5),
                         vy=random.uniform(-7, -1),
                         vida=random.randint(22, 44),
                         tam=random.randint(2, 6))
            elif fuente == 'combo':
                ang = random.uniform(0, math.pi * 2)
                spd = random.uniform(3, 7)
                p.update(vx=math.cos(ang)*spd, vy=math.sin(ang)*spd - 3,
                         vida=random.randint(28, 55), tam=random.randint(3, 7))
            elif fuente == 'humo':
                p.update(vx=random.uniform(-1.5, 1.5), vy=random.uniform(-2.5, -0.5),
                         vida=random.randint(15, 30), tam=random.randint(4, 10))
            elif fuente == 'estrella':
                ang = random.uniform(0, math.pi * 2)
                spd = random.uniform(1.5, 5.5)
                p.update(vx=math.cos(ang)*spd, vy=math.sin(ang)*spd - 2,
                         vida=random.randint(30, 65), tam=random.randint(2, 5),
                         forma='estrella')
            elif fuente == 'polvo':
                p.update(vx=random.uniform(-2, 2), vy=random.uniform(-3, -0.5),
                         vida=random.randint(10, 22), tam=random.randint(2, 5))
            elif fuente == 'golpe':
                ang = random.uniform(0, math.pi * 2)
                spd = random.uniform(1.5, 4)
                p.update(vx=math.cos(ang)*spd, vy=math.sin(ang)*spd - 1.5,
                         vida=random.randint(12, 22), tam=random.randint(2, 4))
            elif fuente == 'ataque':
                ang = random.uniform(-math.pi/3, math.pi/3)
                spd = random.uniform(3, 7)
                p.update(vx=math.cos(ang)*spd, vy=math.sin(ang)*spd - 2,
                         vida=random.randint(15, 28), tam=random.randint(3, 6))
            elif fuente == 'chispa':
                ang = random.uniform(0, math.pi * 2)
                spd = random.uniform(2, 8)
                p.update(vx=math.cos(ang)*spd, vy=math.sin(ang)*spd - 3,
                         vida=random.randint(10, 20), tam=random.randint(1, 3),
                         forma='linea')
            elif fuente == 'fuego_artificial':
                ang = random.uniform(0, math.pi * 2)
                spd = random.uniform(1, 6)
                p.update(vx=math.cos(ang)*spd, vy=math.sin(ang)*spd,
                         vida=random.randint(35, 70), tam=random.randint(2, 5),
                         forma='estrella')
            else:
                p.update(vx=random.uniform(-2, 2), vy=random.uniform(-3, -1),
                         vida=20, tam=3)

            p['vida_max'] = p['vida']
            self.particulas.append(p)

    def actualizar(self):
        for p in self.particulas[:]:
            if p.get('forma') == 'linea':
                p['trail'].append((p['x'], p['y']))
                if len(p['trail']) > 4:
                    p['trail'].pop(0)

            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.18
            p['vx'] *= 0.97
            p['vida'] -= 1
            if p['vida'] <= 0:
                self.particulas.remove(p)

    def dibujar(self, pantalla):
        for p in self.particulas:
            alpha = p['vida'] / p['vida_max']
            tam = max(1, int(p['tam'] * alpha))
            c = p['color']
            col = (int(c[0]*alpha), int(c[1]*alpha), int(c[2]*alpha))
            ix, iy = int(p['x']), int(p['y'])
            forma = p.get('forma', 'circulo')

            if forma == 'linea' and p['trail']:
                for i, (tx, ty) in enumerate(p['trail']):
                    a2 = (i / len(p['trail'])) * alpha * 0.6
                    tc = (int(c[0]*a2), int(c[1]*a2), int(c[2]*a2))
                    if i > 0:
                        t0 = p['trail'][i-1]
                        pygame.draw.line(pantalla, tc, (int(t0[0]), int(t0[1])), (int(tx), int(ty)), 1)
                pygame.draw.circle(pantalla, col, (ix, iy), max(1, tam-1))
            elif forma == 'estrella':
                r = tam
                for ang in [0, math.pi/2, math.pi, 3*math.pi/2]:
                    ex = ix + int(math.cos(ang) * r * 1.5)
                    ey = iy + int(math.sin(ang) * r * 1.5)
                    pygame.draw.line(pantalla, col, (ix, iy), (ex, ey), 1)
                pygame.draw.circle(pantalla, col, (ix, iy), max(1, tam-1))
            else:
                pygame.draw.circle(pantalla, col, (ix, iy), tam)
