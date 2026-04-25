from LEBL import *
from airport import *
from aircraft import *
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

#---AIRPORT SECTION---
airports_file=None  #We put the airport file as None so the default state is without any information, and we can add whatever file we want
airports=[] #We put the airports as a list, just like it was in the airport
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
        #We establish the code, latitude and longitude by input, and we make sure to leave out unnecessary data (ex. extra spaces at the end) with .strip()
        code=code_entry.get().strip()
        lat=lat_entry.get().strip()
        lon=lon_entry.get().strip()
        try:
            if len(list(code))!=4:
                messagebox.showwarning("Input Error","Incorrect ICAO code.")
            elif code and lat and lon:
                airports=AddAirport(airports,Airport(code,float(lat),float(lon)))  #We call the AddAirport from the airport to add it
                if len(airports)==original_length:
                    messagebox.showwarning("Input Error", "That airport already exists.")
                else:
                    text_area.insert(tk.END,f"Added airport {code}\n")
                    add_window.destroy()
            else:   #If we don't have all the information we asked for we pop up an error message
                messagebox.showwarning("Input Error","All fields are required.")
        except ValueError:  #In case of an error in the values (like inputting letters in tha latitude or longitude) show an error message
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
            airports=RemoveAirport(airports,code)   #We call the AddAirport from the airport to remove it
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
    del_window.transient(principal)  # La mantiene vinculada a la principal
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
        airports[i].sche=SetSchengen(airports[i])    #We call the SetSchengen from the airport to look if the airport is or isn't Schengen
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
        SaveSchengenAirports(airports,filename) #We call the SaveSchengenAirports from the airport to create and fill the new file
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
        PlotAirports(airports)  #We call the PlotAirports from the airport to do the graph
    return

def ShowMap():  #Function to create the code for the Google Earth to place all the airports
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save the airports",defaultextension=".kml")
    MapAirports(airports,filename)  #We call the PlotAirports from the airport to do the graph
    text_area.insert(tk.END, f"{filename} generated. Open it in Google Earth.\n")
    text_area.see(tk.END)
    return

#---AIRPORT SECTION---
aircrafts_file=None  #We put the aircrafts file as None so the default state is without any information, and we can add whatever file we want
aircrafts=[] #We put the aircrafts as a list, just like it was in the aircraft

def LoadAricrafts():
    global aircrafts,aircrafts_file
    filename=filedialog.askopenfilename(title="Select airports file")  # Similar to putting a variable=input(), we ask for the file, but searching in our files
    if filename:
        aircrafts=LoadArrivals(filename)  # We call the LoadAirport from the airport to give us the list we knew (and still know here) as airports
        aircrafts_file=filename  # We clarify, globally, that now there's a file for the airports
        text_area.insert(tk.END, f"Loaded {len(aircrafts)} airports from {filename}\n")
    text_area.see(tk.END)
    return

def ShowAircrafts(): #Function to show all the current information from all the current airports in the list
    if len(aircrafts)==0:
        messagebox.showwarning("No Data","No aircrafts loaded.")
        return
    text_area.insert(tk.END,"---Aircrafts---\n")
    i=0
    while i<len(aircrafts):
        info=PrintAircrafts(aircrafts[i])
        text_area.insert(tk.END,info)
        i=i+1
    text_area.see(tk.END)
    return

def SaveArrivals(): #Function to save all the Schengen airports into a separate file of our choice
    if len(aircrafts)==0:
        messagebox.showwarning("No Data","No arrivals loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save Arrivals",defaultextension=".txt")
    if filename:
        SaveFlights(aircrafts,filename) #We call the SaveSchengenAirports from the airport to create and fill the new file
        text_area.insert(tk.END,f"Arrivals saved to {filename}\n")
    text_area.see(tk.END)
    return

