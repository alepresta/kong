extends Node2D

class_name JuegoKongArgentino

# Constantes del juego
const ANCHO_PANTALLA = 1024
const ALTO_PANTALLA = 768
const FPS = 60
const GRAVEDAD = 980.0
const VELOCIDAD_JUGADOR = 300.0
const SALTO_VELOCIDAD = -450.0

# Estados del juego
enum EstadoJuego { MENU, JUGANDO, PAUSA, GAME_OVER, VICTORIA, VICTORIA_FINAL }

# Señales
signal estado_cambiado(nuevo_estado)
signal nivel_completado(nivel)
signal jugador_muerto()

# Variables principales
var estado_actual: EstadoJuego = EstadoJuego.MENU
var nivel_actual: int = 1
var puntuacion: int = 0
var high_score: int = 0
var vidas: int = 3
var pausa: bool = false

# Referencias a nodos
@onready var jugador: CharacterBody2D = $Jugador
@onready var kong: Area2D = $Kong
@onready var princesa: Area2D = $Princesa
@onready var plataformas: TileMap = $Plataformas
@onready var escaleras: TileMap = $Escaleras
@onready var hinchada: Node2D = $Hinchada
@onready var barriles: Node2D = $Barriles
@onready var items: Node2D = $Items
@onready var hud: CanvasLayer = $HUD
@onready var controles_tactiles: CanvasLayer = $ControlesTactiles

# Gestión de audio
var generador_sonidos: AudioStreamPlayer

func _ready() -> void:
	# Configurar ventana
	DisplayServer.window_set_size(Vector2(ANCHO_PANTALLA, ALTO_PANTALLA))
	DisplayServer.window_set_title("KONG ARGENTINO")
	
	# Cargar high score
	cargar_high_score()
	
	# Inicializar controles táctiles para móvil
	if OS.has_feature("mobile") or DisplayServer.window_get_size().x > 500:
		controles_tactiles.visible = true
	else:
		controles_tactiles.visible = false
	
	# Conectar señales de controles táctiles
	if controles_tactiles:
		controles_tactiles.salto_presionado.connect(_on_salto_presionado)
		controles_tactiles.salto_liberado.connect(_on_salto_liberado)
		controles_tactiles.ataque_presionado.connect(_on_ataque_presionado)
	
	cambiar_estado(EstadoJuego.MENU)

func _process(delta: float) -> void:
	match estado_actual:
		EstadoJuego.MENU:
			_process_menu(delta)
		EstadoJuego.JUGANDO:
			if not pausa:
				_process_juego(delta)
		EstadoJuego.PAUSA:
			pass
		EstadoJuego.GAME_OVER:
			_process_game_over(delta)
		EstadoJuego.VICTORIA:
			_process_victoria(delta)
		EstadoJuego.VICTORIA_FINAL:
			_process_victoria_final(delta)

func _process_juego(delta: float) -> void:
	# Actualizar jugador
	if jugador:
		jugador.mover(delta)
	
	# Actualizar barriles
	for barril in barriles.get_children():
		if barril is Barril:
			barril.actualizar(delta)
	
	# Actualizar hinchada
	for hincha in hinchada.get_children():
		if hincha is HinchaBase:
			hincha.actualizar(delta)
	
	# Actualizar items
	for item in items.get_children():
		if item is Item:
			item.actualizar(delta)
	
	# Verificar colisiones
	_verificar_colisiones()
	
	# Verificar victoria de nivel
	if jugador and princesa and jugador.global_position.distance_to(princesa.global_position) < 50:
		_nivel_completado()

func _verificar_colisiones() -> void:
	if not jugador:
		return
	
	# Colisión con barriles
	for barril in barriles.get_children():
		if barril is Barril and jugador.global_position.distance_to(barril.global_position) < 40:
			if jugador.invencible:
				barril.destruir()
				puntuacion += 50
			else:
				_jugador_golpeado()
	
	# Colisión con items
	for item in items.get_children():
		if item is Item and jugador.global_position.distance_to(item.global_position) < 40:
			item.recoger(jugador)
			puntuacion += item.puntos

