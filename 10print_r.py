# 10 print

from cortexdraw import *

slantmag = 10

xlen = 15
ylen = 15
size = 10

lines = []

def getlines():
    l = []
    for x in range(0, xlen):
        for y in range(0,ylen):
            if random.random() > 0.5:  
                l.append([ [x*size,y*size], [(x+1)*size,(y+1)*size] ])
                l.append([ [x*size,y*size], [(x+1)*size,(y+1)*size] ])
                l.append([ [x*size,y*size], [(x+1)*size,(y+1)*size] ])
            else: 
                l.append([ [(x+1)*size,y*size], [x*size,(y+1)*size] ])
                l.append([ [(x+1)*size,y*size], [x*size,(y+1)*size] ])
                l.append([ [(x+1)*size,y*size], [x*size,(y+1)*size] ])
    return l


def getarcs(): 
    l = []
    for x in range(0, xlen):
        for y in range(0,ylen):
            if random.random() > 0.5:  
                l.append([ [(x-1)*size, y*size], size*2, size*2, 0, 90] )
            else:
                l.append([ [x*size, (y+0)*size], size*2, size*2, 90, 180] )
    return l

def getquarters(): 
    l = []
    for x in range(0, xlen):
        for y in range(0,ylen):
            if random.random() > 0.5:  
                l.append([ [(x-1)*size, y*size], size, size, 0, 90] )
                l.append([ [x*size, (y+1)*size], size, size, 180, 270] )
            else:
                1 == 1
                l.append([ [(x-1)*size, (y+1)*size], size, size, 270, 360] )
                l.append([ [x*size, y*size], size, size, 90, 180] )
    return l
    
def getgrid():
    g = []
    for x in range(0, xlen+1):
        g.append([ [0,x*size], [ylen*size,x*size]])
    for y in range(0, ylen+1):
        g.append([ [y*size,0], [y*size,xlen*size]])
    return g

def slant(lines):
    for l in lines:
        mag = 1/(len(l))
        for p in l:
            p[0] += (random.random() - 0.5) * slantmag * mag
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

#grid = getgrid()
#lines = getlines()
#lines = divide(lines,2)
#lines = slant(lines)

lines = getquarters()

#for p in grid:
#    patches.append(mpatches.Polygon(p, closed=False, fill=None, color="grey"))

#for p in lines: patches.append(mpatches.Polygon(p, closed=False, fill=None, color="black"))

for p,w,h,t1,t2 in lines: ax.add_patch(mpatches.Arc(p,width=w,height=h,angle=0,theta1=t1,theta2=t2))

plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-10, xlen*size + 10]
y_bounds = [-10, ylen*size + 10]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('10print.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['10print.svg'])


