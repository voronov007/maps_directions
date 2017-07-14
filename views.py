from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

# from .models import Base
from maps_directions import directions_calc
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///maps_directions.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/directions', methods=['POST'])
def directions():
    origin = request.json.get('origin')
    destination = request.json.get('destination')
    pass


@app.route('/temp', methods=['GET'])
def temp():
    directions_calc()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
