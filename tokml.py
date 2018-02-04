#!/usr/bin/env python3

import simplekml
import json
import os
import sys
import argparse


def import_point(year, kml_folder):
    try:
        print(year)
        with open(os.path.join(year, '裝車場及車站.geojson')) as fd:
            d = json.load(fd)
    except:
        return

    if len(d['features']) > 0:
        doc = kml_folder.newdocument(name=year + ' 裝車場及車站')
        for p in d['features']:
            doc.newpoint(
                coords=[p['geometry']['coordinates']],
                description=' '.join([str(i) for i in p['properties'].values()]),
                name=p['properties']['name'])


def import_line(year, kml_folder):
    try:
        print(year)
        with open(os.path.join(year, '路線.geojson')) as fd:
            d = json.load(fd)
    except:
        return

    if len(d['features']) > 0:
        doc = kml_folder.newdocument(name=year +' 路線')
        for l in d['features']:
            name = l['properties']['name']
            desc = ' '.join([str(i) for i in l['properties'].values()])
            if l['geometry']['type'] == 'LineString':
                line = doc.newlinestring(name=name, description=desc)
                line.coords = l['geometry']['coordinates']
            elif l['geometry']['type'] == 'MultiLineString':
                multiline = doc.newmultigeometry(name=name, description=desc)
                for c in l['geometry']['coordinates']:
                    multiline.newlinestring(coords=c)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='convert tsc railway map from GeoJSON to KML.')
    parser.add_argument('-o', metavar='tsc_railway_map.kml', type=str, default='tsc_railway_map.kml')
    parser.add_argument('year', metavar='YEAR', type=str, nargs='+')
    args = parser.parse_args()

    kml = simplekml.Kml()
    for year in args.year:
        fol = kml.newfolder(name=year)
        import_point(year, fol)
        import_line(year, fol)
    kml.save(args.o)

