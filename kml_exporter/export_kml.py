import csv
import sys
from uuid import uuid4
from pathlib import Path

PING_TIMEOUT = 9999

if len(sys.argv) < 5:
    print("Usage: export_kml.py <datalog_file> <output_file> <base_station_lat> <base_station_lon>")

datalog_file_path = Path(sys.argv[1]).expanduser()
output_file_path = Path(sys.argv[2]).expanduser()
base_station_lat = sys.argv[3]
base_station_lon = sys.argv[4]

with open('fileTemplate.xml', 'r') as infile:
    file_template = infile.read()

with open('placemarkTemplate.xml', 'r') as infile:
    placemark_template = infile.read()

placemarks = []


def create_placemark(lon, lat):
    placemark = placemark_template.replace('{lon}', str(lon)).replace('{lat}', str(lat))
    return placemark.replace('{markerId}', f'marker_{uuid4()}')


def append_connected_placemark(lon, lat):
    placemark = create_placemark(lon, lat)
    placemark = placemark.replace('{markerR}', '0').replace('{markerG}', '255').replace('{markerB}', '0')
    placemark = placemark.replace('{labelArgb}', 'ff00ff00')
    placemark = placemark.replace('{name}', '')
    placemarks.append(placemark)


def append_disconnected_placemark(lon, lat):
    placemark = create_placemark(lon, lat)
    placemark = placemark.replace('{markerR}', '255').replace('{markerG}', '0').replace('{markerB}', '0')
    placemark = placemark.replace('{labelArgb}', 'ffff0000')
    placemark = placemark.replace('{name}', '')
    placemarks.append(placemark)


def append_base_station_placemark():
    placemark = create_placemark(base_station_lon, base_station_lat)
    placemark = placemark.replace('{markerR}', '0').replace('{markerG}', '0').replace('{markerB}', '255')
    placemark = placemark.replace('{labelArgb}', 'ff0000ff')
    placemark = placemark.replace('{name}', 'Base Station')
    placemarks.append(placemark)


with open(datalog_file_path) as infile:
    reader = csv.reader(infile, delimiter=';')
    next(reader, None)
    for row in reader:
        lon = float(row[2])
        lat = float(row[1])
        time_since_last_ping = int(row[0])
        if time_since_last_ping > PING_TIMEOUT:
            append_disconnected_placemark(lon, lat)
        else:
            append_connected_placemark(lon, lat)

append_base_station_placemark()

result = file_template.replace('{placemarks}', '\n'.join(placemarks))

with open(output_file_path, 'w') as outfile:
    outfile.write(result)
