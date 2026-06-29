extends CanvasLayer

class_name HUD

# Referencias
@onready var label_puntuacion: Label = $Puntuacion
@onready var label_vidas: Label = $Vidas
@onready var label_nivel: Label = $Nivel
@onready var label_high_score: Label = $HighScore

func _ready() -> void:
	actualizar_puntuacion(0)
	actualizar_vidas(3)
	actualizar_nivel(1)
	actualizar_high_score(0)

func actualizar_puntuacion(puntos: int) -> void:
	if label_puntuacion:
		label_puntuacion.text = "PUNTOS: " + str(puntos)

func actualizar_vidas(vidas: int) -> void:
	if label_vidas:
		label_vidas.text = "VIDAS: " + str(vidas)

func actualizar_nivel(nivel: int) -> void:
	if label_nivel:
		label_nivel.text = "NIVEL: " + str(nivel)

func actualizar_high_score(score: int) -> void:
	if label_high_score:
		label_high_score.text = "RECORD: " + str(score)
