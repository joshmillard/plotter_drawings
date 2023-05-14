"""Draw an over-under looping rendering of the Recaman Sequence"""

from cortexdraw import *


def recaman(n):
    # this nice concise implementation was nicked from https://oeis.org/A005132
    seq = []
    for i in range(n):
        if i == 0:
            x = 0
        else:
            x = seq[i - 1] - i
        if x >= 0 and x not in seq:
            seq += [x]
        else:
            seq += [seq[i - 1] + i]
    return seq


def collatz(seed):
    # 12/8/22 -- shoehorning a Collatz variant in here
    product = seed
    col = [product]
    while product != 1:
        if product % 2 == 0:
            product = int(product / 2)
        else:
            product = int(3 * product + 1)
        col.append(product)
    return col


seq = recaman(100)
# seq = collatz(8351)

fig, ax = plt.subplots(figsize=(10, 10), frameon=False)

circles = []

for i in range(len(seq) - 1):
    step = seq[i + 1] - seq[i]  # how far from point n to point n+1
    rad = abs(step) / 2  # arc radius is half that
    center = seq[i] + (step / 2)  # draw forward or back depending on step

    c = [center, 0]
    # r = rad * (random.random()-0.5) + 0.5
    r = rad
    circles.append((c, r))

patches = []

RGB = [0.5, 0.5, 0.5]

count = 0
dy = 1
for c, r in circles:
    # patches.append(mpatches.Circle(c, r, fill=None, edgecolor='blue'))
    th1 = 0
    th2 = 180
    if count % 2:
        th1 = 180
        th2 = 0
    dy = 1
    # dy += (random.random()-0.6)
    # RGB[0] += (random.random()-0.5)/5
    # RGB[1] += (random.random()-0.5)/5
    # RGB[2] += (random.random()-0.5)/5

    ax.add_patch(mpatches.Arc(c, r * 2, r * 2 * dy, angle=0, theta1=th1, theta2=th2, edgecolor=RGB))
    count += 1

plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-2, max(seq) + 2]
# y_bounds = [-1*len(seq), len(seq)]
y_bounds = [max(seq) * -0.5, max(seq) * 0.5]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('mrec.svg', bbox_inches='tight', pad_inches=0)
plt.show()

vpypeout(['mrec.svg'])
