""" cortexlib.py: a library of useful plotter drawing functions accreting over time

some principles to aim for:
- every shape is handled by default as a list of points appropriate for feeding to patches.Polygon
- closed polygons should skip the repeated closing point in the list and use closed=True in the patch attrs
-- OR SHOULD THEY, MIGHT REVERSE COURSE ON THIS since it's easier to ignore a final segment when it's not needed
--   than it is to construct a missing one on the fly when it is
- angles should default to radians to work nicely with math.sin etc without conversion
- lets get rid of those bloody global variables where possible, eh


some hatching functions to (re)implement:
- chaotic random lines through a polygon
- lines radiating from a single point (on or off a poly's edge)

"""

import random
import math
import copy
import os

import matplotlib.pyplot as plt


# Mathematical utility functions

# given points for two line segments [p0,p1] and [p2,p3], return whether they intersect
# nicked from stack overflow, thank you random SO person for your service
def find_intersection(p0, p1, p2, p3):
    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1]
    denom = s10_x * s32_y - s32_x * s10_y
    if denom == 0:
        return None  # collinear

    denom_is_positive = denom > 0

    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]
    s_numer = s10_x * s02_y - s10_y * s02_x
    if (s_numer < 0) == denom_is_positive:
        return None  # no collision

    t_numer = s32_x * s02_y - s32_y * s02_x
    if (t_numer < 0) == denom_is_positive:
        return None  # no collision
    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive:
        return None  # no collision

    # collision detected
    t = t_numer / denom
    intersection_point = [p0[0] + (t * s10_x), p0[1] + (t * s10_y)]

    return intersection_point


# takes a polyline, returns a pair of points defining bottom left and top right of a tight bounding rectangle
# around the poly's segments
def getboundingbox(poly):
    # calculate a tight bounding box around this polygon
    # establish initial min/max bounds at a known point in the poly
    #    xmin = poly[0][0]
    #    ymin = poly[0][1]
    #    xmax = poly[0][0]
    #    ymax = poly[0][1]
    # trying this out instead of the above, in case I was doing something dumb with the assumptions there,
    # though it doesn't seem to have fixed the issue I'm bug-hunting; probably there's a more appropriate
    # maxint type system/library value to use here anyway
    xmin = 999999
    ymin = 999999
    xmax = -999999
    ymax = -999999

    # then iterate through the poly and push out the min and max bounds as new ones are found
    for p in poly:
        if p[0] < xmin:
            xmin = p[0]
        if p[0] > xmax:
            xmax = p[0]
        if p[1] < ymin:
            ymin = p[1]
        if p[1] > ymax:
            ymax = p[1]

    return [xmin, ymin], [xmax, ymax]


# given a start and an end coordinate and a midpoint position 0..1, return a new coord at that point on line ab
# - utility function that I'm not sure is in use anywhere at the moment
def getlinebisect(a, b, portion):
    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]

    dx = x2 - x1
    dy = y2 - y1

    newx = x1 + dx * portion
    newy = y1 + dy * portion

    return [newx, newy]


# given a list of lines, take each and add xshift and yshift to every coordinate point in the line,
# returns a new list object
# - should probably just call this "translate" since it's literally doing translation
# - rotation and scale functions to complement this would make for a whole basic set of 
#   transformation functions
# - there is probably a perfectly good way to do this with existing libraries, math. or matplotlib. or whatnot,
#   but I haven't gotten there yet
# TODO: am i even using this for anything now, and should it be retired if so in favor of using multiple axes
# objects to render different elements in space?
def copyshift(lines, xshift, yshift):
    lout = []
    for line in lines:
        lnew = copy.deepcopy(line)
        lnew[0][0] += xshift
        lnew[0][1] += yshift
        lnew[1][0] += xshift
        lnew[1][1] += yshift
        lout.append(lnew)
    return lout


# line/poly manipulation and perturbation operations
# TODO: revisit and regularize these, make a consistent approach to line-based vs. poly-based functions
#       an probably rework any poly-based functions to in turn call line-based versions as needed

