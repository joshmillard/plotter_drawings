# one line

from cortexdraw import *

width = 100
height = 100
jittermag = 0.1

# barf out several identical vertical lines to start
lines = [ [[50,0],[50,height]] ] * 100

def jitter(lines):
    for l in lines:
#        mag = 1/(len(l))
        for p in l:
            p[0] += (random.random() - 0.5) * jittermag 
            #p[1] += (random.random() - 0.5) * jittermag * mag
    return lines

def divide(lines, iterations):
    newl = []
    for k in range(iterations):
        for i in range(len(lines)):
            newl.append( [ [lines[i][0][0], lines[i][0][1] ] ] )
            for j in range(len(lines[i])-1): 
                p1 = [lines[i][j][0], lines[i][j][1]]
                p2 = [lines[i][j+1][0], lines[i][j+1][1]]
                mid = [ (p1[0] + p2[0]) / 2,  ( p1[1] + p2[1]) / 2 ]
                newl[i].append(mid)
                newl[i].append(p2)
        
        lines = newl
        newl = []
    return lines

def sine(lines):
    for l in lines:
        k = (random.random() - 0.5) * 80
        for p in l:
            p[0] += math.cos(p[1]/31.8) * k
    return lines

fig, ax = plt.subplots(figsize=(11, 8.5), frameon=False)

patches = []

lines = divide(lines,6)
lines = sine(lines)
#lines = jitter(lines)

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

plt.savefig('oneline.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['oneline.svg'])
