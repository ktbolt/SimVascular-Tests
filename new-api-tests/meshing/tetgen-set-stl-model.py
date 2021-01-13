'''Test meshing an STL solid model and using set_model from the TetGen class interface.

   Writes: 'cylinder-mesh.vtu'

   Note: Be careful with global_edge_size, must match model Remesh Size resolution.
'''
import sv
import sys
import vtk
sys.path.insert(1, '../graphics/')
import graphics as gr

## Create renderer and graphics window.
win_width = 500
win_height = 500
renderer, renderer_window = gr.init_graphics(win_width, win_height)

## Read in an STL model
modeler = sv.modeling.Modeler(sv.modeling.Kernel.POLYDATA)
file_name = "../data/models/cylinder.stl"
model = modeler.read(file_name)
print("Model type: " + str(type(model)))
face_ids = model.compute_boundary_faces(angle=60.0)
print("Model face IDs: " + str(face_ids))

## Remesh the model.
#
#  If the STL model contains long triangles then it is a good idea to remesh it. 
#
#  Note: The model may need to be remeshed twice to get a new surface representation.
#
if True:
    model_surf = model.get_polydata()
    remesh_model = sv.mesh_utils.remesh(model.get_polydata(), hmin=0.4, hmax=0.4)
    model.set_surface(surface=remesh_model)
    model.compute_boundary_faces(angle=60.0)

    remesh_model = sv.mesh_utils.remesh(model.get_polydata(), hmin=0.4, hmax=0.4)
    model.set_surface(surface=remesh_model)
    model.compute_boundary_faces(angle=60.0)

## Compute boundary faces.
face_ids = model.compute_boundary_faces(angle=60.0)
print("Model face IDs: " + str(face_ids))

## Create a TetGen mesher.
mesher = sv.meshing.TetGen()
mesher.set_model(model)

## Set the face IDs for model walls.
face_ids = [1]
mesher.set_walls(face_ids)

## Compute model boundary faces.
face_ids = mesher.get_model_face_ids()
print("Mesh face ids: " + str(face_ids))

## Set meshing options.
#
# Note: Be careful with global_edge_size, must match model Remesh Size resolution.
print("Set meshing options ... ")
options = sv.meshing.TetGenOptions(global_edge_size=0.4, surface_mesh_flag=True, volume_mesh_flag=True)

## Generate the mesh. 
#
if True:
    mesher.generate_mesh(options)

    ## Get the mesh as a vtkUnstructuredGrid. 
    mesh = mesher.get_mesh()
    print("Mesh:");
    print("  Number of nodes: {0:d}".format(mesh.GetNumberOfPoints()))
    print("  Number of elements: {0:d}".format(mesh.GetNumberOfCells()))

    ## Write the mesh.
    mesher.write_mesh(file_name='cylinder-mesh.vtu')

## Show the mesh.
#
if True:
#if False:
    #mesh_polydata = gr.convert_ug_to_polydata(mesh)
    mesh_surface = mesher.get_surface()
    gr.add_geometry(renderer, mesh_surface, color=[1.0, 1.0, 1.0], wire=True, edges=True)
    #gr.add_geometry(renderer, mesh_polydata, color=[1.0, 1.0, 1.0], wire=False, edges=True)

    #mesh_model_polydata = mesher.get_model_polydata()
    #gr.add_geometry(renderer, mesh_model_polydata, color=[0.0, 1.0, 1.0], wire=True, edges=True)

    face1_polydata = mesher.get_face_polydata(1)
    gr.add_geometry(renderer, face1_polydata, color=[1.0, 0.0, 0.0], wire=False, edges=True)

    face2_polydata = mesher.get_face_polydata(2)
    gr.add_geometry(renderer, face2_polydata, color=[0.0, 1.0, 0.0], wire=False, edges=True)

    face3_polydata = mesher.get_face_polydata(3)
    gr.add_geometry(renderer, face3_polydata, color=[0.0, 0.0, 1.0], wire=False, edges=True)

    gr.display(renderer_window)
