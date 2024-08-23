extends Node3D

enum kind {LEFT, RIGHT}

@export
var step_kind: kind

@export
var attributes = {"start_tick": 0,
		"end_tick": 0,
		"left_pos": 0,
		"right_pos": 10000,
		"kind": 1,
		"player_id": 0
	}
	
var mesh

# Called when the node enters the scene tree for the first time.
func _ready():
	mesh = get_node("MeshInstance3D")
	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
