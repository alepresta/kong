"""
PRESTALABS-PLAY - CONSTANTES DEL JUEGO
"""

VERSION = "1.0.0"
NOMBRE_JUEGO = "PRESTALABS-PLAY"

ANCHO = 1024
ALTO = 768
FPS = 60

VIDAS = 9
VELOCIDAD_JUGADOR = 5
VELOCIDAD_BARRILES = 2
GRAVEDAD = 0.6
SALTO = -12
BARRILES_CADA = 80
TIEMPO_MARTILLO = 180
PUNTUACION_POR_MONEDA = 10
PUNTUACION_POR_NIVEL = 500
PUNTUACION_POR_BARRIL_ROTO = 100

IMAGENES = {
    'mario_still': 'Assets/still.png',
    'mario_right': 'Assets/right.png',
    'mario_right2': 'Assets/right2.png',
    'mario_left': 'Assets/left.png',
    'mario_left2': 'Assets/left2.png',
    'pared': 'Assets/wood_block.png',
    'escalera': 'Assets/ladder.png',
    'moneda1': 'Assets/coin1.png',
    'moneda2': 'Assets/coin2.png',
    'moneda3': 'Assets/coin3.png',
    'moneda4': 'Assets/coin4.png',
    'moneda5': 'Assets/coin5.png',
    'donkey_kong': 'Assets/kong0.png',
    'princesa': 'Assets/princess.png',
    'fondo': 'Assets/background.png',
    'martillo': 'Assets/hammer.png',
    'logo': 'Assets/donkeykongtext.png',
    'start': 'Assets/start.png',
    'start_hover': 'Assets/start1.png',
    'exit': 'Assets/exit.png',
    'exit_hover': 'Assets/exit1.png',
    'restart': 'Assets/restart.png',
    'restart_hover': 'Assets/restart1.png',
}

SONIDOS = {
    'salto': 'Assets/jump.wav',
    'muerte': 'Assets/death.wav',
    'moneda': 'Assets/coin.wav',
    'victoria': 'Assets/levelcomplete.wav',
    'martillo': 'Assets/hammer.wav',
    'ayuda': 'Assets/help.wav',
}

COLORES = {
    'cielo': (135, 206, 235),
    'marrón': (160, 82, 45),
    'marrón_claro': (205, 133, 63),
    'rojo': (220, 50, 50),
    'amarillo': (255, 220, 50),
    'negro': (0, 0, 0),
    'blanco': (255, 255, 255),
    'gris': (150, 150, 150),
    'oro': (255, 215, 0),
    'azul': (50, 100, 200),
    'verde': (50, 200, 50),
}

TAMANO_MARIO = (24, 24)
TAMANO_BARRIL = (18, 18)
TAMANO_MONEDA = (14, 14)
TAMANO_MARTILLO = (16, 16)
TAMANO_DONKEY = (45, 50)
TAMANO_PAULINE = (22, 28)