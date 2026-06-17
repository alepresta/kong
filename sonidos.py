"""
KONG ARGENTINO - SONIDOS PROCEDURALES v2
Creado por Apresta para Prestalabs
"""
import pygame
import numpy as np

class GeneradorSonidos:
    """Genera sonidos proceduralmente sin archivos externos"""
    
    SAMPLE_RATE = 22050
    
    def __init__(self):
        self.sonidos = {}
        self._generar_todos()
    
    def _tono(self, frecuencias, duracion, volumen=0.3, forma='sine', env='fade'):
        n = int(self.SAMPLE_RATE * duracion)
        t = np.linspace(0, duracion, n, False)
        onda = np.zeros(n)
        for f in frecuencias:
            if forma == 'sine':
                onda += np.sin(2 * np.pi * f * t)
            elif forma == 'square':
                onda += np.sign(np.sin(2 * np.pi * f * t))
            elif forma == 'saw':
                onda += 2 * (t * f - np.floor(0.5 + t * f))
            elif forma == 'triangle':
                onda += 2 * np.abs(2 * (t * f - np.floor(t * f + 0.5))) - 1
        onda /= max(len(frecuencias), 1)
        if env == 'fade':
            fade = int(n * 0.25)
            onda[-fade:] *= np.linspace(1, 0, fade)
        elif env == 'attack':
            att = int(n * 0.1)
            onda[:att] *= np.linspace(0, 1, att)
            fade = int(n * 0.3)
            onda[-fade:] *= np.linspace(1, 0, fade)
        onda = np.clip(onda * volumen * 32767, -32767, 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([onda, onda]))
    
    def _ruido(self, duracion, volumen=0.15, filtro=1.0):
        n = int(self.SAMPLE_RATE * duracion)
        onda = np.random.uniform(-1, 1, n)
        if filtro < 1.0:
            # simple low-pass
            alpha = filtro
            for i in range(1, n):
                onda[i] = alpha * onda[i] + (1 - alpha) * onda[i-1]
        fade = int(n * 0.3)
        onda[-fade:] *= np.linspace(1, 0, fade)
        onda = np.clip(onda * volumen * 32767, -32767, 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([onda, onda]))
    
    def _glissando(self, f_inicio, f_fin, duracion, volumen=0.3):
        n = int(self.SAMPLE_RATE * duracion)
        t = np.linspace(0, duracion, n, False)
        freqs = np.linspace(f_inicio, f_fin, n)
        fase = np.cumsum(2 * np.pi * freqs / self.SAMPLE_RATE)
        onda = np.sin(fase)
        fade = int(n * 0.15)
        onda[-fade:] *= np.linspace(1, 0, fade)
        onda = np.clip(onda * volumen * 32767, -32767, 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([onda, onda]))
    
    def _generar_todos(self):
        try:
            pygame.mixer.pre_init(self.SAMPLE_RATE, -16, 2, 512)
            if not pygame.mixer.get_init():
                pygame.mixer.init(self.SAMPLE_RATE, -16, 2, 512)
            
            self.sonidos['salto']     = self._glissando(280, 560, 0.10, 0.22)
            self.sonidos['moneda']    = self._tono([523, 784, 1047], 0.16, 0.28, 'sine', 'attack')
            self.sonidos['golpe']     = self._tono([70, 90], 0.18, 0.45, 'square', 'fade')
            self.sonidos['martillo']  = self._tono([220, 330, 440, 660], 0.28, 0.38, 'square', 'attack')
            self.sonidos['victoria']  = self._tono([523, 659, 784, 1047, 1319], 0.55, 0.38, 'sine', 'attack')
            self.sonidos['game_over'] = self._glissando(400, 100, 0.65, 0.32)
            self.sonidos['beber']     = self._tono([150, 110, 80], 0.22, 0.32, 'saw', 'fade')
            self.sonidos['combo']     = self._tono([659, 880, 1047], 0.14, 0.30, 'triangle', 'attack')
            self.sonidos['nivel']     = self._tono([392, 523, 659, 784, 1047], 0.70, 0.36, 'sine', 'attack')
            self.sonidos['vida']      = self._tono([440, 550, 660], 0.20, 0.30, 'triangle', 'attack')
            self.sonidos['peligro']   = self._tono([200, 150], 0.12, 0.25, 'square', 'fade')
            
        except Exception as e:
            print(f"[Sonidos] No se pudo inicializar: {e}")
            self.sonidos = {}
    
    def reproducir(self, nombre):
        snd = self.sonidos.get(nombre)
        if snd:
            try:
                snd.play()
            except Exception:
                pass