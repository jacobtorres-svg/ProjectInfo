from LEBL import *
from airport import *
from aircraft import *
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog

#---AIRPORT SECTION---
airports_file=None
airports=[]
#important button for aesthetics in the pop-ups
popup_button_style = {"bg": "#2c3e50","fg": "white","activebackground": "#34495e","activeforeground": "white","font": ("Segoe UI", 10, "bold"),"relief": "flat","width": 15,"cursor": "hand2"}

def LoadAirports(): #Function to ask for the file to load the airports we have available
    global airports,airports_file
    filename=filedialog.askopenfilename(title="Select airports file")   #Similar to putting a variable=input(), we ask for the file, but searching in our files
    if filename:
        airports=LoadAirport(filename)  #We call the LoadAirport from the airport to give us the list we knew (and still know here) as airports
        airports_file=filename  #We clarify, globally, that now there's a file for the airports
        text_area.insert(tk.END, f"Loaded {len(airports)} airports from {filename}\n")
    text_area.see(tk.END)
    return

def AddNewAirport(principal): #Function to have the button to ask to add a new airport
    if len(airports)==0:
        messagebox.showwarning("No Data","No airports loaded.")
        return
    def AddAction():    #Function to actually do the work of adding the new airport
        global airports
        original_length=len(airports)
        code=code_entry.get().strip()
        lat=lat_entry.get().strip()
        lon=lon_entry.get().strip()
        try:
            if len(list(code))!=4:
                messagebox.showwarning("Input Error","Incorrect ICAO code.")
            elif code and lat and lon:
                airports=AddAirport(airports,Airport(code,float(lat),float(lon)))
                if len(airports)==original_length:
                    messagebox.showwarning("Input Error", "That airport already exists.")
                else:
                    text_area.insert(tk.END,f"Added airport {code}\n")
                    add_window.destroy()
            else:
                messagebox.showwarning("Input Error","All fields are required.")
        except ValueError:
            messagebox.showwarning("Input Error","Incorrect latitude and/or longitude.")
    text_area.see(tk.END)
    #We decorate the interface
    add_window = tk.Toplevel(principal, padx=30, pady=30, bg="#f0f3f5")
    add_window.title("Add New Airport")
    #main interface
    main_frame=tk.Frame(add_window, bg="#f0f3f5")
    main_frame.pack(expand=True)
    #repetitive style
    lbl_style={"bg": "#f0f3f5", "font": ("Segoe UI", 10)}
    entry_style={"font": ("Segoe UI", 10), "justify": "center"}
    #input of information
    tk.Label(main_frame, text="ICAO Code", **lbl_style).pack()
    code_entry = tk.Entry(main_frame, **entry_style)
    code_entry.pack(pady=(0, 10))
    code_entry.focus_set()
    tk.Label(main_frame, text="Latitude", **lbl_style).pack()
    lat_entry = tk.Entry(main_frame, **entry_style)
    lat_entry.pack(pady=(0, 10))
    tk.Label(main_frame, text="Longitude", **lbl_style).pack()
    lon_entry = tk.Entry(main_frame, **entry_style)
    lon_entry.pack(pady=(0, 20))
    #the button
    tk.Button(main_frame, text="Add Airport", command=AddAction, **popup_button_style).pack()
    #center at the start
    CenterWindow(add_window)
    return

