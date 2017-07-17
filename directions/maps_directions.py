import sys
from datetime import timedelta
import requests
from collections import OrderedDict
import re


gmaps_key = 'AIzaSyAshRoc9eSnjUxZehRdCHweNNc3TjQF4TA'  # Andrew's key with referer restiction
# gmaps_key = 'AIzaSyDg856CXKH3pud-BtxzJxh8_pue0V13OYQ'  # key from the test code
# gmaps_key = 'AIzaSyAxNkIJfWft1IwItg36-mboV7mL35-49uU'  # last key from Comvoy
directions_url = 'https://maps.googleapis.com/maps/api/directions/json'


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
            headers = {
                'referer': 'https://gmaps-directions.herokuapp.com/',
                'origin': 'https://gmaps-directions.herokuapp.com/'
            }
            r = requests.get(directions_url, params=data, verify=False,
                             headers=headers)
            directions = r.json()['routes'][0]['legs'][0]
            self.origin_country = self.get_origin_country(directions['start_address'])
        except Exception as e:
            print(sys.exc_info())
            print(e)
            return {'message': 'Error during request to the Google Maps'}

        self.total_distance = directions['distance']['value']
        self.duration = str(timedelta(seconds=directions['duration']['value']))

        coords = [[directions['steps'][0]['start_location']['lat'],
                   directions['steps'][0]['start_location']['lng']]]
        country = self.origin_country
        self.countries[country] = 0
        for step in directions['steps']:
            distance = step['distance']['value']
            coords.append([step['end_location']['lat'],
                           step['end_location']['lng']])
            self.countries[country] += distance

            # Looking if we are in the new country
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
            'distance': self.total_distance,
            'duration': self.duration ,
            'countries': self.countries,
            'coordinates': coords
        }

    @staticmethod
    def get_origin_country(origin_address):
        split_array = origin_address.split(', ')
        return split_array[-1]


def gmaps_directions(origin, destintation):
    map_direction = MapsDirection(origin, destintation)
    return map_direction.get_distance_per_country()


# gmaps_directions([50.455208, 30.355092], [50.850329, 4.351687])
