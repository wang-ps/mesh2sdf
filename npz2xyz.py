import sys
import numpy as np

filename = sys.argv[1]
# filename = 'C:/Users/penwan/Desktop/debug/d18592d9615b01bbbc0909d98a1ff2b4.npz'
data = np.load(filename)

xyz = data['xyz']
grad = data['grad']
sdf = data['sdf']

mask = np.abs(sdf) < 0.1

xyz = xyz.astype(np.float32) / 64.0 - 1.0
point_cloud = np.concatenate([xyz, grad, np.expand_dims(sdf, axis=-1)], axis=1)
np.savetxt(filename[:-3] + 'xyz', point_cloud[mask], fmt='%f')
