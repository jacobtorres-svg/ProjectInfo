class BarcelonaAP:  #We open the class for the airport with all the variables we are going to use
    def __init__(self,code,list_terminal):
        self.code=code
        self.list_terminal=list_terminal

class Terminal:  #We open the class for the airport with all the variables we are going to use
    def __init__(self,name,list_obj,list_code):
        self.name=name
        self.list_obj=list_obj
        self.list_code=list_code

class BoardingArea:  #We open the class for the airport with all the variables we are going to use
    def __init__(self,name,sche,gate_list):
        self.name=name
        self.sche=sche
        self.gate_list=gate_list

class Gate:  #We open the class for the airport with all the variables we are going to use
    def __init__(self,name,ocup,id):
        self.name=name
        self.ocup=ocup
        self.id=id

def SetGates (area, init_gate, end_gate, prefix):
    area=[]
    try:
        file=open("Terminals.txt", "r")
        file.readline()
        information=file.readline()
        while information!="":
            info=information.split()
            i=0
            while i<len(info):
                if info[i]==" ":
                    info[i].pop(" ")
                i=i+1
            if info[0]=="Terminal":
                prefix=info[1]+"BA"
            if info[0]=="Area":
                vector=[info[1],info[4],info[6],prefix]
                area.append(vector)
            print(area)
            information=file.readline()
    except FileNotFoundError:  # This exception indicates that if we can't find the file instead of shooting an error it just returns an empty vector
        return []
    return area
print(SetGates(0,0,0,"T1BA"))

def LoadAirlines (terminal, t_name):
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