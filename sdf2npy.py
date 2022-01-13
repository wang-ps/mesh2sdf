import os
import argparse
import trimesh
import numpy as np
from tqdm import tqdm
import skimage.measure


parser = argparse.ArgumentParser()
parser.add_argument('--root_folder', required=True, type=str)
parser.add_argument('--filelist', required=True, type=str)
parser.add_argument('--output_path', required=True, type=str)
parser.add_argument('--scale', type=float, default=128)
parser.add_argument('--level', type=float, default=0.015)  # 2/128 = 0.015625
parser.add_argument('--start', type=int, default=0)
parser.add_argument('--end', type=int, default=57449)
parser.add_argument('--sdfgen', type=str,
                    default='build\\bin\\Release\\SDFGen.exe')
parser.add_argument('--pieces', type=str,
                    default='extract_pieces')
args = parser.parse_args()
mul = 0.8

with open(args.filelist, 'r') as fid:
  lines = fid.readlines()
filenames = [line.split()[0] for line in lines]

for filename in tqdm(filenames[args.start:args.end], ncols=80):
  filename_in = os.path.join(args.root_folder, filename)
  filename_sobj = os.path.join(args.output_path + '.scale', filename)
  filename_robj = os.path.join(args.output_path + '.raw', filename)
  filename_nobj = os.path.join(args.output_path + '.new', filename)
  filename_bbox = os.path.join(args.output_path + '.bbox', filename[:-3] + 'npy')
  filename_npy  = os.path.join(args.output_path + '.npy', filename[:-3] + 'npy')

  path_obj = os.path.dirname(filename_sobj)
  if not os.path.exists(path_obj):
    os.makedirs(path_obj)
  path_raw = os.path.dirname(filename_robj)
  if not os.path.exists(path_raw):
    os.makedirs(path_raw)
  path_new = os.path.dirname(filename_nobj)
  if not os.path.exists(path_new):
    os.makedirs(path_new)
  path_npy = os.path.dirname(filename_npy)
  if not os.path.exists(path_npy):
    os.makedirs(path_npy)
  path_bbox = os.path.dirname(filename_bbox)
  if not os.path.exists(path_bbox):
    os.makedirs(path_bbox)

  # load mesh and rescale mesh to [-1, 1], note the factor **mul**
  mesh = trimesh.load(filename_in, force='mesh')
  bbmin, bbmax = mesh.vertices.min(axis=0), mesh.vertices.max(axis=0)
  center = (bbmin + bbmax) / 2.0
  scale = 2.0 * mul / ((bbmax - bbmin).max() + 1.0e-6)
  mesh = trimesh.Trimesh((mesh.vertices - center) * scale, mesh.faces)
  mesh.export(filename_sobj)

  # save bbmin and bbmax
  np.savez(filename_bbox, bbmax=bbmax, bbmin=bbmin, mul=mul)

  # run sdfgen
  cmds = [args.sdfgen, filename_sobj, str(2.0 / args.scale)]
  cmd = ' '.join(cmds)
  print(cmd)
  os.system(cmd)

  # convert sdfgen to npy
  filename_sdf = filename_sobj[:-4] + '.sdf'
  sdf = np.fromfile(filename_sdf, dtype=np.float32)
  sdf = np.reshape(sdf, [args.scale] * 3)
  sdf = np.transpose(sdf, (2, 1, 0))
  sdf = np.abs(sdf)  # !!! Note: the negative value is not reliable !!!
  os.remove(filename_sdf)

  # extract mesh
  vtx, faces, _, _ = skimage.measure.marching_cubes_lewiner(sdf, args.level)
  vtx = vtx * (2.0 / args.scale) - 1.0
  mesh = trimesh.Trimesh(vtx, faces)
  mesh.export(filename_robj)

  # keep the max component of the extracted mesh -> get filename_nobj
  cmds = [args.pieces, '--filename', filename_robj, '--output_path', path_new]
  cmd = ' '.join(cmds)
  print(cmd)
  os.system(cmd)

  # run sdfgen
  cmds = [args.sdfgen, filename_nobj, str(2.0 / args.scale)]
  cmd = ' '.join(cmds)
  print(cmd)
  os.system(cmd)

  # convert sdfgen to npy
  filename_sdf = filename_nobj[:-4] + '.sdf'
  sdf = np.fromfile(filename_sdf, dtype=np.float32)
  sdf = np.reshape(sdf, [args.scale] * 3)
  sdf = np.transpose(sdf, (2, 1, 0))
  np.save(filename_npy, sdf)
  os.remove(filename_sdf)
