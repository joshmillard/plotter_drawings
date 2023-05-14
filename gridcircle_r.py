# circles in a grid

from cortexdraw import *

points = []

xlen = 20
ylen = 20

# generate grid of points
def getpoints():
    grid = [0] * xlen
    for x in range(xlen):
        grid[x] = [0] * ylen
        for y in range(xlen):
            grid[x][y] = [0] * 4
            for i in range(0,4):
                if(random.random() > 0.85 ):
                    grid[x][y][i] = 1
    return grid

# throw out some random points
def cullpoints(g):
    for x in range(xlen):
        for y in range(ylen):
            if random.random() > 0.5: g[x][y] = 0
    return g

# throw out some points in a rectangular area
def cullrect(g):
    x1 = random.randint(0,xlen)
    x2 = random.randint(x1, xlen)
    y1 = random.randint(0,ylen)
    y2 = random.randint(y1,ylen)
    for x in range(x1, x2):
        for y in range(y1, y2):
            g[x][y] = 0
    return g

# throw out contiguous-ish chunks of points
def cullchunks(p):
    culling = False
    newp = []
    for l in p:
        if random.random() > 0.99: culling = not culling
        if not culling: newp.append(l)
    return newp
    
fig, ax = plt.subplots(figsize=(11, 8.5), frameon=False)

linep = []

grid = getpoints()
#grid = cullpoints(grid)
#grid = cullrect(grid)
#grid = cullrect(grid)
#grid = cullrect(grid)


# connecting lines bewteen adjacent dots
for x in range(xlen):
    for y in range(ylen - 1):
        for i in [1,3]:
            if grid[x][y][i] == 1: 
                linep.append(mpatches.Circle([x,y],radius=(.125 + i*.1), fill=None, color=[1-(i/4),i/4,i/4]))

#linep = cullchunks(linep)


plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-2, xlen + 2]
y_bounds = [-2, ylen + 2]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(linep, match_original=True)
ax.add_collection(collection)

plt.savefig('gridcircle.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['gridcircle.svg'])

