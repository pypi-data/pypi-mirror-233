<!--
SPDX-FileCopyrightText: 2019,2020 Freemelt AB

SPDX-License-Identifier: Apache-2.0
-->

# OBPlib-Python
Python library to generate OBP data for metal 3d printers.

## Minimum example
Create two points and a set of beam parameters. Create a line with these params and a speed. Write as binary and textual OBP data to files. 

```
import obplib as obp

a = obp.Point(1,1)
b = obp.Point(2,2)

bp = obp.Beamparameters(1,1)

line = obp.Line(a,b,1,bp)

obp.write_obpj([line], "test.obpj")
obp.write_obp([line], "test.obp")
```

# OBP-compiler (obpc)
This package contains the obpc tool that can convert back and forth between binary and textual OBP. 

# Viewer
![obpviewer](/uploads/0144f0b0756bf3a14c7a84f54e757786/obpviewer.gif)

Usage:

```
usage: obpviewer.py [-h] [--slice-size SLICE_SIZE] [--index INDEX] obp_file

Use the mouse or keyboard to navigate.

supported objects:
  Line, AcceleratingLine, Curve, AcceleratingCurve,
  Restore and SyncPoint.

not supported:
  TimedPoints, Metadata and vendor_setup.

keyboard shortcuts:

  right        step forward
  shift+right  step forward 10 steps
  ctrl+right   step forward 100 steps
  alt+right    step forward 1000 steps

  left         step backward
  shift+left   step backward 10 steps
  ctrl+left    step backward 100 steps
  alt+left     step backward 1000 steps

  p            same as right
  n            same as left

  a            jump to start of file
  e            jump to end of file

  s            jump to spot size change
  b            jump to beam power change
  r            jump to restore point

  0-9          jump to sync point change (digit specifies
               sync point: 1st, 2nd, ..., etc)

positional arguments:
  obp_file              Path to obp file.

optional arguments:
  -h, --help            show this help message and exit
  --slice-size SLICE_SIZE
                        Initial slice size (default: 100).
  --index INDEX         Initial index (default: 100).
```