def AddNewAircraft(principal): #Function to have the button to ask to add a new airport
    if len(aircrafts)==0:
        messagebox.showwarning("No Data","No aircrafts loaded.")
        return
    def AddAction():
        global aircrafts
        original_length=len(aircrafts)
        id=id_entry.get().strip().upper()
        origin=origin_entry.get().strip().upper()
        landing=landing_entry.get().strip()
        airline=airline_entry.get().strip().upper()
        if len(id)<3:
            messagebox.showwarning("Input Error", "Incorrect ID.")
        elif len(origin)!=4:
            messagebox.showwarning("Input Error", "Origin ICAO must be 4 characters.")
        elif ":" not in landing or len(landing)!=5:
            messagebox.showwarning("Input Error", "Landing time must be HH:MM.")
        elif len(airline)!=3:
            messagebox.showwarning("Input Error", "Airline code must be 3 characters.")
        elif id and origin and landing and airline:
            aircrafts=AddAircraft(aircrafts,Aircraft(id,origin,landing,airline))
            if len(aircrafts)==original_length:
                messagebox.showwarning("Input Error", "That arrival already exists.")
            else:
                text_area.insert(tk.END, f"Added arrival from {origin} at {landing}\n")
                add_window.destroy()
        else:
            messagebox.showwarning("Input Error", "All fields are required.")
    text_area.see(tk.END)
    #We decorate the interface
    add_window = tk.Toplevel(principal, padx=30, pady=30, bg="#f0f3f5")
    add_window.title("Add Arrival")
    #main interface
    main_frame = tk.Frame(add_window, bg="#f0f3f5")
    main_frame.pack(expand=True)
    #repetitive style
    lbl_style = {"bg": "#f0f3f5", "font": ("Segoe UI", 10)}
    entry_style = {"font": ("Segoe UI", 10), "justify": "center"}
    #input of information
    tk.Label(main_frame, text="Aircraft ID (e.g. ECMKV)", **lbl_style).pack()
    id_entry = tk.Entry(main_frame, **entry_style)
    id_entry.pack(pady=(0, 10))
    id_entry.focus_set()
    tk.Label(main_frame, text="Origin ICAO (e.g. LYBE)", **lbl_style).pack()
    origin_entry = tk.Entry(main_frame, **entry_style)
    origin_entry.pack(pady=(0, 10))
    tk.Label(main_frame, text="Landing Time (HH:MM)", **lbl_style).pack()
    landing_entry = tk.Entry(main_frame, **entry_style)
    landing_entry.pack(pady=(0, 10))
    tk.Label(main_frame, text="Airline Code (3 chars)", **lbl_style).pack()
    airline_entry = tk.Entry(main_frame, **entry_style)
    airline_entry.pack(pady=(0, 20))
    #the button
    tk.Button(main_frame, text="Add Aircraft", command=AddAction, **popup_button_style).pack()
    #center at the start
    CenterWindow(add_window)
    return

def DeleteAircraft(principal):   #Function to have the button to ask to delete an airport
    if len(airports)==0:
        messagebox.showwarning("No Data","No airports loaded.")
        return
    def RemoveAction():
        global aircrafts
        original_length=len(aircrafts)
        time= time_entry.get().strip()
        info= info_entry.get().strip().upper()
        if ":" in time and info:
            aircrafts=RemoveAircraft(aircrafts,time,info)
            if len(aircrafts)==original_length:
                messagebox.showwarning("Input Error", "That arrival doesn't exist.")
            else:
                text_area.insert(tk.END, f"Search completed for {time} - {info}\n")
                remove_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please provide Landing Time and one extra info.")
    text_area.see(tk.END)
    #We decorate the interface
    remove_window = tk.Toplevel(principal, padx=30, pady=30, bg="#f0f3f5")
    remove_window.title("Remove Arrival")
    #main interface
    main_frame = tk.Frame(remove_window, bg="#f0f3f5")
    main_frame.pack(expand=True)
    #repetitive style
    lbl_style = {"bg": "#f0f3f5", "font": ("Segoe UI", 10)}
    entry_style = {"font": ("Segoe UI", 10), "justify": "center"}
    #input of information
    tk.Label(main_frame, text="Landing Time (HH:MM)", **lbl_style).pack()
    time_entry = tk.Entry(main_frame, **entry_style)
    time_entry.pack(pady=(0, 10))
    tk.Label(main_frame, text="Extra Info (ID, Origin or Airline)", **lbl_style).pack()
    info_entry = tk.Entry(main_frame, **entry_style)
    info_entry.pack(pady=(0, 20))
    #the button
    tk.Button(main_frame, text="Remove Aircraft", command=RemoveAction, **popup_button_style).pack()
    #center at the start
    CenterWindow(remove_window)
    return

