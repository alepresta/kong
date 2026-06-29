extends CharacterBody2D

class_name Jugador

# Constantes
const VELOCIDAD = 300.0
const SALTO_VELOCIDAD = -450.0
const GRAVEDAD = 980.0

# Señales
signal ataque_realizado()

# Variables
var velocidad_horizontal: float = 0.0
var en_suelo: bool = false
var en_escalera: bool = false
var subiendo_escalera: bool = false
var bajando_escalera: bool = false
var atacando: bool = false
var invencible: bool = false
var direccion: int = 1  # 1 derecha, -1 izquierda
var tiempo_invencibilidad: float = 0.0
var tiempo_ataque: float = 0.0

# Referencias
@onready var sprite: Sprite2D = $Sprite2D
@onready var collision: CollisionShape2D = $CollisionShape2D
@onready var area_ataque: Area2D = $AreaAtaque
@onready var raycast_suelo: RayCast2D = $RaycastSuelo
@onready var raycast_escalera: RayCast2D = $RaycastEscalera

func _ready() -> void:
	pass

func _physics_process(delta: float) -> void:
	aplicar_gravedad(delta)
	procesar_movimiento(delta)
	
	if invencible:
		tiempo_invencibilidad -= delta
		if tiempo_invencibilidad <= 0:
			invencible = false
			sprite.modulate.a = 1.0
		else:
			# Parpadeo cuando es invencible
			sprite.modulate.a = sin(tiempo_invencibilidad * 20) * 0.5 + 0.5
	
	if atacando:
		tiempo_ataque -= delta
		if tiempo_ataque <= 0:
			atacando = false
			area_ataque.set_deferred("monitoring", false)

func procesar_input(event: InputEvent) -> void:
	# Movimiento horizontal
	if event.is_action_pressed("move_left"):
		velocidad_horizontal = -VELOCIDAD
		direccion = -1
	elif event.is_action_released("move_left"):
		if velocidad_horizontal < 0:
			velocidad_horizontal = 0.0
	
	if event.is_action_pressed("move_right"):
		velocidad_horizontal = VELOCIDAD
		direccion = 1
	elif event.is_action_released("move_right"):
		if velocidad_horizontal > 0:
			velocidad_horizontal = 0.0
	
	# Salto
	if event.is_action_pressed("jump") and en_suelo and not en_escalera:
		saltar()
	
	# Escaleras
	if en_escalera:
		if event.is_action_pressed("jump"):  # Arriba
			subir_escalera()
		elif event.is_action_pressed("attack"):  # Abajo (usamos attack como abajo por ahora)
			bajar_escalera()
	
	# Ataque
	if event.is_action_pressed("attack") and not atacando:
		atacar()

func mover(delta: float) -> void:
	# Obtener input directo (para controles táctiles)
	var input_izquierda = Input.is_action_pressed("move_left")
	var input_derecha = Input.is_action_pressed("move_right")
	
	if input_izquierda:
		velocidad_horizontal = -VELOCIDAD
		direccion = -1
	elif input_derecha:
		velocidad_horizontal = VELOCIDAD
		direccion = 1
	else:
		velocidad_horizontal = 0.0
	
	# Aplicar movimiento
	velocity.x = velocidad_horizontal
	
	# Verificar escaleras
	en_escalera = raycast_escalera.is_colliding()
	
	if en_escalera:
		# Movimiento vertical en escalera
		var input_arriba = Input.is_action_pressed("jump")
		var input_abajo = Input.is_action_pressed("attack")
		
		if input_arriba:
			velocity.y = -VELOCIDAD * 0.7
		elif input_abajo:
			velocity.y = VELOCIDAD * 0.7
		else:
			velocity.y = 0.0
	else:
		aplicar_gravedad(delta)
	
	move_and_slide()
	
	# Verificar si está en el suelo
	en_suelo = is_on_floor()
	
	# Actualizar sprite
	if direccion == -1:
		sprite.flip_h = true
	else:
		sprite.flip_h = false

func aplicar_gravedad(delta: float) -> void:
	if not en_escalera:
		velocity.y += GRAVEDAD * delta
		if velocity.y > 1000:
			velocity.y = 1000

func saltar() -> void:
	if en_suelo and not en_escalera:
		velocity.y = SALTO_VELOCIDAD
		en_suelo = false

func detener_salto() -> void:
	if velocity.y < 0:
		velocity.y *= 0.5

func atacar() -> void:
	atacando = true
	tiempo_ataque = 0.3
	area_ataque.set_deferred("monitoring", true)
	ataque_realizado.emit()

func hacer_invencible(duracion: float) -> void:
	invencible = true
	tiempo_invencibilidad = duracion

func subir_escalera() -> void:
	subiendo_escalera = true
	bajando_escalera = false

func bajar_escalera() -> void:
	bajando_escalera = true
	subiendo_escalera = false

func _on_area_ataque_body_entered(body: Node2D) -> void:
	if atacando and body is Barril:
		body.destruir()