# given a list of lines, for each goes through and subdivides each consecutive pair of points by inserting a
# third point in the middle, repeating the overall process iterations times
# - there are times it might be preferable to specify a target number of segments rather than the more
#   abstract "iterations" approach; could mean reworking how this function works, could mean just
#   defining a different more meat-and-potatoes function
# - this code as such won't work correctly with an implicitly closed polygon: no subdivisions of the 
#   implied line from last point back to first point.  Hrm.  Maybe it would be better to include, and then
#   just often ignore, the final explicit segment of closed polygons to avoid this issue.
# TODO: I appear to have broken this in the process of trying to convert it to handle a single line instead
# of a list of lines
def divide(line, iterations):
    newl = []
    for k in range(iterations):
        newl.append([line[0]])  # include the initial point
        for j in range(len(line) - 1):
            p1 = line[j]
            p2 = line[j + 1]
            mid = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
            newl.append(mid)
            newl.append(p2)
        line = newl
    return line


# given a polyline, perturbs the x/y values of each point.  Doesn't change start and end point unless 
# ends_too is True
def jitter(poly, mag=1, ends_too=False):
    start = 1
    end = len(poly) - 1
    out = []
    if ends_too:
        start -= 1
        end += 1
    for i in range(start, end):
        out.append([poly[i][0] + (random.random() - 0.5) * 2 * mag, poly[i][1] + (random.random() - 0.5) * 2 * mag])
    if not ends_too:
        out.insert(0, poly[0])
        out.append(poly[-1])
    return out


def perlinize(p1, p2, iterations=1, mag=1):
    """ given two points defining a line segment, subdivide and perturb midpoints repeatedly to create perlin-style
        jittering and return the new line
    """
    old = [p1, p2]
    new = old
    # if(iterations < 1): return old
    for k in range(iterations):
        new = []
        new.append(old[0])
        for i in range(len(old) - 1):
            dx = abs(old[i][0] - old[i + 1][0])
            dy = abs(old[i][1] - old[i + 1][1])
            dv = math.sqrt(dx ** 2 + dy ** 2)
            newx = (old[i][0] + old[i + 1][0]) / 2
            newy = (old[i][1] + old[i + 1][1]) / 2
            newx += (random.random() - 0.5) * mag * 2 * dv
            newy += (random.random() - 0.5) * mag * 2 * dv

            newp = [newx, newy]
            new.append(newp)
            new.append(old[i + 1])
        old = copy.deepcopy(new)
    return new


''' misc perturbation functions that should be rewritten to be more flexible
def slant(lines,slantmag=2):
    for l in lines:
        mag = 1/(len(l))
        for p in l:
            p[0] += (random.random() - 0.5) * slantmag * mag
    return lines

def twist(lines):
    for l in lines:
        l[1][0] = width - l[1][0]
    return lines

def feather(lines,feathermag=2):
    for l in lines:
        for p in l:
            p[1] += (random.random() - 0.5) * feathermag
    return lines
'''


# Hatching-centric functions for filling a polygon with new lines

# given a polyline, cycle through consecutive edges adding a segment from midpoint n to midpoint n+1
# - could be improved for esp. small values of numhatch by choosing the initial edge at random
# - could be improved by returning one long polyline instead of a set of short segments
# - is there an error with how the cycling happens now that creates a retreat or backtrack early on?
def circuitpolyline(p, numhatch=10):
    hatches = []
    points = p
    cycle = len(points)

    # initial line
    [a, b] = [[p[0], p[1]], [p[1], p[2]]]
    p1 = getlinebisect(a[0], a[1], random.random())
    p2 = getlinebisect(b[0], b[1], random.random())
    hatches.append([p1, p2])

    for i in range(1, numhatch):
        # b = edges[(i+1)%cycle]
        b = [p[i % cycle], p[(i + 1) % cycle]]
        p1 = hatches[i - 1][1]
        p2 = getlinebisect(b[0], b[1], random.random())
        hatches.append([p1, p2])

    hatches.append([hatches[-1][1], hatches[0][0]])

    return hatches


