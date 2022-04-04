import os
import argparse
import trimesh
import trimesh.sample
import numpy as np
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('--root_folder', required=True, type=str)
parser.add_argument('--output_path', required=True, type=str)
parser.add_argument('--filelist', type=str, default='')
parser.add_argument('--samples', type=int, default=40000)
args = parser.parse_args()

if args.filelist:
  with open(args.filelist, 'r') as fid:
    lines = fid.readlines()
  filenames = [line.strip() for line in lines]
else:
  filenames = sorted(os.listdir(args.root_folder))

for filename in tqdm(filenames, ncols=80):
  filename_obj = os.path.join(args.root_folder, filename)
  filename_pts = os.path.join(args.output_path, filename[:-3] + 'npy')

  folder_pts = os.path.dirname(filename_pts)
  if not os.path.exists(folder_pts):
    os.makedirs(folder_pts)

  mesh = trimesh.load(filename_obj)
  points, idx = trimesh.sample.sample_surface(mesh, args.samples)
  normals = mesh.face_normals[idx]

  point_cloud = np.concatenate((points, normals), axis=-1).astype(np.float16)
  np.save(filename_pts, point_cloud)
