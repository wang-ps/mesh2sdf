import argparse
import matplotlib.pyplot as plt
import numpy as np
import skimage.measure
import trimesh

parser = argparse.ArgumentParser()
parser.add_argument('--filename', type=str, required=True)
parser.add_argument('--rescale', type=str, required=False, default='false')
args = parser.parse_args()

filename = args.filename
rescale = args.rescale.lower() == 'true'

# levels = [-0.2, -0.1, -0.05, -0.02, -0.01, 0.0, 0.01, 0.02, 0.05, 0.1, 0.2]
levels = [-0.01, 0.0, 0.01]


# marching cube
sdf = np.load(filename)
# sdf = sdf[::2, ::2, ::2]
size = sdf.shape[0]
if rescale:
  # sdf = (1- sdf) * 2 - 1  # !!! rescale SDF
  sdf = sdf * 2 - 1  # !!! rescale SDF

print(sdf.max(), sdf.min())

for i, level in enumerate(levels):
  vtx, faces, _, _ = skimage.measure.marching_cubes_lewiner(sdf, level)

  ## save to ply
  vtx = vtx * (2.0 / size) - 1.0
  mesh = trimesh.Trimesh(vtx, faces)
  mesh.export(filename[:-3] + 'l%.2f.obj' % level)

  # mesh = o3d.geometry.TriangleMesh()
  # mesh.vertices = o3d.utility.Vector3dVector(vtx)
  # mesh.triangles = o3d.utility.Vector3iVector(faces)
  # plyname = filename[:-4] + '_%02d_l%0.2f.ply' % (i, level)
  # o3d.io.write_triangle_mesh(plyname, mesh)


## draw image
for i in range(size):
  array_2d = sdf[i,:,:]

  num_levels = 6
  fig, ax = plt.subplots(figsize=(2.75, 2.75), dpi=300)
  levels_pos = np.logspace(-2, 0, num=num_levels)  # logspace
  levels_neg = -1. * levels_pos[::-1]
  levels = np.concatenate((levels_neg, np.zeros((0)), levels_pos), axis=0)
  colors = plt.get_cmap("Spectral")(np.linspace(0., 1., num=num_levels*2+1))

  sample = np.flipud(array_2d)
  CS = ax.contourf(sample, levels=levels, colors=colors)
  # cbar = fig.colorbar(CS)

  ax.contour(sample, levels=levels, colors='k', linewidths=0.1)
  ax.contour(sample, levels=[0], colors='k', linewidths=0.3)
  ax.axis('off')
  plt.savefig(filename + '.z.%03d.png' % i)
  # plt.show()