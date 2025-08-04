# tests for learning czi file data schema

using from pylibCZIrw import czi as pyczi

## SCHEMA when using pylibCZIrw:

#### T = Time -> (0, 1) 1 timepoint -> (index 0 only)

#### Z = Z-slice -> (0, 1) 1 depth slice -> (no 3D stack)

#### C = Channel -> (0, 2) 2 channels -> (indexes 0 and 1)

#### B = Block -> (0, 1) 1 pyramid -> resolution block (level 0 only)

#### X = Width -> (0, 21718) -> Image width: 21718 pixels

#### Y = Height -> (0, 1440) -> Image height: 1 440 pixels

## SCHEMA when using Czifile:

#### S = 1 → 1 scene

#### T = 10 → 10 timepoints

#### C = 3 → 3 channels

#### Z = 15 → 15 slices per volume

#### Y = 512 → height

#### X = 512 → width

## data storage

mydrive > code > biology
<br/>
<a href = "https://drive.google.com/drive/folders/1Eqcssc273RVy1VwyI8_q92myCDlL4ThM?usp=drive_link">location link</a>
