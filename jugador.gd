extends CharacterBody2D

const SPEED = 400.0

func _physics_process(delta):
	var direction = 0
	if Input.is_action_pressed("ui_right"):
		direction += 1
	elif Input.is_action_pressed("ui_left"):
		direction -= 1
	
	velocity.x = direction * SPEED
	move_and_slide()
