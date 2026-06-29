extends CanvasLayer

class_name ControlesTactiles

# Señales
signal salto_presionado()
signal salto_liberado()
signal ataque_presionado()
signal movimiento_cambiado(x: float, y: float)

# Variables del joystick
var joystick_activo: bool = false
var joystick_id: int = -1
var joystick_centro: Vector2 = Vector2(150, 618)
var joystick_radio: float = 80.0
var joystick_posicion: Vector2 = Vector2.ZERO
var zona_muerta: float = 0.15

# Botones
var boton_salto_rect: Rect2
var boton_ataque_rect: Rect2
var boton_salto_activo: bool = false
var boton_ataque_activo: bool = false

# Referencias
@onready var sprite_joystick_base: Sprite2D = $JoystickBase
@onready var sprite_joystick_mano: Sprite2D = $JoystickMano
@onready var boton_salto: Button = $BotonSalto
@onready var boton_ataque: Button = $BotonAtaque

func _ready() -> void:
	# Configurar botones
	boton_salto_rect = Rect2(Vector2(ANCHO_PANTALLA - 200, ALTO_PANTALLA - 120), Vector2(80, 80))
	boton_ataque_rect = Rect2(Vector2(ANCHO_PANTALLA - 100, ALTO_PANTALLA - 120), Vector2(80, 80))
	
	# Conectar señales de botones
	boton_salto.pressed.connect(_on_boton_salto_presionado)
	boton_salto.released.connect(_on_boton_salto_liberado)
	boton_ataque.pressed.connect(_on_boton_ataque_presionado)
	boton_ataque.released.connect(_on_boton_ataque_liberado)

func _input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		_procesar_toque(event)
	elif event is InputEventScreenDrag:
		_procesar_arrastre(event)

func _procesar_toque(event: InputEventScreenTouch) -> void:
	var touch_pos = event.position
	var touch_id = event.index
	
	# Verificar joystick (lado izquierdo)
	if touch_pos.x < ANCHO_PANTALLA / 2:
		var dist = touch_pos.distance_to(joystick_centro)
		if dist <= joystick_radio and event.pressed:
			joystick_activo = true
			joystick_id = touch_id
			_actualizar_joystick(touch_pos)
		elif not event.pressed and joystick_id == touch_id:
			joystick_activo = false
			joystick_id = -1
			joystick_posicion = Vector2.ZERO
			movimiento_cambiado.emit(0.0, 0.0)
			_input_action_release("move_left")
			_input_action_release("move_right")
			_input_action_release("jump")
			_input_action_release("attack")
	
	# Verificar botones (lado derecho) - ya manejados por Button nodes

func _procesar_arrastre(event: InputEventScreenDrag) -> void:
	if joystick_activo and event.index == joystick_id:
		_actualizar_joystick(event.position)

func _actualizar_joystick(posicion: Vector2) -> void:
	var dx = posicion.x - joystick_centro.x
	var dy = posicion.y - joystick_centro.y
	var dist = sqrt(dx * dx + dy * dy)
	
	# Normalizar a [-1, 1]
	if dist > 0:
		var max_dist = min(dist, joystick_radio)
		var nx = (dx / dist) * (max_dist / joystick_radio)
		var ny = (dy / dist) * (max_dist / joystick_radio)
		joystick_posicion = Vector2(nx, ny)
	else:
		joystick_posicion = Vector2.ZERO
	
	# Actualizar posición visual del joystick
	if sprite_joystick_mano:
		sprite_joystick_mano.position = Vector2(
			joystick_centro.x + joystick_posicion.x * joystick_radio,
			joystick_centro.y + joystick_posicion.y * joystick_radio
		) - sprite_joystick_base.position
	
	# Aplicar zona muerta y emitir señales
	var abs_x = abs(joystick_posicion.x)
	var abs_y = abs(joystick_posicion.y)
	
	if joystick_posicion.x < -zona_muerta:
		_input_action_press("move_left")
		_input_action_release("move_right")
	elif joystick_posicion.x > zona_muerta:
		_input_action_release("move_left")
		_input_action_press("move_right")
	else:
		_input_action_release("move_left")
		_input_action_release("move_right")
	
	if joystick_posicion.y < -zona_muerta:
		_input_action_press("jump")
		_input_action_release("attack")
	elif joystick_posicion.y > zona_muerta:
		_input_action_release("jump")
		_input_action_press("attack")
	else:
		_input_action_release("jump")
		_input_action_release("attack")
	
	movimiento_cambiado.emit(joystick_posicion.x, joystick_posicion.y)

func _on_boton_salto_presionado() -> void:
	salto_presionado.emit()
	_input_action_press("jump")

func _on_boton_salto_liberado() -> void:
	salto_liberado.emit()
	_input_action_release("jump")

func _on_boton_ataque_presionado() -> void:
	ataque_presionado.emit()
	_input_action_press("attack")

func _on_boton_ataque_liberado() -> void:
	_input_action_release("attack")

# Simular input de teclado para compatibilidad
func _input_action_press(action: String) -> void:
	var event = InputEventAction.new()
	event.action = action
	event.pressed = true
	Input.parse_input_event(event)

func _input_action_release(action: String) -> void:
	var event = InputEventAction.new()
	event.action = action
	event.pressed = false
	Input.parse_input_event(event)

func _draw() -> void:
	# Dibujar joystick base
	draw_circle(joystick_centro, joystick_radio, Color(0.2, 0.2, 0.2, 0.3), false, 3)
	
	# Dibujar joystick mano
	if joystick_activo:
		var mano_pos = joystick_centro + joystick_posicion * joystick_radio
		draw_circle(mano_pos, 30, Color(0.4, 0.6, 1.0, 0.6))
	else:
		draw_circle(joystick_centro, 30, Color(0.4, 0.6, 1.0, 0.3))
	
	# Dibujar botones
	var color_salto = Color(0.4, 0.8, 0.4, 0.5) if not boton_salto_activo else Color(0.5, 0.9, 0.5, 0.7)
	var color_ataque = Color(0.8, 0.4, 0.4, 0.5) if not boton_ataque_activo else Color(0.9, 0.5, 0.5, 0.7)
	
	draw_circle(boton_salto_rect.get_center(), 40, color_salto, true)
	draw_circle(boton_salto_rect.get_center(), 40, color_salto, false, 3)
	
	draw_circle(boton_ataque_rect.get_center(), 40, color_ataque, true)
	draw_circle(boton_ataque_rect.get_center(), 40, color_ataque, false, 3)