func _jugador_golpeado() -> void:
	vidas -= 1
	hud.actualizar_vidas(vidas)
	
	if vidas <= 0:
		cambiar_estado(EstadoJuego.GAME_OVER)
	else:
		# Hacer invencible temporalmente
		jugador.hacer_invencible(3.0)
		# Reposicionar jugador
		jugador.global_position = Vector2(100, ALTO_PANTALLA - 100)

func _nivel_completado() -> void:
	puntuacion += 1000 * nivel_actual
	hud.actualizar_puntuacion(puntuacion)
	
	if nivel_actual >= 6:
		cambiar_estado(EstadoJuego.VICTORIA_FINAL)
	else:
		nivel_actual += 1
		cambiar_estado(EstadoJuego.VICTORIA)

func cambiar_estado(nuevo_estado: EstadoJuego) -> void:
	estado_actual = nuevo_estado
	estado_cambiado.emit(nuevo_estado)
	
	match nuevo_estado:
		EstadoJuego.MENU:
			_setup_menu()
		EstadoJuego.JUGANDO:
			_setup_nivel()
		EstadoJuego.PAUSA:
			pausa = true
		EstadoJuego.GAME_OVER:
			_guardar_high_score()
		EstadoJuego.VICTORIA:
			pass
		EstadoJuego.VICTORIA_FINAL:
			_guardar_high_score()

func _setup_menu() -> void:
	pausa = false
	if jugador:
		jugador.visible = false
		jugador.set_physics_process(false)

func _setup_nivel() -> void:
	pausa = false
	if jugador:
		jugador.visible = true
		jugador.set_physics_process(true)
		jugador.global_position = Vector2(100, ALTO_PANTALLA - 100)
	
	# Generar nivel
	_generar_nivel(nivel_actual)

func _generar_nivel(nivel: int) -> void:
	# Limpiar elementos anteriores
	for barril in barriles.get_children():
		barril.queue_free()
	for hincha in hinchada.get_children():
		hincha.queue_free()
	for item in items.get_children():
		item.queue_free()
	
	# Aquí iría la lógica de generación de niveles
	# Similar al generator.py original
	pass

func reiniciar_juego() -> void:
	nivel_actual = 1
	puntuacion = 0
	vidas = 3
	hud.actualizar_vidas(vidas)
	hud.actualizar_puntuacion(puntuacion)
	cambiar_estado(EstadoJuego.JUGANDO)

func siguiente_nivel() -> void:
	cambiar_estado(EstadoJuego.JUGANDO)

# Manejo de inputs
func _input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		if estado_actual == EstadoJuego.JUGANDO:
			cambiar_estado(EstadoJuego.MENU)
		elif estado_actual == EstadoJuego.MENU:
			get_tree().quit()
	
	if event.is_action_pressed("pause") and estado_actual == EstadoJuego.JUGANDO:
		pausa = not pausa
	
	if event.is_action_pressed("jump"):
		if estado_actual == EstadoJuego.MENU:
			reiniciar_juego()
	
	# Controles de movimiento
	if estado_actual == EstadoJuego.JUGANDO and not pausa:
		if jugador:
			jugador.procesar_input(event)

# Callbacks de controles táctiles
func _on_salto_presionado() -> void:
	if estado_actual == EstadoJuego.JUGANDO and not pausa:
		if jugador:
			jugador.saltrar()

func _on_salto_liberado() -> void:
	if jugador:
		jugador.detener_salto()

func _on_ataque_presionado() -> void:
	if estado_actual == EstadoJuego.JUGANDO and not pausa:
		if jugador:
			jugador.atacar()

# Persistencia
func cargar_high_score() -> void:
	var file = FileAccess.open("user://high_score.dat", FileAccess.READ)
	if file:
		high_score = file.get_var()
		file.close()

func _guardar_high_score() -> void:
	if puntuacion > high_score:
		high_score = puntuacion
		var file = FileAccess.open("user://high_score.dat", FileAccess.WRITE)
		if file:
			file.store_var(high_score)
			file.close()

# Procesamiento por estado
func _process_menu(delta: float) -> void:
	pass

func _process_game_over(delta: float) -> void:
	pass

func _process_victoria(delta: float) -> void:
	pass

func _process_victoria_final(delta: float) -> void:
	pass
