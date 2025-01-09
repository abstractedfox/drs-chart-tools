extends Node

#Width of the entire lane. Used to keep objects relative to the lane scaled correctly 
var laneWidth = 10
var laneAtom = float(laneWidth) / float(65536)

#the amount of vertical physical space to place between notes for a single tick
var timeScaleMul = 1
var timeScale = (1/480) * timeScaleMul
var timeOffset = 0

func _ready():
	pass
