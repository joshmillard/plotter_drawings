# hatching polygons of various shapes or whatever

from cortexdraw import *

# generate a list of irregular polygons laid out in a checkerboard arrangement
def getpolyfield(w=8,h=5,len=10):
	quads = []
	for i in range(w):
		for j in range(h):
			# growth = 0
			growth = (random.random() - 0.5) * 0.5
			x1 = (i-growth)*len
			y1 = (j-growth)*len
			x2 = (i+1+growth)*len
			y2 = (j+1+growth)*len
			newsq = [ [x1,y1], [x1,y2], [x2, y2], [x2, y1] ]
			quads.append(newsq)
	return quads

# return a squared-off grid with random intervals for each row and column
def getunevengrid(w=7,h=6,length=10):
	quads = []

	# generate a set of intervals
	dx = [0]
	dy = [0]
	sumx = 0
	sumy = 0
	for i in range(w): 
		#dx.append( (random.random() - 0.5)*(length) + length + dx[-1])
		dx.append( (random.random()+0.25)*length + dx[-1])
	for j in range(h): 
		#dy.append( (random.random() - 0.5)*(length) + length + dy[-1]) 
		dy.append( (random.random()+0.25)*length + dy[-1])

	# and then normalize them
	sumx = w*length / dx[-1]
	sumy = h*length / dy[-1]
	for i in range(len(dx)): dx[i] *= sumx
	for i in range(len(dy)): dy[i] *= sumy 

	# and then turn 'em into squares
	for i in range(w):
		for j in range(h):
			x1 = dx[i]
			y1 = dy[j]
			x2 = dx[i+1]
			y2 = dy[j+1]
			newsq = [ [x1,y1], [x1,y2], [x2, y2], [x2, y1] ]
			quads.append(newsq)
	return quads

# generate a connected net of perturbed squares
def getperturbedgrid(w=8,h=7,len=10):
	points = []
	polys = []
	mag = len * 1
	# generate grid vertices from which net of polygons will be constructed
	points = [None] * (w + 1)
	for i in range(w + 1):
		points[i] = [None] * (h + 1)
		for j in range(h + 1):
			#points[i][j] = [i*len,j*len]
			# do some perturbation...
			points[i][j] = [i*len + (random.random() - 0.5)*mag, j*len + (random.random() - 0.5)*mag]
	

	# ...and then construct actual polygon objects from vertices
	for i in range(w):
		for j in range(h):
			newsq = [ points[i][j], points[i][j+1], points[i+1][j+1], points[i+1][j]]
			polys.append(newsq)
	return polys


width = 4
height = 3
length = 8

fig = plt.figure(figsize=(12, 9), dpi=100, frameon=False)

axs = makeaxesgrid(fig, 4,2,2)

permagrid = getunevengrid(width,height,length)

count = 0
for a in axs:
	patches = [] 
	#permagrid = getunevengrid(width,height,length)
#	quads = getperturbedgrid(width,height,length)
	quads = copy.deepcopy(permagrid)
	for q in quads:
#		q = jitter(q,2,True)
		#patches.append(mpatches.Polygon(q,closed=True,fill=None, color="black"))
		#hatching = crophatch(q, random.random()*math.pi*0.2, random.random()/4 +.25)
		#if(random.random() > 0.1): continue
		hatching = crophatch(q, random.random()*math.pi, random.random()/3 +.25)
		#hatching = circuitpolyline(q,int(random.random() * 20)+10)
		for l in hatching:
			#if(random.random() > 0.5): continue
			l = jitter(l,0.1,True)
			patches.append(mpatches.Polygon(l,closed=False,fill=None))

	count += 1

	x_bounds = [-5, width*length + 5]
	y_bounds = [-5, height*length + 5]

	a.set_xlim(x_bounds)
	a.set_ylim(y_bounds)

	collection = PatchCollection(patches, match_original=True)
	a.add_collection(collection)


writefigure(fig)
plt.show()