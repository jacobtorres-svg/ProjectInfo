from matplotlib import pyplot
from numpy import *

class Aircraft:
    def __init__(self,id,icao_origin,icao_destination,landing,departure,icao_airline):
        self.id=id  #ID of the airplane
        self.icao_origin=icao_origin    #ICAO code of the airport of origin
        self.icao_destination=icao_destination  #ICAO code of the airport of destination
        self.landing=landing    #Landing time
        self.departure=departure    #Departure time
        self.icao_airline=icao_airline  #ICAO code of the airline

def LoadArrivals (filename):    #Function to load the arrivals
    arrivals=[]
    try:
        file=open(filename,"r")
        file.readline()
        arrive=file.readline() #We ride two lines in one go to skip the title
        while arrive != "":
            info=arrive.split(" ")
            if len(info[0])<5:
                info[0]="-"
            if len(list(info[1]))!=4:
                info[1]="-"
            time=list(info[2])
            if not (0<=int(time[0])<=2 and time[2]==":" and 0<=int(time[3])<=5):
                if int(time[0])==2 and int(time[1])>4:
                    info[2]="-"
            airline=info[3].strip()
            if len(airline)!=3:
                airline="-"
            aircraft_class=Aircraft(info[0],info[1],None,info[2],None,airline)
            arrivals.append(aircraft_class)
            arrive=file.readline()
        file.close()
    except FileNotFoundError:
        return []
    return arrivals

def PrintAirrivals(aircrafts):  #Function to write all the variables from the arrivals
    info = (f"ID: {aircrafts.id}\n"
            f"Origin: {aircrafts.icao_origin}\n"
            f"Landing time: {aircrafts.landing}\n"
            f"Aircraft: {aircrafts.icao_airline}\n\n")
    return info

def PlotArrivals (aircrafts):   #Function to show the amount of arrivals every hour
    Vy=[0]*24
    i=0
    while i<len(aircrafts):
        time=aircrafts[i].landing
        if ":" in time:
            hour=int(time.split(":")[0])
            Vy[hour]+=1
        i=i+1
    pyplot.bar(range(24),Vy,label="Arriving aircrafts")
    pyplot.xticks(range(24))
    pyplot.xlabel("Hours")
    pyplot.ylabel("Flights")
    pyplot.legend()
    pyplot.show()
    return

def SaveFlights(aircrafts, filename):   #Function to save all the arrivals after being processed properly
    new_file=open(filename, "w")
    i=0
    if len(aircrafts)>0:
        while i<len(aircrafts):
            info=aircrafts[i]
            vector_aircrafts=[info.id,"\t",info.icao_origin,"\t",info.landing,"\t",info.icao_airline,"\n"]
            new_file.write("".join(vector_aircrafts))
            i=i+1
    else:
        print("No aircrafts found")
    new_file.close()
    return

def AddAircraft(aircrafts, new_aircraft):   #Function to add an arrival
    i=0
    end=False
    while i<len(aircrafts) and end==False:
        if aircrafts[i].id==new_aircraft.id and aircrafts[i].landing==new_aircraft.landing:
            end=True
        i=i+1
    if end==True:
        return aircrafts
    end=False
    position=0
    while position<len(aircrafts) and end==False:
        if new_aircraft.landing<aircrafts[position].landing:
            aircrafts.insert(position,new_aircraft)
            end=True
        position=position+1
    if end==False:
        aircrafts.append(new_aircraft)
    return aircrafts

def RemoveAircraft(aircrafts, landing_time, extra_info):    #Function to remove an arrival
    i=0
    found=False
    while i<len(aircrafts) and found==False:
        if aircrafts[i].landing==landing_time:
            if (aircrafts[i].id == extra_info or aircrafts[i].icao_origin==extra_info or aircrafts[i].icao_airline==extra_info):
                aircrafts.pop(i)
                found=True
        i=i+1
    return aircrafts

