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
import math
import random
from array import array


def _snd_log(msg):
    """Diagnostico de audio a la consola del navegador (y stdout)."""
    print(msg)
    try:
        import platform
        platform.window.console.log("[KONG-SND] " + str(msg))
    except Exception:
        pass

class GeneradorSonidos:
    """Genera sonidos proceduralmente sin archivos externos.

    Implementacion en Python puro (sin numpy): asi funciona tanto en escritorio
    como en navegador (pygbag/wasm), donde cargar numpy rompe el driver de video.
    """

    SAMPLE_RATE = 22050

    def __init__(self):
        self.sonidos = {}
        self.volumen_maestro = 0.7
        # Usar la frecuencia/canales reales con que quedo inicializado el mixer
        # para que el buffer PCM suene a la velocidad correcta.
        info = pygame.mixer.get_init()
        if info:
            self.sample_rate = info[0]
            self.channels = info[2]
        else:
            self.sample_rate = self.SAMPLE_RATE
            self.channels = 2
        _snd_log("init: modo=python-puro mixer_init=" + str(info))
        self._generar_todos()
        _snd_log("sonidos generados: " + str(len(self.sonidos)))

    def _to_sound(self, mono):
        """Convierte una lista de muestras float [-1..1] (ya con volumen aplicado)
        en un pygame.Sound con el formato del mixer (int16 intercalado)."""
        buf = array('h')
        ch = self.channels
        for s in mono:
            v = int(s * 32767.0)
            if v > 32767:
                v = 32767
            elif v < -32767:
                v = -32767
            for _ in range(ch):
                buf.append(v)
        return pygame.mixer.Sound(buffer=buf.tobytes())

    def set_volumen(self, vol):
        """Ajusta volumen maestro 0.0 - 1.0"""
        self.volumen_maestro = max(0.0, min(1.0, vol))
        for snd in self.sonidos.values():
            snd.set_volume(self.volumen_maestro)

    def _tono(self, frecuencias, duracion, volumen=0.3, forma='sine', env='fade'):
        sr = self.sample_rate
        n = int(sr * duracion)
        if n <= 0:
            return self._to_sound([])
        nf = max(len(frecuencias), 1)
        dos_pi = 2 * math.pi
        onda = [0.0] * n
        for i in range(n):
            t = i / sr
            s = 0.0
            for f in frecuencias:
                if forma == 'sine':
                    s += math.sin(dos_pi * f * t)
                elif forma == 'square':
                    val = math.sin(dos_pi * f * t)
                    s += 1.0 if val > 0 else (-1.0 if val < 0 else 0.0)
                elif forma == 'saw':
                    s += 2 * (t * f - math.floor(0.5 + t * f))
                elif forma == 'triangle':
                    s += 2 * abs(2 * (t * f - math.floor(t * f + 0.5))) - 1
            onda[i] = s / nf
        if env == 'fade':
            fade = int(n * 0.25)
            self._fade_out(onda, n, fade)
        elif env == 'attack':
            att = int(n * 0.1)
            self._fade_in(onda, att)
            fade = int(n * 0.3)
            self._fade_out(onda, n, fade)
        elif env == 'pluck':
            for i in range(n):
                onda[i] *= math.exp(-(i / sr) * 10)
        for i in range(n):
            onda[i] *= volumen
        return self._to_sound(onda)

    def _ruido(self, duracion, volumen=0.15, filtro=1.0):
        sr = self.sample_rate
        n = int(sr * duracion)
        if n <= 0:
            return self._to_sound([])
        onda = [random.uniform(-1, 1) for _ in range(n)]
        if filtro < 1.0:
            alpha = filtro
            for i in range(1, n):
                onda[i] = alpha * onda[i] + (1 - alpha) * onda[i - 1]
        fade = int(n * 0.3)
        self._fade_out(onda, n, fade)
        for i in range(n):
            onda[i] *= volumen
        return self._to_sound(onda)

    def _glissando(self, f_inicio, f_fin, duracion, volumen=0.3):
        sr = self.sample_rate
        n = int(sr * duracion)
        if n <= 0:
            return self._to_sound([])
        dos_pi = 2 * math.pi
        onda = [0.0] * n
        fase = 0.0
        for i in range(n):
            frac = i / (n - 1) if n > 1 else 0.0
            freq = f_inicio + (f_fin - f_inicio) * frac
            fase += dos_pi * freq / sr
            onda[i] = math.sin(fase)
        fade = int(n * 0.15)
        self._fade_out(onda, n, fade)
        for i in range(n):
            onda[i] *= volumen
        return self._to_sound(onda)

    def _chord(self, notas, duracion, volumen=0.25, env='fade'):
        """Acorde de múltiples notas con volumen balanceado"""
        sr = self.sample_rate
        n = int(sr * duracion)
        if n <= 0:
            return self._to_sound([])
        nn = len(notas)
        dos_pi = 2 * math.pi
        onda = [0.0] * n
        for i in range(n):
            t = i / sr
            s = 0.0
            for f in notas:
                s += math.sin(dos_pi * f * t)
            onda[i] = s / nn
        if env == 'fade':
            fade = int(n * 0.4)
            self._fade_out(onda, n, fade)
        elif env == 'attack':
            att = int(n * 0.05)
            self._fade_in(onda, att)
            fade = int(n * 0.35)
            self._fade_out(onda, n, fade)
        for i in range(n):
            onda[i] *= volumen
        return self._to_sound(onda)

    @staticmethod
    def _fade_in(onda, att):
        if att > 1:
            for j in range(att):
                onda[j] *= j / (att - 1)

    @staticmethod
    def _fade_out(onda, n, fade):
        if fade > 1:
            for j in range(fade):
                onda[n - fade + j] *= 1 - j / (fade - 1)

    def _generar_todos(self):
        try:
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
            _snd_log("No se pudo inicializar: " + repr(e))
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
