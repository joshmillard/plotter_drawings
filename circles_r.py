# circles

from cortexdraw import *

fig, ax = plt.subplots(figsize=(10, 10), frameon=False)

numcircles = 1
circles = []
circles2 = []
lines = []

# make some sort of circle action
def circlearcs():
    for i in range(numcircles):
        
        c = [math.sin((i+2)/5)*2,-math.sin((i+2)/5)*2]

    #   r = i + 10 + ( (random.random() - 0.5) * 1 )
        r = i + 1
    #    r = i

        offset = random.random() * 50 -50

        th1 = 0 + offset
        th2 = th1 + random.random() * 50
     #   th1 = th1 = random.random() * 30 + 330
     #   th2 = th1 + random.random() * 30 + 330
    #    th1 = math.sin(i/2) * 2 - i*5
    #    th2 = 140 + math.sin(i/2) * 2 - i*5

        circles.append((c,r,th1,th2))
#        circles2.append((c,r,th3,th4))

# make a gradient of one circle color to another
def circlegradient():
    for i in range(numcircles):
        c = [math.sin((i+2)/5),-math.sin((i+2)/5)]
        c = [0,0]
        r = i + 1
        th1 = 270 - i**.5
        th2 = 270 + i**.7

        if(random.random() > i/numcircles - 0.25): 
            circles.append((c,r,th1,th2))
        if(random.random() < i/numcircles ):
            circles2.append((c,r,th1,th2))

# create two offset sets of concentric circles
def circlemoire():
    for i in range(numcircles):
        #c = [0,0]
        r = i + 1
        th1 = 0
        th2 = 360
        if(i%2): 
            circles.append(([2,0],r,th1,th2))
        else:
            circles2.append(([-2,0],r,th1,th2))

def circletangents():
    for i in range(numcircles):
        # draw some concentric circles
        r = i + 1
        c = [0,0]
        th1 = 0
        th2 = 360
#        circles.append( (c,r,th1,th2) )

        numtans = 1000
        for i in range(numtans):
            # now draw a random tangent line
            theta = random.random() * math.pi * 2

            # line from center to point p on circle c along angle theta
            rscale = 1
            roff = r * ((1 - 0.05/rscale) + random.random()/rscale )
            p = [math.cos(theta) * roff, math.sin(theta) * roff]
    #        circles.append( (p, 0.03, 0, 360))
    #        lines.append( (c, p) )  

            #tangent line running through p
            wobble = 10
            tantheta = theta + (math.pi / 2) + (math.pi/(wobble * 2)) - (random.random() * math.pi/wobble)
            l1 = 0.5 * random.random() * random.random()
            l2 = 0.5 * random.random() * random.random()
            t1 = [p[0] - math.cos(tantheta) * l1, p[1] - math.sin(tantheta) * l1 ]
            t2 = [p[0] + math.cos(tantheta) * l2, p[1] + math.sin(tantheta) * l2 ]
            lines.append( (t1, t2))


#circlearcs()
#circlegradient()
#circlemoire()
circletangents()

patches = []

count = 0
dy = 1
for c, r, th1, th2 in circles:
   
    ax.add_patch(mpatches.Arc(c, r*2, r*2, angle=0, theta1=th1, theta2=th2, color=[1,0,0,0.5]))
    count += 1

for c, r, th3, th4 in circles2:

    ax.add_patch(mpatches.Arc(c, r*2, r*2, angle=0, theta1=th3, theta2=th4, color=[0,0,1,0.5]))
    count += 1

for line in lines:
    patches.append(mpatches.Polygon(line,closed=False, fill=None, color=[0,0,0]))

plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-numcircles - 1, numcircles + 1]
y_bounds = [-numcircles - 1, numcircles + 1]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('circles.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['circles.svg'])


