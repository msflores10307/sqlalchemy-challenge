from flask import Flask, jsonify
import datetime as dttm
from datetime import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine,reflect = True)

measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """Return the justice league data as json"""

    return ('~Endpoints~<br/>'
            '/api/v1.0/precipitation<br/>'
            '/api/v1.0/stations<br/>'
            '/api/v1.0/tobs<br/>'
            '/api/v1.0/"start" <br/>'
            '/api/v1.0/"start"/"end" <br/>')


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    results = session.query(measurement.date,measurement.prcp).all()
    session.close()

    prcp_dict = {}
    for day in results:
        prcp_dict[day[0]] = day[1]
    
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    results = session.query(station.station,station.name).all()
    session.close()

    stations_list = []
    for row in results:
        st_dict = {"station_id":row[0],"station_name":row[1]}
        stations_list.append(st_dict)
    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    max_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    lastdate = dt.strptime(max_date,'%Y-%m-%d')
    datelimit = ((lastdate-dttm.timedelta(365)).isoformat()).split('T')[0]

    station_rank = session.query(measurement.station,func.count(measurement.id)).group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()
    max_station = station_rank[0][0]

    max_station_temp = session.query(measurement.date,measurement.tobs).filter(measurement.date>datelimit).filter(measurement.station == max_station).all()
    session.close()

    tobs = []
    for row in max_station_temp:
        tdict = {"date":row[0],"tobs":row[1]}
        tobs.append(tdict)

    return jsonify(tobs)

@app.route("/api/v1.0/<startdate>")
def start(startdate):

    if not (len(startdate) == 8) or startdate.isnumeric() == False:
        return("Incorrect format: Please use yyyymmdd. Numerals only")
    elif len(startdate) == 8:
        start = startdate
        start = f'{start[0:4]}-{start[4:6]}-{start[6:8]}'

        session = Session(engine)
        station_rank = session.query(measurement.station,func.count(measurement.id)).group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()
        max_station = station_rank[0][0]
        
        try:
            results = session.query(measurement.station,func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.station == max_station).filter(measurement.date >= start).group_by(measurement.station).all()
            aggregates = {"tmin":results[0][1],"tavg":results[0][3],"tmax":results[0][2]}
            return(jsonify(aggregates))
        except: 
            print("Query Error")
            
        session.close()

@app.route("/api/v1.0/<startdate>/<enddate>")
def startend(startdate,enddate):

    if (not (len(startdate) == 8) or startdate.isnumeric() == False) or (not (len(enddate) == 8) or enddate.isnumeric() == False):
        return("Incorrect format: Please use yyyymmdd/yyyymmdd. Numerals only")

    elif startdate > enddate:
        return("Start Date must be before End Date")
    else:

        start = startdate
        start = f'{start[0:4]}-{start[4:6]}-{start[6:8]}'

        end = enddate
        end = f'{end[0:4]}-{end[4:6]}-{end[6:8]}'

        # replace with function
        session = Session(engine)
        station_rank = session.query(measurement.station,func.count(measurement.id)).group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()
        max_station = station_rank[0][0]
        
        try:
            results = session.query(measurement.station,func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.station == max_station).filter(measurement.date >= start).filter(measurement.date <= end).group_by(measurement.station).all()
            aggregates = {"tmin":results[0][1],"tavg":results[0][3],"tmax":results[0][2]}
            return(jsonify(aggregates))
        except: 
            return("Query Error")
            
        session.close()





# @app.route("/other/<start_date>_<end_date>")
# def justice_league_character(real_name):
#     """Fetch the Justice League character whose real_name matches
#        the path variable supplied by the user, or a 404 if not."""

#     canonicalized = real_name.replace(" ", "").lower()
#     for character in justice_league_members:
#         search_term = character["real_name"].replace(" ", "").lower()

#         if search_term == canonicalized:
#             return jsonify(character)

#     return jsonify({"error": f"Character with real_name {real_name} not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)
