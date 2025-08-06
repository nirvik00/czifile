# write files
import os
import itertools as it
import cv2
import numpy as np
from pylibCZIrw import czi as pyczi
from skimage import data, io
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import imageio
import datetime
import time


def write_czi():
    data = data.kidney()
    print(f'num of dims = {data.ndim}')
    print(f'shape = {data.shape}')
    print(f'dtype = {data.dtype}')
    newczi_4dstack = os.path.join("data", "newCZI_z=16_ch=3.czi")
    numCh = 3
    numZ = 16
    with pyczi.create_czi(newczi_4dstack) as czidoc_w:
        for z, ch in it.product(range(numZ), range(numCh)):
            # get the 2d array for the current plane and add axis to get (Y, X, 1) as shape
            array2d = data[z, ..., ch][..., np.newaxis]
            czidoc_w.write(
                data=array2d,
                plane={"Z": z, "C": ch}
            )  # write the plane with shape (Y, X, 1) to the new CZI file


def show_img_z_stack():
    fn = os.path.join(os.getcwd(), "data")
    fn = os.path.join(fn, "newCZI_z=16_ch=3.czi")
    fig, ax = plt.subplots(4, 4, figsize=(16, 16))
    with pyczi.open_czi(fn) as czidoc:
        print(czidoc.total_bounding_box)
        print(czidoc.scenes_bounding_rectangle)
        count = 0
        for i in range(4):
            for j in range(4):
                # change channel here
                img = czidoc.read(plane={'Z': count, 'C': 1})
                cv2.imwrite(f'output/img{count}.png', img)
                ax[i][j].imshow(img, cmap=cm.inferno, vmin=100, vmax=4000)
                # ax[i][j].imshow(img, cmap=cm.Greens_r, vmin=100, vmax=4000)
                ax[i][j].set_title(f'z={count}')
                count += 1
    plt.show()


def get_write_imgs_z_stack():
    fn = os.path.join(os.getcwd(), "data")
    fn = os.path.join(fn, "newCZI_z=16_ch=3.czi")
    with pyczi.open_czi(fn) as czidoc:
        print(czidoc.total_bounding_box)
        print(czidoc.scenes_bounding_rectangle)
        count = 0
        for i in range(4):
            for j in range(4):
                img = czidoc.read(plane={'Z': count, 'C': 1})
                plt.imshow(img, cmap=cm.inferno, vmin=100, vmax=4000)
                plt.savefig(f'output/img{count}')
                count += 1

    img_folder = 'output'
    files = [f for f in os.listdir(img_folder) if f.lower().endswith('.png')]
    print(len(files))
    # frames=[]
    # for file in files:
    #     img = cv2.imread(file)
    #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     frames.append(img_rgb)
    # imageio.mimsave("output.gif", frames, duration=200, loop=0)


def get_gif_img():
    fn = os.path.join(os.getcwd(), "data")
    # fn = os.path.join(fn, "newCZI_z=16_ch=3.czi")
    img_folder = 'output'
    files = [f for f in os.listdir(img_folder) if f.lower().endswith('.png')]
    frames = []
    for file in files:
        img = cv2.imread(os.path.join(img_folder, file))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frames.append(img_rgb)
    imageio.mimsave("output.gif", frames, duration=1, loop=0)


# write_czi()
# show_img_z_stack()
# get_write_imgs_z_stack()
# get_gif_img()

def read_gen_gif():
    fn = os.path.join(os.getcwd(), "data")
    fn = os.path.join(fn, "newCZI_z=16_ch=3.czi")  # input filename
    output_dir = "new_output2"
    try:
        os.mkdir(os.path.join(os.getcwd(), output_dir))
    except:
        pass  # output_dir exists
    with pyczi.open_czi(fn) as czidoc:
        print(czidoc.total_bounding_box)
        z_num = czidoc.total_bounding_box['Z'][1]
        for i in range(z_num):
            img = czidoc.read(plane={'Z': i, 'C': 1})
            plt.imshow(img, cmap=cm.inferno, vmin=100, vmax=4000)
            plt.savefig(f'{output_dir}/img{i}.png')

        files = [f for f in os.listdir(
            output_dir) if f.lower().endswith('.png')]
        frames = []
        for file in files:
            img = cv2.imread(os.path.join(output_dir, file))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frames.append(img_rgb)
        imageio.mimsave(f"{output_dir}/output.gif", frames, duration=1, loop=0)


read_gen_gif()
