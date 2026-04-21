class BarcelonaAP:  #We open the class for the airport with all the variables we are going to use
    def __init__(self,code):
        self.code=code
        self.list_terminal=[]

class Terminal:  #We open the class for the airport with all the variables we are going to use
    def __init__(self,name):
        self.name=name
        self.list_obj=[]
        self.list_code=[]

class BoardingArea:  #We open the class for the airport with all the variables we are going to use
    def __init__(self,name,sche):
        self.name=name
        self.sche=sche
        self.gate_list=[]

class Gate:  #We open the class for the airport with all the variables we are going to use
    def __init__(self,name):
        self.name=name
        self.occupancy=None
        self.id=""

def SetGates (area, init_gate, end_gate, prefix):
    if end_gate <= init_gate:
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
        letters=info[1]
        if letters[3]=="\n":
            info[1]="".join(letters[0:3])
        terminal.list_obj.append(info[0])
        terminal.list_code.append(info[1])
        terminal_info=file.readline()
    file.close()
    return

def LoadAirportStructure (filename):
    return

def GateOccupancy (bcn):
    return

def IsAirlineInTerminal (terminal, name):
    return

def SearchTerminal (bcn, name):
    return

def AssignGate (bcn, aircraft):
    return

if __name__ == "__main__":
    test_area=BoardingArea("Area A", "Schengen")
    inicio=1
    fin=11
    prefijo="T1A"

    print(f"--- Probando SetGates con {prefijo} de {inicio} a {fin} ---")

    resultado = SetGates(test_area, inicio, fin, prefijo)
    print(f"Número de puertas creadas: {len(test_area.gate_list)}")

    for gate in test_area.gate_list:
        print(f"Puerta: {gate.name} | Ocupada: {gate.occupied} | Avión: '{gate.aircraft_id}'")

    mi_terminal = Terminal("T1")
    LoadAirlines(mi_terminal, "T1")
    print(f"Terminal: {mi_terminal.name}")
    print(f"Names: {mi_terminal.list_obj}")
    print(f"Codes: {mi_terminal.list_code}")