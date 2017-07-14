import sys
from datetime import datetime, timedelta
import requests
from collections import OrderedDict
import re

import googlemaps

gmaps_key = 'AIzaSyDd3xYNorMNdmhj2ojL41vcgdDzCtP13l0'
directions_url = 'https://maps.googleapis.com/maps/api/directions/json'
gmaps = googlemaps.Client(key=gmaps_key)


class MapsDirection:
    total_distance = 0
    duration = 0
    countries = OrderedDict()
    origin_country = ''

    def __init__(self, origin, destination):
        self.origin = str(origin[0]) + ',' + str(origin[1])
        self.destination = str(destination[0]) + ',' + str(destination[1])

    def get_distance_per_country(self):
        try:
            data = {
                'origin': self.origin,
                'destination': self.destination,
                'language': 'en',
                'mode': 'driving',
                'region': 'en',
                'key': gmaps_key
            }
            r = requests.get(directions_url, params=data, verify=False)
            directions = r.json()['routes'][0]['legs'][0]
            self.origin_country = self.get_origin_country(directions['start_address'])
            print(directions)
        except Exception as e:
            print(sys.exc_info())
            print(e)
            return 0

        self.total_distance = directions['distance']['value']
        self.duration = timedelta(seconds=directions['duration']['value'])
        country = self.origin_country
        self.countries[country] = 0
        for step in directions['steps']:
            distance = step['distance']['value']
            self.countries[country] += distance
            match_obj = re.search(r'Entering (.+)</div>',
                                  step['html_instructions'])

            if match_obj:
                country = match_obj.group(1)
                if country.startswith('the '):
                    country = country[4:]  # Drop the 'the '

                if country not in self.countries:
                    # We're in a new country, and the total driven distance here
                    # is zero so far
                    self.countries[country] = 0

        return {
            'distance': directions['distance']['value'],
            'duration': timedelta(seconds=directions['duration']['value']),
            'countries': self.countries,
        }

    @staticmethod
    def get_origin_country(origin_address):
        split_array = origin_address.split(', ')
        return split_array[-1]


def directions_calc():
    map_direction = MapsDirection([50.455208, 30.355092], [50.850329, 4.351687])
    result = map_direction.get_distance_per_country()
    print(result)

directions_calc()