def GraphAirlines():    #Function to ask for the plot to create a graph of Schengen vs Non-Schengen airports
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return

    PlotAirlines(aircrafts)  #We call the PlotAirlines from the airport to do the graph
    return

def GraphFlightType():    #Function to ask for the plot to create a graph of Schengen vs Non-Schengen airports
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    elif len(aircrafts)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    elif airports[0].sche==None:
        messagebox.showwarning("Input Error","No Schengen stablished.")
    else:
        PlotFlightsType(aircrafts)  #We call the PlotFlightsType from the airport to do the graph
    return

def ShowMapRoute():  #Function to create the code for the Google Earth to place all the flight routes
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save the route",defaultextension=".kml")
    MapFlights(aircrafts,airports,filename)  #We call the PlotAirports from the airport to do the graph
    text_area.insert(tk.END, f"{filename} generated. Open it in Google Earth.\n")
    text_area.see(tk.END)
    return

def ShowMapLongDistance():  #Function to create the code for the Google Earth to place all the long distance flights
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save long distance",defaultextension=".kml")
    LongDistanceArrivals(aircrafts,airports,filename)  #We call the PlotAirports from the airport to do the graph
    text_area.insert(tk.END, f"{filename} generated. Open it in Google Earth.\n")
    text_area.see(tk.END)
    return

#---LEBL SECTION---
terminals_file=None  #We put the terminals file as None so the default state is without any information, and we can add whatever file we want
gate_info=[] #We put the gate information as a list, just like it was in the LEBL

def LoadTerminals():
    global terminals_file, gate_info
    filename=filedialog.askopenfilename(title="Select terminal file")  #Similar to putting a variable=input(), we ask for the file, but searching in our files
    if filename:
        gate_info=GateOccupancy(LoadAirportStructure("Terminals.txt"))  #We call the LoadTerminal from the airport to give us the list we knew (and still know here) as airports
        terminals_file=filename  # We clarify, globally, that now there's a file for the airports
        text_area.insert(tk.END, f"Loaded terminals from {filename}\n")
    text_area.see(tk.END)
    return

def ShowGateInfo(): #Function to show all the current information from all the current airports in the list
    if len(gate_info)==0:
        messagebox.showwarning("No Data","No aircrafts loaded.")
        return
    text_area.insert(tk.END,"---Gate Information---\n")
    i=0
    while i<len(gate_info):
        info=PrintGateInfo(gate_info[i])
        text_area.insert(tk.END,info)
        i=i+1
    text_area.see(tk.END)
    return

