import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
     """List all available api routes."""
     return (
         f"Available Routes:<br/>"
         f"/api/v1.0/precipitation<br/>"
         f"/api/v1.0/stations<br/>"
         f"/api/v1.0/tobs<br/>"
         f"/api/v1.0/start<br/>"
         f"/api/v1.0/start/end"
     )


@app.route('/api/v1.0/precipitation')
def precipitation():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)

# Query the Measurement table
    results = session.query(Measurement).all()

# Create a dictionary from the row data and append to a list of precipitation (all_prcp)
    all_prcp = []
    for prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = prcp.date
        prcp_dict["prcp_value"] = prcp.prcp
        all_prcp.append(prcp_dict)
# Return the JSON representation of your dictionary
    return jsonify(all_prcp)

@app.route('/api/v1.0/stations')
def stations():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
# Query the stations
    results=session.query(Station.station, Station.name).all()
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route('/api/v1.0/tobs')
def tobs():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
# query for the dates and temperature observations from a year from the last data point
    results=session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
    all_tobs = list(np.ravel(results))
    return jsonify(all_tobs)


@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def start_end (start, end=None):

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)

    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    if end is not None:
        results =session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date>=start).filter(Measurement.date<=end).all()
        all_stats=list(np.ravel(results))
        return jsonify(all_stats)
    
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    else:
        results =session.query(func.count(Measurement.tobs),func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date>=start).all()
        all_stats=list(np.ravel(results))
        return jsonify(all_stats)
       

if __name__ == '__main__':
    app.run(debug=True)
