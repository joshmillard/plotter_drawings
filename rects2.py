# rectangle thing

import numpy as np
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

import random
import math
import copy


width = 100
height = 100

rects = []

# generate a bunch of rectangles
def getrekt(num):
    rects = []
    maxx = 100
    maxy = 100
    for i in range(num):
        w = random.random() * 25 + 5
        h = random.random() * 25 + 5
        x = random.random() * (maxx - w)
        y = random.random() * (maxy - h)
        a = 0
        rects.append([[x,y],w,h,a])
    return rects

# generate a checkerboard of rectangles
def getcheckerboard():
    rects = []
    step = 50
    dim = 2
    for i in range(dim):
        for j in range(dim):
            #if(not (i+j) % 2): continue
            rects.append([[i*step,j*step],step-10,step-10,0])
    return rects

# return a bunch of triangle polygons
def gettris(num):
    tris = []
    maxx = 100
    maxy = 100
    for i in range(num):
        x1 = random.random() * maxx
        x2 = random.random() * maxx
        x3 = random.random() * maxx
        y1 = random.random() * maxy
        y2 = random.random() * maxy
        y3 = random.random() * maxy

        tris.append([ [[x1,y1],[x2,y2]] , [[x1,y1],[x3,y3]] , [[x3,y3],[x2,y2]] ])

    return tris

# return a nice geometric arrangement of triangles
def getpyramid(num):
    tris = []
    size = 100/num
    xstep = 1 * size
    ystep = .866 * size
            
    sierpex = [ [1,1], [1,3], [1,5], [5,1], [3,1], [3,2], [3,3], [2,2], [2,3] ]  # deeply bullshit approach to producing Sierpinski triangle for small n

    for i in range(num):
        for j in range(num-i):
            if [i,j] in sierpex: continue
            xoff = (i * xstep) + (j * xstep / 2)
            yoff = j * ystep
            x1 = xoff
            y1 = yoff
            x2 = xoff + xstep
            y2 = yoff 
            x3 = xoff + (xstep/2)
            y3 = yoff + ystep
            tris.append([ [[x1,y1],[x2,y2]] , [[x1,y1],[x3,y3]] , [[x3,y3],[x2,y2]] ])

    return tris


# given a rectangle definition, create some hatch lines inside it
def hatchrect(xy,w,h):
    hatches = []
    step = random.random() + 0.5
    rx = xy[0]
    ry = xy[1]
    x = rx
    y = ry
    if random.random() > 0.5:
        while x < rx+w:
            hatches.append([[x,ry], [x, ry+h]])
            x += step
    else:
        while y < ry+h:
            hatches.append([[rx,y], [rx+w, y]])
            y += step
    return hatches

# do some chaotic hatching of a rect
def hackrect(xy,w,h):
    hatches = []
    step = random.random() + 0.5
    sides = random.sample([0,1,2,3],2)

    edges = [ [ [xy[0],xy[1]], [xy[0],xy[1]+h] ], [ [xy[0],xy[1]],[xy[0]+w,xy[1]] ], [ [xy[0],xy[1]+h],[xy[0]+w, xy[1]+h] ], [ [xy[0]+w,xy[1]],[xy[0]+w,xy[1]+h] ] ]

    #[A,B] = random.sample(edges,2)

    numhatch = int(random.random()*50 + 5)

    for i in range(numhatch):
        [A,B] = random.sample(edges,2)
        p1 = getlinebisect(A[0], A[1], random.random())
        p2 = getlinebisect(B[0], B[1], random.random())
        hatches.append([p1, p2])

    return hatches

# generalize hackrect to work on arbitrary (implicitly convex for the hatching to behave) polygon
def hackpoly(p):
    hatches = []
    edges = p
    numhatch = int(random.random()*50 + 5)

    for i in range(numhatch):
        [A,B] = random.sample(edges,2)
        p1 = getlinebisect(A[0], A[1], random.random())
        p2 = getlinebisect(B[0], B[1], random.random())
        hatches.append([p1, p2])

    return hatches

# chaotic hatching in a continuous polyline
def circuitpoly(p):
    hatches = []
    edges = p
    cycle = len(edges)
    numhatch = int(random.random()*50 + 5)
  
    # initial line
    [A,B] = [ edges[0], edges[1] ]
    p1 = getlinebisect(A[0], A[1], random.random())
    p2 = getlinebisect(B[0], B[1], random.random())
    hatches.append([p1, p2])

    for i in range(1,numhatch):
        B = edges[(i+1)%cycle]
        p1 = hatches[i-1][1]
        p2 = getlinebisect(B[0], B[1], random.random())
        hatches.append([p1, p2])

    hatches.append([hatches[-1][1], hatches[0][0]])
    
    return hatches

# buggy circuitpoly draft that is actually kinda cool tho
def laserpoly(p):
    hatches = []
    edges = p
    cycle = len(edges)
    numhatch = int(random.random()*50 + 5)
  
    # initial line
    [A,B] = [ edges[0], edges[1] ]
    p1 = getlinebisect(A[0], A[1], random.random())
    p2 = getlinebisect(B[0], B[1], random.random())
    hatches.append([p1, p2])

    for i in range(1,numhatch):
        B = edges[(i+1)%cycle]
        p1 = hatches[i-1][0]
        p2 = getlinebisect(B[0], B[1], random.random())
        hatches.append([p1, p2])

    return hatches