def DeleteAirport(principal):   #Function to have the button to ask to delete an airport
    if len(airports)==0:
        messagebox.showwarning("No Data","No airports loaded.")
        return
    def DeleteAction(): #Function to actually do the work of deleting the airport
        global airports
        original_length=len(airports)
        code=code_entry.get().strip()
        if len(list(code))!=4:
            messagebox.showwarning("Input Error","Incorrect ICAO code.")
        elif code:
            airports=RemoveAirport(airports,code)
            if len(airports)==original_length:
                messagebox.showwarning("Input Error", "That airport doesn't exist.")
            else:
                text_area.insert(tk.END,f"Deleted airport {code}\n")
            del_window.destroy()
        else:
            messagebox.showwarning("Input Error","ICAO code required.")
    text_area.see(tk.END)
    #We decorate the interface
    del_window = tk.Toplevel(principal, padx=40, pady=30, bg="#f0f3f5")
    del_window.title("Delete Airport")
    #main interface
    main_frame = tk.Frame(del_window, bg="#f0f3f5")
    main_frame.pack(expand=True)
    #repetitive style
    lbl_style = {"bg": "#f0f3f5", "font": ("Segoe UI", 10)}
    entry_style = {"font": ("Segoe UI", 10), "justify": "center"}
    #code entry
    tk.Label(main_frame, text="ICAO Code", **lbl_style).pack()
    code_entry = tk.Entry(main_frame, **entry_style)
    code_entry.pack(pady=(0, 10))
    code_entry.focus_set()
    #the button
    tk.Button(main_frame,text="Delete Airport",command=DeleteAction,**popup_button_style).pack()
    #center at the start
    CenterWindow(del_window)
    return

def SetNewSchengen():   #Function to make the current airports get their Schengen/Non-Schengen information
    global airports
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    i=0
    while i<len(airports):
        airports[i].sche=SetSchengen(airports[i])
        i=i+1
    text_area.insert(tk.END,"Updated Schengen attribute for all airports.\n")
    text_area.see(tk.END)
    return airports

def ShowAirports(): #Function to show all the current information from all the current airports in the list
    if len(airports)==0:
        messagebox.showwarning("No Data","No airports loaded.")
        return
    text_area.insert(tk.END,"---Airports---\n")
    i=0
    while i<len(airports):
        info=PrintAirport(airports[i])
        text_area.insert(tk.END,info)
        i=i+1
    text_area.see(tk.END)
    return

def SaveSchengen(): #Function to save all the Schengen airports into a separate file of our choice
    if len(airports)==0:
        messagebox.showwarning("No Data","No airports loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save Schengen Airports",defaultextension=".txt")
    if filename:
        SaveSchengenAirports(airports,filename)
        text_area.insert(tk.END,f"Schengen airports saved to {filename}\n")
    text_area.see(tk.END)
    return

def GraphAirports():    #Function to ask for the plot to create a graph of Schengen vs Non-Schengen airports
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    elif airports[0].sche==None:
        messagebox.showwarning("Input Error","No Schengen stablished.")
    else:
        PlotAirports(airports)
    return

def ShowMap():  #Function to create the code for the Google Earth to place all the airports
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save the airports",defaultextension=".kml")
    MapAirports(airports,filename)
    text_area.insert(tk.END, f"{filename} generated. Open it in Google Earth.\n")
    text_area.see(tk.END)
    return

#---AIRPORT SECTION---
arrivals_file=None
arrivals=[]
departures_file=None
departures=[]
merged=[]

def LoadArrival():  #Function to load the arrivals
    global arrivals,arrivals_file,merged,departures
    filename=filedialog.askopenfilename(title="Select airports file")
    if filename:
        arrivals=LoadArrivals(filename)
        arrivals_file=filename
        text_area.insert(tk.END, f"Loaded {len(arrivals)} arrivals from {filename}\n")
    text_area.see(tk.END)
    if len(departures)!=0:  #Condition to merge arrivals and departures in case both have been loaded
        merged=MergeMovements(arrivals,departures)
    return

def LoadDeparture():    #Function to load the departures
    global departures,departures_file, merged, arrivals
    filename=filedialog.askopenfilename(title="Select airports file")
    if filename:
        departures=LoadDepartures(filename)
        departures_file=filename
        text_area.insert(tk.END, f"Loaded {len(departures)} departures from {filename}\n")
    text_area.see(tk.END)
    if len(arrivals)!=0:    #Condition to merge arrivals and departures in case both have been loaded
        merged=MergeMovements(arrivals,departures)
    return

