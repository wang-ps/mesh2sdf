import os
import numpy as np

filename_list = 'D:/Paper/DualOCNN/data/ae.metric/all_test_im.txt'
root_folder = 'E:/penwan/ShapeNetCore.v1/0907.mesh.bbox'
filename_out = 'D:/Paper/DualOCNN/data/ae.metric/all_test_im_scale.csv'

with open(filename_list, 'r') as fid:
  lines = fid.readlines()
filenames = [line.split()[0] for line in lines]

with open(filename_out, 'w') as fid:
  for filename in filenames:
    full_name = os.path.join(root_folder, filename + '.npy.npz')
    bbox = np.load(full_name)
    scale = 2.0 * bbox['mul'] / ((bbox['bbmax'] - bbox['bbmin']).max() + 1.0e-6)
    fid.write('{}, {}\n'.format(filename, scale))
