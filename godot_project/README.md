# KONG ARGENTINO - Migración a Godot Engine

## Estructura del Proyecto

```
godot_project/
├── project.godot              # Configuración principal
├── icon.svg                   # Icono del proyecto
├── scenes/                    # Escenas (.tscn)
│   ├── main.tscn             # Escena principal
│   ├── jugador.tscn          # Escena del jugador
│   ├── barril.tscn           # Escena de barriles
│   ├── hincha.tscn           # Escena de hinchada
│   └── niveles/              # Escenas de niveles
├── scripts/                   # Scripts GDScript (.gd)
│   ├── juego_principal.gd    # Lógica principal del juego
│   ├── jugador.gd            # Controlador del jugador
│   ├── barril.gd             # Lógica de barriles
│   ├── item.gd               # Items (cerveza, mate)
│   ├── controles_tactiles.gd # Controles para móvil
│   └── hud.gd                # Interfaz de usuario
├── assets/                    # Recursos
│   ├── sprites/              # Imágenes y sprites
│   ├── audio/                # Sonidos y música
│   └── fonts/                # Fuentes
└── addons/                    # Complementos
```

## Características Implementadas

### 1. Controles Táctiles para Móvil
- **Joystick virtual** en lado izquierdo para movimiento
- **Botones táctiles** en lado derecho (salto 🦘 y ataque 💥)
- Detección automática de plataforma móvil
- Zona muerta configurable para mejor precisión

### 2. Sistema de Juego
- Estados: MENU, JUGANDO, PAUSA, GAME_OVER, VICTORIA, VICTORIA_FINAL
- 6 niveles progresivos
- Sistema de puntuación y high score persistente
- Vidas e invencibilidad temporal

### 3. Entidades
- **Jugador**: Movimiento, salto, escaleras, ataque
- **Barriles**: Física, colisiones, destrucción
- **Hinchada**: NPCs con IA (pendiente de migrar)
- **Items**: Cerveza (puntos) y Mate (invencibilidad)
- **Kong**: Antagonista (pendiente)
- **Princesa**: Objetivo del nivel (pendiente)

### 4. HUD
- Puntuación actual
- Vidas restantes
- Nivel actual
- High score

### 5. Persistencia
- Guardado automático de high score en `user://high_score.dat`

## Controles

### Teclado (Desktop)
- **A / Flecha Izquierda**: Mover izquierda
- **D / Flecha Derecha**: Mover derecha
- **W / Flecha Arriba**: Saltar / Subir escalera
- **S / Flecha Abajo**: Bajar escalera
- **Espacio**: Atacar
- **P**: Pausa
- **ESC**: Volver al menú / Salir
- **Enter**: Iniciar juego (en menú)

### Táctil (Móvil)
- **Joystick izquierdo**: Movimiento en todas direcciones
- **Botón 🦘**: Saltar
- **Botón 💥**: Atacar

## Próximos Pasos

### Pendientes de Migración
1. **Entidades completas**
   - Kong Cervecero con animaciones
   - Princesa con Copa del Mundo
   - Todos los tipos de hinchada (Argentina, Viejo, Borrachín, etc.)

2. **Generación de niveles**
   - Migrar algoritmo de generación de Python
   - Configurar TileMaps para plataformas y escaleras

3. **Sistema de audio**
   - Migrar generador de sonidos
   - Efectos de sonido y música

4. **Gráficos**
   - Sprites para todas las entidades
   - Animaciones
   - Partículas y efectos

5. **UI adicional**
   - Pantalla de menú completa
   - Pantallas de Game Over y Victoria
   - Secuencia de celebración final

### Exportación a Móvil

#### Android
1. Instalar Godot 4.3+
2. Configurar Android Build Template
3. Ajustar configuración de exportación
4. Generar APK

#### iOS
1. Configurar certificado de desarrollo
2. Exportar para iOS
3. Compilar en Xcode

## Notas Técnicas

- **Motor**: Godot 4.3+
- **Resolución**: 1024x768 (escalable)
- **Física**: 2D integrada de Godot
- **Renderizado**: Forward Plus
- **Capas de colisión**:
  - 1: Jugador
  - 2: Plataformas
  - 3: Barriles
  - 4: Hinchada
  - 5: Items

## Comparación con Versión Python/Pygame

| Característica | Pygame | Godot |
|---------------|--------|-------|
| Controles táctiles | Manual con pygame.FINGER* | InputEventScreenTouch nativo |
| Física | Implementación manual | Motor físico integrado |
| Audio | Generación en Python | AudioStreamPlayer |
| Exportación móvil | pygbag (web) | APK/iOS nativo |
| Rendimiento | Limitado por Python | Optimizado C++ |
| Editor | Código | Visual + Código |

## Instrucciones de Uso

1. **Abrir proyecto**: 
   - Instalar Godot 4.3+
   - Abrir `project.godot`

2. **Ejecutar**:
   - Presionar F5 en el editor
   - O exportar para plataforma objetivo

3. **Probar en móvil**:
   - Exportar para Android/iOS
   - O usar remote debug via WiFi

---

**Estado**: Migración básica completada ✅
**Próximo**: Completar entidades y niveles
