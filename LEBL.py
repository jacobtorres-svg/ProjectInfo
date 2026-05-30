from aircraft import *
import matplotlib.pyplot as pyplot
class BarcelonaAP:
    def __init__(self,code):
        self.code=code  #Code of the airport (LEBL)
        self.list_terminal=[]   #List composed of the class Terminal

class Terminal:
    def __init__(self,name):
        self.name=name  #Name of the terminal
        self.list_obj=[]    #List composed of the class BoardingArea
        self.list_code=[]   #Airlines codes

class BoardingArea:
    def __init__(self,name,sche):
        self.name=name  #Name of the area (ex. "Area A")
        self.sche=sche  #If it's Schengen
        self.gate_list=[]   #List composed of the class Gate

class Gate:
    def __init__(self,name):
        self.name=name  #Name of the gate (ex. "T1AG1")
        self.occupancy=None #Status of occupancy
        self.aircraft="-"  #ID of the aircraft in the case of occupancy=True

def SetGates (area, init_gate, end_gate, prefix):   #Function to create all the gates there are with proper names
    if end_gate<=init_gate:
        return -1
    i=init_gate
    while init_gate<=i<=end_gate:
        gate_name=prefix+"G"+str(i)
        new_gate=Gate(gate_name)
        area.gate_list.append(new_gate)
        i=i+1
    return

def LoadAirlines (terminal, t_name):    #Function to load all the airlines from their corresponding terminals
    file=open(f"{t_name}_Airlines.txt", "r")
    terminal_info=file.readline()
    while terminal_info!="":
        info=terminal_info.split("\t")
        letters=info[1].strip()
        terminal.list_code.append(letters)
        terminal_info=file.readline()
    file.close()
    return

def LoadAirportStructure (filename):    #Function to complete all the information from the airport in their respective classes
    try:
        file=open(filename, "r")
        info=file.readline().split()
        if not info:
            file.close()
            return -1
        bcn=BarcelonaAP(info[0])    #Name of the airport (LEBL)
        num_terminals=int(info[1])
        i = 0
        while i < num_terminals:
            term=file.readline().split()
            t_name=term[1]
            num_areas=int(term[2])
            terminal=Terminal(t_name)   #Name of the terminal
            LoadAirlines(terminal, t_name)  #Name of airlines from that terminal
            j=0
            while j<num_areas:
                info_area=file.readline().split()
                area=BoardingArea(info_area[0]+" "+info_area[1],info_area[2])   #Name of the boarding area and if it admits Schengen flights
                SetGates(area,int(info_area[4]),int(info_area[6]),t_name+info_area[1])  #Name of the gates from that area
                terminal.list_obj.append(area)
                j=j+1
            bcn.list_terminal.append(terminal)
            i=i+1
        file.close()
        return bcn
    except FileNotFoundError:
        return

def  GateOccupancy (bcn):   #Function to set the occupation of the gates
    all_info=[]
    i=0
    while i<len(bcn.list_terminal): #[LEBL,TERMINAL]
        terminal=bcn.list_terminal[i]   #We look at the TERMINAL
        j=0
        while j<len(terminal.list_obj): #[LEBL,[T1,BOARDING AREA,abcd]]
            area=terminal.list_obj[j]   #We look at the BOARDING AREA
            k=0
            while k<len(area.gate_list):    #[LEBL,[T1,["Area A",Schengen,GATE],abcd]]
                gate=area.gate_list[k]  #We look at GATE
                if gate.occupancy:
                    status="Occupied"
                    code=gate.aircraft
                else:
                    status="Free"
                    code="-"
                list_gates=(f"Name: {gate.name}\n"
                            f"Code: {code}\n"
                            f"Status: {status}\n\n")
                all_info.append(list_gates)
                k+=1
            j+=1
        i+=1
    return all_info

def PrintGateInfo(all_info):    #Function to print the gate information
    info=all_info
    return info

def IsAirlineInTerminal (terminal, name):   #Function to see if an airline is part of terminal or not (if it's allowed to land there)
    if name == "":
        return False
    if len(terminal.list_code)==0:
        return False
    return name in terminal.list_code

