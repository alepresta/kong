extends Area2D

class_name Item

# Tipos de items
enum TipoItem { CERVEZA, MATE }

# Variables
var tipo: TipoItem = TipoItem.CERVEZA
var puntos: int = 100
var activo: bool = true

# Referencias
@onready var sprite: Sprite2D = $Sprite2D

func _ready() -> void:
	# Configurar según el tipo
	match tipo:
		TipoItem.CERVEZA:
			puntos = 100
			# Cargar sprite de cerveza
		TipoItem.MATE:
			puntos = 200
			# Cargar sprite de mate

func actualizar(_delta: float) -> void:
	pass

func recoger(jugador: Node2D) -> void:
	if not activo:
		return
	
	activo = false
	
	match tipo:
		TipoItem.CERVEZA:
			jugador.puntuacion += puntos
		TipoItem.MATE:
			jugador.hacer_invencible(5.0)
	
	queue_free()
