
Rendering OpenStreetMap with Mapnik into Polar-Centric Tiles or Images
----------------------------------------------------------------------

***
This is not the Style you should use to render arbitrary Images. The Style and
the supplied Tools are specialized for rendering Polar Regions.
***

Welcome, if you have Mapnik and osm2pgsql installed and you want
to render your own OSM tiles, you've come to the right place.

This is the development location of the Mapnik XML stylesheets powering
http://polar.openstreetmap.de/antarctica/

This directory also holds an assortment of helpful utility scripts for
working with Mapnik and the OSM Mapnik XML stylesheets.

However, the easiest way to start rendering Mapnik tiles is to use the 
'render_tiles.py' script located within this directory.


Quick References
----------------
If you need additional info, please read:
 - http://wiki.openstreetmap.org/wiki/Mapnik

If you are new to Mapnik see:
 - http://mapnik.org


Required
--------

Mapnik >= 2.0.0 | The rendering library
 * Built with the PostGIS plugin
 * http://trac.mapnik.org/wiki/Mapnik-Installation

osm2pgsql trunk | Tool for importing OSM data into PostGIS
 * The latest trunk source is highly recommended
 * http://svn.openstreetmap.org/applications/utils/export/osm2pgsql

Coastline Shapefiles
 * Download these locally using ./get-coastlines.sh

Antarctica data in PostGIS
 * An Antarctica-extract
   - http://download.geofabrik.de/openstreetmap/antarctica.osm.pbf
 * Import this into PostGIS with osm2pgsql



Quickstart
----------

    git clone https://github.com/MaZderMind/mapnik-stylesheets.git mapnik-stylesheets-polar
    cd mapnik-stylesheets-polar
    ./get-coastlines.sh
    ./generate_xml.py --epsg 4326 --extent -180,-90,180,90 --dbname=$USER --prefix ant --accept-none
    wget http://download.geofabrik.de/openstreetmap/antarctica.osm.pbf
    osm2pgsql --create --cache 1024 --database $USER --prefix ant --latlong antarctica.osm.pbf
    
    # render an image
    ./render_polar.py --style osm.xml --bbox -3000000,0,0,3000000 --file top-left --size 500x500
    
    # render tiles
    ./render_polar_tiles.py --minzoom 1 --maxzoom 4 --threads 4 --style osm.xml

    # render tiles around stations, peaks, islands, ... (NOTE: currently only McMurdo is counted as interesting)
    ./render_polar_tiles.py --minzoom 5 --maxzoom 18 --threads 4 --style osm.xml --only-interesting
    
    # show tiles via view.html

Manually editing 'inc' files
----------------------------

To manually configure your setup you will need to work with the XML snippets 
in the 'inc' directory which end with 'template'.

Copy them to a new file and strip off the '.template' extension.

    cp inc/datasource-settings.xml.inc.template inc/datasource-settings.xml.inc
    cp inc/fontset-settings.xml.inc.template inc/fontset-settings.xml.inc
    cp inc/settings.xml.inc.template inc/settings.xml.inc

Then edit the settings variables (e.g. '%(value)s') in those files to match your configuration.
Details can be found in each file. Stick with the recommended defaults unless you know better.

Troubleshooting
---------------

If trying to read the XML with Mapnik (or any of the python scripts included here that use Mapnik)
fails with an error like `XML document not well formed` or `Entity 'foo' not defined`, then try running
xmllint, which may provide a more detailed error to help you find the syntax problem in the XML (or its
referenced includes):

    xmllint osm.xml --noout

Not output from the above command indicates the stylesheet should be working fine.

If you see an error like: `warning: failed to load external entity "inc/datasource-settings.xml.inc"` then this
likely indicates that an include file is missing, which means that you forgot to follow the steps above to generate the needed includes on the fly either by using `generate_xml.py` or manually creating your inc files.