def SearchTerminal (bcn, name): #Function to search for which terminal the airline you have is at
    terminal=bcn.list_terminal
    if IsAirlineInTerminal(terminal[0], name):
        return terminal[0].name
    elif IsAirlineInTerminal(terminal[1], name):
        return terminal[1].name
    else:
        return ""

def AssignGate (bcn,aircraft):  #Function to assign the gates to each airline properly depending on their specifications
    try:
        terminal_name=SearchTerminal(bcn, aircraft.icao_airline)
        if not terminal_name:
            return -1
        sche_prefixes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI',
                         'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
        type_flight="Schengen" if aircraft.icao_origin[:2] in sche_prefixes else "non-Schengen"
        i=0
        found=False
        assigned_gate=None
        while i < len(bcn.list_terminal) and found==False:
            terminal=bcn.list_terminal[i]
            if terminal.name==terminal_name:
                j=0
                while j<len(terminal.list_obj) and found==False:
                    area=terminal.list_obj[j]
                    if area.sche.strip()==type_flight:
                        k=0
                        while k<len(area.gate_list) and found==False:
                            gate=area.gate_list[k]
                            if not gate.occupancy:
                                gate.occupancy=True
                                gate.aircraft=aircraft.id
                                assigned_gate=gate
                                found=True
                            k += 1
                    j += 1
            i += 1
        if found:
            return assigned_gate
        else:
            return "Free"
    except Exception:
        return "error"


def PrintOccupancy(gate):   #Function to print the gate occupancy
    if gate.occupancy==True:
        status="Occupied"
        code=gate.aircraft
    else:
        status="Free"
        code="-"
    info=(f"Name: {gate.name}\n"
            f"Code: {code}\n"
            f"Status: {status}\n\n")
    return info

def AssignNightGates (bcn, aircrafts):  #Function to pre-assign some gates as occupied for the flights that were at the airport form the night before
    try:
        terminal_name = SearchTerminal(bcn, aircrafts.icao_airline)
        if not terminal_name:
            return -1
        sche_prefixes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI',
                         'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
        type_flight = "Schengen" if aircrafts.icao_origin[:2] in sche_prefixes else "non-Schengen"
        i = 0
        found = False
        assigned_night_gate = None
        while i < len(bcn.list_terminal) and found == False:
            terminal = bcn.list_terminal[i]
            if terminal.name == terminal_name:
                j = 0
                while j < len(terminal.list_obj) and found == False:
                    area = terminal.list_obj[j]
                    if area.sche.strip() == type_flight:
                        k = 0
                        while k < len(area.gate_list) and found == False:
                            gate = area.gate_list[k]
                            if not gate.occupancy:
                                gate.occupancy = True
                                gate.aircraft = aircrafts.id
                                assigned_night_gate = gate
                                found = True
                            k += 1
                    j += 1
            i += 1
        if found:
            return assigned_night_gate
        else:
            return "Free"
    except Exception:
        return "error"

def FreeGate (bcn, id): #Function to free an occupied gate
    try:
        i=0
        j=0
        k=0
        found = False
        while i < len(bcn.list_terminal) and found==False:
            terminal = bcn.list_terminal[i]
            while j < len(terminal.list_obj) and found==False:
                area = terminal.list_obj[j]
                while k < len(area.gate_list) and found==False:
                    gate = area.gate_list[k]
                    if gate.aircraft==id:
                        found=True
                        gate.aircraft="-"
                        gate.occupancy="Free"
                    k=k+1
                j=j+1
            i=i+1
        if found == False:
            return found
        else:
            return found
    except:
        return "Error in FreeGate."

def AssignGatesAtTime (bcn, aircrafts, time):   #Function to assign the gates but depending on the time
    hour=int(time.split(":")[0])
    i=0
    while i<len(bcn.list_terminal):
        terminal=bcn.list_terminal[i]
        j=0
        while j<len(terminal.list_obj):
            area=terminal.list_obj[j]
            k=0
            while k<len(area.gate_list):
                gate=area.gate_list[k]
                if gate.occupancy==True and gate.aircraft is not None:
                    l=0
                    found=False
                    while l<len(aircrafts) and found==False:
                        airplane=aircrafts[l]
                        if airplane.id==gate.aircraft:
                            if airplane.departure is None:
                                gate.occupancy=False
                                gate.aircraft=None
                                found=True
                            else:
                                departure=int(airplane.departure.split(":")[0])
                                if departure==hour:
                                    gate.occupancy=False
                                    gate.aircraft=None
                                    found=True
                        l=l+1
                    if found==False:
                        gate.occupancy=False
                        gate.aircraft=None
                k=k+1
            j=j+1
        i=i+1
    i=0
    gateless=0
    while i<len(aircrafts):
        aircraft=aircrafts[i]
        if aircraft.landing!=None:
            landing=int(aircraft.landing.split(":")[0])
            if landing==hour:
                assinged=AssignGate(bcn, aircraft)
                if assinged==-1 or assinged =="error":
                    gateless=gateless+1
        i=i+1
    return gateless

