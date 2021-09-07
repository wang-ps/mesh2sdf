import os
import sys
import numpy as np
import skimage.measure
import trimesh

filename = 'C:/Users/penwan/Desktop/debug/car/100715345ee54d7ae38b52b4ee9d36a3.obj'
sdfgen = 'D:/Projects/SDFGen/build/bin/Release/SDFGen.exe'

level = 0.015
scale = 128
filename_sdf = filename[:-3] + 'sdf'
filename_obj = filename[:-3] + 'new.1.obj'
filename_npy = filename[:-3] + 'npy'


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
vtx, faces, _, _ = skimage.measure.marching_cubes_lewiner(sdf, level)
vtx = vtx * (2.0 / scale) - 1.0
mesh = trimesh.Trimesh(vtx, faces)

mesh.export(filename_obj)