# working from code snagged from Gary Whitehead in masto conversation:
# https://mastodon.social/@grwster/109734946667028881

import numpy as np

from cortexdraw import *
fig, ax = plt.subplots(figsize=(10, 10), frameon=False)

circles = []
patches = []

squaresize = 2

width = squaresize * 2
height = squaresize * 2


def op2(m):
    tophalf = int(height/2)
    bottomhalf = height
    for i in range(tophalf):
        m[i].insert(0,0)
        m[i].pop()
    for i in range(tophalf + 1, bottomhalf):
        m[i].append(0)
        m[i].pop(0)

def op1(m):
    for i in range(11):
        newgrid = [[row[i] for row in m] for i in range(width)]
        op2(newgrid)
        m = [[row[i] for row in newgrid] for i in range(width)]

# construct a 2D array of zero values and stock it with square shape number values
# in the center
# - NOTE: squaresize is expected to be a multiple of 2!

def makearray(squaresize):

    gsize = squaresize * 2
    grid = []
    # create an array of zeros big enough to allow space to shift the square's bits around
    for i in range(gsize):
        newl = []
        for j in range(gsize):
            newl.append(0)
        grid.append(newl)

    # and then add squares digits to the center
    dxy = int(squaresize/2)
    for i in range(1, squaresize*squaresize + 1):
        grid[i % squaresize + dxy][int(i/squaresize)] = i

    return grid

m = makearray(squaresize)
print(m)

def newpatch(dx, dy):
    offx = dx * width + 1
    offy = dy * height + 1
    for x in range(len(m)):
        for y in range(len(m[x])):
            r = 1
            if m[x][y] > 0:
#                r = 0.1
                circles.append( ([x+offx,y+offy],r) )

    for c, r in circles:   
        ax.add_patch(mpatches.Arc(c, r, r, color=[0,0,0]))

newpatch(0,0)
for i in range(1,6,2):
    op1(m)
    print(m)
    newpatch(i,0)
    op2(m)
    newpatch(i+1,0)




#for i in range(6):
#    newpatch(i,0)

plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-1, width * 6 + 1]
y_bounds = [-1, height * 1 + 1]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('cutandshift.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['cutandshift.svg'])