def PlotDayOccupancy (bcn, aircrafts):  #Function to create two plots; one to show occupancy of each terminal per hour, and the other to show unassigned aircraft per hour
    h=[]
    t1_occ=[]
    t2_occ=[]
    unassigned=[]
    i=0
    while i<24:
        if i<10:
            time="0"+str(i)+":00"
        else:
            time=str(i)+":00"
        h.append(time)
        not_assigned=AssignGatesAtTime(bcn, aircrafts, time)
        unassigned.append(not_assigned)
        occupied_t1=0
        occupied_t2=0
        j=0
        while j<len(bcn.list_terminal):
            terminal=bcn.list_terminal[j]
            k=0
            while k<len(terminal.list_obj):
                area=terminal.list_obj[k]
                g=0
                while g<len(area.gate_list):
                    gate=area.gate_list[g]
                    if gate.occupancy==True:
                        if terminal.name=="T1":
                            occupied_t1+=1
                        elif terminal.name=="T2":
                            occupied_t2+=1
                    g+=1
                k+=1
            j+=1
        t1_occ.append(occupied_t1)
        t2_occ.append(occupied_t2)
        i+=1
    pyplot.figure(figsize=(12,6))
    pyplot.plot(h, t1_occ, label="T1")
    pyplot.plot(h, t2_occ, label="T2")
    pyplot.xlabel("Hour")
    pyplot.ylabel("Occupied gates")
    pyplot.title("Gate Occupancy During the Day")
    pyplot.legend()
    pyplot.xticks(rotation=45)
    pyplot.grid()
    pyplot.show()
    pyplot.figure(figsize=(12,4))
    pyplot.bar(h, unassigned)
    pyplot.xlabel("Hour")
    pyplot.ylabel("Aircrafts not assigned")
    pyplot.title("Unassigned Aircrafts")
    pyplot.xticks(rotation=45)
    pyplot.grid()
    pyplot.show()
    return

if __name__ == "__main__":  #Test area
    test_area=BoardingArea("Area A", "Schengen")
    results=SetGates(test_area, 1, 11, "T1A")
    print(f"Número de puertas creadas: {len(test_area.gate_list)}")
    for gate in test_area.gate_list:
        print(f"Gate: {gate.name} | Occupancy: {gate.occupancy} | Aircraft: '{gate.aircraft}'")
    terminal=Terminal("T2")
    LoadAirlines(terminal, "T2")
    print(f"Terminal: {terminal.name}")
    print(f"Codes: {terminal.list_code}")
    arrivals=LoadArrivals("Arrivals.txt")
    airport=LoadAirportStructure("Terminals.txt")
    print(SearchTerminal(airport, "VLG"))
    for a in arrivals:
        assign=AssignGate(airport,a)
        if assign != -1 and not isinstance(assign, str):
            print("it's", PrintOccupancy(assign))
            print(f"Airline {a.icao_airline} assigned to {assign.name}")

    departures=LoadDepartures("Departures.txt")
    merged=MergeMovements(arrivals,departures)
    night=NightAircraft(merged)
    for n in night:
        assign = AssignNightGates(airport,n)
        if assign != -1 and not isinstance(assign, str):
            print("it's", PrintOccupancy(assign))
            print(f"Airline {n.icao_airline} assigned to {assign.name}")

    free=FreeGate(airport,"ECMKV")
    print(free)

    assign_time=AssignGatesAtTime(airport, merged, "18:00")
    print(assign_time)
    print(PlotDayOccupancy(airport,merged))