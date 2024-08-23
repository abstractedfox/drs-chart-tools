extends Node3D
	
@export
var steps = []

func stepToDict(step: String):
	var sliced = step.split(" ")
	if sliced[0] != "step":
		return false
		
	return {"start_tick": sliced[1],
		"end_tick": sliced[2],
		"left_pos": sliced[3],
		"right_pos": sliced[4],
		"kind": sliced[5],
		"player_id": sliced[6]
	}

func apiTest():
	var command = "python3.12 chart_tools_api.py init testyy.xml : bpm add 57300 0"
	var cmdReturn = []
	
	#OS.execute("which", ["python3.12"], cmdReturn)
	#OS.execute("python3.12", ["../chart_tools_api.py init godottestyy.xml : bpm add 57300 0"], cmdReturn, true)
	OS.execute("bash", ["-c", "python3.12 ../chart_tools_api.py init godottestyy.xml : bpm add 57300 0 : note add 100 100 100 200 1 0 : chart get"], cmdReturn, true)
	
	print_debug("ayo? " + cmdReturn[0])

# Called when the node enters the scene tree for the first time.
func _ready():
	apiTest()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
