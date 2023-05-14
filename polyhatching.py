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


# generate a polygon!
def getpoly(sides, center=[0,0], length=1, inittheta=0):
	polys = []

	newpoly = []
	for i in range(sides):
		theta = inittheta + (2*math.pi)/sides * i
		px = center[0] + math.cos(theta)*length
		py = center[1] + math.sin(theta)*length
		newpoly.append([px,py])

	polys.append(newpoly)
	return polys

# generate coronas of hexagons
def gethexplex(center=[0,0], num=1, length=1):
	hexes = []
	cx = center[0]
	cy = center[1]

	# center hex
	myl = length * (0.25 + random.random())
	hexes.append(getpoly(6,[cx,cy],myl)[0])

	inradius = math.sqrt(3)

	# first ring
	for i in range(6):
		myl = length * (0.25 + random.random())
		dx = length * math.cos(2*math.pi*((i+0.5)/6)) * inradius
		dy = length * math.sin(2*math.pi*((i+0.5)/6)) * inradius

		newhex = getpoly(6,[cx+dx,cy+dy], myl)
		hexes.append(newhex[0])

	return hexes

# generate a rectangular grid of hexes
def gethexgrid(origin=[0,0], width=3, height=3, length=10, yoff=0):
	hexes = []
	ox = origin[0]
	oy = origin[1]

	inradius = math.sqrt(3)

	k = (random.random() * 10 + 10) * length
	m = (random.random() * 10 + 10) * length
	q = (random.random() * 1) 
	for i in range(width):
		for j in range(height):
			dx = length * (3*i + (j%2 * 1.5)) 
			dy = length * inradius * 0.5 * j

			#if(random.random() > abs(i-j+3)/20): continue
			if(random.random() > abs((i*1.5)-(j/2)+yoff)/6 + 0.1): continue
#			if(random.random() > abs(k*i - j*m)/q ): continue
			hexes.append(getpoly(6,[ox+dx,oy+dy],length)[0])

	return hexes


# generate a rectangular grid of hexes
def gethexconcentricgrid(origin=[0,0], width=3, height=3, length=10, skip=False):
	hexes = []
	ox = origin[0]
	oy = origin[1]

	inradius = math.sqrt(3)
	d = 0.1

	for i in range(width):
		for j in range(height):
			d = random.random()/3 + 0.1
			rad = length
			if(skip): rad -= random.random()*d
			dx = length * (3*i + (j%2 * 1.5)) 
			dy = length * inradius * 0.5 * j

			#if(random.random() > abs(i-j+3)/20): continue
			#if(random.random() > abs((i*1.5)-(j/2)+yoff)/6 + 0.1): continue
			th = 0
			#th = random.random()*math.pi
			while(rad > 0):
				hexes.append(getpoly(6,[ox+dx,oy+dy],rad,th)[0])
				rad -= random.random()*d
				

	return hexes



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

# return list with a bunch of the middle removed
def skipmiddle(mylist):
	threshold = 0.1
	l = len(mylist)
	if l < 3: return mylist

	stop = int(l * threshold) + 1
	resume = int(l * (1 - threshold))

	mylist = mylist[0:stop] + mylist[resume:-1]

	return mylist


width = 1
height = 1
length = 3

fig = plt.figure(figsize=(12, 9), dpi=100, frameon=False)

axs = makeaxesgrid(fig, 3)

#permagrid = getunevengrid(width,height,length)
#permagrid = getpoly(4,[width*length/2, height*length/2], length)

count = 0
for a in axs:
	patches = [] 
	#sides = int(random.random()*7)+3
	sides = 6
	#permagrid = getpoly(sides,[width*length/2, height*length/2], length, random.random()*math.pi)
#	permagrid = getpoly(sides,[width*length/2, height*length/2], length, random.random()/20)
	skip = False
	if(count > 0): skip = True
	permagrid = gethexconcentricgrid([length,length],width,height,length,skip)
	#permagrid = gethexplex([width*length/2, height*length/2], 1, length)
	#permagrid = getunevengrid(width,height,length)
#	quads = getperturbedgrid(width,height,length)
	quads = copy.deepcopy(permagrid)
	for q in quads:
		q = jitter(q,0.02,True)
		patches.append(mpatches.Polygon(q,closed=True,fill=None, color="black"))
		#hatching = crophatch(q, random.random()*math.pi*0.2, random.random()/4 +.25)
		#if(random.random() > 0.5): continue
		hatching = []
		#hatching = crophatch(q, random.random() * math.pi, random.random() + 0.25)
		#hatching = skipmiddle(hatching)
		#hatching = circuitpolyline(q,int(random.random() * 20)+10)
		for l in hatching:
			#if(random.random() > 0.5): continue
			l = jitter(l,0.1,True)
			patches.append(mpatches.Polygon(l,closed=False,fill=None))

	count += 1

	x_bounds = [-1, width*length*3.5 + 1]
	y_bounds = [-1, height*length + 1]

	a.set_xlim(x_bounds)
	a.set_ylim(y_bounds)

	collection = PatchCollection(patches, match_original=True)
	a.add_collection(collection)


writefigure(fig)
plt.show()