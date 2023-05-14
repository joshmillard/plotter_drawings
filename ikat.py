# ikat weaving experiment

from cortexdraw import *

width = 200
height = 200
nickname = "ikat"

def build_ikat_hash():
    newline = []
    xrange = []
    xrange.append(range(40,60))
    xrange.append(range(140,160))
    for r in xrange:
        for x in r:
            yoff = np.random.uniform(-5,5)
            y1 = 20 + yoff
            y2 = 180 + yoff
            newline.append( [ [x,y1],[x,y2] ] )

    yrange = []
    yrange.append(range(40,60))
    yrange.append(range(140,160))
    for r in yrange:
        for y in r:
            xoff = np.random.uniform(-5, 5)
            x1 = 20 + xoff
            x2 = 180 + xoff
            newline.append([[x1, y], [x2, y]])
    return newline

lines = build_ikat_hash()

fig, ax = plt.subplots(figsize=(14, 11), frameon=False)

patches = []

for p in lines:
    patches.append(mpatches.Polygon(p, closed=False, fill=None))

plt.grid(False)  # ???
plt.axis('off')  # suppress matplotlibs default graph axis
ax.set_aspect('equal')  # suppress automatic scaling of x vs. y aspect, to keep 1:1 aspect ratio in place

x_bounds = [-10, width + 10]  # define coordinate bounds for the drawing in raw units
y_bounds = [-10, height + 10]  # ditto for y axis

ax.set_xlim(x_bounds)  # set the x bound
ax.set_ylim(y_bounds)  # set the y bound

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

writefigure(fig)

# plt.savefig(f'{nickname}.svg', bbox_inches = 'tight', pad_inches = 0)
# plt.show()
#
# vpypeout([f'{nickname}.svg'])
