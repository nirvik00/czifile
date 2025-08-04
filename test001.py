from czifile import CziFile
import numpy as np
import matplotlib.pyplot as plt


def show_image(image_data):
    # Show the first 2D image (simplest case)
    plt.imshow(image_data[0, 0, 0, 0, 0, :, :, 0], cmap='gray')
    plt.title('First image slice')
    plt.show()


fn="C:\\Users\\nsdev\code\\biology\\MouseBrain_41Slices_1Tile_3Channel_2Illuminations_2Angles.czi"

# # Load a CZI file
# with CziFile(fn) as czi:
#     image_data = czi.asarray()

with CziFile(fn) as czi:
    print("Axes:", czi.axes)        # e.g., 'STCZYX'
    print("Shape:", czi.shape)      # matches axes
    # print("Metadata:", czi.metadata())  # returns XML metadata as string


