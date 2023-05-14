# random walks

from cortexdraw import *

walklength = 10

xmin = -1
xmax = 1
ymin = -1
ymax = 1

# given coordinate values x and y, check to see if either is a new min or max, update if so
def checkbounds(x,y):
    global xmin, xmax, ymin, ymax
    if(x < xmin): xmin = x
    if(x > xmax): xmax = x
    if(y < ymin): ymin = y
    if(y > ymax): ymax = y


def getrandomwalk():
    l = []
    x = xold = 0
    y = yold = 0
    for i in range(0, walklength):
        if(random.random() > 0.5):
            if(random.random() > 0.5): x += 1
            else: x += -1
        else:
            if(random.random() > 0.5): y += 1
            else: y += -1
        l.append([ [xold,yold], [x,y] ])
        xold = x
        yold = y
    return l

def getselfavoidingwalk(startx=0,starty=0):
    l = []
    poly =[ [0,0] ]
    visited = [ [0,0] ]
    x = startx
    y = starty
    for i in range(0, walklength):
        candidates = []
        fourdirs = [ [x+1,y], [x-1,y], [x,y+1], [x,y-1] ]
        # check to see if this point has been visited, if so, eliminate
        for d in fourdirs:
            if d in visited: continue
            candidates.append(d)
        # if no valid directions, we're stuck, stop
        if len(candidates) == 0: return l

        # otherwise choose from among valid directions
        dir = random.choice(candidates)
        l.append([[x,y], dir])
        poly.append(dir)
        visited.append(dir)
        x = dir[0]
        y = dir[1]
    return [poly]
#    return l

# same idea as basic self-avoiding walk, but with parameterized block length
def getstepwalk(step = 1,startx=0,starty=0):
    poly =[ [startx,starty] ]
    x = startx
    y = starty
    for i in range(0, walklength):
        candidates = []
        fourdirs = [ [x+step,y], [x-step,y], [x,y+step], [x,y-step] ]
        # check to see if this point has been visited, if so, eliminate
        for d in fourdirs:
            if d in poly: continue
            candidates.append(d)
        # if no valid directions, we're stuck, stop
        if len(candidates) == 0: return [poly]

        # otherwise choose from among valid directions
        dir = random.choice(candidates)
        poly.append(dir)
        checkbounds(dir[0],dir[1])

        x = dir[0]
        y = dir[1]
    return [poly]
    
def slant(lines):
    slantmag = 1 
    for l in lines:
        #mag = 1/(len(l))
        mag = 0.15
        for i in range(1,len(l)-1):
            l[i][0] += (random.random() - 0.5) * slantmag * mag
            l[i][1] += (random.random() - 0.5) * slantmag * mag
    return lines


def divide(lines, iterations):
    newl = []
    for k in range(iterations):
        for i in range(len(lines)):
            newl.append( [lines[i][0]] )
            for j in range(len(lines[i])-1): 
                p1 = lines[i][j]
                p2 = lines[i][j+1]
                mid = [ (p1[0] + p2[0]) / 2,  ( p1[1] + p2[1]) / 2  ]
                newl[i].append(mid)
                newl[i].append(p2)
        
        lines = newl
        newl = []
    return lines

fig, ax = plt.subplots(figsize=(11, 8.5), frameon=False)
patches = []

numruns = 10
for i in range(numruns):

    lines = []

    #lines = getrandomwalk()
    scale = 2**(i%3)
    if(scale ==1): lines = getstepwalk(scale,(random.randrange(48)-24),(random.randrange(48)-24))
    else: lines = getstepwalk(scale)

    lines = divide(lines,2)
    lines = slant(lines)

    mycolor = [i/numruns, 0.2, 0.2, 1]

    if i == 0: patches.append(mpatches.Circle(lines[0][0], 0.3, fill=None, color="red"))

    for p in lines: patches.append(mpatches.Polygon(p, closed=False, fill=None, color=mycolor))
    
    lastl = lines[len(lines)-1]
    lastp = lastl[len(lastl)-1]
    patches.append(mpatches.Circle(lastp, 0.15, fill=None, color=mycolor))


x_bounds = [xmin - 1, xmax + 1]
y_bounds = [ymin - 1, ymax + 1]


plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.tight_layout()

plt.savefig('randomwalk.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['randomwalk.svg'])

