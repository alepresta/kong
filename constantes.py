"""
KONG ARGENTINO - CONSTANTES DEL JUEGO v3.2
Creado por Apresta para Prestalabs
"""

VERSION = "3.2.0"
NOMBRE_JUEGO = "KONG ARGENTINO"

ANCHO = 1024
ALTO = 768
FPS = 60

VIDAS = 3
VELOCIDAD_JUGADOR = 6
VELOCIDAD_JUGADOR_ESCALERA = 4
VELOCIDAD_BARRILES = 3
GRAVEDAD = 0.65
SALTO = -14
SALTO_ESCALERA = -10
BARRILES_CADA = 80
TIEMPO_PODER = 300
PUNTUACION_POR_CERVEZA = 10
PUNTUACION_POR_NIVEL = 1000
PUNTUACION_POR_BARRIL_ROTO = 150
MULTIPLICADOR_COMBO_MAX = 5
TIEMPO_COMBO = 120
INVENCIBILIDAD_DESPUES_GOLPE = 120
TIEMPO_RESPAWN = 60
TIEMPO_ATAQUE = 20  # Duración del ataque en frames
DISTANCIA_ATAQUE = 40  # Distancia del hitbox de ataque

# Dificultad por nivel
DIFICULTAD_NIVEL = {
    1: {'vel_barril': 2.0, 'cadencia': 120, 'max_barriles': 3,  'vel_kong': 0.8},
    2: {'vel_barril': 2.5, 'cadencia': 100, 'max_barriles': 4,  'vel_kong': 1.0},
    3: {'vel_barril': 3.0, 'cadencia': 85,  'max_barriles': 5,  'vel_kong': 1.3},
    4: {'vel_barril': 3.5, 'cadencia': 70,  'max_barriles': 6,  'vel_kong': 1.6},
    5: {'vel_barril': 4.0, 'cadencia': 55,  'max_barriles': 7,  'vel_kong': 2.0},
}

# Colores Argentinos
COLORES = {
    'cielo':         (117, 190, 218),
    'blanco':        (255, 255, 255),
    'negro':         (0, 0, 0),
    'oro':           (255, 215, 0),
    'marron':        (101, 67, 33),
    'verde':         (76, 153, 0),
    'verde_oscuro':  (30, 100, 0),
    'azul':          (50, 100, 200),
    'gris':          (150, 150, 150),
    'gris_oscuro':   (60, 60, 60),
    'celeste':       (117, 190, 218),
    'celeste_oscuro':(70, 140, 180),
    'amarillo':      (255, 220, 50),
    'rojo':          (220, 50, 50),
    'rojo_oscuro':   (150, 20, 20),
    'marron_claro':  (205, 133, 63),
    'naranja':       (255, 140, 0),
    'violeta':       (150, 50, 200),
    'rosa':          (255, 150, 180),
    'transparente':  (0, 0, 0, 0),
}

# Tamaños
TAMANO_JUGADOR  = (32, 38)
TAMANO_BARRIL   = (32, 32)
TAMANO_CERVEZA  = (20, 20)
TAMANO_PODER    = (24, 24)
TAMANO_KONG     = (80, 90)
TAMANO_PRINCESA = (32, 38)
TAMANO_BORRACHO = (32, 32)