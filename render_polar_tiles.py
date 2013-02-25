#!/usr/bin/python
#
# render data from postgresql to an tiles in an polar projection
#

from optparse import OptionParser
import sys, os

import mapnik

cairo_exists = True

try:
    import cairo
except ImportError:
    cairo_exists = False

def main():
    style = "/usr/share/osm-mapnik/osm.xml"
    dir = "tiles"
    type = "png"
    scale = 6000000
    minzoom = 1
    maxzoom = 6
    
    parser = OptionParser()
    parser.add_option("-s", "--style", action="store", type="string", dest="style", 
                      help="path to the mapnik stylesheet xml, defaults to the openstreetmap default style: "+style)
    
    parser.add_option("-d", "--dir", action="store", type="string", dest="dir", 
                      help="path to the destination folder, defaults to "+type)
    
    parser.add_option("-t", "--type", action="store", type="string", dest="type", 
                      help="file type to render, defaults to "+type)
    
    parser.add_option("-z", "--minzoom", action="store", type="int", dest="minzoom", 
                      help="minimum zoom level to render, defaults to "+minzoom)
    
    parser.add_option("-Z", "--maxzoom", action="store", type="int", dest="maxzoom", 
                      help="maximum zoom level to render, defaults to "+maxzoom)
    
    (options, args) = parser.parse_args()
    if options.style:
        style = options.style
    
    if options.dir:
        dir = options.dir
    
    if options.type:
        type = options.type
    
    if options.minzoom:
        minzoom = options.minzoom
    
    if options.maxzoom:
        maxzoom = options.maxzoom
    
    # create map
    m = mapnik.Map(255,255)
    
    # load style
    mapnik.load_map(m, style)
    
    for z in range(minzoom, maxzoom+1):
        n = 2**z
        for x in range(0, n):
            for y in range(0, n):
                render_tile(m, z, x, y, scale, dir, type)

def render_tile(m, z, x, y, scale, dir, type):
    n = 2**z
    n2 = n/2
    x2n = x-n2
    y2n = (n-y-1)-n2

    tilesize = scale / n;


    bbox = [
        tilesize * x2n,
        tilesize * y2n,
        tilesize * (x2n+1),
        tilesize * (y2n+1)
    ]
    print "z=%u x=%u y=%u -> n=%u, n2=%u -> (x2n=%u, y2n=%u) -> (%f,%f,%f,%f)" % (z, x, y, n, n2, x2n, y2n, bbox[0], bbox[1], bbox[2], bbox[3])

    e = mapnik.Box2d(*bbox)
    
    # zoom map to bounding box
    m.zoom_to_box(e)
    
    pdir = dir + "/" + str(z) + "/" + str(x)
    if not os.path.exists(pdir):
        os.makedirs(pdir)

    file = dir + "/" + str(z) + "/" + str(x) + "/" + str(y) + "." + type
    s = mapnik.Image(255, 255)
    
    mapnik.render(m, s)
    
    view = s.view(0, 0, 255, 255)
    view.save(file, type)

if __name__ == "__main__":
  main()
