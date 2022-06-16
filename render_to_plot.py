import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as image
from matplotlib.widgets import Slider

#lacking_3d_version = np.loadtxt("lor_rendering/500000_3cyl.data") MEDDLED
lacking_3d_version = np.loadtxt("testrender.data") #use the right file name for your purposes

third_dim_size = 1

print(np.shape(lacking_3d_version))

#reshaped = np.reshape(np.ravel(lacking_3d_version), (400,400,400)) MEDDLED
reshaped = np.reshape(np.ravel(lacking_3d_version), (400,400,1))

print(np.shape(reshaped))
# print(reshaped[0,2,399])

# smoothed = image.gaussian_filter(reshaped, 3)

#slice = 210 MEDDLED
slice = 0

mid_slice = reshaped[:,:,slice]

# smoothed_slice = smoothed[:,:,slice]

fig, ax = plt.subplots()
# fig, ay = plt.subplots()

# axslice = plt.axes([0.25, 0.1, 0.65, 0.03])
# slice_slider = Slider(
#     ax=axslice,
#     label='Layer',
#     valmin=0,
#     valmax=399,
#     valinit=200,
# 	valfmt='%i'
# )

# def update(val):
# 	ax.imshow(reshaped[:,:,slice_slider.val])

ax.imshow(mid_slice)

# slice_slider.on_changed(update)

# ay.imshow(smoothed_slice)

plt.show()