def ShowArrivals(): #Function to show all the information about the arrivals
    if len(arrivals)==0:
        messagebox.showwarning("No Data","No arrivals loaded.")
        return
    text_area.insert(tk.END,"---Arrivals---\n")
    i=0
    while i<len(arrivals):
        info=PrintAirrivals(arrivals[i])
        text_area.insert(tk.END,info)
        i=i+1
    text_area.see(tk.END)
    return

def ShowDepartures(): #Function to show all the information about the departures
    if len(departures)==0:
        messagebox.showwarning("No Data","No departures loaded.")
        return
    text_area.insert(tk.END,"---Departures---\n")
    i=0
    while i<len(departures):
        info=PrintDepartures(departures[i])
        text_area.insert(tk.END,info)
        i=i+1
    text_area.see(tk.END)
    return

def SaveArrivals(): #Function to save all the arrivals into a separate file of our choice
    if len(arrivals)==0:
        messagebox.showwarning("No Data","No arrivals loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save Arrivals",defaultextension=".txt")
    if filename:
        SaveFlights(arrivals,filename)
        text_area.insert(tk.END,f"Arrivals saved to {filename}\n")
    text_area.see(tk.END)
    return

def GraphAirlines():    #Function to graph how many arrivals each airline has
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    if len(arrivals)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return

    PlotAirlines(arrivals)
    return

def GraphFlightType():    #Function to create a graph of Schengen vs Non-Schengen arrivals
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    elif len(arrivals)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    elif airports[0].sche==None:
        messagebox.showwarning("Input Error","No Schengen stablished.")
    else:
        PlotFlightsType(arrivals)
    return

def GraphArrivals():    #Function to show how many arrivals there are per hour
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    elif len(arrivals)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    elif airports[0].sche==None:
        messagebox.showwarning("Input Error","No Schengen stablished.")
    else:
        PlotArrivals(arrivals)
    return

def ShowMapRoute():  #Function to create the code for the Google Earth to place all the flight routes
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    if len(arrivals)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save the route",defaultextension=".kml")
    MapFlights(arrivals,airports,filename)
    text_area.insert(tk.END, f"{filename} generated. Open it in Google Earth.\n")
    text_area.see(tk.END)
    return

def ShowMapLongDistance():  #Function to create the code for the Google Earth to place all the long distance flights
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    if len(arrivals)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save long distance",defaultextension=".kml")
    LongDistanceArrivals(arrivals,airports,filename)
    text_area.insert(tk.END, f"{filename} generated. Open it in Google Earth.\n")
    text_area.see(tk.END)
    return

#---LEBL SECTION---
terminals_file=None  #We put the terminals file as None so the default state is without any information, and we can add whatever file we want
gate_info=[] #We put the gate information as a list, just like it was in the LEBL
bcn=[]
map=None

def LoadTerminals():    #Function to load the terminals
    global terminals_file, gate_info, bcn
    filename=filedialog.askopenfilename(title="Select terminal file")
    if filename:
        bcn=LoadAirportStructure(filename)
        gate_info=GateOccupancy(bcn)
        terminals_file=filename
        text_area.insert(tk.END, f"Loaded terminals from {filename}\n")
    text_area.see(tk.END)
    return

def AssignGates():  #Function to automatically assign gates to all incoming flights (regardless of their departure time)
    global gate_info, bcn, merged, map
    try:
        if len(gate_info)==0:
            messagebox.showwarning("No Data","No terminals loaded.")
            return
        elif airports[0].sche==None:
            messagebox.showwarning("No Data","No Schengen value established.")
            return
        elif len(merged)==0:
            messagebox.showwarning("No Data","No arrivals and/or departures loaded.")
            return
        i=0
        while i<len(arrivals):
            AssignGate(bcn,arrivals[i])
            i=i+1
        gate_info=GateOccupancy(bcn)
        text_area.insert(tk.END,"Updated Gates occupancy.\n")
        text_area.see(tk.END)
        if 'map' in globals() and map and tk.Toplevel.winfo_exists(map.root):
            map.ChangeTerminals(map.updated)
    except ValueError:
        return
    return

