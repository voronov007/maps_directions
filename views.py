from flask import Flask, jsonify, request
import json

from maps_directions import gmaps_directions

app = Flask(__name__)


@app.route('/directions', methods=['POST'])
def directions():
    data = json.loads(request.data)
    origin = data['origin']
    destination = data['destination']
    result = gmaps_directions(origin, destination)
    return jsonify(result)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