# generates a bounded set of parallel lines at a given angle and spacing and returns them as "out"
# - uses slope to determine whether to iterate over x or y axis while drawing lines, within 
#   what is essentially a larger outer bounding box, so that it's guaranteed to generate lines
#   that hatch the whole target figure.  This could be improved, possibly by using a circumscribing
#   circle as the outer boundary, tangent to the corners of the inner bounding box or even with
#   more work the polygon itself
def parallelhatch(minxy, maxxy, angle=0.001, step=1):
    xmin, ymin = minxy
    xmax, ymax = maxxy

    out = []  # our accumulating set of hatch lines

    # calculate the spans of these bounds, dy and dx, and expand them by a tiny amount to help make sure bounding
    # box intersections happen even with parallel edges on the source polyline.
    # - would be better to handle those edge cases exactly, but this seems to work fine in general
    dx = xmax - xmin
    dy = ymax - ymin
    xmin -= 0.00001
    ymin -= 0.00001
    xmax += 0.00001
    ymax += 0.00001

    # cheap div by zero insurance
    if angle % math.pi / 2 == 0:
        angle += 0.001

    # calculate slope of our hatch lines
    slope = math.tan(angle)
    stepx = step / abs(math.sin(angle))
    stepy = step / abs(math.cos(angle))

    # there are four classes of slope for which generating hatch lines can happen, where the 
    # iteration is forward or backward and on the y or x axes.  This code is messy and has been
    # debugged at least once.
    if slope >= 1:
        x = xmin - dx
        while x < xmax:
            out.append([[x, ymin], [x + (dy / slope), ymax]])
            x += stepx
    elif slope >= 0:
        y = ymin - dx * slope
        while y < ymax:
            out.append([[xmin, y], [xmax, y + (dx * slope)]])
            y += stepy
    elif slope >= -1:
        y = ymin
        while y < ymax + abs(dx * slope):
            out.append([[xmin, y], [xmax, y + (dx * slope)]])
            y += stepy
    else:
        x = xmax + dx
        while x > xmin:
            out.append([[x, ymin], [x + (dy / slope), ymax]])
            x -= stepx

    return out


# hatch the interior of convex polygon poly by cropping some lines to fit
# - angle is in radians, convert from degrees before passing
# - seems to work okay on self-intersecting and non-convex polygons as well, though
#   I didn't originally write it to do so and haven't tested it thoroughly at all
def crophatch(poly, angle=0.001, step=1):
    inhatch = []  # the uncropped hatch lines
    outhatch = []  # the cropped hatch we're producing

    # get a bounding rect around the poly
    minxy, maxxy = getboundingbox(poly)
    print("min and max xy: ", minxy, ", ", maxxy)

    # fetch some hatch lines
    inhatch = parallelhatch(minxy, maxxy, angle, step)

    # The main job of htis function: for each inhatch line, try to intersect with each line in 
    # our polygon.
    # - when there are two intersections, that means a hatch line entered and then exited the polygon
    #   and should be cropped down at those two intersection points to create a new, shorter line.
    # - intersections should come in pairs: for a non-convex or self-intersecting polygon this means
    #   we might get two, four, six, etc. points out of the tests on a given inhatch line, and should
    #   record each of those pairs as a hatch line segment
    # - current code can produce odd numbered of intersections, something about which I have accomplished
    #   no useful thinking or testing, currently just throwing those results the fuck out and moving on. 
    for line in inhatch:
        out = []  # our located points of intersection
        p1 = line[0]  # p1 and p2 are start and end points of the hatch line we're testing
        p2 = line[1]
        # iterate through our polyline, taking points 1 and 2, 2 and 3, 3 and 4, etc and testing the 
        # line segment defined by that pair against the hatch line
        for i in range(len(poly)):
            p3 = poly[i]
            # special case to test the implied last segment of a closed polygon, the first and last points
            if i == len(poly) - 1:
                p4 = poly[0]
            else:
                p4 = poly[i + 1]
            newp = find_intersection(p1, p2, p3, p4)
            # if newp != None:
            if newp:
                out.append(newp)
        # there might be 2, 4, 6...intersections in valid hatch line vs. a non-convex poly; handling this
        # correctly requires sorting the segments of the carved up hatch line in asc. or desc. order along
        # the line, e.g. by x or y coord (edge case for cardinal lines I suppose)
        # - currently using out.sort() which...seems to work?  I have not tested or thought through this
        # - have seen length 1 lists in out, don't know if 3+ odd lists have shown up but handling that
        #   case just in case as well
        if len(out) > 1 and len(out) % 2 == 0:
            out.sort()
            for i in range(0, len(out), 2):
                outhatch.append([out[i], out[i + 1]])

    return outhatch


# More general drawing functions

# generate a 2D array of squares as polylines
def getsquaregrid(w=8, h=5, length=10):
    squareg = [None] * w
    for i in range(w):
        squareg[i] = [None] * h
        for j in range(h):
            x1 = i * length
            y1 = j * length
            x2 = (i + 1) * length
            y2 = (j + 1) * length
            newsq = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
            squareg[i][j] = newsq
    return squareg


# File management functions ######

