import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route('/')
def home():
    return(
        f'Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'^^^ get the max, min and average temp from \'YYYY-MM-DD\' forward<br/>'
        f'/api/v1.0/<start>/<end><br/>'
        f' ^^^get the max, min and average temp between \'/YYYY-MM-DD/\' and \n \'/YYYY-MM-DD/\'<br/>'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results= session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    prcp_per_date = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        prcp_per_date.append(precip_dict)

    return jsonify(prcp_per_date)

    
@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    results = session.query(Measurement.station).all()
    
    session.close()
    
    stations = list(np.ravel(results))
    unique_stations = []
    for station in stations:
        if station not in unique_stations:
            unique_stations.append(station)
    
    return jsonify(unique_stations)
    
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date,
                         Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(func.strftime('%Y-%m-%d', Measurement.date) > '2016-08-18').\
    order_by(Measurement.date.desc()).all()
    
    session.close()
    
    observations = list(np.ravel(results))
    
    return jsonify(observations)
    
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    sel = [func.max(Measurement.tobs),
       func.min(Measurement.tobs),
       func.avg(Measurement.tobs)]
    results = (session.query(*sel).\
    filter(func.strftime('%Y-%m-%d', Measurement.date) >= func.strftime('%Y-%m-%d',start))).all()

    temps = list(np.ravel(results))
    
    return jsonify(temps)
    
    
    
@app.route("/api/v1.0/<start>/<end>")
def two_dates(start,end):
    session = Session(engine)
    sel = [func.max(Measurement.tobs),
       func.min(Measurement.tobs),
       func.avg(Measurement.tobs)]
    results = (session.query(*sel).\
    filter(func.strftime('%Y-%m-%d', Measurement.date) >= func.strftime('%Y-%m-%d',start)).\
    filter(func.strftime('%Y-%m-%d', Measurement.date) <= func.strftime('%Y-%m-%d',end))).all()

    temps = list(np.ravel(results))
    
    return jsonify(temps)
    
    
    
        

