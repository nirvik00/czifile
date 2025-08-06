from fastapi import FastAPI, HTTPException, APIRouter, Path, Query
from pydantic import BaseModel
import os
import pathlib
import cv2
from pylibCZIrw import czi as pyczi
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import base64
router = APIRouter(prefix='/fileops', tags=['file operations'])


@router.get('/')
def init():
    return {"msg": "file operations"}


class FileRequest(BaseModel):
    file_path: str


@router.get('/read_data_from_file')
async def read_data_from_file(file_path: str = Query(..., description="Windows path to file")):
    file_path = file_path.strip('"')
    fn = file_path
    print(fn)
    try:
        bbx = None
        with pyczi.open_czi(fn) as czidoc:
            print("bbx:", czidoc.total_bounding_box)        # e.g., 'STCZYX'
            bbx = czidoc.total_bounding_box
        return {"msg": "filepath", "bbx": bbx}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"input path error\n{e}")
