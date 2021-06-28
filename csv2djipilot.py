#!/usr/bin/env python3

from string import Template
import csv
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('csvfile', type=argparse.FileType('r'),
                    help="Specify csv input file")
#parser.add_argument('-outputfile',type=string, required=False, default="pilot.kml")
parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                    default=sys.stdout, help="Specify output file (default:stdout)")

args = parser.parse_args()

CsvFile = args.csvfile.name

print(f'{CsvFile} to {args.output.name}')
#CsvFile = 'exemple.csv'
#CsvFile = 'exemple_simple.csv'
csv_header = False

XML_string = """<?xml version="1.0" encoding="UTF-8"?>

<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document xmlns="">
    <name>chambon_small</name>
    <open>1</open>
    <ExtendedData xmlns:mis="www.dji.com">
      <mis:type>Waypoint</mis:type>
      <mis:stationType>0</mis:stationType>
    </ExtendedData>
    <Style id="waylineGreenPoly">
      <LineStyle>
        <color>FF0AEE8B</color>
        <width>6</width>
      </LineStyle>
    </Style>
    <Style id="waypointStyle">
      <IconStyle>
        <Icon>
          <href>https://cdnen.dji-flighthub.com/static/app/images/point.png</href>
        </Icon>
      </IconStyle>
    </Style>
    <Folder>
      <name>Waypoints</name>
      <description>Waypoints in the Mission.</description>"""
name = None
lon = None
lat = None
height = None
heading = None
gimbal = None
all_coordinates = ""
waypoint_number = 1

waypoint = Template("""      <Placemark>
        <name>Waypoint$waypoint_number</name>
        <visibility>1</visibility>
        <description>Waypoint</description>
        <styleUrl>#waypointStyle</styleUrl>
        <ExtendedData xmlns:mis="www.dji.com">
          <mis:useWaylineAltitude>false</mis:useWaylineAltitude>
          <mis:heading>$heading</mis:heading>
          <mis:turnMode>Auto</mis:turnMode>
          <mis:gimbalPitch>$gimbal</mis:gimbalPitch>
          <mis:useWaylineSpeed>true</mis:useWaylineSpeed>
          <mis:speed>5.0</mis:speed>
          <mis:useWaylineHeadingMode>true</mis:useWaylineHeadingMode>
          <mis:useWaylinePointType>true</mis:useWaylinePointType>
          <mis:pointType>LineStop</mis:pointType>
          <mis:cornerRadius>0.2</mis:cornerRadius>
          <mis:actions param="1000" accuracy="0" cameraIndex="0" payloadType="0" payloadIndex="0">Hovering</mis:actions>
          <mis:actions param="0" accuracy="0" cameraIndex="0" payloadType="0" payloadIndex="0">ShootPhoto</mis:actions>
          <mis:actions param="1000" accuracy="0" cameraIndex="0" payloadType="0" payloadIndex="0">Hovering</mis:actions>
        </ExtendedData>
        <Point>
          <altitudeMode>relativeToGround</altitudeMode>
          <coordinates>$lon,$lat,$height</coordinates>
        </Point>
      </Placemark>""")

all_coordinates_template = Template("$lon,$lat,$height")
xml_end = Template("""    </Folder>
    <Placemark>
      <name>Wayline</name>
      <description>Wayline</description>
      <visibility>1</visibility>
      <ExtendedData xmlns:mis="www.dji.com">
        <mis:altitude>50.0</mis:altitude>
        <mis:autoFlightSpeed>5.0</mis:autoFlightSpeed>
        <mis:actionOnFinish>GoHome</mis:actionOnFinish>
        <mis:headingMode>UsePointSetting</mis:headingMode>
        <mis:gimbalPitchMode>UsePointSetting</mis:gimbalPitchMode>
        <mis:powerSaveMode>false</mis:powerSaveMode>
        <mis:waypointType>LineStop</mis:waypointType>
        <mis:droneInfo>
          <mis:droneType>COMMON</mis:droneType>
          <mis:advanceSettings>false</mis:advanceSettings>
          <mis:droneCameras/>
          <mis:droneHeight>
            <mis:useAbsolute>false</mis:useAbsolute>
            <mis:hasTakeoffHeight>false</mis:hasTakeoffHeight>
            <mis:takeoffHeight>0.0</mis:takeoffHeight>
          </mis:droneHeight>
        </mis:droneInfo>
      </ExtendedData>
      <styleUrl>#waylineGreenPoly</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <altitudeMode>relativeToGround</altitudeMode>
        <coordinates>$all_coordinates</coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>""")

with open(CsvFile, newline='') as csvfile:
    if csv.Sniffer().has_header(csvfile.read(1024)):
        #print("Header detected !")
        csv_header = True
    csvfile.seek(0)
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    csv_lines = csv.reader(csvfile, dialect)
    if csv_header:
        next(csv_lines, None)  # skip the headers

    for row in csv_lines:
        if row:
            name = row[0]
            lon = row[1]
            lat = row[2]
            if lon[0] == '_':
              lon=lon[1:]
            if lat[0] == '_':
              lon=lat[1:]
            height = row[3]
            heading = row[4]
            gimbal = row[5]

            XML_string += waypoint.substitute(lon=lon, lat=lat, height=height,
                                              waypoint_number=waypoint_number, heading=heading, gimbal=gimbal)+"\n"
            all_coordinates += all_coordinates_template.substitute(
                lon=lon, lat=lat, height=height)+" "
        waypoint_number += 1
# remove last space from coordinates string
all_coordinates = all_coordinates[:-1]
XML_string += xml_end.substitute(all_coordinates=all_coordinates)


with args.output as outpufile:
    outpufile.write(XML_string)
