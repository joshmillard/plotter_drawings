# that x to y mod 9 thing

from cortexdraw import *

points = []

xlen = 64
ylen = 64

# generate grid of points
def getpoints():
    grid = [0] * xlen
    for x in range(xlen):
        grid[x] = [0] * ylen
        for y in range(xlen):
            if( (x ^ y) % 3 == 0 ):
                grid[x][y] = 1
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
        if grid[x][y] == 0: continue
        if grid[x][y+1] == 1: linep.append(mpatches.Polygon([[x,y],[x,y+1]], closed=False, color="black"))
        if x < xlen - 1:
            if grid[x+1][y] == 1: linep.append(mpatches.Polygon([[x,y],[x+1,y]], closed=False, color="black"))
            if grid[x+1][y+1] == 1: linep.append(mpatches.Polygon([[x,y],[x+1,y+1]], closed=False, color="black"))
        if x > 0:
            if grid[x-1][y+1] == 1: linep.append(mpatches.Polygon([[x,y],[x-1,y+1]], closed=False, color="black"))

#linep = cullchunks(linep)


plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-5, xlen + 5]
y_bounds = [-5, ylen + 5]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(linep, match_original=True)
ax.add_collection(collection)

plt.savefig('xymod.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['xymod.svg'])


