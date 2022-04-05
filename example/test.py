import os
import trimesh
import mesh2sdf
import numpy as np
import skimage.measure


filename = os.path.join(os.path.dirname(__file__), 'data', 'plane.obj')
mesh = trimesh.load(filename, force='mesh')

mesh_scale = 0.9
vertices = mesh.vertices
bbmin = vertices.min(0)
bbmax = vertices.max(0)
center = (bbmin + bbmax) * 0.5
scale = 2.0 * mesh_scale / (bbmax - bbmin).max()
vertices = (vertices - center) * scale

size = 128
sdf = mesh2sdf.compute(vertices, mesh.faces, size, fix=True, level=2/size)
v, f, _, _ = skimage.measure.marching_cubes(sdf, level=0)

v = v * (2.0 / size) - 1.0
v = v / scale + center
mesh = trimesh.Trimesh(vertices=v, faces=f)
mesh.export(filename[:-4] + '.fixed.obj')
np.save(filename[:-4] + '.npy', sdf)
