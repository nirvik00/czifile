# write files
import os
import itertools as it
import cv2
import numpy as np
from pylibCZIrw import czi as pyczi
from skimage import data
data = data.kidney()

print(f'num of dims = {data.ndim}')
print(f'shape = {data.shape}')
print(f'dtype = {data.dtype}')

newczi_4dstack = os.path.join("data", "newCZI_z=16_ch=3.czi")
numCh = 3
numZ=16

with pyczi.create_czi(newczi_4dstack) as czidoc_w:
    for z, ch in it.product(range(numZ), range(numCh)):
        array2d = data[z, ..., ch][..., np.newaxis]# get the 2d array for the current plane and add axis to get (Y, X, 1) as shape
        czidoc_w.write(
            data=array2d,
            plane={"Z": z, "C": ch}
        ) # write the plane with shape (Y, X, 1) to the new CZI file

