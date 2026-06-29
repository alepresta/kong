extends RigidBody2D

class_name Barril

# Constantes
const VELOCIDAD_INICIAL = 150.0
const ACELERACION = 20.0
const VELOCIDAD_MAXIMA = 400.0

# Variables
var velocidad: float = VELOCIDAD_INICIAL
var direccion: int = 1  # 1 derecha, -1 izquierda
var en_aire: bool = false
var activo: bool = true

# Referencias
@onready var sprite: Sprite2D = $Sprite2D
@onready var collision: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	# Configurar colisiones
	collision_layer = 3  # Capa de barriles
	collision_mask = 2  # Solo plataformas
	
	# Inicializar dirección aleatoria
	direccion = 1 if randf() > 0.5 else -1
	apply_central_impulse(Vector2(direccion * velocidad, 0))

func _physics_process(delta: float) -> void:
	if not activo:
		return
	
	# Acelerar gradualmente
	if velocidad < VELOCIDAD_MAXIMA:
		velocidad += ACELERACION * delta
	
	# Aplicar velocidad horizontal
	linear_velocity.x = direccion * velocidad
	
	# Verificar si está en el aire
	en_aire = not is_on_floor()
	
	# Actualizar sprite
	sprite.flip_h = direccion == -1

func destruir() -> void:
	activo = false
	queue_free()

func _on_body_entered(body: Node2D) -> void:
	if body is Jugador:
		if not body.invencible:
			body._jugador_golpeado()
