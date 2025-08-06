from skimage import io
import matplotlib.pyplot as plt


# read the image stack
img = io.imread('a_image.tif')
# show the image
plt.imshow(img,cmap='gray')
plt.axis('off')
# save the image
plt.savefig('output.tif', transparent=True, dpi=300, bbox_inches="tight", pad_inches=0.0)