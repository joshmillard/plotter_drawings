""" draw circular figures randomly implementing the Lazy Caterer procedure """

from cortexdraw import *

prefig = plt.figure()


def draw_caterer():
    """ draw a single lazy caterer diagram """
    twopi = 2 * math.pi

    circles = []
    cx = [0, 0]
    r = 1
    # a single bounding circle, probably don't actually need a list but hey who knows
    circles.append([cx, r])

    chords = []

    # let's pick two initial points at random to create our initial circle
    th1 = random.random() * twopi
    th2 = random.random() * twopi
    p1 = [math.cos(th1), math.sin(th1)]
    p2 = [math.cos(th2), math.sin(th2)]

    chords.append([p1, p2])

    # now let's find valid chords
    for i in range(4):
        # flag for whether to invert the order of chord points
        invert = False
        # choose one random chord from our accumulated list
        index = random.randrange(len(chords))
        # index = 0

        c1 = chords[index]
        # get the next chord in the list, which might involve wrapping around to the start of the list
        # in which case we need to invert the order of those following coordinates
        index2 = index + 1
        if index2 >= len(chords):
            index2 = 0
            invert = not invert

        c2 = chords[index2]
        if invert:
            c2 = c2[::-1]

        # calculate start and end points of the first arc
        th1 = math.atan2(c1[0][1], c1[0][0])
        th2 = math.atan2(c2[0][1], c2[0][0])
        if th2 < th1:
            th2 += twopi
        dth = th2 - th1
        # pick an angle within that arc range
        # newth1 = (random.random() * dth) + th1
        newth1 = (random.random() * dth * 0.6) + th1 + 0.2 * dth

        # calculate start and end for second, opposing arc
        th1 = math.atan2(c1[1][1], c1[1][0])
        th2 = math.atan2(c2[1][1], c2[1][0])
        if th2 < th1:
            th2 += twopi
        dth = th2 - th1
        # and pick an engle in there too
        # newth2 = (random.random() * dth) + th1
        newth2 = (random.random() * dth * 0.6) + th1 + 0.2 * dth

        # cacluate points on circle for those two angles
        p1 = [math.cos(newth1), math.sin(newth1)]
        p2 = [math.cos(newth2), math.sin(newth2)]

        # insert this new pair in the last after the first of our two random chords (and hence
        # between the first and the second, creating a new pair of sets of opposing arcs that bisect
        # the set of opposing arc were just working with
        chords.insert(index + 1, [p1, p2])

    return [circles, chords]


# bounds in local (not normalized Figure) units for the visible content on a given axis.  Anything outside these
# bounds will be cropped.
x_bounds = [-1.1, 1.1]
y_bounds = [-1.1, 1.1]

# our collection of generated axes objects
axs = []
axs += makeaxesgrid(prefig, 1, 4, 3)

# Actually putting content into the axes is not generalizable; any given program might want to manipulate any 
# combination of axes doing different things in different ways.  So creating a set of axes and putting stuff into them
# is a per-program process (and really the intent here is for that to be pretty much the ONLY thing a given drawing
# program needs to do, with everything else library calls for generalized processes).

colors = ["black", "red", "blue", "green"]
for a in axs:
    patches = []
    inters = []
    (circs, lines) = draw_caterer()
    for c in circs:
        patches.append(mpatches.Circle(c[0], c[1], fill=False, color="grey"))

    count = 0
    for line in lines:
        patches.append(mpatches.Polygon(line, closed=False, fill=False,
                                        color=[random.random(), random.random(), random.random() / 2, 0.8]))
        count += 1

    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            p1 = lines[i][0]
            p2 = lines[i][1]
            p3 = lines[j][0]
            p4 = lines[j][1]
            p = find_intersection(p1, p2, p3, p4)
            if p:
                # patches.append(mpatches.Circle(p, radius= 0.01, fill=None, color="green"))
                inters.append(p)
    # for i in range(len(inters)-1):
    #     for j in range(i+1, len(inters)):
    #         patches.append(mpatches.Polygon([ inters[i],inters[j] ], closed=False, fill=None, color="red" ))
    ''' zooming in
    minx = 99999
    miny = 99999
    maxx = -99999
    maxy = -99999
    for i in range(len(inters)):
        if(inters[i][0] < minx): minx = inters[i][0]
        if(inters[i][0] > maxx): maxx = inters[i][0]
        if(inters[i][1] < miny): miny = inters[i][1]
        if(inters[i][1] > maxy): maxy = inters[i][1]

    x_bounds = [minx - .1, maxx + .1]
    y_bounds = [miny - .1, maxy + .1]
    '''

    collection = PatchCollection(patches, match_original=True)
    a.add_collection(collection)

    a.set_xlim(x_bounds)
    a.set_ylim(y_bounds)

# write this out to svgs

writefigure(prefig, xbounds=x_bounds, ybounds=y_bounds, filename="lazycaterer")
plt.show()