def FreeGates(principal):   #Function to free a gate by typing the id of the aircraft there's in it
    global gate_info, bcn, merged, map
    if len(gate_info) == 0:
        messagebox.showwarning("No Data", "No terminals loaded.")
        return
    elif airports[0].sche == None:
        messagebox.showwarning("No Data", "No Schengen value established.")
        return
    elif len(merged) == 0:
        messagebox.showwarning("No Data", "No arrivals and/or departures loaded.")
        return
    def FreeAction():   #Function that actually does that and automatically refreshes the map
        global bcn, gate_info, map
        aircraft_target=id_entry.get().strip()
        if not aircraft_target:
            messagebox.showwarning("Warning", "Please enter a gate name.")
            return
        try:
            found=FreeGate(bcn, aircraft_target)
            if found == False:
                messagebox.showwarning("No Data", f"Aircraft [{aircraft_target}] is not in any gate.")
            else:
                text_area.insert(tk.END, f"Aircraft [{aircraft_target}] has been successfully freed from its gate.\n")
                text_area.see(tk.END)
                if 'map' in globals() and map and map.root.winfo_exists():
                    map.ChangeTerminals(map.updated)
            add_window.destroy()
        except ValueError:
            return
    text_area.see(tk.END)
    #We decorate the interface
    add_window = tk.Toplevel(principal, padx=30, pady=30, bg="#f0f3f5")
    add_window.title("Free Gate")
    #main interface
    main_frame = tk.Frame(add_window, bg="#f0f3f5")
    main_frame.pack(expand=True)
    #repetitive style
    lbl_style = {"bg": "#f0f3f5", "font": ("Segoe UI", 10)}
    entry_style = {"font": ("Segoe UI", 10), "justify": "center"}
    #input of information
    tk.Label(main_frame, text="Enter the aircraft id you want to free", **lbl_style).pack()
    id_entry = tk.Entry(main_frame, **entry_style)
    id_entry.pack(pady=(0, 20))
    id_entry.focus_set()
    #the button
    tk.Button(main_frame, text="Free aircraft", command=FreeAction, **popup_button_style).pack()
    #center at the start
    CenterWindow(add_window)
    return

def InterfaceAssignAtTime():    #Function to assign gates/look at gates at a specific time
    global secondary, bcn, merged, terminals_file
    if len(merged) == 0:
        messagebox.showwarning("No Data", "No arrivals and/or departures loaded.")
        return
    elif len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    elif airports[0].sche==None:
        messagebox.showwarning("No Data", "No Schengen value established.")
        return
    elif terminals_file==None:
        messagebox.showwarning("No Data", "No terminals loaded.")
        return
    time_window = tk.Toplevel(secondary, padx=20, pady=20, bg="#f0f3f5")
    time_window.title("Assign Gates at Time")
    time_window.transient(secondary)
    time_window.wm_attributes("-topmost", True)
    tk.Label(time_window, text="Select Simulation Hour:", font=("Segoe UI", 10, "bold"), bg="#f0f3f5").pack(pady=5)
    hours_options = []
    i = 0
    while i < 24:
        if i < 10:
            hours_options.append("0" + str(i) + ":00")
        else:
            hours_options.append(str(i) + ":00")
        i += 1
    main_time_combo = ttk.Combobox(time_window, values=hours_options, state="readonly", width=10, font=("Segoe UI", 10))
    main_time_combo.set("00:00")
    main_time_combo.pack(pady=10)
    def RunSimulation():    #Function that actually does that and automatically refreshes the map
        global bcn, merged, gate_info
        selected_time = main_time_combo.get()
        gateless=AssignGatesAtTime(bcn, merged, selected_time)
        gate_info=GateOccupancy(bcn)
        text_area.insert(tk.END, f"Gates have been updated to [{selected_time}].\nThere are {gateless} aircrafts waiting for an available gate.\n")
        text_area.see(tk.END)
        if 'map' in globals() and map and tk.Toplevel.winfo_exists(map.root):
            map.ChangeTerminals(map.updated)
        time_window.destroy()
        return
    tk.Button(time_window, text="Simulate Hour", command=RunSimulation, **popup_button_style).pack(pady=5)
    time_window.after(10, lambda: CenterWindow(time_window))
    return

