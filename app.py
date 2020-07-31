#import dependencies
from flask import Flask, jsonify
import datetime as dttm
from datetime import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Flask Setup

app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect = True)
measurement = Base.classes.measurement
station = Base.classes.station

# defining functions for later use:

def maxstation():
    session = Session(engine)
    station_rank = session.query(measurement.station,func.count(measurement.id)).group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()
    max_station = station_rank[0][0]
    session.close()
    return(max_station)

# API Endpoints: The following section of code contains functions to produce api endpoints

# home/root: this function displays this api's possible endpoints
@app.route("/")
def home():
    """Return the justice league data as json"""

    return ('~Endpoints~<br/>'
            '/api/v1.0/precipitation<br/>'
            '/api/v1.0/stations<br/>'
            '/api/v1.0/tobs<br/>'
            '/api/v1.0/"start" <br/>'
            '/api/v1.0/"start"/"end" <br/>')

# Precipitation : this function pulls precipitation data from the sqlite db and displays at the endpoint
@app.route("/api/v1.0/precipitation")
def precipitation():

    # sqlalchemy query to sqlite db 
    session = Session(engine)
    results = session.query(measurement.date,measurement.prcp).all()
    session.close()

    # conform results to a python dictionary 
    prcp_dict = {}
    for day in results:
        prcp_dict[day[0]] = day[1]
    
    # returns json
    return jsonify(prcp_dict)


# stations: this function pulls station name and id from sqlite db and displays at endpoint
@app.route("/api/v1.0/stations")
def stations():

    # sqlalchemy query to sqlite db 
    session = Session(engine)
    results = session.query(station.station,station.name).all()
    session.close()

    # conforms output to python dictionary
    stations_list = []
    for row in results:
        st_dict = {"station_id":row[0],"station_name":row[1]}
        stations_list.append(st_dict)
    
    # returns json
    return jsonify(stations_list)

# tobs: this function pulls observed temperate data from the databsase and displays at the endpoint.
@app.route("/api/v1.0/tobs")
def tobs():

    # queries to find most active station
    max_station = maxstation()

    # identifies limit date for last 12 months of available data
    session = Session(engine)
    max_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    lastdate = dt.strptime(max_date,'%Y-%m-%d')
    datelimit = ((lastdate-dttm.timedelta(365)).isoformat()).split('T')[0]

    # queries to pull temperature data for most active station
    max_station_temp = session.query(measurement.date,measurement.tobs).filter(measurement.date>datelimit).filter(measurement.station == max_station).all()
    session.close()

    # conforms results to dictionary
    tobs = []
    for row in max_station_temp:
        tdict = {"date":row[0],"tobs":row[1]}
        tobs.append(tdict)

    return jsonify(tobs)

# this function pulls temperature data for most active station after a given startdate
@app.route("/api/v1.0/<startdate>")
def start(startdate):

    # ensures date format is reasonably met
    if not (len(startdate) == 8) or startdate.isnumeric() == False:
        return("Incorrect format: Please use yyyymmdd. Numerals only")
    elif len(startdate) == 8:

        # conforms given date to iso standard
        start = startdate
        start = f'{start[0:4]}-{start[4:6]}-{start[6:8]}'

        
        max_station = maxstation()
        
        # attempts query to sqlite db
        try:
            # queries temperature data for most active station after given date
            session = Session(engine)
            results = session.query(measurement.station,func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.station == max_station).filter(measurement.date >= start).group_by(measurement.station).all()
            aggregates = {"tmin":results[0][1],"tavg":results[0][3],"tmax":results[0][2]}
            return(jsonify(aggregates))
        except: 
            print("Query Error")
            
        session.close()

# this function pulls observed temperature data for most active station within a given start and end date
@app.route("/api/v1.0/<startdate>/<enddate>")
def startend(startdate,enddate):

    # ensures date format is reasonably met
    if (not (len(startdate) == 8) or startdate.isnumeric() == False) or (not (len(enddate) == 8) or enddate.isnumeric() == False):
        return("Incorrect format: Please use yyyymmdd/yyyymmdd. Numerals only")

    # checks to make sure startdate comes before enddate
    elif startdate > enddate:
        return("Start Date must be before End Date")
    else:

        # comnforms both dates to iso standard
        start = startdate
        start = f'{start[0:4]}-{start[4:6]}-{start[6:8]}'

        end = enddate
        end = f'{end[0:4]}-{end[4:6]}-{end[6:8]}'

        max_station = maxstation()
        
        try:
            session = Session(engine)
            results = session.query(measurement.station,func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.station == max_station).filter(measurement.date >= start).filter(measurement.date <= end).group_by(measurement.station).all()
            aggregates = {"tmin":results[0][1],"tavg":results[0][3],"tmax":results[0][2]}
            return(jsonify(aggregates))
        except: 
            return("Query Error")
            
        session.close()


if __name__ == "__main__":
    app.run(debug=True)
