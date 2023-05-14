# a hitomezashi stitching thing

from cortexdraw import *

width = 128
height = 96

def stitchcode(harray, varray):
    newline = []
    for v in range(len(varray)):
        off = varray[v] # give me a 0 or a 1
        for i in range(math.floor(len(harray)/2)):
            newline.append( [ [i*2+off,v],[i*2+off+1,v] ] )

    for h in range(len(harray)):
        off = harray[h]
        for i in range(math.floor(len(varray)/2)):
            newline.append( [ [h,i*2+off],[h,i*2+off+1] ] )

    return newline

# generate strings of random 0s and 1s to length
harr = np.random.randint(0,2,width)
varr = np.random.randint(0,2,height)
# feed those strings to the stitch generator et voila
lines = stitchcode(harr,varr)


fig, ax = plt.subplots(figsize=(14, 11), frameon=False)

patches = []

for p in lines:
    patches.append(mpatches.Polygon(p, closed=False, fill=None))

plt.grid(False)
plt.axis('off')
ax.set_aspect('equal')

x_bounds = [-10, width + 10]
y_bounds = [-10, height + 10]

ax.set_xlim(x_bounds)
ax.set_ylim(y_bounds)

collection = PatchCollection(patches, match_original=True)
ax.add_collection(collection)

plt.savefig('hitomezashi.svg', bbox_inches = 'tight', pad_inches = 0)
plt.show()

vpypeout(['hitomezashi.svg'])
