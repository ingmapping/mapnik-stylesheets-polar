Rendering OpenStreetMap with Mapnik into Polar-Centric Tiles or Images
----------------------------------------------------------------------

***
The Style and the supplied Tools are specialized for rendering Polar Regions.
***

Welcome, if you have Mapnik and osm2pgsql installed and you want to render your own OSM tiles of the Antarctic Polar region , you've come to the right place. Due to the position of Antarctica around the South Pole the usual map web map projections [e.g. Web Mercator](https://epsg.io/3857) show Antarctica rather distorted. This project can help you if you want to generate raster tiles of the Antartica based on OpenStreetMap and Natural Earth data in custom [WGS 84 / Antarctic Polar Stereographic projection](https://epsg.io/3031) with tools like Mapnik and osm2psql.

This project was forked from https://github.com/MaZderMind/mapnik-stylesheets-polar which is the development location of the Mapnik XML stylesheets powering http://polar.openstreetmap.de/. The website is not working anymore since the OSM Antarctica Map is currently unmaintained. 

To this new directory, modifications (e.g. links and instructions) have been made in order to update the project and make it work again. The update.sh script was taken from another fork: https://github.com/giggls/mapnik-stylesheets-polar and updated for proper use here. 

Quick References
----------------
If you need additional info, please read:
 - http://wiki.openstreetmap.org/wiki/Mapnik
 - https://wiki.openstreetmap.org/wiki/Antarctica/Creating_a_map

If you are new to Mapnik see:
 - http://mapnik.org
 
Required
--------

Mapnik >= 2.0.0 | The rendering library
 * Built with the PostGIS plugin
 * http://mapnik.org/pages/downloads.html 

osm2pgsql | Tool for importing OSM data into PostGIS
 * https://wiki.openstreetmap.org/wiki/Osm2pgsql
 * https://github.com/openstreetmap/osm2pgsql

Coastline Shapefiles
 * run update.sh or download shapefiles manually into data folder:
   - http://data.openstreetmapdata.com/land-polygons-complete-4326.zip
   - https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_populated_places.zip
   - http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_boundary_lines_land.zip

Antarctica data in PostGIS
 * An Antarctica-extract
   - http://download.geofabrik.de/antarctica-latest.osm.pbf
 * Import this into PostGIS with osm2pgsql

Quickstart
----------

    git clone https://github.com/ingmapping/mapnik-stylesheets-polar.git mapnik-stylesheets-polar
    cd mapnik-stylesheets-polar
    ./update.sh
   

Instructions to generate tiles with render_polar_tiles.py (if update.sh script was not used)
----------
First, load antarctica osm data into your postgis database. 

    osm2pgsql --create --database antarctica --latlong --prefix ant --style=osm2pgsql.style --cache 2000 data/antarctica-     latest.osm.pbf

Afterwards, create the 'inc' files with generate_xml.py or by manually creating them.

    ./generate_xml.py --accept-none --dbname antarctica --prefix ant --epsg=4326 --world_boundaries=/mapnik-stylesheets-polar/data
    
    # render an image
    ./render_polar.py --style osm.xml --bbox -3000000,0,0,3000000 --file top-left --size 500x500
    
    # render tiles
    ./render_polar_tiles.py --style=osm.xml --dir=../antarctica_tiles/tiles --minzoom=1 --maxzoom=7

    # render tiles around stations, peaks, islands,...etc.
    ./render_polar_tiles.py --style=osm.xml --dir=../antarctica_tiles/tiles --minzoom=8 --maxzoom=18 --db=dbname=antarctica --only-   interesting 
    
    # show tiles via view.html, which should be in the antarctica_tiles folder. If the tiles don't load, check the path to the tiles inside the view.html file.


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
