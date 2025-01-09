extends Node3D
	
@export
var steps = []
var stepInstances = []

func stepToDict(step: String):
	var sliced = step.split(" ")
	if sliced[0] != "note":
		return false
		
	return {"start_tick": int(sliced[1]),
		"end_tick": int(sliced[2]),
		"left_pos": int(sliced[3]),
		"right_pos": int(sliced[4]),
		"kind": int(sliced[5]),
		"player_id": int(sliced[6])
	}
	
func parseChart(chart: String):
	for line in chart.split("\n"):
		if line.find("note") > -1:
			steps.append(stepToDict(line))
			print(steps)

func apiTest():
	#var command = "python3.12 chart_tools_api.py init testyy.xml : bpm add 57300 0"
	var cmdReturn = []
	
	#on macos you have to put the full path to python
	#OS.execute("bash", ["-c", "python3.12 ../chart_tools_api.py init godottestyy.xml : bpm add 57300 0 : note add 100 100 100 200 1 0 : chart get"], cmdReturn, true)
	OS.execute("bash", ["-c", "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 ../chart_tools_api.py init godottestyy.xml : bpm add 57300 0 : note add 100 100 100 200 1 0 : note add 200 200 1000 2000 1 0 : chart get"], cmdReturn, true)
	
	print_debug("raw in: " + cmdReturn[0])
	parseChart(cmdReturn[0])

# Called when the node enters the scene tree for the first time.
func _ready():
	steps = [] #apparently when you export an empty array, it's populated with a null at [0]
	stepInstances = []
	apiTest()
	for note in steps:
		var new_note = load("res://note.tscn")
		
		var instance = new_note.instantiate()
		instance.attributes = note
		stepInstances.append(instance)
		add_child(stepInstances[-1])

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	for step in stepInstances:
		pass
	pass
