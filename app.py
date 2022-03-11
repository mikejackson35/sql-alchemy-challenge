from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
# reflect the tables

base.prepare(engine, reflect=True)
stations = base.classes.station
measurements = base.classes.measurement

app = Flask(__name__)
app.config["JSON_SORT_KEYS"]=False

@app.route("/")
def home():
    return (
        f"Home Page with links to:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    results = session.query(measurements.date, measurements.prcp).filter(measurements.date >= "2016-08-23").all()
    session.close()
    precips = []
    for date, prcp in results:
        precips_dict = {}
        precips_dict['date'] = date
        precips_dict['prcp'] = prcp
        precips.append(precips_dict)

    return jsonify(precips)

@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    actives = session.query(measurements.station, func.count(measurements.station)).group_by(measurements.station).order_by(func.count(measurements.station).desc()).all()
    session.close()
    return jsonify(stations={d:p for d,p in actives})

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    tobs_query= session.query(measurements.date, measurements.tobs).filter(measurements.date >= "2016-08-23").all()
    session.close()
    tobs = []
    for date, tob in tobs_query:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tob
        tobs.append(tobs_dict)
    return jsonify(tobs_dict)

@app.route("/api/v1.0/start")
def start():
    session=Session(engine)

    session.close()

@app.route("/api/v1.0/start_end")
def start_end():
    session=Session(engine)

    session.close()

if __name__=="__main__":
    app.run(debug=True)