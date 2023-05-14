# landscape generator

from cortexdraw import *

width = 100
height = 10

fig = plt.figure(figsize=(12, 9), dpi=100, frameon=False)

axs = makeaxesgrid(fig, 4)

count = 0
for a in axs:
	patches = [] 
	xoff = 0
	yoff = 0
	# get a nice diagonal
	line = [[0,height + count*5 + random.random()*20],[width,height + count*5 + random.random()*20]]

	# make it into an organic craggy landscpe with noise
	line = perlinize(line[0],line[1],10,0.13)
	# turn that into a close polygon by adding a box underneath
	line.append([width+count*xoff,0 + count*yoff])
	line.append([0+count*xoff,0 + count*yoff])
#		line.append(line[0])
	patches.append(mpatches.Polygon(line,closed=True,fill=None))
	hatching = crophatch(line, random.random()*math.pi*0.1, random.random()/4 +.25)
#	hatching = crophatch(line, random.random()*math.pi, random.random() +.75)
	for l in hatching:
		l = jitter(l,0.1,True)
		patches.append(mpatches.Polygon(l,closed=False,fill=None))

	count += 1

	x_bounds = [-5, width + count*xoff + 5]
	y_bounds = [-5, height + 50]

	a.set_xlim(x_bounds)
	a.set_ylim(y_bounds)

	collection = PatchCollection(patches, match_original=True)
	a.add_collection(collection)


writefigure(fig)
plt.show()

