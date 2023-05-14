# doing some hatched grids

from cortexdraw import *


width = 7
height = 7
step = 10

fig = plt.figure(figsize=(12, 9), dpi=100, frameon=False)

axs = makeaxesgrid(fig, 3)

for a in axs:
    patches = []
    squareg = getsquaregrid(width,height,step)

    for i in range(len(squareg)):
        for j in range(len(squareg[i])):
            # grid gradient variant
            #lines = circuitpolyline(squareg[i][j],int((i+j)**1.1 + 2))
            if(random.random() > 0.75): continue
            lines = crophatch(squareg[i][j],random.random()*2*math.pi, (random.random()*0.3) + 0.5 )
            jmag = 0
            if(random.random() > 0.5):
                jmag = random.random()
            for l in lines:
                l = jitter(l,jmag,True)
                patches.append(mpatches.Polygon(l,closed=False,fill=None,color="black"))
        
    x_bounds = [-5, width*step + 5]
    y_bounds = [-5, height*step + 5]

    a.set_xlim(x_bounds)
    a.set_ylim(y_bounds)

    collection = PatchCollection(patches, match_original=True)
    a.add_collection(collection)


writefigure(fig)
plt.show()
