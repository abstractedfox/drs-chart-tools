extends Node3D

var tmpMesh = Mesh.new()
var vertices = PackedVector3Array()
var UVs = PackedVector2Array()
var mat = StandardMaterial3D.new()
var color = Color(0, 0, 10)
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
	#mesh = get_node("MeshInstance3D")
	vertices.push_back(Vector3(100,0,0))
	vertices.push_back(Vector3(100,0,100))
	vertices.push_back(Vector3(0,0,100))
	vertices.push_back(Vector3(0,0,0))
	
	'''
	vertices.push_back(Vector3(100,100,0))
	vertices.push_back(Vector3(100,100,100))
	vertices.push_back(Vector3(0,100,100))
	vertices.push_back(Vector3(0,100,0))
	
	UVs.push_back(Vector2(0,0))
	UVs.push_back(Vector2(0,1))
	UVs.push_back(Vector2(1,1))
	UVs.push_back(Vector2(1,0))
	'''
	UVs.push_back(Vector2(0,0))
	UVs.push_back(Vector2(0,1))
	UVs.push_back(Vector2(1,1))
	UVs.push_back(Vector2(1,0))
	
	mat.albedo_color = color
	
	var surfacetool = SurfaceTool.new()
	surfacetool.begin(Mesh.PRIMITIVE_TRIANGLES)
	surfacetool.set_material(mat)
	
	for vertex in vertices.size():
		surfacetool.set_color(color)
		surfacetool.set_uv(UVs[vertex])
		surfacetool.add_vertex(vertices[vertex])
		
	surfacetool.commit(tmpMesh)
	
	$MeshInstance3D.mesh = tmpMesh

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
