# sketchy approximate circles from tangent lines

from cortexdraw import *

fig, ax = plt.subplots(figsize=(10, 10), frameon=False)

circles = []
lines = []

def circletangents(number=100, spread=10, wobble=10, radius=1, center=[0,0]):
    
    # draw some concentric circles
    r = radius
    c = center
    th1 = 0
    th2 = 360
#   circles.append( (c,r,th1,th2) )

#        number = 1000
    for i in range(number):
        # now draw a random tangent line
        theta = random.random() * math.pi * 2

        # line from center to point p on circle c along angle theta
#            rscale = 1
        roff = r * ((1 - 0.05/spread) + random.random()/spread )
        
        p = [math.cos(theta) * roff, math.sin(theta) * roff] 

        #tangent line running through p
#            wobble = 10
        tantheta = theta + (math.pi / 2) + (math.pi/(wobble * 2)) - (random.random() * math.pi/wobble)
        l1 = 0.5 * random.random() * random.random() 
        l2 = 0.5 * random.random() * random.random() 
        t1 = [p[0] - math.cos(tantheta) * l1 + c[0], p[1] - math.sin(tantheta) * l1 + c[1] ]
        t2 = [p[0] + math.cos(tantheta) * l2 + c[0], p[1] + math.sin(tantheta) * l2 + c[1] ]
        lines.append( (t1, t2))

# connect the endpoints of our lines to one another
def chainlines():
    for i in range(len(lines) - 1):
        if(random.random() > 0.2):
            continue
        l1 = lines[i]
        l2 = lines[i+1]
        lines.append( [l1[1],l2[0]] )



circletangents(100,.1,1,1,[0,0])
circletangents(100,1,3,1,[0,0])
circletangents(100,1.5,9,1,[0,0])
circletangents(100,4,27,1)
circletangents(150,8,81,1)
circletangents(200,160,200,1)

#chainlines()

patches = []

count = 0
dy = 1
for c, r, th1, th2 in circles:
   
    ax.add_patch(mpatches.Arc(c, r*2, r*2, angle=0, theta1=th1, theta2=th2, color=[1,0,0,0.5]))
    count += 1

for line in lines:
    patches.append(mpatches.Polygon(line,closed=False, fill=None, color=[0,0,0]))

plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-2, 2]
y_bounds = [-2, 2]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('circles.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['circles.svg'])


