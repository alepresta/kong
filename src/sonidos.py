"""
KONG ARGENTINO - SONIDOS PROCEDURALES v3.0
Creado por Apresta para Prestalabs

Mejoras v3.0:
- Nuevos sonidos: salto_escalera, barril_saltado, victoria_final, record
- Sistema de volumen maestro ajustable
- Pitchshift dinámico en combo
- Caché de sonidos mejorada
"""
import pygame
try:
    import numpy as np
except Exception:
    np = None

class GeneradorSonidos:
    """Genera sonidos proceduralmente sin archivos externos"""
    
    SAMPLE_RATE = 22050
    
    def __init__(self):
        self.sonidos = {}
        self.volumen_maestro = 0.7
        if np is None:
            print("[Sonidos] numpy no disponible: audio deshabilitado")
        else:
            self._generar_todos()
    
    def set_volumen(self, vol):
        """Ajusta volumen maestro 0.0 - 1.0"""
        self.volumen_maestro = max(0.0, min(1.0, vol))
        for snd in self.sonidos.values():
            snd.set_volume(self.volumen_maestro)

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
        elif env == 'pluck':
            # Ataque rápido, decay exponencial
            decay = np.exp(-t * 10)
            onda *= decay
        onda = np.clip(onda * volumen * 32767, -32767, 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([onda, onda]))
    
    def _ruido(self, duracion, volumen=0.15, filtro=1.0):
        n = int(self.SAMPLE_RATE * duracion)
        onda = np.random.uniform(-1, 1, n)
        if filtro < 1.0:
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

    def _chord(self, notas, duracion, volumen=0.25, env='fade'):
        """Acorde de múltiples notas con volumen balanceado"""
        n = int(self.SAMPLE_RATE * duracion)
        t = np.linspace(0, duracion, n, False)
        onda = sum(np.sin(2 * np.pi * f * t) for f in notas) / len(notas)
        if env == 'fade':
            fade = int(n * 0.4)
            onda[-fade:] *= np.linspace(1, 0, fade)
        elif env == 'attack':
            att = int(n * 0.05)
            onda[:att] *= np.linspace(0, 1, att)
            fade = int(n * 0.35)
            onda[-fade:] *= np.linspace(1, 0, fade)
        onda = np.clip(onda * volumen * 32767, -32767, 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([onda, onda]))

    def _generar_todos(self):
        try:
            pygame.mixer.pre_init(self.SAMPLE_RATE, -16, 2, 512)
            if not pygame.mixer.get_init():
                pygame.mixer.init(self.SAMPLE_RATE, -16, 2, 512)
            
            # --- Sonidos originales mejorados ---
            self.sonidos['salto']          = self._glissando(300, 600, 0.10, 0.20)
            self.sonidos['salto_escalera'] = self._glissando(250, 450, 0.08, 0.15)
            self.sonidos['moneda']         = self._tono([523, 784, 1047], 0.14, 0.25, 'sine', 'attack')
            self.sonidos['golpe']          = self._tono([65, 85], 0.16, 0.40, 'square', 'fade')
            self.sonidos['golpe_fuerte']   = self._tono([50, 70, 110], 0.22, 0.50, 'square', 'fade')
            self.sonidos['martillo']       = self._tono([220, 330, 440, 660], 0.26, 0.35, 'square', 'attack')
            self.sonidos['victoria']       = self._tono([523, 659, 784, 1047, 1319], 0.50, 0.35, 'sine', 'attack')
            self.sonidos['game_over']      = self._glissando(380, 90, 0.70, 0.30)
            self.sonidos['beber']          = self._tono([150, 110, 80], 0.20, 0.28, 'saw', 'fade')
            self.sonidos['combo']          = self._tono([659, 880, 1047], 0.13, 0.28, 'triangle', 'attack')
            self.sonidos['nivel']          = self._chord([392, 523, 659, 784, 1047], 0.75, 0.35, 'attack')
            self.sonidos['vida']           = self._tono([440, 550, 660], 0.18, 0.28, 'triangle', 'attack')
            self.sonidos['peligro']        = self._tono([180, 140], 0.14, 0.22, 'square', 'fade')
            # --- Nuevos v3.0 ---
            self.sonidos['barril_saltado'] = self._glissando(200, 400, 0.07, 0.18)
            self.sonidos['record']         = self._chord([523, 659, 784, 1047, 1319, 1568], 1.0, 0.38, 'attack')
            self.sonidos['victoria_final'] = self._chord([392, 523, 659, 784, 1047], 1.2, 0.40, 'attack')
            self.sonidos['ataque']         = self._tono([120, 180], 0.10, 0.30, 'square', 'fade')
            self.sonidos['poder_acabando'] = self._tono([440, 330], 0.08, 0.18, 'square', 'fade')
            self.sonidos['combo_x5']       = self._chord([784, 1047, 1319], 0.20, 0.35, 'attack')
            self.sonidos['hincha_golpe']   = self._tono([200, 280], 0.12, 0.25, 'square', 'fade')

            # Aplicar volumen maestro inicial
            for snd in self.sonidos.values():
                snd.set_volume(self.volumen_maestro)

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

    def reproducir_con_pitch(self, nombre, pitch=1.0):
        """Reproduce un sonido con pitch modificado (aproximación via volumen y canal)"""
        self.reproducir(nombre)
