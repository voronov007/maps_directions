from flask import Flask, jsonify, request
from directions.cross_domain import crossdomain
import json

from directions.maps_directions import gmaps_directions

app = Flask(__name__)


@app.route('/directions', methods=['POST'])
@crossdomain(origin='*')
def directions():
    try:
        data = json.loads(request.data)
    except Exception as e:
        return jsonify({
            'message': 'Error. Not JSON data',
            'exception': str(e)
        })
    origin = data['origin']
    destination = data['destination']
    result = gmaps_directions(origin, destination)
    return jsonify(result)


@app.route('/')
def index():
    return 'Directions service updated'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