# take in a list of one or more .svg files in the local directory, and optional layout arguments, and
# execute a shell call to vypye to write out a single multi-layer svg file containing each source file
# as a separate layer
def vpypeout(outfiles, outname="out", scalew=11, scaleh=8, pagew=14, pageh=11, landscape=True, linemerge=True,
             linesort=True):
    vstring = "vpype "
    for i in range(len(outfiles)):
        vstring += 'read --single-layer --layer ' + str(i + 1) + ' ' + outfiles[i] + ' '
    # linemerge = False
    vstring += 'scaleto ' + str(scalew) + 'in ' + str(scaleh) + 'in '
    vstring += 'layout '
    if landscape:
        vstring += '--landscape '
    vstring += str(pagew) + 'inx' + str(pageh) + 'in '
    if linemerge:
        vstring += 'linemerge '
    if linesort:
        vstring += 'linesort '

    vstring += 'write ' + outname + '.svg'

    os.system(vstring)


def new_artwork():
    """ wrapper around matplotlib plt.figure() function to hide library-specific call """
    artwork = plt.figure()
    return add_layer(artwork)


def add_layer(artwork):
    """ wrapper around matplotlib-centric axes functions """
    artwork.axes.append(makeaxes(artwork))
    return artwork


def writefigure(fig, xbounds=[0, 100], ybounds=[0, 100], name="out", drawingsize=[12, 9], pagesize=[14, 11]):
    """ given a matplotlib Figure object fig, goes through and draws each individual axis in the figure
        to an intermediate .svg file; then invokes a shell call to vpype to combine all of those files into
        a single optimized multi-layer final .svg.

        fig: Figure - the required matplotlib Figure object
        xbounds: optional [x1, x2] pair defining far left and right coordinates of the figure space to render
            relative to the literal coordinate values of lines etc in the source drawing
        ybounds: optional [y1, x1] ibid for top and bottom coordinates
        name: optional specific filename string to write
        drawingsize: optional [width, height] pair in inches into which to autoscale the drawing
        pagesize: optional [width, height] pair in inches to define the page size

        Default xbounds and ybounds may not be terribly helpful, but are generous enough that it should be
        easy enough in a glance at the resulting drawing to tell what kind of scale issues the defaults cause.

        Default page size corresponds to the 14"x11" bristol I tend to use for most of my plotter drawings.
        Default drawing size produces a consistent minimum one inch border of blank page on such drawings.
    """
    outfiles = []
    fig.frameon = False
    fig.dpi = 100
    fig.figsize = drawingsize
    # take in a list of axes and write out individual files
    for a in fig.axes:
        # turn off rendering of every axes except the one we're drawing
        # also need to do set_axis_off() for all axes, every time, for some reason?
        for j in fig.axes:
            j.set_axis_off()
            j.set_visible(False)

        a.set_xlim(xbounds)
        a.set_ylim(ybounds)

        a.set_visible(True)
        tempfile = 'temp' + str(random.random()) + '.svg'
        outfiles.append(tempfile)
        fig.savefig(tempfile, pad_inches=0)

    # pipe output through vpype to create final output file
    vpypeout(outfiles, name, drawingsize[0], drawingsize[1], pagesize[0], pagesize[1])

    for a in fig.axes:
        a.set_visible(True)

    # finally, display the figure on screen
    # TODO: consider replacing this with a direct display of the svg file rendered above
    plt.show()


# matplotlib Axes generation utility functions #############################

def makeaxes(fig, num=1, arect=[0.0, 0.0, 1.0, 1.0]):
    """ create a set of Axes objects attached to Figure object fig, each occupying a portion of fig's drawing space,
        which is defined in normalized coordinate space 0,0 at bottom left to 1,1 top right.  The rect coords are
        x origin, y origin, x width, y height.  e.g. [0.5,0,0.5,0.5] would fill the bottom right quadrant of the fig.

        Calling without optional arguments creates a single axes object occupying the entire Figure drawing area.

        Returns a list of the created Axes.
    """
    axs = []
    for i in range(num):
        newax = fig.add_axes(arect, frameon=False, label=str(random.random()))
        newax.set_frame_on(False)
        newax.set_aspect('equal')
        axs.append(newax)
    return axs


def makeaxesgrid(fig, num=1, cols=1, rows=1):
    """ Create and return an evenly distributed grid of axes based on divvying up the full figure area
        into cols x rows rects.
    """
    axs = []
    dx = 1 / cols
    dy = 1 / rows
    for i in range(cols):
        for j in range(rows):
            newax = makeaxes(fig, num, [dx * i, dy * j, dx, dy])
            for a in newax:
                axs.append(a)
    return axs
