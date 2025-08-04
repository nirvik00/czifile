# tests for learning czi file data schema

using from pylibCZIrw import czi as pyczi

## SCHEMA when using pylibCZIrw:

T = Time -> (0, 1) 1 timepoint -> (index 0 only)<br/>
Z = Z-slice -> (0, 1) 1 depth slice -> (no 3D stack)<br/>
C = Channel -> (0, 2) 2 channels -> (indexes 0 and 1)<br/>
B = Block -> (0, 1) 1 pyramid -> resolution block (level 0 only)<br/>
X = Width -> (0, 21718) -> Image width: 21718 pixels<br/>
Y = Height -> (0, 1440) -> Image height: 1 440 pixels<br/>

## SCHEMA when using Czifile:

S = 1 → 1 scene <br/>
T = 10 → 10 timepoints <br/>
C = 3 → 3 channels <br/>
Z = 15 → 15 slices per volume <br/>
Y = 512 → height <br/>
X = 512 → width <br/>

## data storage

mydrive > code > biology
<br/>
<a href = "https://drive.google.com/drive/folders/1Eqcssc273RVy1VwyI8_q92myCDlL4ThM?usp=drive_link">location link</a>
