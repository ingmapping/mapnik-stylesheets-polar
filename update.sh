#!/bin/sh

START=`date +"%Y-%m-%d %H:%M:%S"`

echo "`date +"%Y-%m-%d %H:%M:%S"` downloading files"
wget -nv http://download.geofabrik.de/antarctica-latest.osm.pbf -O data/antarctica-latest.osm.pbf
wget -nv http://data.openstreetmapdata.com/land-polygons-complete-4326.zip -O data/land-polygons-complete-4326.zip
wget -nv http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_populated_places.zip -O data/ne_10m_populated_places.zip
wget -nv http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_boundary_lines_land.zip -O data/ne_110m_admin_0_boundary_lines_land.zip

echo "`date +"%Y-%m-%d %H:%M:%S"` unpacking data"
unzip -o data/land-polygons-complete-4326.zip -d data
unzip -o data/ne_10m_populated_places.zip -d data
unzip -o data/ne_110m_admin_0_boundary_lines_land.zip -d data

echo "`date +"%Y-%m-%d %H:%M:%S"` importing database"
osm2pgsql --create --database antarctica --latlong --prefix ant --style=osm2pgsql.style --cache 2000 data/antarctica-latest.osm.pbf

echo "`date +"%Y-%m-%d %H:%M:%S"` re-generating mapnik xml"
./generate_xml.py --accept-none --dbname antarctica --prefix ant --epsg=4326 --world_boundaries=~/mapnik-stylesheets-polar/data/

echo "`date +"%Y-%m-%d %H:%M:%S"` rerender base tiles"
 ./render_polar_tiles.py --style=osm.xml --dir=../antarctica_tiles/tiles --minzoom=1 --maxzoom=7

echo "`date +"%Y-%m-%d %H:%M:%S"` rerender interesting zoom-tiles"
./render_polar_tiles.py --style=osm.xml --dir=../antarctica_tiles/tiles --minzoom=8 --maxzoom=18 --db=dbname=antarctica --only-interesting --only-interesting-list=../htdocs/interesting.json

echo "`date +"%Y-%m-%d %H:%M:%S"` updating view"
sed "s/###TIME###/`date +'%d.%m.%Y %H:%M:%S'`/g" <view.html >../antarctica_tiles/index.html
