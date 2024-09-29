extends Node3D

#var tmpMesh = Mesh.new()
var tmpMesh = ArrayMesh.new()
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
	
	$MeshInstance3D.scale.x = float(attributes.right_pos - attributes.left_pos) * Globals.laneAtom
	
	return
	
	#mesh = get_node("MeshInstance3D")
	var size = 1000
	'''vertices.push_back(Vector3(0,0,0))
	vertices.push_back(Vector3(0,0,600))
	vertices.push_back(Vector3(600,0,600))
	'''
	
	vertices.push_back(Vector3(0, 0, 0))
	vertices.push_back(Vector3(0, 0, size))
	vertices.push_back(Vector3(size, 0, 0))
	
	vertices.push_back(Vector3(0, 0, size))
	vertices.push_back(Vector3(size, 0, 0))
	vertices.push_back(Vector3(size, 0, size))
	
	vertices.push_back(Vector3(0, size, 0))
	vertices.push_back(Vector3(0, size, size))
	vertices.push_back(Vector3(size, size, 0))
	
	vertices.push_back(Vector3(0, size, size))
	vertices.push_back(Vector3(size, size, 0))
	vertices.push_back(Vector3(size, size, size))
	
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
		#surfacetool.set_uv(UVs[vertex])
		#surfacetool.set_normal(Vector3(0, 0, 1))
		surfacetool.add_vertex(vertices[vertex])
		
	#surfacetool.commit(tmpMesh)
	#$MeshInstance3D.mesh = tmpMesh
	
	#$MeshInstance3D.mesh = surfacetool.commit()
	
	surfacetool.commit($MeshInstance3D.mesh)
	
	#ok what if we just copypasta the example lmao
	var st = SurfaceTool.new()

	st.begin(Mesh.PRIMITIVE_TRIANGLES)

	# Prepare attributes for add_vertex.
	#st.set_normal(Vector3(0, 0, 1))
	# Call last for each vertex, adds the above attributes.
	#st.add_vertex(Vector3(-1, -1, 0))
	
	#st.set_normal(Vector3(0, 0, 1))
	#st.add_vertex(Vector3(-1, 1, 0))

	#st.set_normal(Vector3(0, 0, 1))
	#st.add_vertex(Vector3(1, 1, 0))
	
	#this works
	'''
	st.add_vertex(Vector3(0, 0, 0))
	st.add_vertex(Vector3(0, 1, 0))
	st.add_vertex(Vector3(1, 1, 0))'''
	
	#this works
	'''
	st.add_vertex(Vector3(0, 0, 0))
	st.add_vertex(Vector3(0, size, 0))
	st.add_vertex(Vector3(size, size, 0))'''
	
	#this does not work
	'''
	st.add_vertex(Vector3(0, 0, 0))
	st.add_vertex(Vector3(0, 0, size))
	st.add_vertex(Vector3(size, 0, 0))'''
	
	st.add_vertex(Vector3(0, 0, 0))
	st.add_vertex(Vector3(0, 0, size))
	st.add_vertex(Vector3(size, 0, 0))
	
	$MeshInstance3D.mesh = st.commit()

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
