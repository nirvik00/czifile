from czifile import CziFile
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()

##
from pylibCZIrw import czi as pyczi
import json
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os, sys
from tqdm import tqdm
from tqdm.contrib import itertools as it
from matplotlib.patches import Rectangle
from lxml import etree

# show the used python env
print("Using:", sys.executable)
fn_mouse ="data/MouseBrain_41Slices_1Tile_3Channel_2Illuminations_2Angles.czi"
fn_stacks= os.path.join("data", r"T=3_Z=5_CH=2_X=240_Y=170.czi") # 5d-stack
fn_scenes = os.path.join("data", r"w96_A1+A2.czi") # scene file


def show_image(image_data):
    # Show the first 2D image (simplest case)
    plt.imshow(image_data[0, 0, 0, 0, 0, :, :, 0], cmap='gray')
    plt.title('First image slice')
    plt.show()


def read_czi_file_xml():
    with CziFile(fn_stacks) as czi:
        print("Axes:", czi.axes)        # 'STCZYX'
        print("Shape:", czi.shape)      # matches axes
        print("Metadata:", czi.metadata())  # returns XML metadata as string

def recursive_dict_parser(obj, counter=0):
    print(f"\n\n --->{counter}-->")
    counter+=1
    if not isinstance(obj, dict):
        return
    else:
        for k, v in obj.items():
            print(k)
            recursive_dict_parser(v, counter)

def read_czi_file_json():
    with pyczi.open_czi(fn_stacks) as czi_doc:
        md_dict = czi_doc.metadata
    # print(json.dumps(md_dict, indent=4))   
    for key, values in md_dict["ImageDocument"]["Metadata"].items():
        print(key)
    print(json.dumps(md_dict["ImageDocument"]["Metadata"]["Information"]["Image"], sort_keys=False, indent=4))


def get_img_dims():
    with pyczi.open_czi(fn_stacks) as czidoc:
        b_total = czidoc.total_bounding_box
    print(f'size of total {b_total}')
    #
    with pyczi.open_czi(fn_scenes) as czidoc:
        b_scene = czidoc.scenes_bounding_rectangle
    print(f'size of scenes: {b_scene}')
    #
    with pyczi.open_czi(fn_mouse) as czidoc:
        b2_total = czidoc.total_bounding_rectangle
        b2_scene = czidoc.scenes_bounding_rectangle
    print(f'size of mouse scenes: {b2_scene}, {b2_total}')


def get_channel_pixel_types():
    with pyczi.open_czi(fn_scenes) as czidoc:
        c0_pixel_type= czidoc.get_channel_pixel_type(0)
        pixel_type = czidoc.pixel_types
    print(c0_pixel_type)
    print(pixel_type)


def get_image():
    fn = [fn_stacks, fn_mouse]
    with pyczi.open_czi(fn[0]) as czidoc:    
        plane_1 = {'C': 0, 'Z': 2, 'T': 1}# define some plane coordinates
        plane_2 = {'C': 1, 'Z': 3, 'T': 2}# define some plane coordinates
        frame_0 = czidoc.read() # equivalent to reading {'C': 0, 'Z': 0, 'T': 0}
        # get the shape of the 2d plane - the last dime indicates the pixel type
        print("Array Shape: ", frame_0.shape) # 3 = BGR and 1 = Gray
        frame_1 = czidoc.read(plane=plane_1) # get specific planes 
        frame_2 = czidoc.read(plane=plane_2) # get specific planes 

    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].imshow(frame_0[..., 0], cmap=cm.inferno)
    ax[0].set_title("Frame_0")
    ax[1].imshow(frame_1[..., 0], cmap=cm.inferno)
    ax[1].set_title("Frame_1")
    ax[2].imshow(frame_2[..., 0], cmap=cm.Greens_r)
    ax[2].set_title("Frame_2")
    plt.show()

def get_img_roi():
    fn = [fn_stacks, fn_scenes, fn_mouse]
    my_roi = (200, 400, 800, 600)
    with pyczi.open_czi(fn[1]) as czidoc:
        ch0 = czidoc.read(roi=my_roi, plane={'C': 0})
        ch1 = czidoc.read(roi=my_roi, plane={'C': 1})
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(ch0[..., 0], cmap=cm.inferno, vmin=100, vmax=4000)
    ax[0].set_title("ch0")
    ax[1].imshow(ch1[..., 0], cmap=cm.Greens_r, vmin=100, vmax=4000)
    ax[1].set_title("ch1")
    plt.show()

def get_img_roi_scenes():
    fn = [fn_stacks, fn_scenes, fn_mouse]
    with pyczi.open_czi(fn[1]) as czidoc:
        print(czidoc.total_bounding_box)
        print(czidoc.scenes_bounding_rectangle)
        if len(czidoc.scenes_bounding_rectangle.keys()) > 0:
            c0_s0 = czidoc.read(plane={'C': 0}, scene=0)
            c1_s0 = czidoc.read(plane={'C': 1}, scene=0)
            c0_s1 = czidoc.read(plane={'C': 0}, scene=1)
            c1_s1 = czidoc.read(plane={'C': 1}, scene=1)
        else:
            print('no scenes')
            return
    fig, ax = plt.subplots(2,2, figsize=(16, 16))
    ax[0,0].imshow(c0_s0[...,0], cmap=cm.inferno, vmin=100, vmax=4000)
    ax[0,0].set_title('scene:0, channel=0')

    ax[0,1].imshow(c1_s0[...,0], cmap=cm.Greens_r, vmin=100, vmax=4000)
    ax[0,1].set_title('scene:0, channel=1')
    
    ax[1,0].imshow(c0_s1[...,0], cmap=cm.inferno, vmin=100, vmax=4000)
    ax[1,0].set_title('scene:0, channel=0')
    
    ax[1,1].imshow(c1_s1[...,0], cmap=cm.Greens_r, vmin=100, vmax=4000)
    ax[1,1].set_title('scene:1, channel=1')
    plt.show()

def get_img_roi_NO_scenes():
    fn = [fn_stacks, fn_scenes, fn_mouse]
    with pyczi.open_czi(fn[2]) as czidoc:
        print(czidoc.total_bounding_box)
        print(czidoc.scenes_bounding_rectangle)
        c0 = czidoc.read(plane={'C': 0})
        c1 = czidoc.read(plane={'C': 1})
        c2 = czidoc.read(plane={'C': 2})
    fig, ax = plt.subplots(2,2, figsize=(16, 16))
    ax[0,0].imshow(c0[...,0], cmap=cm.inferno, vmin=100, vmax=4000)
    ax[0,1].imshow(c1[...,0], cmap=cm.Greens_r, vmin=100, vmax=4000)
    ax[1,0].imshow(c2[...,0], cmap=cm.Greens_r, vmin=100, vmax=4000)
    ax[0,0].set_title('scene:0, channel=0')
    ax[0,1].set_title('scene:0, channel=1')
    ax[1,0].set_title('scene:0, channel=2')
    plt.show()

# read_czi_file_xml()
# read_czi_file_json()
# get_img_dims()
# get_channel_pixel_types()
# get_image()
# get_img_roi()
get_img_roi_scenes()
# get_img_roi_NO_scenes()

