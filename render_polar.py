#!/usr/bin/python
#
# render data from postgresql to an image or a pdf
#

from optparse import OptionParser
import sys, os

try:
    import mapnik2 as mapnik
except:
    import mapnik

cairo_exists = True

try:
    import cairo
except ImportError:
    cairo_exists = False

def main():
    style = "/usr/share/osm-mapnik/osm.xml"
    file = "map"
    type = "png"
    width = 800
    height = 600
    bbox = (-180, -90, 180, 90)
    
    parser = OptionParser()
    parser.add_option("-s", "--style", action="store", type="string", dest="style", 
                      help="path to the mapnik stylesheet xml, defaults to the openstreetmap default style: "+style)
    
    parser.add_option("-f", "--file", action="store", type="string", dest="file", 
                      help="path to the destination file without the file extension, defaults to "+file)
    
    parser.add_option("-t", "--type", action="store", type="string", dest="type", 
                      help="file type to render, defaults to "+type)
    
    parser.add_option("-x", "--size", action="store", type="string", dest="size", 
                      help="requested sizeof the resulting image in pixels, format is <width>x<height>, defaults to "+str(width)+"x"+str(height))
    
    parser.add_option("-b", "--bbox", action="store", type="string", dest="bbox", 
                      help="the bounding box to render in the format l,b,r,t, defaults to "+str(bbox))
    
    parser.add_option("-z", "--zoom", action="store", type="int", dest="zoom", 
                      help="the zoom level to render. this overrules the default size but it can't be used together with an explicit --size option")
    
    (options, args) = parser.parse_args()
    if options.style:
        style = options.style
    
    if options.file:
        file = options.file
    
    if options.type:
        type = options.type
    
    if options.size and options.zoom:
        print "can't combine --size and --zoom"
        print
        parser.print_help()
        sys.exit(1)
    
    if options.size:
        try:
            (width, height) = map(int, options.size.split("x"))
        except ValueError, err:
            print "invalid syntax in size argument"
            print
            parser.print_help()
            sys.exit(1)
    
    if options.bbox:
        try:
            bbox = map(float, options.bbox.split(","))
            if len(bbox) < 4:
                raise ValueError
        except ValueError, err:
            print "invalid syntax in bbox argument"
            print
            parser.print_help()
            sys.exit(1)
    
    if options.zoom:
        (width, height) = zoom2size(bbox, options.zoom);
    
    print "rendering bbox %s in style %s to file %s which is of type %s in size %ux%u\n" % (bbox, style, file, type, width, height)
    
    # create map
    m = mapnik.Map(width,height)
    
    # load style
    mapnik.load_map(m, style)
    
    # create projection object
    #prj = mapnik.Projection("+proj=stere +lat_0=-90 +lat_ts=-71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
    
    #c0 = prj.forward(Coord(bbox[0],bbox[1]))
    #c1 = prj.forward(Coord(bbox[2],bbox[3]))
    #e = Envelope(c0.x,c0.y,c1.x,c1.y)
    
    # project bounds to map projection
    #e = mapnik.forward_(mapnik.Envelope(*bbox), prj)
    e = mapnik.Envelope(*bbox)
    
    # zoom map to bounding box
    m.zoom_to_box(e)
    #m.zoom_all()
    
    file = file + "." + type
    if(type in ("png", "jpeg")):
        s = mapnik.Image(width, height)
    
    elif cairo_exists and type == "svg":
        s = cairo.SVGSurface(file, width, height)
    
    elif cairo_exists and type == "pdf":
        s = cairo.PDFSurface(file, width, height)
    
    elif cairo_exists and type == "ps":
        s = cairo.PSSurface(file, width, height)
    
    else:
        print "invalid image type"
        print
        parser.print_help()
        sys.exit(1)
    
    mapnik.render(m, s)
    
    if isinstance(s, mapnik.Image):
        view = s.view(0, 0, width, height)
        view.save(file, type)
    
    elif isinstance(s, cairo.Surface):
        s.finish()

def zoom2size(bbox, zoom):
    prj = mapnik.Projection("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs^")
    e = mapnik.forward_(mapnik.Envelope(*bbox), prj)
    wm = e.maxx - e.minx;
    hm = e.maxy - e.miny;
    
    if zoom == 1:
        scale = 279541132.014
    
    elif zoom == 2:
        scale = 139770566.007
    
    elif zoom == 3:
        scale = 69885283.0036
    
    elif zoom == 4:
        scale = 34942641.5018
    
    elif zoom == 5:
        scale = 17471320.7509
    
    elif zoom == 6:
        scale = 8735660.37545
    
    elif zoom == 7:
        scale = 4367830.18772
    
    elif zoom == 8:
        scale = 2183915.09386
    
    elif zoom == 9:
        scale = 1091957.54693
    
    elif zoom == 10:
        scale = 545978.773466
    
    elif zoom == 11:
        scale = 272989.386733
    
    elif zoom == 12:
        scale = 136494.693366
    
    elif zoom == 13:
        scale = 68247.3466832
    
    elif zoom == 14:
        scale = 34123.6733416
    
    elif zoom == 15:
        scale = 17061.8366708
    
    elif zoom == 16:
        scale = 8530.9183354
    
    elif zoom == 17:
        scale = 4265.4591677
    
    elif zoom == 18:
        scale = 2132.72958385
    
    # map_width_in_pixels = map_width_in_metres / scale_denominator / standardized_pixel_size
    # see http://www.britishideas.com/2009/09/22/map-scales-and-printing-with-mapnik/
    
    wp = int(wm / scale / 0.00028)
    hp = int(hm / scale / 0.00028)
    
    return (wp, hp)

if __name__ == "__main__":
  main()
