# draw lines and find intersections

from cortexdraw import *

width = 100
height = 100

lines = []

fig, ax = plt.subplots(figsize=(11, 8.5), frameon=False)
patches = []

# gin up some random lines
lines = []
inters = []
for i in range(10):
    lines.append([ [random.random() * 50, random.random() * 50], [random.random() * 50, random.random() * 50]])
    patches.append(mpatches.Polygon(lines[i],closed=False, fill=None, color="black"))

# test them all for intersections
for i in range(len(lines)-1):
    for j in range(i+1, len(lines)):
        p1 = lines[i][0]
        p2 = lines[i][1]
        p3 = lines[j][0]
        p4 = lines[j][1]
        p = find_intersection(p1,p2,p3,p4)
        if(p != None): 
            patches.append(mpatches.Circle(p, radius= 0.5, fill=None, color="green"))
            inters.append(p)

for i in range(len(inters)-1):
    for j in range(i+1, len(inters)):
        patches.append(mpatches.Polygon([ inters[i],inters[j] ], closed=False, fill=None, color="red" ))

plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-5, 55]
y_bounds = [-5, 55]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('hatch.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['hatch.svg'])
