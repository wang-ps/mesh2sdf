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
# default='D:\\Projects\\LibGP\\Example\\RemovePieces\\x64\\Release\\DeletePiece.exe'
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
  filename_npy = os.path.join(args.output_path + '.npy', filename[:-3] + 'npy')

  path_obj = os.path.dirname(filename_sobj)
  if not os.path.exists(path_obj):
    os.makedirs(path_obj)
  path_raw = os.path.dirname(filename_robj)
  if not os.path.exists(path_raw):
    os.makedirs(path_raw)
  path_npy = os.path.dirname(filename_npy)
  if not os.path.exists(path_npy):
    os.makedirs(path_npy)

  # # load mesh and rescale mesh
  # mesh = trimesh.load(filename_in, force='mesh')
  # bbmin, bbmax = mesh.vertices.min(axis=0), mesh.vertices.max(axis=0)
  # center = (bbmin + bbmax) / 2.0
  # scale = 2.0 * mul / ((bbmax - bbmin).max() + 1.0e-6)
  # mesh = trimesh.Trimesh((mesh.vertices - center) * scale, mesh.faces)
  # mesh.export(filename_sobj)

  # # run sdfgen
  # cmds = [args.sdfgen, filename_sobj, str(2.0 / args.scale)]
  # cmd = ' '.join(cmds)
  # os.system(cmd)

  # # convert sdfgen to npy
  # # filename_npy = filename_obj[:-4] + '.npy'
  # filename_sdf = filename_sobj[:-4] + '.sdf'
  # sdf = np.fromfile(filename_sdf, dtype=np.float32)
  # sdf = np.reshape(sdf, [args.scale] * 3)
  # sdf = np.transpose(sdf, (2, 1, 0))
  # # np.save(filename_npy, sdf)
  # os.remove(filename_sdf)

  # # extract mesh
  # vtx, faces, _, _ = skimage.measure.marching_cubes_lewiner(sdf, args.level)
  # vtx = vtx * (2.0 / args.scale) - 1.0
  # mesh = trimesh.Trimesh(vtx, faces)
  # mesh.export(filename_robj)

  # # keep the max component of the extracted mesh -> get filename_nobj
  # input_folders = args.output_path + '.raw'
  # output_path = args.output_path + '.new'
  # folders = os.listdir(input_folders)
  # for folder in folders:
  #   filenames = os.path.join(input_folders, folder, '*.obj')
  #   output_path = os.path.join(output_path, folder)
  #   if not os.path.exists(output_path):
  #     os.makedirs(output_path)
  #   cmds = [args.pieces, '--filenames', filenames, '--output_path', output_path]
  #   cmd = ' '.join(cmds)
  #   os.system(cmd)

  # run sdfgen
  cmds = [args.sdfgen, filename_nobj, str(2.0 / args.scale)]
  cmd = ' '.join(cmds)
  os.system(cmd)

  # convert sdfgen to npy
  filename_sdf = filename_nobj[:-4] + '.sdf'
  sdf = np.fromfile(filename_sdf, dtype=np.float32)
  sdf = np.reshape(sdf, [args.scale] * 3)
  sdf = np.transpose(sdf, (2, 1, 0))
  np.save(filename_npy, sdf)
  os.remove(filename_sdf)