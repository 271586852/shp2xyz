from osgeo import ogr, osr

shp_ds = ogr.Open(r'test\test_line.shp')
if shp_ds is None:
    raise ValueError(f"Could not open shapefile: ")
shp_lyr = shp_ds.GetLayer()
print ('found %d number of features!' % len(shp_lyr))
first_line = True

# 获取地理参考
shp_srs = shp_lyr.GetSpatialRef()
print('Shapefile Coordinate System:', shp_srs)

# 创建转换对象 CGCS2000
target_srs = osr.SpatialReference()
target_srs.ImportFromEPSG(4490)  # CGCS2000 EPSG code
transform = osr.CoordinateTransformation(shp_srs, target_srs)

line_count = 0
mid_point_count = 0
interp_line_count = 0

for feat in shp_lyr:
    geom = feat.GetGeometryRef()
    geom.Transform(transform)  # 转换到CGCS2000
    print(geom.GetGeometryName())
    print(geom.GetPointCount())
    for i in range(0, geom.GetPointCount()):
        if first_line:
            line = ''.join([str(geom.GetPoint(i)[0]), ' ', str(geom.GetPoint(i)[1]), ' ', '1\n'])
            first_line = False
        else:
            line = ''.join([str(geom.GetPoint(i)[0]), ' ', str(geom.GetPoint(i)[1]), ' ', '0\n'])
        print('line', line)
        line_count += 1
        # 添加中点值
        if i < geom.GetPointCount() - 1:
            # 线性插值
            num_points = 5  # 设置插值点的数量
            for j in range(1, num_points):
                interp_x = geom.GetPoint(i)[0] + (geom.GetPoint(i+1)[0] - geom.GetPoint(i)[0]) * j / num_points
                interp_y = geom.GetPoint(i)[1] + (geom.GetPoint(i+1)[1] - geom.GetPoint(i)[1]) * j / num_points
                interp_line = ''.join([str(interp_x), ' ', str(interp_y), ' ', '0\n'])
                print('interp_line', interp_line)
                interp_line_count += 1

print('Number of lines:', line_count)
print('Number of interpolated points:', interp_line_count)

