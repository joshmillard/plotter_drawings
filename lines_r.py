# lnes foolin'

from cortexdraw import *

width = 100
height = 100
slantmag = 50
feathermag = 5

lines = []

def getlines():
    l = []
    x = 0
    step = 0.5
    while x < width:
        l.append([ [x,0], [x,height] ])
        x += random.random()*step
        # do some step size variation throughout
        step += (random.random() -0.5) * 0.5
        if(step < 0.1): step = 0.1
        if(step > 5): step = 10

    return l
    
def slant(lines):
    for l in lines:
        mag = 1/(len(l))
        for p in l:
            p[0] += (random.random() - 0.5) * slantmag * mag
    return lines

def twist(lines):
    for l in lines:
        l[1][0] = width - l[1][0]
    return lines

def feather(lines):
    for l in lines:
        for p in l:
            p[1] += (random.random() - 0.5) * feathermag
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

lines = getlines()
lines = divide(lines,6)
lines = slant(lines)
lines = feather(lines)
#lines = twist(lines)

for p in lines:
    patches.append(mpatches.Polygon(p, closed=False, fill=None))

plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-10, 110]
y_bounds = [-10, 110]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('lines.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['lines.svg'])


