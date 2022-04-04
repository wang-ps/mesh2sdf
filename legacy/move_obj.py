import os

folder_in = 'E:/penwan/02691156/02691156'
folder_out = 'E:/penwan/02691156_out'

os.makedirs(folder_out)

filenames = os.listdir(folder_in)
for filename in filenames:
  src_name = os.path.join(folder_in, filename, 'model.obj')
  des_name = os.path.join(folder_out, filename + '.obj')
  if os.path.exists(src_name):    
    os.rename(src_name, des_name)
    print(src_name)
