# cortexdraw.py - a collection of self-contained higher-level drawing routines using the cortexlib library

import numpy as np
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

from cortexlib import *



# draw a series of hatches on a square grid normal to and proportional dense farther from a centerpoint
# - note: this absolutely eats shit if cx or cy is an integer value, needs some extra checks to avoid taht
#   issue
def draw_pooloflight(width,height,step,cx=.1,cy=.1):
    patches = []
    squareg = getsquaregrid(width,height,step)
    a = 0

    for i in range(len(squareg)):
        for j in range(len(squareg[i])):
            dx = i-cx
            dy = j-cy
            a = math.atan(dy/dx) + math.pi/2
            lines = crophatch(squareg[i][j],a,4/math.sqrt(dx**2 + dy**2))
            for l in lines:
                l = jitter(l,1,True)
                l = perlinize(l[0],l[-1],5,.1)
                patches.append(mpatches.Polygon(l,closed=False,fill=None,color="black"))
    return patches

# draw a gradient of circuitously-hatched tiles with hatching density increasing toward the top right
def draw_circuitgradient(width,height,step):
    patches = []
    squareg = getsquaregrid(width,height,step)

    for i in range(len(squareg)):
        for j in range(len(squareg[i])):
            lines = circuitpolyline(squareg[i][j],int((i+j)**1.1 + 2))
            for l in lines:
                patches.append(mpatches.Polygon(l,closed=False,fill=None,color="black"))
    return patches

# draw a grid of squares
def draw_grid(width,height,step):
    patches = []
    squareg = getsquaregrid(width,height,step)

    for i in range(len(squareg)):
        for j in range(len(squareg[i])):
            patches.append(mpatches.Polygon(squareg[i][j],closed=True,fill=None,color="black"))
    return patches

# draw a line thing
def draw_linebranch(width,height,numlines):
    patches = []
    lines = []
    startx = width*.4
    endx = width*.6
    step = (endx - startx)/numlines
    for i in range(numlines):
        bend = (random.random() * 0.5 + 0.3) * height
        drop = (random.random() * 0.2) * height
        xoff = (height-bend)*0.8
        if(random.random() > 0.5): xoff *= -1
        x = startx + step*i + (random.random() - 0.5)*step
        lines.append([[x,0],[x,bend],[x-xoff, bend], [x-xoff, bend-drop]])

    for l in lines:
#        l = divide(l,4)
        l = jitter(l,1)
        for i in range(len(l)-1):
            newl = perlinize(l[i],l[i+1], 8,0.02 *(i**2+1))
            patches.append(mpatches.Polygon(newl,closed=False,fill=None))
    return patches

# draw a checkerboard of hatches
def draw_checkerhatch(width,height,step):
    patches = []
    grid = getsquaregrid(width,height,step)
    x = width / 2 - 0.49
    y = height / 2 - 0.49
    for i in range(len(grid)):
        for j in range(len(grid[i])):
#            angle = random.random()*.2*math.pi
#            density = random.random()/2 + 0.25
            angle = random.random() * math.pi
#            density = 0.25 +  (random.random()+0.5)*(i+j+1)*0.1

            density = 0.15 + math.sqrt((j-y)**2 + (i-x)**2)/10
#            if(density > 0.75): continue

            lines = crophatch(grid[i][j],angle,density)
            print("lines: ", lines)
            for l in lines:
                patches.append(mpatches.Polygon(l,closed=False,fill=None))
    return patches



# draw a, uh, crooked spiral
# TODO: implement a clamp() function to make clamping a one-liner
def draw_crookedspiral(width,height,step):
    patches = []
    cx = width*step / 2
    cy = height*step / 2
    x = cx
    y = cy
    r = 0 # radius of our spiral arm
    theta = 0 # current angle
    dtheta = math.pi / 5 # per rotation sweep

    line = [[cx,cy]]
    yep = True

    while(yep):
        theta += dtheta
        r += step * 0.0075 + (random.random() -0.5) * 0.5
        x = math.cos(theta) * r + cx 
        y = math.sin(theta) * r + cy
        # pick a step length with noise
        line.append([x,y])
        # bounds check for termination once we hit the edge of the draw areas
        if(r > width or r > height): yep = False

    patches.append(mpatches.Polygon(line,closed=False, fill=None))
    return patches

