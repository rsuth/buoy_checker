#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re

BUOY_URL = 'https://www.ndbc.noaa.gov/data/realtime2/46225.txt'

def get_raw_data():
    try:
        response = requests.get(BUOY_URL)
        return response.text
    except requests.exceptions.RequestException:
        return 'Cannot Get Data'

def parse_raw_data(raw_data):
    pattern = r'(?P<year>20\d{2}) (?P<month>\d\d) (?P<day>\d\d) (?P<hour>\d\d) (?P<minute>\d\d)(?:  MM ){3}  (?P<wave_height>\d+.\d) +(?P<dom_period>\d\d) +(?P<avg_period>\d+.\d) (?P<degrees>\d{3})(?: +MM){2} +(?P<temp>\d+.\d)'
    m = re.search(pattern, raw_data)
    
    if m:
        return m.groupdict()
    else:
        return 'Error Parsing Data'

def build_output_string(parsed_data):
    wave_ft = float(parsed_data['wave_height'])*3.28
    degrees = int(parsed_data['degrees'])
    cardinal = degrees_to_cardinal(degrees)
    return f"🌊 {wave_ft} ft @ {parsed_data['dom_period']}s from {degrees}° {cardinal} 🌊"

# from https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
def degrees_to_cardinal(d):
    '''
    note: this is highly approximate...
    '''
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((d + 11.25)/22.5)
    return dirs[ix % 16]


raw_data = get_raw_data()
parsed_data = parse_raw_data(raw_data)
output = build_output_string(parsed_data)

print(output)
