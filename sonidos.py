"""
PRESTALABS-PLAY - SONIDOS SINTETIZADOS
"""
import pygame
import math
import array

class GeneradorSonidos:
    def __init__(self):
        self.sonidos = {}
        self.frecuencia_muestreo = 22050
        self.volumen = 0.5
        self.generar_todos_los_sonidos()
    
    def crear_sonido(self, samples):
        samples_int = [int(s) for s in samples]
        samples_array = array.array('h', samples_int)
        return pygame.mixer.Sound(buffer=samples_array.tobytes())
    
    def generar_tono_ascendente(self, frecuencia_inicial, frecuencia_final, duracion, volumen=None):
        if volumen is None:
            volumen = self.volumen
        n_muestras = int(self.frecuencia_muestreo * duracion)
        samples = []
        for i in range(n_muestras):
            progreso = i / n_muestras
            frecuencia = frecuencia_inicial + (frecuencia_final - frecuencia_inicial) * progreso
            valor = int(volumen * 32767 * math.sin(2.0 * math.pi * frecuencia * i / self.frecuencia_muestreo))
            samples.append(valor)
        return self.crear_sonido(samples)
    
    def generar_tono_descendente(self, frecuencia_inicial, frecuencia_final, duracion, volumen=None):
        if volumen is None:
            volumen = self.volumen
        n_muestras = int(self.frecuencia_muestreo * duracion)
        samples = []
        for i in range(n_muestras):
            progreso = i / n_muestras
            frecuencia = frecuencia_inicial - (frecuencia_inicial - frecuencia_final) * progreso
            valor = int(volumen * 32767 * math.sin(2.0 * math.pi * frecuencia * i / self.frecuencia_muestreo))
            samples.append(valor)
        return self.crear_sonido(samples)
    
    def generar_salto(self):
        return self.generar_tono_ascendente(400, 900, 0.12, 0.35)
    
    def generar_moneda(self):
        n_muestras = int(self.frecuencia_muestreo * 0.12)
        samples = []
        for i in range(n_muestras):
            decay = 1 - i / n_muestras
            valor = int(0.4 * 32767 * math.sin(2.0 * math.pi * 1200 * i / self.frecuencia_muestreo) * decay)
            samples.append(valor)
        for i in range(n_muestras):
            decay = 1 - i / n_muestras
            valor = int(0.3 * 32767 * math.sin(2.0 * math.pi * 1600 * i / self.frecuencia_muestreo) * decay)
            samples.append(valor)
        return self.crear_sonido(samples)
    
    def generar_muerte(self):
        return self.generar_tono_descendente(500, 150, 0.5, 0.4)
    
    def generar_victoria(self):
        n_muestras = int(self.frecuencia_muestreo * 0.8)
        samples = []
        notas = [523, 659, 784, 523]
        duracion_nota = n_muestras // len(notas)
        for idx, nota in enumerate(notas):
            for i in range(duracion_nota):
                fade = 1.0 if idx > 0 else 0.6
                volumen_actual = 0.35 * fade
                valor = int(volumen_actual * 32767 * math.sin(2.0 * math.pi * nota * (idx * duracion_nota + i) / self.frecuencia_muestreo))
                samples.append(valor)
        return self.crear_sonido(samples)
    
    def generar_martillo(self):
        n_muestras = int(self.frecuencia_muestreo * 0.2)
        samples = []
        for i in range(n_muestras):
            decay = 1 - i / n_muestras
            frecuencia = 600 + 200 * decay
            valor = int(0.4 * decay * 32767 * math.sin(2.0 * math.pi * frecuencia * i / self.frecuencia_muestreo))
            samples.append(valor)
        return self.crear_sonido(samples)
    
    def generar_ayuda(self):
        n_muestras = int(self.frecuencia_muestreo * 0.3)
        samples = []
        for i in range(n_muestras):
            pulsacion = 0.5 + 0.5 * math.sin(2.0 * math.pi * 15 * i / self.frecuencia_muestreo)
            frecuencia = 550 + 30 * math.sin(2.0 * math.pi * 8 * i / self.frecuencia_muestreo)
            valor = int(0.4 * pulsacion * 32767 * math.sin(2.0 * math.pi * frecuencia * i / self.frecuencia_muestreo))
            samples.append(valor)
        return self.crear_sonido(samples)
    
    def generar_todos_los_sonidos(self):
        print("=== GENERANDO SONIDOS SINTETIZADOS ===")
        self.sonidos['salto'] = self.generar_salto()
        print("  ✓ salto")
        self.sonidos['moneda'] = self.generar_moneda()
        print("  ✓ moneda")
        self.sonidos['muerte'] = self.generar_muerte()
        print("  ✓ muerte")
        self.sonidos['victoria'] = self.generar_victoria()
        print("  ✓ victoria")
        self.sonidos['martillo'] = self.generar_martillo()
        print("  ✓ martillo")
        self.sonidos['ayuda'] = self.generar_ayuda()
        print("  ✓ ayuda")
        print("=====================================\n")
    
    def reproducir(self, nombre):
        sonido = self.sonidos.get(nombre)
        if sonido:
            try:
                sonido.play()
                return True
            except:
                pass
        return False