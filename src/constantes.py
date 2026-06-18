"""
KONG ARGENTINO - CONSTANTES DEL JUEGO v4.0
Creado por Apresta para Prestalabs
"""

VERSION = "4.0.0"
NOMBRE_JUEGO = "KONG ARGENTINO"

ANCHO = 1024
ALTO = 768
FPS = 60

VIDAS = 3
VELOCIDAD_JUGADOR = 2
VELOCIDAD_JUGADOR_ESCALERA = 2
VELOCIDAD_BARRILES = 2
GRAVEDAD = 0.95
SALTO = -16
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
TIEMPO_ATAQUE = 20
DISTANCIA_ATAQUE = 40

# ─── NUEVAS CONSTANTES v4.0 ──────────────────────────────────────
PUNTUACION_POR_BARRIL_SALTADO = 25   # puntos por saltar un barril
TIEMPO_PARPADEO_INVENCIBLE = 4       # frames entre destellos de invencibilidad
MAX_PARTICULAS = 300                 # límite para no saturar CPU
TIEMPO_FREEZE_PANTALLA = 8           # frames de freeze al recibir golpe fuerte
VELOCIDAD_NUBES = 0.3                # velocidad de movimiento de nubes
TIEMPO_ANIMACION_MUERTE = 90         # frames de animación al morir
SHAKE_DURACION = 18                  # frames de cámara shake
SHAKE_INTENSIDAD = 5
# ─────────────────────────────────────────────────────────────────

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
    # Nuevos v4.0
    'cyan':          (0, 220, 255),
    'magenta':       (220, 0, 220),
    'lima':          (150, 255, 0),
}

# Tamaños
TAMANIO_JUGADOR  = (32, 38)
TAMANIO_BARRIL   = (32, 32)
TAMANIO_CERVEZA  = (20, 20)
TAMANIO_PODER    = (24, 24)
TAMANIO_KONG     = (80, 90)
TAMANIO_PRINCESA = (32, 38)
TAMANIO_BORRACHO = (32, 32)

# Compatibilidad con nombre antiguo (TAMANO sin Ñ)
TAMANO_JUGADOR  = TAMANIO_JUGADOR
TAMANO_BARRIL   = TAMANIO_BARRIL
TAMANO_CERVEZA  = TAMANIO_CERVEZA
TAMANO_PODER    = TAMANIO_PODER
TAMANO_KONG     = TAMANIO_KONG
TAMANO_PRINCESA = TAMANIO_PRINCESA
TAMANO_BORRACHO = TAMANIO_BORRACHO

# ─── TABLA DE HIGH SCORES (persistencia simple) ──────────────────
ARCHIVO_HIGHSCORE = "kong_scores.dat"
