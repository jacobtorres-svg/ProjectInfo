from matplotlib import pyplot

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

def PlotAirlines (aircrafts):
    
    return
def PlotFlightsType (aircrafts):
    
    return
def MapFlights(aircrafts):
    return
def LongDistanceArrivals(aircrafts):
    return

# test section
if __name__ == "__main__":
    aircrafts=LoadArrivals("Arrivals.txt")
    PlotArrivals(aircrafts)
    print(aircrafts)
    SaveFlights(aircrafts,"new.txt")