def PlotAirlines(aircrafts):    #Function to see the number of arrivals each airline has
    try:
        Vx=[]
        Vy=[]
        if len(aircrafts)==0:
            print("Error")
            return
        i=0
        while i<len(aircrafts):
            airline=aircrafts[i].icao_airline
            j = 0
            found=False
            while j<len(Vx):
                if Vx[j]==airline:
                    Vy[j]=Vy[j]+1
                    found=True
                    break
                j=j+1
            if found==False:
                Vx.append(airline)
                Vy.append(1)
            i=i+1
        pyplot.figure(figsize=(14, 15))
        pyplot.barh(Vx, Vy, label="Airline Flights")
        pyplot.yticks(size=12)
        pyplot.xlabel("Flights")
        pyplot.ylabel("Airlines")
        pyplot.legend()
        pyplot.tight_layout()
        pyplot.show()
    except FileNotFoundError:
        return
    return

def PlotFlightsType(aircrafts): #Function to show how many of these arrivals are Schengen
    try:
        i=0
        countsche=countnosche=0
        sche=['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
        while i < len(aircrafts):
            j = 0
            found = False
            while j<len(sche) and not found:
                if aircrafts[i].icao_origin[:2] == sche[j]:
                    found = True
                    countsche += 1
                j += 1
            if not found:
                countnosche += 1
            i += 1
        pyplot.bar(["Type"], [countsche], label="Schengen")
        pyplot.bar(["Type"], [countnosche], bottom=[countsche], label="No Schengen")
        pyplot.ylabel("Arrivals")
        pyplot.legend()
        pyplot.show()
    except FileNotFoundError:
        return
    return

def MapFlights(aircrafts,airports,filename):    #Function to create the .kml file to show the flight routes in Google Earth
    new_file=open(filename, "w")
    new_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    new_file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    new_file.write("<Document>\n")
    i=0
    while i<len(aircrafts):
        j=0
        while j<len(airports):
            if aircrafts[i].icao_origin==airports[j].icao_code:
                new_file.write("\t<Placemark>\n")
                new_file.write(f'\t\t<name>"Route {aircrafts[i].icao_origin}-LEBL"</name>\n')
                new_file.write("\t\t<LineString>\n")
                new_file.write("\t\t\t<altitudeMode>clampToGround</altitudeMode>\n")
                new_file.write("\t\t\t<extrude>1</extrude>\n")
                new_file.write("\t\t\t<tessellate>1</tessellate>\n")
                new_file.write("\t\t\t\t<coordinates>\n")
                new_file.write("\t\t\t\t\t2.078333,41.296944\n")
                new_file.write(f"\t\t\t\t\t{airports[j].longitude},{airports[j].latitude}\n")
                new_file.write("\t\t\t\t</coordinates>\n")
                new_file.write("\t\t</LineString>\n")
                new_file.write("\t\t<Style>\n")
                new_file.write("\t\t\t<LineStyle>\n")
                print(type(airports[j].sche))
                if airports[j].sche==True:
                    new_file.write("\t\t\t\t<color>ff00ff00</color>\n")
                elif airports[j].sche==False:
                    new_file.write("\t\t\t\t<color>ff0000ff</color>\n")
                new_file.write("\t\t\t</LineStyle>\n")
                new_file.write("\t\t</Style>\n")
                new_file.write(f"\t</Placemark>\n")
            j=j+1
        i=i+1
    new_file.write("</Document>\n")
    new_file.write("</kml>\n")
    new_file.close()
    return

def LongDistanceArrivals(aircrafts,airports,filename):  #Function to only show the long distance routes in Google Earth
    new_file = open(filename, "w")
    new_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    new_file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    new_file.write("<Document>\n")
    i = 0
    while i<len(aircrafts):
        j = 0
        while j<len(airports):
            if aircrafts[i].icao_origin==airports[j].icao_code:
                bcnlat=41.296944
                bcnlon=2.078333
                a=sin(radians(airports[j].latitude-bcnlat)/2)**2+cos(radians(bcnlat))*cos(radians(airports[j].latitude))*sin(radians(bcnlon-airports[j].longitude)/2)**2
                c=2*atan2(sqrt(a),sqrt(1-a))
                d=6371*c
                if d>=2000:
                    new_file.write("\t<Placemark>\n")
                    new_file.write(f'\t\t<name>"Route {aircrafts[i].icao_origin}-LEBL"</name>\n')
                    new_file.write("\t\t<LineString>\n")
                    new_file.write("\t\t\t<altitudeMode>clampToGround</altitudeMode>\n")
                    new_file.write("\t\t\t<extrude>1</extrude>\n")
                    new_file.write("\t\t\t<tessellate>1</tessellate>\n")
                    new_file.write("\t\t\t\t<coordinates>\n")
                    new_file.write("\t\t\t\t\t2.078333,41.296944\n")
                    new_file.write(f"\t\t\t\t\t{airports[j].longitude},{airports[j].latitude}\n")
                    new_file.write("\t\t\t\t</coordinates>\n")
                    new_file.write("\t\t</LineString>\n")
                    new_file.write(f"\t</Placemark>\n")
            j=j+1
        i=i+1
    new_file.write("</Document>\n")
    new_file.write("</kml>\n")
    new_file.close()
    return

def LoadDepartures(filename):   #Function to load the departures
    departures=[]
    try:
        file=open(filename,"r")
        file.readline()
        depart=file.readline() #We read two lines in one go to skip the title
        while depart != "":
            info=depart.split(" ")
            if len(info[0])<5:
                info[0]="-"
            if len(list(info[1]))!=4:
                info[1]="-"
            time=list(info[2])
            if not (0<=int(time[0])<=2 and time[2]==":" and 0<=int(time[3])<=5):
                if int(time[0])==2 and int(time[1])>4:
                    info[2]="-"
            airline=info[3].strip()
            if len(airline)!=3:
                airline="-"
            aircraft_class=Aircraft(info[0],None,info[1],None,info[2],airline)
            departures.append(aircraft_class)
            depart=file.readline()
        file.close()
    except FileNotFoundError:   #This exception indicates that if we can't find the file instead of shooting an error it just returns an empty vector
        return []
    return departures

def PrintDepartures(aircrafts):  #Function to write all the variables from the departures
    info = (f"ID: {aircrafts.id}\n"
            f"Destination: {aircrafts.icao_destination}\n"
            f"Departure time: {aircrafts.departure}\n"
            f"Aircraft: {aircrafts.icao_airline}\n\n")
    return info

def MergeMovements(arrivals, departures):   #Function to combine arrivals and departures information
    complete_flights=[]
    i=0
    j=0
    end=False
    while i<len(arrivals):
        new=i
        while j<len(departures) and end==False:
            if arrivals[i].id==departures[j].id and arrivals[i].icao_airline==departures[i].icao_airline:
                if arrivals[i].landing<departures[j].departure:
                    flight=Aircraft(arrivals[i].id,arrivals[i].icao_origin,departures[j].icao_destination,arrivals[i].landing,departures[j].departure,arrivals[i].icao_airline)
                    complete_flights.append(flight)
                    end=True
                    new=new+1
            j=j+1
        j=0
        end=False
        if new==i:
            complete_flights.append(arrivals[i])
        i=i+1
    i=0
    j=0
    end=False
    while i<len(departures):
        new=i
        while j<len(arrivals) and end==False:
            if departures[i].id==arrivals[j].id and departures[i].icao_airline==arrivals[j].icao_airline:
                if departures[i].departure>arrivals[j].landing:
                    end=True
                    new=new+1
            j=j+1
        j=0
        end=False
        if new==i:
            complete_flights.append(departures[i])
        i=i+1
    return complete_flights

def NightAircraft (complete_flights):   #Function to indicate which airplanes stayed over from the previous day
    try:
        night_list=[]
        i=0
        while i<len(complete_flights):
            if complete_flights[i].icao_origin==None and complete_flights[i].icao_destination!=None:
                night_list.append(complete_flights[i])
            i+=1
    except FileNotFoundError:
        return []
    return night_list

if __name__ == "__main__":  #Test area
    arrivals=LoadArrivals("Arrivals.txt")
    departures=LoadDepartures("Departures.txt")
    merge=MergeMovements(arrivals,departures)
    night=NightAircraft(merge)
    for m in merge:
        print(m.__dict__)
    print("\n\n\n")
    for n in night:
        print(n.__dict__)