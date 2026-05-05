from aircraft import *

class BarcelonaAP:
    def __init__(self,code):
        self.code=code  #code of the airport (LEBL)
        self.list_terminal=[]   #list composed of the class Terminal

class Terminal:
    def __init__(self,name):
        self.name=name  #name of the terminal
        self.list_obj=[]    #list composed of the class BoardingArea
        self.list_code=[]   #airlines codes

class BoardingArea:
    def __init__(self,name,sche):
        self.name=name  #name of the area (ex. "Area A")
        self.sche=sche  #if it's schengen
        self.gate_list=[]   #list composed of the class Gate

class Gate:
    def __init__(self,name):
        self.name=name  #name of the gate (ex. "T1AG1")
        self.occupancy=None #status of occupancy
        self.aircraft="-"  #ID of the aircraft in the case of occupancy=True

def SetGates (area, init_gate, end_gate, prefix):
    if end_gate<=init_gate:
        return -1
    i=init_gate
    while init_gate<=i<=end_gate:
        gate_name=prefix+"G"+str(i)
        new_gate=Gate(gate_name)
        new_gate.occupied=False
        new_gate.aircraft_id =""
        area.gate_list.append(new_gate)
        i=i+1
    return

def LoadAirlines (terminal, t_name):
    file=open(f"{t_name}_Airlines.txt", "r")
    terminal_info=file.readline()
    while terminal_info!="":
        info=terminal_info.split("\t")
        letters=info[1].strip()
        terminal.list_code.append(letters)
        terminal_info=file.readline()
    file.close()
    return

def LoadAirportStructure (filename):
    try:
        file=open(filename, "r")
        info=file.readline().split()
        if not info:
            file.close()
            return -1
        bcn=BarcelonaAP(info[0])
        num_terminals=int(info[1])
        i = 0
        while i < num_terminals:
            term=file.readline().split()
            t_name=term[1]
            num_areas=int(term[2])
            terminal=Terminal(t_name)
            LoadAirlines(terminal, t_name)
            j=0
            while j<num_areas:
                info_area=file.readline().split()
                area=BoardingArea(info_area[0]+" "+info_area[1],info_area[2])
                SetGates(area,int(info_area[4]),int(info_area[6]),t_name+info_area[1])
                terminal.list_obj.append(area)
                j=j+1
            bcn.list_terminal.append(terminal)
            i=i+1
        file.close()
        return bcn
    except FileNotFoundError:
        return

def  GateOccupancy (bcn):
    all_info=[]
    i=0
    while i<len(bcn.list_terminal): #[LEBL,TERMINAL]
        terminal=bcn.list_terminal[i]   #We look at the TERMINAL
        j=0
        while j<len(terminal.list_obj): #[LEBL,[T1,BOARDING AREA,abcd]]
            area=terminal.list_obj[j]   #We look at the BOARDING AREA
            k=0
            while k<len(area.gate_list):    #[LEBL,[T1,["Area A",schengen,GATE],abcd]]
                gate=area.gate_list[k]  #We look at GATE
                if gate.occupied:
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

def PrintGateInfo(all_info):
    info=all_info
    return info

def IsAirlineInTerminal (terminal, name):
    if name == "":
        return False
    if len(terminal.list_code)==0:
        return False
    return name in terminal.list_code

def SearchTerminal (bcn, name):
    terminal=bcn.list_terminal
    if IsAirlineInTerminal(terminal[0], name):
        return terminal[0].name
    elif IsAirlineInTerminal(terminal[1], name):
        return terminal[1].name
    else:
        return ""

def AssignGate (bcn,aircraft):
    try:
        terminal_name = SearchTerminal(bcn, aircraft.icao_airline)
        if not terminal_name:
            return -1
        sche_prefixes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI',
                         'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
        tipo_vuelo = "Schengen" if aircraft.icao_origin[:2] in sche_prefixes else "non-Schengen"
        i = 0
        found = False
        while i < len(bcn.list_terminal) and not found:
            terminal = bcn.list_terminal[i]
            if terminal.name == terminal_name:
                j = 0
                while j < len(terminal.list_obj) and not found:
                    area = terminal.list_obj[j]
                    if area.sche.strip() == tipo_vuelo:
                        k = 0
                        while k < len(area.gate_list) and not found:
                            gate = area.gate_list[k]
                            if gate.occupancy is None or gate.occupancy == False:
                                gate.occupancy = True
                                gate.aircraft=aircraft.id
                                print(gate.aircraft)
                                found = True
                            k += 1
                    j += 1
            i += 1
        if found:
            return gate.name
        else:
            return "Free"
    except Exception:
        return "error"

def PrintOccupancy(bcn):
    if gate.occupancy == True:
        status = "Occupied"
        code = gate.aircraft
    else:
        status = "Free"
        code = "-"
    info = (f"Name: {gate.name}\n"
            f"Code: {code}\n"
            f"Status: {status}\n\n")
    return info
if __name__ == "__main__":
    print(LoadAirportStructure("Terminals.txt"))
    test_area=BoardingArea("Area A", "Schengen")
    inicio=1
    fin=11
    prefijo="T1A"

    print(f"--- Probando SetGates con {prefijo} de {inicio} a {fin} ---")

    resultado = SetGates(test_area, inicio, fin, prefijo)
    print(f"Número de puertas creadas: {len(test_area.gate_list)}")

    for gate in test_area.gate_list:
        print(f"Puerta: {gate.name} | Ocupada: {gate.occupied} | Avión: '{gate.aircraft}'")

    mi_terminal = Terminal("T1")
    LoadAirlines(mi_terminal, "T1")
    print(f"Terminal: {mi_terminal.name}")
    print(f"Codes: {mi_terminal.list_code}")
    print(GateOccupancy(LoadAirportStructure("Terminals.txt")))
    aviones = LoadArrivals("Arrivals.txt") #aircrafts from aircrafts
    aeropuerto = LoadAirportStructure("Terminals.txt") #bcn

    for un_avion in aviones:
        resultado = AssignGate(aeropuerto, un_avion)
        print ("it's",PrintOccupancy(aeropuerto))
        if resultado != -1:
            print(f"Aerolinea {un_avion.icao_airline}: {resultado}")
    print(SearchTerminal(aeropuerto, "VLG"))
