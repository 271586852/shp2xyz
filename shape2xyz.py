#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import gdal, ogr,osr

def shp2xyz(shpin, xyz):
    '''
    collector of functions that reformats shapefiles (.shp) to .xyz files
    :param shpin: shapefile (point, line, or polygon)
    :param xyz: filename to store output
    :return: MIKE compatible .xyz formated shapefile
    '''
    shp_ds = ogr.Open(shpin)
    shp_lyr = shp_ds.GetLayer()

    # gets the shapefile type and applies the necessary function
    if shp_lyr.GetGeomType() == 1:
        print("Type: point")
        point2xyz(shpin, xyz)
    elif shp_lyr.GetGeomType() == 2:
        print("Type: polyline")
        line2xyz(shpin, xyz)
    elif shp_lyr.GetGeomType() == 3:
        print("Type: polygon")
        poly2xyz(shpin, xyz)


def point2xyz(shpin, xyz):
    '''
    reformat point-type .shp to .xyz
    :param shpin:
    :param xyz:
    :return:
    '''
    shp_ds = ogr.Open(shpin)
    shp_lyr = shp_ds.GetLayer()

    print ('found %d number of features!' % len(shp_lyr))

    fopen = open(xyz, 'a')

    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        print (geom.GetGeometryType())

        connectivity = feat.GetFieldAsInteger('CON')
        print (connectivity)
        line = ''.join([str(geom.GetX()), ' ', str(geom.GetY()), ' ', str(connectivity), '\n'])
        fopen.write(line)

    fopen.close()

def line2xyz(shpin, xyz):
    '''
    reformat line-type .shp to .xyz
    :param shpin:
    :param xyz:
    :return:
    '''
    shp_ds = ogr.Open(shpin)
    shp_lyr = shp_ds.GetLayer()

    print ('found %d number of features!' % len(shp_lyr))

    first_line = True

    fopen = open(xyz, 'a')

    # shp_ds = ogr.Open(r'test\test_line.shp')
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
            fopen.write(line)
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
                    fopen.write(line)

    print('Number of lines:', line_count)
    print('Number of interpolated points:', interp_line_count)


    fopen.close()

def poly2xyz(shpin, xyz):
    '''
    reformat polygon-type .shp to .xyz
    :param shpin:
    :param xyz:
    :return:
    '''
    shp_ds = ogr.Open(shpin)
    shp_lyr = shp_ds.GetLayer()

    print ('found %d number of features!' % len(shp_lyr))

    first_line = True

    fopen = open(xyz, 'a')

    for feat in shp_lyr:
        geom = feat.GetGeometryRef()
        ring = geom.GetGeometryRef(0)
        for i in range(0, ring.GetPointCount()):
            if first_line:
                line = ''.join([str(ring.GetPoint(i)[0]), ' ', str(ring.GetPoint(i)[1]), ' ', '1\n'])
                first_line = False
            else:
                line = ''.join([str(ring.GetPoint(i)[0]), ' ', str(ring.GetPoint(i)[1]), ' ', '0\n'])
            fopen.write(line)
    fopen.close()



if __name__=='__main__':
    test_folder = './test/'

    shp_point = 'test_point.shp'
    shp_point_xyz = 'test_point.xyz'

    shp_line = 'test_line.shp'
    shp_line_xyz = 'test_line.xyz'

    shp_poly = 'test_poly.shp'
    shp_poly_xyz = 'test_poly.xyz'

    # point2xyz(test_folder + shp_point, test_folder + shp_point_xyz)
    line2xyz(test_folder + shp_line, test_folder + shp_line_xyz)
    # poly2xyz(test_folder + shp_poly, test_folder + shp_poly_xyz)
    # shp2xyz(test_folder + shp_poly, test_folder + shp_poly_xyz)