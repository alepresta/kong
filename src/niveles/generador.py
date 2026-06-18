"""
KONG ARGENTINO - GENERADOR DE NIVELES
"""
from constantes import ANCHO, ALTO

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