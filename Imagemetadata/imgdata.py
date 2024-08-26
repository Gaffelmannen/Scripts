#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pprint import pprint
from PIL import Image, ExifTags
import piexif
import os

codec = "ISO-8859-1"
baseurl = "https://www.google.com/maps/place/"
directory = '.'

def exif_to_tag(exif_dict):
    exif_tag_dict = {}

    thumbnail = exif_dict.pop('thumbnail')
    try:
        exif_tag_dict['thumbnail'] = thumbnail.decode(codec)
    except:
        pass

    for ifd in exif_dict:
        exif_tag_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode(codec)

            except AttributeError:
                element = exif_dict[ifd][tag]

            exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

    return exif_tag_dict

def main():
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.jpeg'):
                check_coords(filename)

def check_coords(filename):
    im = Image.open(filename)

    exif_dict = piexif.load(im.info.get('exif'))
    exif_dict = exif_to_tag(exif_dict)

    coords = get_gps(exif_dict["GPS"])
    
    if coords is None:
        print("{} - No coords found".format(filename))
    else:
        url  = "{}{},{}".format(baseurl, coords['latitude'], coords['longitude'])
        print("{} - {}".format(filename, url))

def print_content(exif_dict):
    for _ in exif_dict:
        print(_)
        if _ == "GPS":
            pprint(exif_dict[_])
        else:
            print(len(exif_dict[_]))

def _convert_to_degress(value):
    d = float(value[0][0]) / float(value[0][1])
    m = float(value[1][0]) / float(value[1][1])
    s = float(value[2][0]) / float(value[2][1])
    return d + (m / 60.0) + (s / 3600.0)

def get_gps(gps_exif):
    if not "GPSLatitude" in gps_exif.keys():
        return None

    latitude = gps_exif.get('GPSLatitude')
    latitude_ref = gps_exif.get('GPSLatitudeRef')
    longitude = gps_exif.get('GPSLongitude')
    longitude_ref = gps_exif.get('GPSLongitudeRef')

    if latitude:
        lat_value = _convert_to_degress(latitude)
        if latitude_ref != 'N':
            lat_value = -lat_value
    else:
        return {}
    if longitude:
        lon_value = _convert_to_degress(longitude)
        if longitude_ref != 'E':
            lon_value = -lon_value
    else:
        return {}
    return {'latitude': lat_value, 'longitude': lon_value}

if __name__ == '__main__':
   main()