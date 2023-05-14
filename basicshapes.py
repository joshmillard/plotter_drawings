#!/usr/bin/env python
#coding:utf-8

# let's goof with shit

try:
    import svgwrite
except ImportError:
    # if svgwrite is not 'installed' append parent dir of __file__ to sys.path
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import svgwrite
from svgwrite import cm, mm   

import random

def basic_shapes(name):
    dwg = svgwrite.Drawing(filename=name, size=("20cm","20cm"), debug=True)
    cir = dwg.add(dwg.g(id='circles', stroke='green', fill='none'))
    for y in range(21):
        for x in range(21):
            xc = x*cm
            yc = y*cm
            rc = (random.random()*0.25 + 0.25)
            while (rc > 0):
                cir.add(dwg.circle(center=(xc,yc), r=rc*cm ))
                rc -= 0.1
    dwg.save()


if __name__ == '__main__':
    basic_shapes('basic_shapes.svg')
