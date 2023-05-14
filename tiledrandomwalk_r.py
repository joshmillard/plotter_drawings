# tiling random walks

from cortexdraw import *

walklength = 20

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
#    l = []
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


fig, ax = plt.subplots(figsize=(11, 8.5), frameon=False)
patches = []

w = 5
h = 5
lines = []

for i in range(w):
    for j in range(h):
        lines = getstepwalk(1,i*20,j*20)
        mycolor = [0,0,0]
        for p in lines: patches.append(mpatches.Polygon(p, closed=False, fill=None, color=mycolor))
        
        lastl = lines[len(lines)-1]
        lastp = lastl[len(lastl)-1]
        patches.append(mpatches.Circle(lastp, 0.15, fill=None, color=mycolor))


x_bounds = [-20,100]
y_bounds = [-20,100]

plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.tight_layout()

plt.savefig('tiledrandomwalk.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['tiledrandomwalk.svg'])


