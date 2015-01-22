## Loading the modules
import os
import simplekml


os.chdir('data')

## Loading osgeo
try:
  from osgeo import ogr, osr
  print 'Import of ogr and osr from osgeo worked.  Hurray!\n'
except:
  print 'Import of ogr and osr from osgeo failed\n\n'

## Is the ESRI Shapefile driver available?
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName

## choose your own name
## make sure this layer does not exist in your 'data' folder
fn = "pointfile.shp"
layername = "points"

## Create shape file
ds = drv.CreateDataSource(fn)
print ds.GetRefCount()

# Set spatial reference
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

## Create Layer
layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)
print(layer.GetExtent())

## Create a point
point1 = ogr.Geometry(ogr.wkbPoint)
point2 = ogr.Geometry(ogr.wkbPoint)

coordspoint1=[5.666449, 51.987009]
coordspoint2=[5.679311, 51.9781475]

## SetPoint(self, int point, double x, double y, double z = 0)
point1.SetPoint(0, coordspoint1[0], coordspoint1[1]) 
point2.SetPoint(0, coordspoint2[0], coordspoint2[1])

## Create a KML file
kml = simplekml.Kml()
kml.newpoint(name="Gaia", coords=[(coordspoint1)])
kml.newpoint(name="Asserpark", coords=[(coordspoint2)])
kml.save("points.kml")

## Export to KML:
print "KML file export"

print point1.ExportToKML()

## Feature is defined from properties of the layer:
layerDefinition = layer.GetLayerDefn()
feature1 = ogr.Feature(layerDefinition)
feature2 = ogr.Feature(layerDefinition)

## Lets add the points to the feature
feature1.SetGeometry(point1)
feature2.SetGeometry(point2)

## Lets store the feature in a layer
layer.CreateFeature(feature1)
layer.CreateFeature(feature2)
print "The new extent"
print layer.GetExtent()
