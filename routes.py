# This python script uses Flask APIs to set up routes that can serve as end points
#   for various queries against the hawaii.sqlite data base.
# The python code in this script effectively mimics the code in climate_analysis.ipynb
#   notebook; please refer to that notebook for more details.

# Impoert various modules
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from flask import Flask, jsonify
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurements = Base.classes.measurements
Stations = Base.classes.stations
session = Session(engine)
#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the json list of tobs for the last 12 months"""
    last12_tobs = session.query(Measurements.date, Measurements.station, Measurements.tobs).\
               filter(Measurements.date.between('2016-08-24', '2017-08-23')).\
               group_by(Measurements.date).order_by(Measurements.date).all()

    tobs_data = []
    for rec in range(len(last12_tobs)):
        tobs_dict = {}
        tobs_dict['date'] = last12_tobs[rec][0]
        tobs_dict['temp'] = last12_tobs[rec][2]
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return the json list of all stations in the data set"""
    all_stations = session.query(Stations.station, Stations.name).all()

    stations_data = []
    for rec in range(len(all_stations)):
        station_dict = {}
        station_dict['station_id'] = all_stations[rec][0]
        station_dict['name'] = all_stations[rec][1]
        stations_data.append(station_dict)
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the json list of tobs for the last 12 months"""
    last12_tobs = session.query(Measurements.date, Measurements.station, Measurements.tobs).\
               filter(Measurements.date.between('2016-08-24', '2017-08-23')).\
               group_by(Measurements.date).order_by(Measurements.date).all()

    tobs_data = []
    for rec in range(len(last12_tobs)):
        tobs_dict = {}
        tobs_dict['date'] = last12_tobs[rec][0]
        tobs_dict['temp'] = last12_tobs[rec][2]
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temp_range(start):
    """Return the json list of min, average and max temperatures for a given date"""
    min_temp = session.query(func.min(Measurements.tobs)).\
               filter(Measurements.date == start).first()
    avg_temp = session.query(func.avg(Measurements.tobs)).\
               filter(Measurements.date == start).first()
    max_temp = session.query(func.max(Measurements.tobs)).\
               filter(Measurements.date == start).first()

    tobs_data = [min_temp, avg_temp, max_temp]
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>/<end_date>")
def temp_ranges(start, end_date):
    """Return the json list of min, average and max temperatures for a given date range"""
    min_temp = session.query(func.min(Measurements.tobs)).\
               filter(Measurements.date.between(start, end_date)).first()
    avg_temp = session.query(func.avg(Measurements.tobs)).\
               filter(Measurements.date.between(start, end_date)).first()
    max_temp = session.query(func.max(Measurements.tobs)).\
               filter(Measurements.date.between(start, end_date)).first()
    
    tobs_data = [min_temp, avg_temp, max_temp]
    return jsonify(tobs_data)

if __name__ == "__main__":
    app.run(debug=False)