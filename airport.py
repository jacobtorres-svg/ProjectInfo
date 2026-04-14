from matplotlib import pyplot

class Airport:  #We open the class for the airport with all the variables we are going to use
    def __init__(self,icao_code,latitude,longitude):
        self.icao_code=icao_code
        self.latitude=latitude
        self.longitude=longitude
        self.sche=bool()

def IsSchengenAirport(code):    #Function to check if the code of the input-ed airport is Schengen
    schengen=open("Schengen_codes.txt","r")     #File that contains, in each line, the 2 first letters that make an icao code and indicate it's Schengen
    sche=schengen.readline()
    end=False
    #No posar un arxiu
    true_code=False #Bool that'll indicate if the code is or isn't Schenge to the user
    while sche!="" and end==False:
        sche=sche.replace("\n","")  #We remove the \n at the end of each code (from the file), because that just indicates a change of line
        if code[:2]==sche:
            true_code=True
            end=True
        else:
            true_code=False
        sche=schengen.readline()
    schengen.close()
    return true_code    #The function returns the updated value of the airport Schengen(True)/not Schengen(False)

def SetSchengen(airport):   #Function to ask for the IsSchengenAirport to tell us if it's Schengen, and we add that value to the airport attributes
    airport.sche=IsSchengenAirport(airport.icao_code)
    return

def PrintAirport(airport):  #Function to write all the variables from the Airport class, but updated with our current input-ed airport
    print("ICAO Code:",airport.icao_code)
    print("Latitude:",airport.latitude)
    print("Longitude:",airport.longitude)
    print("Schengen:",airport.sche)
    return

def LoadAirport(filename):  #Function to restructure how latitude and longitude are shown in a file
    airports=[]
    try:    #With this we can easily create the condition (similar to a while) that the code will work unless we get to an exception
        file=open(filename, "r")
        air=file.readline()
        air=file.readline() #We ride two lines in one go to skip the title
        while air != "":
            info=air.split(" ")
            #We separate the information in a vector of [code,latitude,longitude]
            code=info[0]
            lat_=info[1]
            lon_=info[2]
            #We convert the latitude from string to decimal degrees
            lat=round((int(lat_[1:3]))+(int(lat_[3:5])/60)+(int(lat_[5:])/3600),6)
            if lat_[0]=="S":
                lat=-lat
            lon=round((int(lon_[1:4]))+(int(lon_[4:6])/60)+(int(lon_[6:])/3600),6)
            if lon_[0]=="W":
                lon=-lon
            lat=float(lat)
            lon=float(lon)
            one_airport=[code,lat,lon]    #We regroup all the information in a vector that we'll insert in the airports list (essentially creating a matrix)
            airports.append(one_airport)
            air=file.readline()
        file.close()
    except FileNotFoundError:   #This exception indicates that if we can't find the file instead of shooting an error it just returns an empty vector
        return []
    return airports #The function returns the list with all the airports and their correct latitude/longitude in degrees

def SaveSchengenAirports(airports,filename):    #Function to grab a list of airports and create a new file that only includes the Schengen ones
    new_file=open(filename,"w") #We open a new file with whatever name we've input-ed
    i=0
    if len(airports)>0:
        while i<len(airports):
            if IsSchengenAirport(airports[i][0])==True: #We check just the codes of every airport in the list using our first function (IsSchengenAirport)
                #We put each piece of information in a new vector to add the spaces and change of line before turning into text and putting it in
                #the file we had previously created
                vector_airport=[airports[i][0],"\t",str(airports[i][1]),"\t",str(airports[i][2]),"\n"]
                new_file.write("".join(vector_airport))
            i=i+1
    else:   #In case there aren't any airports in the list (it's empty) we return an error message
        print("No airports found")
    new_file.close()
    return

def AddAirport(airports,airport):   #Function to add airports to the list
    airports=LoadAirport(airports)
    i=0
    end=False
    while i<len(airports) and end==False:
        if airports[i][0]==airport.icao_code:
            end=True
        i=i+1
    if end==False:  #If the condition to end the loop early isn't true it means the loop hasn't found the airport, so it's okay to add it
        airport=[airport.icao_code,airport.latitude,airport.longitude]
        airports.append(airport)
    return airports #The function returns the updated list

def RemoveAirport(airport,code):    #Function to delete airports from the list
    airport=LoadAirport(airport)
    i=0
    end=False
    while i<len(airport) and end==False:
        if airport[i][0]==code:
            airport.pop(i)  #The .pop eliminates that position from the vector
            end=True
        i=i+1
    return airport

def PlotAirports(airports): #Function to make the graph of the Schengen vs Non-Schengen airports
    i=0
    no_schengen=0
    schengen=0
    while i<len(airports):
        if IsSchengenAirport(airports[i][0])==True: #For every Schengen airport +1
            schengen=schengen+1
        i=i+1
    no_schengen=len(airports)-schengen
    pyplot.bar(["Airports"],[schengen],label="Schengen")
    pyplot.bar(["Airports"],[no_schengen],bottom= [schengen],label="No Schengen")
    pyplot.legend()
    pyplot.show()
    return

def MapAirports(airports,filename):  #Function to make the code for the Google Earth
    new_file=open(filename, "w")
    new_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    new_file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    new_file.write("<Document>\n")
    i=0
    while i<len(airports):
        new_file.write(f"\t<Placemark> <name>{airports[i][0]}</name>\n")
        new_file.write("\t\t<Point>\n")
        new_file.write("\t\t\t<coordinates>\n")
        new_file.write(f"\t\t\t\t{airports[i][2]},{airports[i][1]}\n")
        new_file.write("\t\t\t</coordinates>\n")
        new_file.write("\t\t</Point>\n")
        new_file.write("\t\t<Style>\n")
        if IsSchengenAirport(airports[i][0])==True:
            new_file.write("\t\t\t<LabelStyle>\n")
            new_file.write("\t\t\t\t<color>ff00ff00</color>\n")
            new_file.write("\t\t\t</LabelStyle>\n")
            new_file.write("\t\t\t<IconStyle>\n")
            new_file.write("\t\t\t\t<color>ff00ff00</color>\n")
            new_file.write("\t\t\t</IconStyle>\n")
        else:
            new_file.write("\t\t\t<LabelStyle>\n")
            new_file.write("\t\t\t\t<color>ff0000ff</color>\n")
            new_file.write("\t\t\t</LabelStyle>\n")
            new_file.write("\t\t\t<IconStyle>\n")
            new_file.write("\t\t\t\t<color>ff0000ff</color>\n")
            new_file.write("\t\t\t</IconStyle>\n")
        new_file.write("\t\t</Style>\n")
        new_file.write(f"\t</Placemark>\n")
        i=i+1
    new_file.write("</Document>\n")
    new_file.write("</kml>\n")
    new_file.close()
    return
