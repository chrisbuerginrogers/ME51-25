from openpiv import tools, validation, filters, scaling, pyprocess
import numpy as np
import matplotlib.pyplot as plt

#basePath = '/Users/crogers/GitHub/ME51-25/PIV/odd_flow'
basePath = '/Users/crogers/GitHub/ME51-25/PIV/steady_flow'
frame_a = tools.imread(basePath+'/frame_0_delay-0.14s.png')
frame_b = tools.imread(basePath+'/frame_1_delay-0.14s.png')

fig, ax = plt.subplots(1, 2, figsize=(10, 8))
ax[0].imshow(frame_a, cmap=plt.cm.gray)
ax[1].imshow(frame_b, cmap=plt.cm.gray)

# Add titles to make it clearer
ax[0].set_title('Frame A')
ax[1].set_title('Frame B')

winsize = 32 # pixels, interrogation window size in frame A
searchsize = 38  # pixels, search area size in frame B
overlap = 17 # pixels, 50% overlap
dt = 0.02 # sec, time interval between the two frames

u0, v0, sig2noise = pyprocess.extended_search_area_piv(
    frame_a.astype(np.int32),
    frame_b.astype(np.int32),
    window_size=winsize,
    overlap=overlap,
    dt=dt,
    search_area_size=searchsize,
    sig2noise_method='peak2peak',
)

x, y = pyprocess.get_coordinates(
    image_size=frame_a.shape,
    search_area_size=searchsize,
    overlap=overlap,
)

invalid_mask = validation.sig2noise_val(
    sig2noise,
    threshold = 1.05,
)
u2, v2 = filters.replace_outliers(
    u0, v0,
    invalid_mask,
    method='localmean',
    max_iter=3,
    kernel_size=3,
)

# convert x,y to mm
# convert u,v to mm/sec

x, y, u3, v3 = scaling.uniform(
    x, y, u2, v2,
    scaling_factor = 96.52,  # 96.52 pixels/millimeter
)

# 0,0 shall be bottom left, positive rotation rate is counterclockwise
x, y, u3, v3 = tools.transform_coordinates(x, y, u3, v3)

tools.save(basePath+'/exp1_001.txt' , x, y, u3, v3, invalid_mask)

fig, ax = plt.subplots(figsize=(8,8))
tools.display_vector_field(
    basePath+'/exp1_001.txt',
    ax=ax, scaling_factor=96.52,
    scale=50, # scale defines here the arrow length
    width=0.0035, # width is the thickness of the arrow
    on_img=True, # overlay on the image
    image_name= basePath+'/frame_0_delay-0.14s.png'
);

try:
    plt.show()
except:
    pass
