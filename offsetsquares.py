# offset squares

from cortexdraw import *

order = 5
size = 20

def makesquares(order, size):
    squares = []
    offs = []
    for i in range(order):
        xoff = random.randrange(-3,3) * order
        yoff = random.randrange(-3,3) * order
        offs.append([xoff,yoff])

    print(offs)
    for i in range(order,size+order):
        x1 = -i + offs[i%order][0]
        x2 = i + offs[i%order][0]
        y1 = -i + offs[i%order][1]
        y2 = i + offs[i%order][1]
        squares.append( [ [x1,y1], [x1,y2], [x2,y2], [x2,y1], [x1,y1] ] )
    return squares

sq = makesquares(order,size)

fig, ax = plt.subplots(figsize=(14, 11), frameon=False)

patches = []

for s in sq:
    patches.append(mpatches.Polygon(s, closed=True, fill=None))

plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

xo = order * 4
x_bounds = [-xo - size, xo + size]
y_bounds = [-xo - size, xo + size]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('offsetsquares.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['offsetsquares.svg'])
