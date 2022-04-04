import trimesh
import mesh2sdf
import skimage.measure

filename = 'C:/Users/penwan/Desktop/bunny.off'
mesh = trimesh.load(filename, force='mesh')

vertices = mesh.vertices
bbmin = vertices.min(0)
bbmax = vertices.max(0)
center = (bbmin + bbmax) * 0.5
scale = 1.8 / (bbmax - bbmin).max()
vertices = (vertices - center) * scale

size = 128
sdf = mesh2sdf.compute(vertices, mesh.faces, size, fix=True, level=2/size)
v, f, _, _ = skimage.measure.marching_cubes(sdf, level=0)

v = v * (2.0 / size) - 1.0
v = v / scale + center
mesh = trimesh.Trimesh(vertices=v, faces=f)
mesh.export(filename[:-4] + '.out.off')
