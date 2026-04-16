from airport import *
from matplotlib import pyplot
from numpy import *

class Aircraft:  #We open the class for the airport with all the variables we are going to use
    def __init__(self,id,icao_airline,icao_origin,landing):
        self.id=id
        self.icao_airline=icao_airline
        self.icao_origin=icao_origin
        self.landing=landing

def LoadArrivals (filename):
    aircrafts=[]
    try:
        file=open(filename,"r")
        arrive=file.readline()
        arrive=file.readline() #We ride two lines in one go to skip the title
        while arrive != "":
            info=arrive.split(" ")
            #Check that the airports are correct in info[1]
            if len(list(info[1]))!=4:
                info[1]="-"
            #Check that the time are correct in info[2]
            time=list(info[2])
            if not (0<=int(time[0])<=2 and time[2]==":" and 0<=int(time[3])<=5):
                if int(time[0])==2 and int(time[1])>4:
                    info[2]="-"
            #Check that the airline are correct in info[3] check the last bit of info!!!
            if len(list(info[3]))!=4:
                info[3]="-"
            else:
                airline=list(info[3])
                airline.pop(3)
                info[3]="".join(airline)
            aircraft=[info[0],info[1],info[2],info[3]]
            aircrafts.append(aircraft)
            arrive=file.readline()
        file.close()
    except FileNotFoundError:   #This exception indicates that if we can't find the file instead of shooting an error it just returns an empty vector
        return []
    return aircrafts

def PlotArrivals (aircrafts):
    Vy=[0]*24
    start=["0","0"]
    i=0
    j=0
    while i<len(aircrafts):
        time=list(aircrafts[i][2])
        if len(time)==5:
            if time[0]==start[0] and time[1]==start[1]:
                Vy[j]=Vy[j]+1
            else:
                start=[time[0],time[1]]
                i=i-1
                j=j+1
        i=i+1
    pyplot.bar(range(24),Vy,label="Arriving aircrafts")
    pyplot.xticks(range(24),rotation=45)
    pyplot.xlabel("Hours")
    pyplot.ylabel("Flights")
    pyplot.legend()
    pyplot.show()
    return

def SaveFlights(aircrafts, filename):
    new_file=open(filename, "w")  # We open a new file with whatever name we've input-ed
    i=0
    j=0
    if len(aircrafts)>0:
        while i < len(aircrafts):
            while j<len(aircrafts[i]):
                if aircrafts[i][j]==" ":
                    aircrafts[i][j]="0"
                j=j+1
            j=0
            vector_aircrafts=[aircrafts[i][0],"\t",aircrafts[i][1],"\t",aircrafts[i][2],"\t",aircrafts[i][3],"\n"]
            new_file.write("".join(vector_aircrafts))
            i=i+1
    else:  # In case there aren't any airports in the list (it's empty) we return an error message
        print("No aircrafts found")
    new_file.close()
    return
print(SaveFlights(LoadArrivals("Arrivals.txt"),"new.txt"))
#Make a function that lets you change information about the aircrafts (both add and delete) and work on the PlotArrive to make space for empty information so that the Save Flights can take it into account

def PlotAirlines(aircrafts):
    try:
        Vx_airlines = []
        Vy_flights = []
        if len(aircrafts) == 0:
            print("Error")
            return
        i = 0
        while i < len(aircrafts):
            aeroline = aircrafts[i][3]
            # buscar si ya existe
            j = 0
            found = False
            while j < len(Vx_airlines):
                if Vx_airlines[j] == aeroline:
                    Vy_flights[j] += 1
                    found = True
                    break
                j += 1
            # si no existe,añadirlo
            if not found:
                Vx_airlines.append(aeroline)
                Vy_flights.append(1)
            i += 1

        pyplot.figure(figsize=(14, 15))
        pyplot.barh(Vx_airlines, Vy_flights, label="Airline Flights")
        pyplot.yticks(size=12)
        pyplot.xlabel("Flights")
        pyplot.ylabel("Airlines")
        pyplot.legend()
        pyplot.tight_layout()
        pyplot.show()
    except FileNotFoundError:
        aircrafts=aircrafts
    return