# draw a crooked spiral with a random irregular polygon
# TODO: implement a clamp() function to make clamping a one-liner
def draw_crookedirregularspiral(width,height,step, seed = 10):
    patches = []
    cx = width*step / 2
    cy = height*step / 2
    x = cx
    y = cy
    r = 0 # radius of our spiral arm
    theta = 0 # current angle

    # lets define an irregular polygon that sums up to 2*pi in chunks

    random.seed(seed)
    sides = 10 # number of sides (doesn't need to be integral)
    sides /= 2
    ths = []
    rs = []

    random.seed(seed)
    while(theta < 2*math.pi):
        dt = random.random() * math.pi/sides + math.pi/16  # for irregular polygons
#        dt = math.pi/sides # for regular polygons
        if(theta + dt > 2*math.pi): 
            dt = 2 * math.pi - theta
        theta += dt
        ths.append(dt)
        rs.append( (random.random() / 2) + 0.25)
    theta = 0

    line = [[cx,cy]]
    yep = True
    count = 0

    random.seed()
    while(yep):
        theta += ths[count % len(ths)] # cycle around the irregular poly
        r += step * 0.02/sides + (random.random() - 0.5) * 0.5 

        r *= rs[count % len(ths)] # enable r* = and r /= lines for concave spirals
        x = math.cos(theta) * r + cx 
        y = math.sin(theta) * r + cy
        r /= rs[count % len(ths)]

        # pick a step length with noise
        line.append([x,y])


        # bounds check for termination once we hit the edge of the draw areas
        if(r > width*step/2 or r > height*step/2): yep = False

        count += 1

    patches.append(mpatches.Polygon(line,closed=False, fill=None, color=[random.random(),random.random(),random.random()]))
    return patches



'''
# interesting buggy failure to implement crookedspiral routine
def draw_notaspiral(width,height,step):
    patches = []
    x = width*step / 2
    y = height*step / 2
    line = [[x,y]]
    count = 0
    yep = True
    while(yep):
        dx = 0
        dy = 0
        # cycle through for cardinal directions
        if(count % 4 == 0): dx = 1
        elif(count % 4 == 1): dy = 1
        elif(count % 4 == 2): dx = -1
        else: dy = -1
        # pick a step length with noise
        dx *= random.random() * step 
        dy *= random.random() * step 
        x += dx
        y += dy
        print("dx, dy: ", dx, ", ", dy)
        # check bounds
        if(x < 0): 
            x = 0
            yep = False
        elif(x > width*step): 
            x = width*step
            yep = False
        if(y < 0): 
            y = 0
            yep = False
        elif(y > height*step): 
            y = height*step
            yep = False

        line.append([x,y])
        print("line: ", line)
        count += 1

    patches.append(mpatches.Polygon(line,closed=False, fill=None))
    return patches
'''

# draw a thing
def draw_thingy(width,height):
    outer = []
    inner = []
    points = [None] * height
    outer.append(mpatches.Polygon([[0,1], [0,0], [width,0], [width, 1]], closed=False, fill=None, color="black"))
    for i in range(len(points)):
        p = random.randint(2, width - 3)
        y = 2*i+1
        
        line = [[0,y], [p-1,y], [p-1,y+1], [0,y+1], [0,y+2]]
        outer.append(mpatches.Polygon(line, closed=False, fill=None, color="black"))

        
        line = [[p,y],[p+1,y],[p+1,y+1],[p,y+1]]
        inner.append(mpatches.Polygon(line, closed=True, fill=None, color="red"))
        hatch = crophatch( line, math.pi/3, .1)
        for h in hatch:
            inner.append(mpatches.Polygon(h, closed=False, fill=None, color="red"))

        line = [[width,y], [p+2,y], [p+2,y+1], [width,y+1], [width,y+2]]
        outer.append(mpatches.Polygon(line, closed=False, fill=None, color="black"))

    outer.append(mpatches.Polygon([[0,2*height+1], [width,2*height+1]], closed=False, fill=None, color="black"))
    return outer, inner







