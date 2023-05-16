""" Draws a grid of randomly cross-hatched squares """

from cortexdraw import *

width = 7
height = 7
step = 10

fig = plt.figure()

axs = makeaxesgrid(fig, 3)

for a in axs:
    patches = []
    squareg = getsquaregrid(width, height, step)

    for i in range(len(squareg)):
        for j in range(len(squareg[i])):
            # grid gradient variant
            # lines = circuitpolyline(squareg[i][j],int((i+j)**1.1 + 2))
            if random.random() > 0.75:
                continue
            lines = crophatch(squareg[i][j], random.random() * 2 * math.pi, (random.random() * 0.3) + 0.5)
            jmag = 0
            if random.random() > 0.5:
                jmag = random.random()
            for line in lines:
                line = jitter(line, jmag, True)
                patches.append(mpatches.Polygon(line, closed=False, fill=None, color="black"))

    x_bounds = [-5, width * step + 5]
    y_bounds = [-5, height * step + 5]

    collection = PatchCollection(patches, match_original=True)
    a.add_collection(collection)

writefigure(fig, xbounds=x_bounds, ybounds=y_bounds, filename="grid_hatch", pagesize=[12, 9], drawingsize=[10, 7])
plt.show()
