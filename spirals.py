# spirals

# TODO: add control parameters to the spiral calls so tweaking this doesn't require fucking with library functions

from cortexdraw import *

# further spiral experiments
def draw_partialspiral(width,height,step, seed = 10):
	patches = []
	cx = width*step / 2
	cy = height*step / 2
	x = cx
	y = cy
	r = 0 # radius of our spiral arm
	theta = 0 # current angle

	# lets define an irregular polygon that sums up to 2*pi in chunks

	random.seed(seed)
	sides = 5 # number of sides (doesn't need to be integral)
	sides /= 2
	ths = []
	rs = []

	random.seed(seed)
	while(theta < 2*math.pi):
		dt = random.random() * math.pi/sides + math.pi/16  # for irregular polygons
#        dt = math.pi/sides # for regular polygons
		if(theta + dt > 2*math.pi): 
			dt = 2 * math.pi - theta
		theta += dt
		ths.append(dt)
		rs.append( (random.random() / 2) + 0.25)
	theta = 0

	line = [[cx,cy]]
 #   line = []
	yep = True
	count = 0

	random.seed()
	while(yep):
		theta += ths[count % len(ths)] # cycle around the irregular poly
		r += step * 0.02/sides + (random.random() - 0.5) * 0.5 

		r *= rs[count % len(ths)] # enable r* = and r /= lines for concave spirals
		x = math.cos(theta) * r + cx 
		y = math.sin(theta) * r + cy
		r /= rs[count % len(ths)]

		rs[count % len(ths)] -= random.random() * 0.01   ### HEY Cool inverted spiral progression thing

		# pick a step length with noise
		line.append([x,y])

		# bounds check for termination once we hit the edge of the draw areas
		if(r > width*step/2 or r > height*step/2): yep = False

		count += 1

	stripes = 0

	# add some number of new break points indices between the start and end indices of the original spiral line
	breaks = random.sample(range(len(line)),stripes)
	breaks.sort()
	breaks.insert(0,0)
	breaks.append(len(line)-1)
	print("Breaks, len: ", breaks, ", ", len(breaks))

	skipindex = 0
	if(random.random() > 0.5): skipindex = 1

	for i in range(skipindex,len(breaks)-1,2):
		newl = line[breaks[i]:breaks[i+1]]
		#print("newl: ", newl)
		patches.append(mpatches.Polygon(newl,closed=False, fill=None, color=[random.random(),random.random(),random.random()]))

#	print("patches: ", patches)
	return patches



w = 10
h = 10
s = 10

prefig = plt.figure(figsize=(12, 9), dpi=100, frameon=False)

x_bounds = [-1 , w*s + 1] 
y_bounds = [-1, h*s + 1]

# our collection of generated axes objects
axs = []
axs += makeaxesgrid(prefig,4)
#axs += makeaxes(prefig, 3)

seed = int(random.random() * 1000000)
for a in axs:

	patches = draw_partialspiral(w,h,s,seed)

	collection = PatchCollection(patches, match_original=True)
	a.add_collection(collection)

	a.set_xlim(x_bounds)
	a.set_ylim(y_bounds)


plt.show()
# write this out to svgs
writefigure(prefig)