import os
import sys
import numpy as np
import skimage.measure
import trimesh

filename = 'E:/room5.obj'
sdfgen = 'D:/Projects/SDFGen/build/bin/Release/SDFGen.exe'

# level = 0.015
level = 0.005
scale = 512
filename_sdf = filename[:-3] + 'sdf'
filename_obj = filename[:-3] + 'new.1.obj'
filename_npy = filename[:-3] + 'npy'

# rescale mesh
mesh = trimesh.load(filename, force='mesh')
vertices = mesh.vertices

bbmin = vertices.min(axis=0)
bbmax = vertices.max(axis=0)
center = (bbmin + bbmax) * 0.5
vertices = (vertices - center) * (0.9 * 2 / (bbmax - bbmin).max())
mesh.vertices = vertices
mesh.export(filename)


# run sdfgen
cmds = [sdfgen, filename, str(2.0 / scale)]
cmd = ' '.join(cmds)
os.system(cmd)

# convert sdfgen to npy
sdf = np.fromfile(filename_sdf, dtype=np.float32)
sdf = np.reshape(sdf, [scale] * 3)
sdf = np.transpose(sdf, (2, 1, 0))
sdf = np.abs(sdf)
np.save(filename_npy, sdf)
# os.remove(filename_sdf)


# extract mesh
sdf = np.load(filename_npy)
vtx, faces, _, _ = skimage.measure.marching_cubes_lewiner(sdf, level)
vtx = vtx * (2.0 / scale) - 1.0
mesh = trimesh.Trimesh(vtx, faces)

mesh.export(filename_obj)