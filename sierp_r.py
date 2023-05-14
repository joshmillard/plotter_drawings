# sierpinski foolin'

from cortexdraw import *

pertmag = 0.005

carpet = []
def getcarpet(n):
    cs = []
    dim = 100

    cs.append([[0,0], [0,dim], [dim,dim], [dim,0]])
    mid = dim/3
    cs.append([[mid,mid], [mid+mid,mid], [mid+mid,mid+mid], [mid, mid+mid]])

    step = dim/3
    off = dim/9
    for i in range(3):
      for j in range(3):
            if i != 1 or j != 1:
                x1 = step*i+off
                x2 = step*i+off+off
                y1 = step*j+off
                y2 = step*j+off+off
                cs.append( [[x1,y1], [x2,y1], [x2,y2], [x1,y2]] )

    step = dim/9
    off = dim/27
    for i in range(9):
        for j in range(9):
            if math.floor(i/3) == 1 and math.floor(j/3) == 1:
                continue
            if (i % 3) != 1 or (j % 3) != 1:
                x1 = step*i+off
                x2 = step*i+off+off
                y1 = step*j+off
                y2 = step*j+off+off
                cs.append( [[x1,y1], [x2,y1], [x2,y2], [x1,y2]] )

    step = dim/27
    off = dim/81
    for i in range(27):
        for j in range(27):
            if math.floor(i/9) == 1 and math.floor(j/9) == 1:
                continue
            if math.floor(i/3) % 3 == 1 and math.floor(j/3) % 3 == 1:
                continue
            if (i % 3) != 1 or (j % 3) != 1:
                x1 = step*i+off
                x2 = step*i+off+off
                y1 = step*j+off
                y2 = step*j+off+off
                cs.append( [[x1,y1], [x2,y1], [x2,y2], [x1,y2]] )


    return cs


# perturb points randomly and uniformly
def perturb(carp):
    for i in range(len(carp)):
        for j in range(len(carp[i])):
            carp[i][j][0] += (random.random() - 0.5) * pertmag
            carp[i][j][1] += (random.random() - 0.5) * pertmag
    return carp

# perturb points randomly and to an increasing degree rightward
def perturb_rightward(carp):
    for i in range(len(carp)):
        for j in range(len(carp[i])):
            carp[i][j][0] += (random.random() - 0.5) * pertmag * i
            carp[i][j][1] += (random.random() - 0.5) * pertmag * i
    return carp

# create random crossings in squares by shuffling points
def crisscross(carp): 
    for i in range(len(carp)):
        random.shuffle(carp[i])
    return carp

# change the width and height and displacement of each square
def squarestretch(carp):
    sfact = 2
    for i in range(len(carp)):
        x1off = (random.random() - 0.5) * sfact
        x2off = (random.random() - 0.5) * sfact
        y1off = (random.random() - 0.5) * sfact
        y2off = (random.random() - 0.5) * sfact
        carp[i][0][0] += x1off
        carp[i][0][1] += y1off
        carp[i][1][0] += x2off
        carp[i][1][1] += y1off
        carp[i][2][0] += x2off
        carp[i][2][1] += y2off
        carp[i][3][0] += x1off
        carp[i][3][1] += y2off
    return carp

# remove some random proportion of polygons
def removerandom(carp):
    rate = 0.5 # odds of removal
    newc = []
    for i in range(len(carp)):
        if random.random() > rate:
            newc.append(carp[i])
    return newc


fig, ax = plt.subplots(figsize=(10, 10), frameon=False)
patches = []

carpet = getcarpet(1)

#carpet = perturb(carpet)
#carpet = perturb_rightward(carpet)
carpet = crisscross(carpet)
carpet = squarestretch(carpet)
carpet = removerandom(carpet)

for p in carpet:
    patches.append(mpatches.Polygon(p, fill=None))

#RGB = [0.2,0.5,0.6]

plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-10, 110]
y_bounds = [-10, 110]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('sierp.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['sierp.svg'])