# nicked from stack overflow, thank you random SO person for your service
def find_intersection( p0, p1, p2, p3 ) :

    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1]
    denom = s10_x * s32_y - s32_x * s10_y
    if denom == 0 : return None # collinear

    denom_is_positive = denom > 0

    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]
    s_numer = s10_x * s02_y - s10_y * s02_x
    if (s_numer < 0) == denom_is_positive : return None # no collision

    t_numer = s32_x * s02_y - s32_y * s02_x
    if (t_numer < 0) == denom_is_positive : return None # no collision
    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision

    # collision detected
    t = t_numer / denom
    intersection_point = [ p0[0] + (t * s10_x), p0[1] + (t * s10_y) ]

    return intersection_point

# hatch the interior of convex polygon poly by cropping some lines to fit
def crophatch(poly):
    inhatch = []  # the uncropped hatch lines
    outhatch = []  # the cropped hatch we're producing

    # let's get a bounding box around this polygon

    xmin = poly[0][0]
    ymin = poly[0][1]
    xmax = 0
    ymax = 0
   
    for p in poly:
        if(p[0] < xmin): xmin = p[0]
        if(p[0] > xmax): xmax = p[0]
        if(p[1] < ymin): ymin = p[1]
        if(p[1] > ymax): ymax = p[1]

    # now let's generate some hash lines within those bounds
#    inhatch = hackrect([xmin,ymin],xmax-xmin,ymax-ymin)


    step = 1
    x = xmin - 10


    while x < xmax:
        inhatch.append([ [x,ymin], [x+(random.random()*10),ymax] ])
        inhatch.append([ [x,ymin], [x,ymax] ])
        x += step

    # now the doozy: for each hatch line, try to intersect with each poly line
    #  if we get two intersections, we should crop it top and bottom
    for l in inhatch:
        out = []
        p1 = l[0]
        p2 = l[1]
        for i in range(len(poly) - 1):
            p3 = poly[i]
            p4 = poly[i+1]
            newp = find_intersection(p1,p2,p3,p4)
            if(newp != None):
                out.append(newp)
        # there might be 2, 4, 6...intersections in valid hatch line vs. a non-convex poly; handling this
        # correctly requires sorting the segments of the carved up hatch line in asc. or desc. order along
        # the line, e.g. by x or y coord (edge case for cardinal lines I suppose)
        if(len(out) > 1 and len(out) % 2 == 0):
            out.sort()
            for i in range(0,len(out),2):
                outhatch.append([out[i],out[i+1]])

    return outhatch




#given a start and an end coordinate and a midpoint position 0..1, return a new coord at that point on line AB
def getlinebisect(A,B,portion):
    x1 = A[0]
    y1 = A[1]
    x2 = B[0]
    y2 = B[1]
    
    dx = x2-x1
    dy = y2-y1

    newx = x1 + dx*portion
    newy = y1 + dy*portion

    return[newx,newy]

def copyshift(lines,xshift,yshift):
    lout = []
    for l in lines:
        lnew = copy.deepcopy(l)
        lnew[0][0] += xshift
        lnew[0][1] += yshift
        lnew[1][0] += xshift
        lnew[1][1] += yshift
        lout.append(lnew)
    return lout

def slant(lines,slantmag=2):
    for l in lines:
        mag = 1/(len(l))
        for p in l:
            p[0] += (random.random() - 0.5) * slantmag * mag
    return lines

def twist(lines):
    for l in lines:
        l[1][0] = width - l[1][0]
    return lines

def feather(lines,feathermag=2):
    for l in lines:
        for p in l:
            p[1] += (random.random() - 0.5) * feathermag
    return lines

def divide(lines, iterations):
    newl = []
    for k in range(iterations):
        for i in range(len(lines)):
            newl.append( [lines[i][0]] )
            for j in range(len(lines[i])-1): 
                p1 = lines[i][j]
                p2 = lines[i][j+1]
                mid = [ (p1[0] + p2[0]) / 2,  ( p1[1] + p2[1]) / 2  ]
                newl[i].append(mid)
                newl[i].append(p2)
        
        lines = newl
        newl = []
    return lines

fig, ax = plt.subplots(figsize=(11, 8.5))

patches = []

for i in range(10):
    t1 = [random.random()*50, random.random()*50]
    t2 = [random.random()*50, random.random()*50]
    t3 = [random.random()*50, random.random()*50]
    t4 = [random.random()*50, random.random()*50]
    t5 = [random.random()*50, random.random()*50]

    tri = [ t1,t2,t3,t4,t5,t1 ]
    #patches.append(mpatches.Polygon(tri,closed=True,fill=None,color="black"))

    lines = crophatch(tri)
    lines = divide(lines,8)
    lines = slant(lines)
#    lines = feather(lines)
    for l in lines:
        patches.append(mpatches.Polygon(l,closed=False,fill=None,color="black"))


#rects = getrekt(100)
#rects = getcheckerboard()

'''
for xy,w,h,a in rects:
#    if(random.random() > 0.75): patches.append(mpatches.Rectangle(xy,w,h,a, fill=None, color="blue"))
    h = hackrect(xy,w,h)
    #h = divide(h,8)
    #h = slant(h,1)
    #h = feather(h,0.2)
    for l in h:
        patches.append(mpatches.Polygon(l,closed=False, fill=None, color="black"))
'''

'''
#tris = gettris(2)
tris = getpyramid(8)
#print(tris)
for t in tris:
    h = laserpoly(t)
    for l in h:
        patches.append(mpatches.Polygon(l,closed=False, fill=None, color="black"))
'''


plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-5, width + 5]
y_bounds = [-5, height*.866 + 5]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('rects.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()


