
"""
The most important function in this file is the get_cylinder function
You should probably not directly use any of the other functions here.

The goal of this file is to take an image of a Poincare disc and put it on the cylinder


Important note: the functions here consider the input image to be a square image,
whose inscribed circle is the boundary of the Poincare disc.

Example Running:

    get_cyl_ok(20,3000,3000,"poincare.png","cylinder.png")

gives a "cylinder.png" that's 3000x3000 pixels large, which is based on "poincare.png",
and goes from a height of 1 to 21 on the hyperbola.

"""

import math
import sys
from PIL import Image

def get_hyp_pt(h,th):
    """
    takes a point on the cylinder (h height, th angle) and gives 
    the associated triple of points on the hyperbola
    (inverse archimedean(?) map)
    given in form (x,y,t)
    """
    t = h
    r = math.sqrt(t*t-1) # radius
    x = r*math.cos(th)
    y = r*math.sin(th)
    return (x,y,t)

def get_poinc_pt(x,y,t):
    """
    takes a point on the hyperbolic plane and does a poincare mapping
    giving us a point on the unit disc (given by (x,y))
    """
    a = 1/(t+1)
    x_out = a*x
    y_out = a*y
    return (x_out,y_out)

def cyl_to_poinc(h,th):
    """
    taking a cylinder point, gives the corresponding poincare model point
    as an x,y tuple
    """
    x,y,t = get_hyp_pt(h,th)
    return get_poinc_pt(x,y,t)

def get_pixel(x,y,pix,sz):
    """
    given x,y coords give the proper pixel
    assumes that center of pix is the origin (0,0)
    assumes square image
    """
    l = sz/2
    x_pic_coord = int(l + x*(l-1))
    y_pic_coord = int(l + y*(l-1))
    return pix[x_pic_coord,y_pic_coord]

def get_cylinder(height,ih,iw,fn,fn2, sheight=1):
    """
    Takes a height, an image height ih, width iw, input filename, and output filename.
    
    Optionally takes sheight, which is the starting height if you don't want to 
    start at the bottom of the hyperboloid.

    Important note: this function considers the input image whose filename is fn
    to be a square image, whose inscribed circle is the boundary of the Poincare disc.
    """
    im = Image.open(fn)
    pixin = im.load()
    pixout = Image.new(im.mode,(iw,ih))
    outaccess = pixout.load()
    
    sz = im.size[0]

    for i in range(ih):
        for j in range(iw):
            th = j*2*math.pi/iw
            h = sheight + height*i/ih
            x,y = cyl_to_poinc(h,th)
            outaccess[j,i] = get_pixel(x,y,pixin,sz)
    pixout.save(fn2)

    
if __name__ == "___main__":
    if len(sys.argv) < 6:
        print("Transforms a circle representing a Poincare model to a cylindrical projection\n\nTakes a height, image width, image height, \ninput filename, output filename, and optionally an initial displacement\n\nNote: the supplied input image must be a square image with the center of the circle at the center of the image")
        return 1
    height = int(sys.argv[1])
    ih = int(sys.argv[2])
    iw = int(sys.argv[3])
    fnin = sys.argv[4]
    fnout = sys.argv[5]
    sheight = 1
    if len(sys.argv) == 7:
        sheight = int(sys.argv[6])
    get_cylinder(height,ih,iw,fnin,fnout,sheight)
    return