#---INTERFACE AESTHETICS---
def CenterWindow(window):
    window.update_idletasks()
    width=window.winfo_width()
    height=window.winfo_height()
    x=(window.winfo_screenwidth()//2)-(width//2)
    y=(window.winfo_screenheight()//2)-(height//2)
    window.geometry(f'{width}x{height}+{x}+{y}')
    return

text_area=None  # We start with an empty text interface
button = {"bg": "#2c3e50","fg": "#f0f3f5","font":("Segoe UI", 10, "bold"),"relief": "flat","padx": 10,"pady": 5,"width": 30,"cursor": "hand2"}

def Main():
    global text_area, secondary
    secondary=tk.Tk()
    secondary.title("Airport & Flight Manager")
    secondary.geometry("1100x850")
    secondary.configure(bg="#f0f3f5")
    #header
    header=tk.Label(secondary,text="FLIGHT CONTROL SYSTEM",font=("Segoe UI", 18, "bold"),bg="#2c3e50",fg="white",pady=10)
    header.pack(fill="x")
    #main interface
    main_container = tk.Frame(secondary, bg="#f0f3f5")
    main_container.pack(fill="both", expand=True)
    canvas = tk.Canvas(main_container, bg="#f0f3f5", width=280, highlightthickness=0)
    canvas.pack(side="left", fill="y")
    scroll_v = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scroll_v.pack(side="left", fill="y")
    menu_frame = tk.Frame(canvas, padx=20, pady=20, bg="#f0f3f5")
    #make scroll possible
    canvas.create_window((0, 0), window=menu_frame, anchor="nw")
    menu_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.configure(yscrollcommand=scroll_v.set)
    #buttons
    tk.Label(menu_frame, text="DATABASE", font=("Segoe UI", 9, "bold"), bg="#f0f3f5", fg="#7f8c8d").pack(anchor="w",pady=(10, 0))
    tk.Button(menu_frame, text="📂 Load Airports", command=LoadAirports, **button).pack(pady=5)
    tk.Button(menu_frame, text="📂 Load Arrivals", command=LoadAricrafts, **button).pack(pady=5)
    tk.Button(menu_frame, text="📂 Load Terminals", command=LoadTerminals, **button).pack(pady=5)
    tk.Label(menu_frame, text="EDIT DATA", font=("Segoe UI", 9, "bold"), bg="#f0f3f5", fg="#7f8c8d").pack(anchor="w",pady=(10, 0))
    tk.Button(menu_frame, text="➕ Add Airport", command=lambda: AddNewAirport(secondary), **button).pack(pady=5)
    tk.Button(menu_frame, text="🗑️ Delete Airport", command=lambda: DeleteAirport(secondary), **button).pack(pady=5)
    tk.Button(menu_frame, text="➕ Add Aircraft", command=lambda: AddNewAircraft(secondary), **button).pack(pady=5)
    tk.Button(menu_frame, text="🗑️ Delete Aircraft", command=lambda: DeleteAircraft(secondary), **button).pack(pady=5)
    tk.Button(menu_frame, text="✈️ Set Schengen Attribute", command=SetNewSchengen, **button).pack(pady=5)
    tk.Label(menu_frame, text="VIEW & SAVE", font=("Segoe UI", 9, "bold"), bg="#f0f3f5", fg="#7f8c8d").pack(anchor="w",pady=(10, 0))
    tk.Button(menu_frame, text="📑 Show Airport Data", command=ShowAirports, **button).pack(pady=5)
    tk.Button(menu_frame, text="📑 Show Arrivals Data", command=ShowAircrafts, **button).pack(pady=5)
    tk.Button(menu_frame, text="📑 Show Gate Information", command=ShowGateInfo, **button).pack(pady=5)
    tk.Button(menu_frame, text="💾 Save Schengen to File", command=SaveSchengen, **button).pack(pady=5)
    tk.Button(menu_frame, text="💾 Save Arrivals to File", command=SaveArrivals, **button).pack(pady=5)
    tk.Label(menu_frame, text="ANALYSIS & MAPS", font=("Segoe UI", 9, "bold"), bg="#f0f3f5", fg="#7f8c8d").pack(anchor="w", pady=(10, 0))
    tk.Button(menu_frame, text="📈 Plot Schengen/Type", command=GraphAirports, **button).pack(pady=5)
    tk.Button(menu_frame, text="📈 Plot Airlines' Stats", command=GraphAirlines, **button).pack(pady=5)
    tk.Button(menu_frame, text="📈 Plot Schengen/Type arrivals", command=GraphFlightType, **button).pack(pady=5)
    tk.Button(menu_frame, text="📍 Show Airports", command=ShowMap, **button).pack(pady=5)
    tk.Button(menu_frame, text="📍 Show Routes", command=ShowMapRoute, **button).pack(pady=5)
    tk.Button(menu_frame, text="📍 Show Long Distance Flights", command=ShowMapLongDistance, **button).pack(pady=5)
    #text display
    display_frame = tk.Frame(main_container, padx=20, pady=20, bg="#f0f3f5")
    display_frame.pack(side="right", fill="both", expand=True)
    tk.Label(display_frame, text="Output Terminal", font=("Consolas", 10), bg="#f0f3f5").pack(anchor="w")
    text_area = tk.Text(display_frame, height=15, width=80, font=("Consolas", 10),bg="white", fg="#2c3e50", relief="solid", borderwidth=1)
    text_area.pack(fill="both", expand=True)
    #scrollbar
    scrollbar=tk.Scrollbar(text_area)
    scrollbar.pack(side="right", fill="y")
    text_area.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_area.yview)
    CenterWindow(secondary)
    secondary.mainloop()
    return

if __name__ == "__main__":
    Main()