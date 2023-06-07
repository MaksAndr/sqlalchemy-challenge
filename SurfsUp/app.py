# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
model_base = automap_base()
# reflect the tables
model_base.prepare(autoload_with=engine)
# Save references to each table
measurement = model_base.classes.measurement
station = model_base.classes.station

#################################################
# Flask Routes
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """All api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-24").all()

    session.close()

    # Convert the list to Dictionary
    year_prcp = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp     
        year_prcp.append(prcp_dict)

    return jsonify(year_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Query all stations
    results = session.query(measurement.station, func.count(measurement.id)).\
            group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)
    

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Return a list of tobs"""
    # Query the last 12 months of temperature observation data for the most active station
    results = session.query(measurement.station, measurement.prcp, \
                            measurement.date,measurement.tobs)\
    .filter(measurement.date >= '2016-08-23')\
    .filter(measurement.station == 'USC00519281')\
    .all()
   
    session.close()

     # Convert list to Dictionary
    all_tobs = []
    for station,prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


if __name__ == '__main__':
    app.run(debug=True)