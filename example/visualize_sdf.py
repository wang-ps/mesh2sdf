import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import skimage.measure
import trimesh

filename = sys.argv[1] if len(sys.argv) > 1 else  \
    os.path.join(os.path.dirname(__file__), 'data', 'plane.npy')

mesh_scale = 0.8
levels = [-0.02, 0.0, 0.02]

folder = filename[:-4]
if not os.path.exists(folder):
  os.makedirs(folder)

sdf = np.load(filename)
size = sdf.shape[0]
print(sdf.max(), sdf.min())

# extract level sets
for i, level in enumerate(levels):
  vtx, faces, _, _ = skimage.measure.marching_cubes(sdf, level)

  vtx = vtx * (mesh_scale * 2.0 / size) - 1.0
  mesh = trimesh.Trimesh(vtx, faces)
  mesh.export(os.path.join(folder, 'l%.2f.obj' % level))


# draw image
for i in range(size):
  array_2d = sdf[:, :, i]

  num_levels = 6
  fig, ax = plt.subplots(figsize=(2.75, 2.75), dpi=300)
  levels_pos = np.logspace(-2, 0, num=num_levels)  # logspace
  levels_neg = -1. * levels_pos[::-1]
  levels = np.concatenate((levels_neg, np.zeros((0)), levels_pos), axis=0)
  colors = plt.get_cmap("Spectral")(np.linspace(0., 1., num=num_levels*2+1))

  sample = array_2d
  # sample = np.flipud(array_2d)
  CS = ax.contourf(sample, levels=levels, colors=colors)

  ax.contour(sample, levels=levels, colors='k', linewidths=0.1)
  ax.contour(sample, levels=[0], colors='k', linewidths=0.3)
  ax.axis('off')

  plt.savefig(os.path.join(folder, '%03d.png' % i))
  # plt.show()
