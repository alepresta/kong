"""
KONG ARGENTINO v4.0 - PUNTO DE ENTRADA
Creado por Apresta para Prestalabs
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from juego.main import KongArgentino

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║          KONG ARGENTINO v4.0 - ¡Edición Mejorada!            ║
    ║                   Creado por Apresta                          ║
    ║                   para PRESTALABS                             ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║   ¡Rescata a la princesa del Kong Cervecero!                  ║
    ║                                                               ║
    ║   CONTROLES:                                                  ║
    ║   A/D o ←/→  : Moverse                                        ║
    ║   W/↑        : Subir escalera / Saltar                        ║
    ║   S/↓        : Bajar escalera                                 ║
    ║   ESPACIO    : Atacar (golpear barriles y hincha)             ║
    ║   P          : Pausar                                         ║
    ║   [ ]        : Bajar / Subir volumen                          ║
    ║   ESC        : Menú                                           ║
    ║                                                               ║
    ║   NUEVO v4.0:                                                 ║
    ║   • High score persistente                                    ║
    ║   • Cámara shake al recibir golpe                             ║
    ║   • Flash de pantalla en eventos críticos                     ║
    ║   • Bonus por saltar barriles (+25)                           ║
    ║   • Nubes animadas, estrellas twinkle                         ║
    ║   • Fuegos artificiales en victoria final                     ║
    ║   • Partículas: chispas, trail, estrellas 4 puntas            ║
    ║   • Control de volumen en tiempo real                         ║
    ║   • Fuentes cacheadas (mejor performance)                     ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    juego = KongArgentino()
    juego.run()
