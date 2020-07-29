import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask,jsonify
import datetime as dttm
from datetime import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine,reflect = True)

measurement = Base.classes.measurement
station = Base.classes.station

# session = Session(engine)
# results = session.query(measurement.date,measurement.prcp).all()
# session.close()

# prcp_dict = {}
# for day in results:
#     prcp_dict[day[0]] = day[1]
# # jsonify(prcp_dict)

# session = Session(engine)
# results = session.query(station.station,station.name).all()
# session.close()
# stations_list = []
# for station in results:
#     st_dict = {"station_id":station[0],"station_name":station[1]}
#     stations_list.append(st_dict)


# session = Session(engine)
# max_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
# lastdate = dt.strptime(max_date,'%Y-%m-%d')
# datelimit = ((lastdate-dttm.timedelta(365)).isoformat()).split('T')[0]

# station_rank = session.query(measurement.station,func.count(measurement.id)).group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()
# max_station = station_rank[0][0]

# max_station_temp = session.query(measurement.date,measurement.tobs).filter(measurement.date>datelimit).filter(measurement.station == max_station).all()
# session.close()

# tobs = []
# for row in max_station_temp:
#     tdict = {"date":row[0],"tobs":row[1]}
#     tobs.append(tdict)

# print(tobs)

#     startdate = '20170602'

# if not (len(startdate) == 8) or startdate.isnumeric() == False:
#     print("Incorrect format: Please use <yyyymmdd>. Numerals only")
# elif len(startdate) == 8:
#     start = startdate
#     start = f'{start[0:4]}-{start[4:6]}-{start[6:8]}'

#     session = Session(engine)
#     station_rank = session.query(measurement.station,func.count(measurement.id)).group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()
#     max_station = station_rank[0][0]
    
#     try:
#         results = session.query(measurement.station,func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.station == max_station).filter(measurement.date >= start).group_by(measurement.station).all()
#         aggregates = {"min":results[0][1],"avg":results[0][3],"max":results[0][2]}
#         print(aggregates)

#     except: 
#         print("Incorrect format. Please use <yyyymmdd>/<yyyymmdd>")
    
#     session.close()
    
    
# elif len(startdate) == 17:
#     start,end = startdate.split('/')
#     dates = [start,end]

#     start = f'{start[0:4]}-{start[4:6]}-{start[6:8]}'
#     end = f'{end[0:4]}-{end[4:6]}-{end[6:8]}'

#     session = Session(engine)

#     station_rank = session.query(measurement.station,func.count(measurement.id)).group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()
#     max_station = station_rank[0][0]
    
#     if start > end:
#         print("StartDate must be before EndDate ")
#     else: 
#         try:
#             results = session.query(measurement.station,func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.station == max_station).filter(measurement.date >= start).filter(measurement.date<=end).group_by(measurement.station).all()
#             aggregates = {"min":results[0][1],"avg":results[0][3],"max":results[0][2]}
#             print(aggregates)
#         except:
#             print("fuck")
#     session.close()

startdate = '20160101' 
enddate = '20170101'

if (not (len(startdate) == 8) or startdate.isnumeric() == False) or (not (len(enddate) == 8) or enddate.isnumeric() == False):
    print("Incorrect format: Please use yyyymmdd/yyyymmdd. Numerals only")

elif startdate > enddate:
    print("Start Date must be before End Date")
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
        aggregates = {"min":results[0][1],"avg":results[0][3],"max":results[0][2]}
        print(aggregates)
    except: 
        print("Query Error")
        
    session.close()