from osgeo import ogr

shp_ds = ogr.Open(r'C:\Users\RISC\Desktop\pythonCode\shp2xyz-master\test\test_line.shp')
if shp_ds is None:
    raise ValueError(f"Could not open shapefile: ")
shp_lyr = shp_ds.GetLayer()
print ('found %d number of features!' % len(shp_lyr))
first_line = True

for feat in shp_lyr:
        print(feat.GetGeometryRef())
        geom = feat.GetGeometryRef()
        print(geom.GetPointCount())
        for i in range(0, geom.GetPointCount()):
            if first_line:
                line = ''.join([str(geom.GetPoint(i)[0]), ' ', str(geom.GetPoint(i)[1]), ' ', '1\n'])
                first_line = False
            else:
                line = ''.join([str(geom.GetPoint(i)[0]), ' ', str(geom.GetPoint(i)[1]), ' ', '0\n'])
            