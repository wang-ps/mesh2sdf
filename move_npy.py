import os

folder_in = 'E:/penwan/ShapeNetCore.v1/mesh.0830.new/02691156'
folder_out = 'E:/penwan/ShapeNetCore.v1/mesh.0830.npy/02691156'

os.makedirs(folder_out)

filenames = os.listdir(folder_in)
for filename in filenames:
  if filename.endswith('.npy'):
    filename_in = os.path.join(folder_in, filename)
    filename_out = os.path.join(folder_out, filename)

    os.rename(filename_in, filename_out)
    print(filename_in)