def ShowGateInfo(): #Function to show all the information of the gates that has currently been updated
    if len(merged)==0:
        messagebox.showwarning("No Data","No arrivals and/or departures loaded.")
        return
    if len(gate_info)==None:
        messagebox.showwarning("No Data", "No terminals loaded.")
        return
    text_area.insert(tk.END,"---Gate Information---\n")
    i=0
    while i<len(gate_info):
        info=PrintGateInfo(gate_info[i])
        text_area.insert(tk.END,info)
        i=i+1
    text_area.see(tk.END)
    return

def GraphDayOccupancy():    #Function to show first the graph of occupancy during the day and then how many aircraft didn't get sorted (all by hour)
    global merged, bcn
    if len(merged) == 0:
        messagebox.showwarning("No Data", "No arrivals and/or departures loaded.")
        return
    PlotDayOccupancy(bcn, merged)
    return

#---EXTRA CONTENT: VISUALIZATION OF THE GATES---
class AirportVisualizer:
    def __init__(self, airport=None):
        self.root = tk.Toplevel()
        self.root.title("Map of the occupancy") #Title of the window
        self.root.geometry("1100x750")  #Dimensions of the window
        self.root.configure(bg="#f4f7f9")   #Background color
        self.airport=airport
        self.updated=0
        #Selection of terminal (frame and buttons)
        control_frame=tk.Frame(self.root, bg="#f4f7f9")
        control_frame.pack(fill=tk.X, padx=15, pady=10)
        tk.Label(control_frame, text="Select Terminal:", font=("Helvetica", 11, "bold"), bg="#f4f7f9", fg="#34495e").pack(side=tk.LEFT, padx=5)
        #While to specifically create buttons depending on the terminals that are in the files
        if self.airport!=ValueError and self.airport.list_terminal:
            terminals=self.airport.list_terminal
            i=0
            while i<len(terminals):
                btn=tk.Button(control_frame,text="Terminal "+str(terminals[i].name),font=("Helvetica", 10, "bold"),bg="#34495e", fg="white", activebackground="#2c3e50", activeforeground="white",relief="flat", padx=10, pady=4,command=lambda i=i: self.ChangeTerminals(i))
                btn.pack(side=tk.LEFT, padx=5)
                i=i+1
        #Main frame for the map of the gates with scrollbars
        time_frame = tk.Frame(control_frame, bg="#f4f7f9")
        time_frame.pack(side=tk.RIGHT, padx=10)
        tk.Label(time_frame, text="Select Hour:", font=("Helvetica", 11, "bold"), bg="#f4f7f9", fg="#34495e").pack(side=tk.LEFT, padx=5)
        hour_options=[]
        i=0
        while i<24:
            hour_options.append(f"{i:02d}:00")
            i+=1
        self.time_combo = ttk.Combobox(time_frame, values=hour_options, state="readonly", width=8,font=("Helvetica", 10))
        self.time_combo.set("00:00")
        self.time_combo.pack(side=tk.LEFT, padx=5)
        self.time_combo.bind("<<ComboboxSelected>>", self.ChangeHour)
        main_frame=ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas=tk.Canvas(main_frame, bg="#f4f7f9", highlightthickness=0)
        scroll_y=ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        scroll_x=ttk.Scrollbar(main_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.content_frame=tk.Frame(self.canvas, bg="#f4f7f9")
        self.canvas_window=self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.canvas.bind("<Configure>", self.Resize)   #Detects the dimensions of the window to resize itself if needed with the Resize function
        self.Drawing()
        CenterWindow(self.root)

    def Resize(self, click):    #Function to adjust the information according to the size of the window
        self.content_frame.update_idletasks()
        width=self.content_frame.winfo_reqwidth()
        height=self.content_frame.winfo_reqheight()
        final_width=__builtins__.max(click.width,width)
        final_height=__builtins__.max(click.height,height)
        self.canvas.itemconfig(self.canvas_window, width=final_width, height=final_height)
        self.canvas.config(scrollregion=(0, 0, width, height))
        self.root.lift()
        return

    def ChangeTerminals(self,n):    #Function to make a button of a terminal depending on the terminals that have been found on the files
        self.updated=n
        list_widgets = self.content_frame.winfo_children()
        i=0
        while i<len(list_widgets):
            list_widgets[i].destroy()
            i=i+1
        self.Drawing()  #Calling the function to "re-draw" itself, but changing the drawing
        return

    def ChangeHour(self, event):    #Function to change the hour in the map (which automatically updates it)
        global merged 
        selected_time = self.time_combo.get()
        AssignGatesAtTime(self.airport, merged, selected_time)
        list_widgets = self.content_frame.winfo_children()
        i=0
        while i<len(list_widgets):
            list_widgets[i].destroy()
            i=i+1
        self.Drawing()  #Calling the function to "re-draw" itself so it updates
        return

    def Drawing(self):  #Function that actually creates the drawing of the gates
        terminal = self.airport.list_terminal[self.updated] #The terminal (if it's T1 or T2)
        header=tk.Frame(self.content_frame, bg="#2c3e50", height=50)
        header.pack(fill=tk.X, padx=15, pady=15)
        tk.Label(header, text="TERMINAL "+ str(terminal.name),fg="white", bg="#2c3e50", font=("Helvetica", 14, "bold")).pack(pady=10)
        #The drawing space
        areas_frame=tk.Frame(self.content_frame, bg="#f4f7f9")
        areas_frame.pack(padx=20, pady=10)
        i=0
        while i<len(terminal.list_obj): #We look at how many gates we have 
            #Area
            area_container=tk.Frame(areas_frame, bg="#ffffff", bd=1, relief="flat", padx=15)
            area_container.pack(side=tk.LEFT, anchor="n", padx=10)
            tk.Label(area_container, text=terminal.list_obj[i].name, font=("Helvetica", 11, "bold"),bg="#ffffff", fg="#34495e").pack(pady=10)   #The area with its name (ex. A)
            gate_canvas=tk.Canvas(area_container, width=190, bg="#ffffff", highlightthickness=0)
            gate_canvas.pack()
            y=30    #Parameter to be able to put the gates at different heights in the line of the area
            #Gates
            gates=terminal.list_obj[i].gate_list
            j=0
            while j<len(gates):
                if gates[j].occupancy==True:    #If the gate is occupied it's red
                    text_display=gates[j].aircraft
                    color = "#d9534f"
                else:   #If it's free it's green
                    text_display=gates[j].name
                    color="#5cb85c"
                if j%2==0:  #If the gate is an even number it goes to the right
                    gate_canvas.create_line(80, y, 55, y, fill="#2c3e50", width=2)
                    gate_canvas.create_rectangle(15, y - 12, 75, y + 12, fill=color, outline="#2c3e50")
                    gate_canvas.create_text(45, y, text=text_display, font=("Helvetica", 8, "bold"), fill="white")
                else:  #If the gate is an odd number it goes to the left
                    gate_canvas.create_line(110,y,135,y,fill="#2c3e50",width=2)
                    gate_canvas.create_rectangle(115,y-12,175,y+12,fill=color,outline="#2c3e50")
                    gate_canvas.create_text(145,y,text=text_display,font=("Helvetica",8,"bold"),fill="white")
                    y=y+45
                j=j+1
            gate_canvas.create_rectangle(80, 0, 110, y, fill="#2c3e50", outline="")
            gate_canvas.config(height=y+40)
            i=i+1
        self.root.update_idletasks()
        width=self.content_frame.winfo_reqwidth()
        height=self.content_frame.winfo_reqheight()
        self.canvas.config(scrollregion=(0, 0,width,height))
        return

def OpenOccupancyMap(): #Function to actually call the whole AirportVisualizer class to open the map
    global bcn, map
    if len(gate_info)==0:
        messagebox.showwarning("No Data", "No terminals loaded.")
        return
    try:
        map=AirportVisualizer(bcn)
    except:
        messagebox.showwarning("Error","Couldn't load the map.")
    return

#---INTERFACE AESTHETICS---
def CenterWindow(window):   #Function to ensure that all the pop-up (and main interface) are come in the center of the screen
    window.update_idletasks()
    width=window.winfo_width()
    height=window.winfo_height()
    x=(window.winfo_screenwidth()//2)-(width//2)
    y=(window.winfo_screenheight()//2)-(height//2)
    window.geometry(f'{width}x{height}+{x}+{y}')
    return

text_area=None  #We start with an empty text interface
button = {"bg": "#2c3e50","fg": "#f0f3f5","font":("Segoe UI", 10, "bold"),"relief": "flat","padx": 10,"pady": 5,"width": 30,"cursor": "hand2"}

def Main(): #All the buttons, text area and details of the main interface
    global text_area, secondary
    #Title
    secondary=tk.Tk()
    secondary.title("LEBL - Flight Control System")
    secondary.geometry("1100x850")
    secondary.configure(bg="#f4f7f9")
    #Colors
    main_color="#2c3e50"
    icon_color="#ecf0f1"
    hover_color="#496785"
    #Buttons from the small menu
    menus={
        "Load":[("Load Airports", LoadAirports), ("Load Arrivals", LoadArrival),("Load Departures", LoadDeparture), ("Load Terminals", LoadTerminals)],
        "Save":[("Save Schengen to File", SaveSchengen), ("Save Arrivals to File", SaveArrivals)],
        "Modify":[("Add Airport", lambda: AddNewAirport(secondary)),("Delete Airport", lambda: DeleteAirport(secondary))],
        "Show":[("Airport Data", ShowAirports), ("Arrivals Data", ShowArrivals),("Departures Data", ShowDepartures)],
        "Dynamic": [("Assign Gates at Time", InterfaceAssignAtTime),("Gate Information", ShowGateInfo),("Free Gate",lambda: FreeGates(secondary))],
        "Plots":[("Schengen/Type", GraphAirports), ("Airlines' arrivals Stats", GraphAirlines), ("Arrivals Stats", GraphFlightType),("Arrivals per Hour", GraphArrivals),("Occupancy and Unassigned aircrafts during the day",GraphDayOccupancy)],
        "Earth":[("Show Airports", ShowMap), ("Show Routes", ShowMapRoute),("Show long distance Routes", ShowMapLongDistance)],
        "Terminal":[("Airport Map", OpenOccupancyMap)],}

    def OpenMenu(click, category):  #Function to open the small "menu" when clicking the icons
        if secondary=="active" and secondary.active.winfo_exists():    #It destroys the small pop-up if it previously existed (so that you can only open one at a time)
            secondary.active.destroy()
        #The pop-up
        menu_popup=tk.Toplevel(secondary)
        menu_popup.overrideredirect(True)  #We delete the borders
        secondary.active=menu_popup
        x=secondary.winfo_rootx()+60
        y=click.y_root-10
        menu_popup.geometry(f"+{x}+{y}")
        #Format of information inside
        btn_style={"bg": "#2c3e50","fg": "#ecf0f1","activebackground": hover_color,"activeforeground": "white","font": ("Segoe UI", 10),"anchor": "w","bd": 0,"padx": 20,"pady": 10,"cursor": "hand2"}
        options = menus.get(category, [])    #Creates the options depending on the information provided (so it's easier to add/delete buttons)
        i=0
        while i<len(options):
            info=options[i]
            btn=tk.Button(menu_popup, text=info[0],command=lambda f=info[1]: [f(),menu_popup.destroy()],**btn_style)
            btn.pack(fill="x")
            i=i+1

        def Close(e):   #Function to automatically close the pop-up if clicked outside of it
            try:
                if menu_popup.winfo_exists():
                    x,y=secondary.winfo_pointerxy()
                    widget=secondary.winfo_containing(x,y)
                    if widget==None or str(widget).find(str(menu_popup))==-1:   #It indicates clicking outside the pop-up
                        menu_popup.destroy()
                        secondary.unbind_all("<Button-1>")
            except:
                return
        secondary.after(100, lambda: secondary.bind_all("<Button-1>", Close))   #Small delay so it doesn't close instantly
        return
    #Actual design (aesthetically speaking)
    #Header
    header=tk.Frame(secondary, bg=main_color, height=50)
    header.pack(side="top", fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="☰", font=("Arial", 18), bg=main_color, fg=icon_color).pack(side="left", padx=15)
    tk.Label(header, text="LEBL FLIGHT CONTROL SYSTEM", font=("Segoe UI", 12, "bold"),bg=main_color, fg=icon_color).pack(expand=True)
    #Bar with the icons
    main_container=tk.Frame(secondary, bg="#f4f7f9")
    main_container.pack(fill="both", expand=True)
    sidebar=tk.Frame(main_container, bg=main_color, width=60)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    #Terminal (where the information appears), clear button and scrollbar
    display_frame = tk.Frame(main_container, bg="#f4f7f9", padx=25, pady=25)
    display_frame.pack(side="right", fill="both", expand=True)
    title_bar = tk.Frame(display_frame, bg="#f4f7f9")
    title_bar.pack(fill="x", pady=(0, 5))
    tk.Label(title_bar, text="TERMINAL OUTPUT", font=("Segoe UI", 8, "bold"), fg="#adb5bd", bg="#f4f7f9").pack(side="left")
    tk.Button(title_bar, text="CLEAR TERMINAL 🗑️", font=("Segoe UI", 7, "bold"), fg="#d9534f", bg="#f4f7f9", bd=0,command=lambda: text_area.delete('1.0', tk.END)).pack(side="right")
    center_bar = tk.Frame(title_bar, bg="#f4f7f9")
    center_bar.pack(side="left", expand=True)
    tk.Button(center_bar, text="⚡ Set Schengen", font=("Segoe UI", 9, "bold"),fg="#2c3e50", bg="#f4f7f9", bd=0, cursor="hand2",command=SetNewSchengen).pack(side="left", padx=10)
    tk.Button(center_bar, text="✈️ Set Gates", font=("Segoe UI", 9, "bold"),fg="#2c3e50", bg="#f4f7f9", bd=0, cursor="hand2",command=AssignGates).pack(side="left", padx=10)
    text_container = tk.Frame(display_frame, bg="white", highlightthickness=1, highlightbackground="#d1d9e0")
    text_container.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(text_container)
    scrollbar.pack(side="right", fill="y")
    text_area = tk.Text(text_container, font=("Consolas", 11), bg="white", fg=main_color,relief="flat", padx=15, pady=15, yscrollcommand=scrollbar.set)
    text_area.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text_area.yview)
    #The actual buttons
    icons = [("📁", "Load"), ("💾", "Save"), ("⌨", "Modify"), ("🔎", "Show"), ("✎", "Dynamic"), ("📊", "Plots"), ("🌍", "Earth"), ("🏢", "Terminal")]
    i=0
    while i<len(icons): #Putting the icons in the sidebar
        icon_text=icons[i]
        f=tk.Frame(sidebar,bg=main_color)
        f.pack(side="top",fill="both",expand=True)
        lbl = tk.Label(f,text=icon_text[0],bg=main_color,fg=icon_color,font=("Segoe UI Symbol", 18),cursor="hand2")
        lbl.place(relx=0.5, rely=0.5, anchor="center")
        lbl.bind("<Button-1>", lambda e, c=icon_text[1]: OpenMenu(e, c))
        i=i+1
    CenterWindow(secondary)
    secondary.mainloop()
    return

if __name__ == "__main__":
    Main()