def PlotFlightsType(aircrafts):
    if len(aircrafts) == 0:
        print("Error")
        return
    i = 0
    countsche = countnosche = 0
    sche = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG',
            'EH', 'LH', 'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP',
            'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    while i < len(aircrafts):
        j = 0
        found = False
        while j < len(sche) and not found:
            if aircrafts[i][1][:2] == sche[j]:
                found = True
                countsche += 1
            j += 1
        if not found:
            countnosche += 1
        i += 1
    Vx=["Schengen","No Schengen"]
    Vy=[countsche,countnosche]
    pyplot.bar(Vx,Vy,label="Arrivals type")
    pyplot.xlabel("Type")
    pyplot.ylabel("Arrivals")
    pyplot.legend()
    pyplot.show()
    return

def MapFlights(aircrafts,filename):
    airports=LoadAirport("Airports.txt")
    new_file=open(filename, "w")
    new_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    new_file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    new_file.write("<Document>\n")
    i=0
    while i<len(aircrafts):
        j=0
        while j<len(airports):
            if aircrafts[i][1]==airports[j][0]:
                new_file.write("\t<Placemark>\n")
                new_file.write(f'\t\t<name>"Route {aircrafts[i][1]}-LEBL"</name>\n')
                new_file.write("\t\t<LineString>\n")
                new_file.write("\t\t\t<altitudeMode>clampToGround</altitudeMode>\n")
                new_file.write("\t\t\t<extrude>1</extrude>\n")
                new_file.write("\t\t\t<tessellate>1</tessellate>\n")
                new_file.write("\t\t\t\t<coordinates>\n")
                new_file.write("\t\t\t\t\t2.078333,41.296944\n")
                new_file.write(f"\t\t\t\t\t{airports[j][2]},{airports[j][1]}\n")
                new_file.write("\t\t\t\t</coordinates>\n")
                new_file.write("\t\t</LineString>\n")
                new_file.write("\t\t<Style>\n")
                new_file.write("\t\t\t<LineStyle>\n")
                if IsSchengenAirport(airports[j][0])==True:
                    new_file.write("\t\t\t\t<color>ff00ff00</color>\n")
                else:
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

def LongDistanceArrivals(aircrafts,filename):
    airports = LoadAirport("Airports.txt")
    new_file = open(filename, "w")
    new_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    new_file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    new_file.write("<Document>\n")
    i = 0
    while i < len(aircrafts):
        j = 0
        while j < len(airports):
            if aircrafts[i][1] == airports[j][0]:
                bcnlat=41.296944
                bcnlon=2.078333
                a=sin(radians(airports[j][1]-bcnlat)/2)**2+cos(radians(bcnlat))*cos(radians(airports[j][1]))*sin(radians(bcnlon-airports[j][2])/2)**2
                c=2*atan2(sqrt(a),sqrt(1-a))
                d=6371*c
                print(d)
                if d>=2000:
                    new_file.write("\t<Placemark>\n")
                    new_file.write(f'\t\t<name>"Route {aircrafts[i][1]}-LEBL"</name>\n')
                    new_file.write("\t\t<LineString>\n")
                    new_file.write("\t\t\t<altitudeMode>clampToGround</altitudeMode>\n")
                    new_file.write("\t\t\t<extrude>1</extrude>\n")
                    new_file.write("\t\t\t<tessellate>1</tessellate>\n")
                    new_file.write("\t\t\t\t<coordinates>\n")
                    new_file.write("\t\t\t\t\t2.078333,41.296944\n")
                    new_file.write(f"\t\t\t\t\t{airports[j][2]},{airports[j][1]}\n")
                    new_file.write("\t\t\t\t</coordinates>\n")
                    new_file.write("\t\t</LineString>\n")
                    new_file.write(f"\t</Placemark>\n")
            j=j+1
        i=i+1
    new_file.write("</Document>\n")
    new_file.write("</kml>\n")
    new_file.close()
    return

# test section
if __name__ == "__main__":
    aircrafts=LoadArrivals("Arrivals.txt")
    PlotFlightsType(aircrafts)