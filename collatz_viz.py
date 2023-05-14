# Collatz visualization based of my existing Recaman code

# brainstorm thought: what if instead of preserving the actual spacing of the sequence on the
#  number line, we collapsed it such that each step between discrete points was length 1
#  e.g. n=5 produces 1,2,4,5,8,16, which could be reduced to 1,2,3,4,5,6 but preserving out vs in moves
#   where teh 5->16 out arc becomes, visually, a 4->6 out arc; all the others become
#   smaller in-arcs: 2->1, 3->2, 5->3, 6->5

from cortexdraw import *
import math


target = 639  # collatz seed n (or max seed n for summing)
loga = False  # whether to apply logarythmic contraction to the values in the rendering
summing = False # wether to collate all collatz series 1-through-target instead of just target

# assemble a simple list of collatz values in order
def collatz(seed):
    product = seed
    col = [product]
    while(product != 1):
        if product % 2 == 0:
            product = int(product/2)
        else:
            product = int(3*product + 1)
        col.append(product)
    return col

# assemble a set of pairs of seed,result values for more complex manipulation later
#  n.b. the degenerate version of this is seeding with 1, which should return [ [1,4] ] 
def collatz_pairs(seed):
    product = 0
    table = []
    while(product != 1):
        if seed % 2 == 0:
            product = int(seed/2)
        else:
            product = int(3*seed + 1)
        table.append([seed,product])
        seed = product
    return table



seq = collatz(target)
tab = collatz_pairs(target)
if summing:
    for i in range(3,target+1):
        tab += collatz_pairs(i)
        seq += collatz(i)

fig, ax = plt.subplots(figsize=(10, 10), frameon=False)

circles = []

# unrelated sneaky thing: A064413, the EKG sequence
# seq = [1, 2, 4, 6, 3, 9, 12, 8, 10, 5, 15, 18, 14, 7, 21, 24, 16, 20, 22, 11, 33, 
# 27, 30, 25, 35, 28, 26, 13, 39, 36, 32, 34, 17, 51, 42, 38, 19, 57, 45, 40, 44, 46, 
# 23, 69, 48, 50, 52, 54, 56, 49, 63, 60, 55, 65, 70, 58, 29, 87, 66, 62, 31, 93, 72, 64, 
# 68, 74, 37, 111, 75, 78, 76, 80, 82]
# tab = []


# i don't actaully need list style anymore in principle, since the table style processing is a 
#  generalization of this; but until i stop being lazy and write up a utility function or line
#  to find the max value in a list of lists from the table, doing a max(seq) is how i currently check
#  drawing view bounds, so, alright, waste some extra cycles duplicating effort instead.

# list style processing
for i in range(len(seq)-1):
    a = seq[i]
    b = seq[i+1]
    if loga:
        a = math.log(a)
        b = math.log(b)
    step = b - a # how far from point n to point n+1
    halve = True
    if(step > 0): halve = False
    rad = abs(step)/2 # arc radius is half that
    center = a + (step/2) # draw forward or back depending on step

    c = [center,0]
    #r = rad * (random.random()-0.5) + 0.5
    r = rad
    #circles.append((c,r,halve))

# table style processing
for i in range(len(tab)):
    a = tab[i][0] 
    b = tab[i][1] 
    if loga:
        a = math.log(a)
        b = math.log(b)
    step = b - a

    halve = True
    if(step > 0): halve = False

    rad = abs(step)/2
    center = a + (step/2)
    c = [center, 0]
    r = rad
    circles.append((c,r,halve))


patches = []

RGB = [0,0,0]
color = {True: [0,0,0], False: [1,0,0]}

count = 0
maxi = len(circles)
dy = 1
for c, r, h in circles:
    th1 = 0
    th2 = 180
    offset = len(circles) % 2
    if ( (count + offset) % 2 ):  # continuous loop style
#    if(h == True):  # segregated style
        th1 = 180
        th2 = 0
    dy = 1

    #col = [1-count/maxi,0,count/maxi]
    col = RGB

    ax.add_patch(mpatches.Arc(c, r*2, r*2*dy, angle=0, theta1=th1, theta2=th2, edgecolor=col))
    count += 1


plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

#x_bounds = [-2, max(seq) + 2]
x_bounds = [0,max(seq)]
#y_bounds = [-1*len(seq), len(seq)]
y_bounds = [max(seq) * -0.5, max(seq) * 0.5]
if loga:
    x_bounds[0] = -0.01
    x_bounds[1] = math.log(x_bounds[1]) + 0.01
    y_bounds[1] = 2
    y_bounds[0] = -2
ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('mrec.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['mrec.svg'])

