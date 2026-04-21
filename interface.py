from airport import *
from aircraft import *
import tkinter as tk
from tkinter import filedialog, messagebox

#---AIRPORT SECTION---
airports_file=None  #We put the airport file as None so the default state is without any information, and we can add whatever file we want
airports=[] #We put the airports as a list, just like it was in the airport
#important button for aesthetics in the pop-ups
popup_button_style = {"bg": "#2c3e50","fg": "white","activebackground": "#34495e","activeforeground": "white","font": ("Segoe UI", 10, "bold"),"relief": "flat","width": 15,"cursor": "hand2"}
def LoadAirports(): #Function to ask for the file to load the airports we have available
    text_area.delete('1.0', tk.END)
    global airports,airports_file
    filename=filedialog.askopenfilename(title="Select airports file")   #Similar to putting a variable=input(), we ask for the file, but searching in our files
    if filename:
        airports=LoadAirport(filename)  #We call the LoadAirport from the airport to give us the list we knew (and still know here) as airports
        airports_file=filename  #We clarify, globally, that now there's a file for the airports
        text_area.insert(tk.END, f"Loaded {len(airports)} airports from {filename}\n")
    return

def AddNewAirport(principal): #Function to have the button to ask to add a new airport
    text_area.delete('1.0', tk.END)
    if len(airports)==0:
        messagebox.showwarning("No Data","No airports loaded.")
        return
    def AddAction():    #Function to actually do the work of adding the new airport
        global airports,airports_file
        #We establish the code, latitude and longitude by input, and we make sure to leave out unnecessary data (ex. extra spaces at the end) with .strip()
        code=code_entry.get().strip()
        lat=lat_entry.get().strip()
        lon=lon_entry.get().strip()
        try:
            if len(list(code))!=4:
                messagebox.showwarning("Input Error","Incorrect ICAO code.")
            elif code and lat and lon:
                airport=Airport(code,float(lat),float(lon))
                airports=AddAirport(LoadAirport(airports_file),airport)  #We call the AddAirport from the airport to add it
                text_area.insert(tk.END,f"Added airport {code}\n")
                add_window.destroy()
            else:   #If we don't have all the information we asked for we pop up an error message
                messagebox.showwarning("Input Error","All fields are required.")
        except ValueError:  #In case of an error in the values (like inputting letters in tha latitude or longitude) show an error message
            messagebox.showwarning("Input Error","Incorrect latitude and/or longitude.")
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
    text_area.delete('1.0', tk.END)
    if len(airports)==0:
        messagebox.showwarning("No Data","No airports loaded.")
        return
    def DeleteAction(): #Function to actually do the work of deleting the airport
        global airports,airports_file
        original_lenght=len(airports)
        code=code_entry.get().strip()
        if len(list(code))!=4:
            messagebox.showwarning("Input Error","Incorrect ICAO code.")
        elif code:
            airports=RemoveAirport(LoadAirport(airports_file),code)   #We call the AddAirport from the airport to remove it
            if len(airports)==original_lenght:
                messagebox.showwarning("Input Error", "That airport doesn't exist.")
            else:
                text_area.insert(tk.END,f"Deleted airport {code}\n")
            del_window.destroy()
        else:
            messagebox.showwarning("Input Error","ICAO code required.")
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
    text_area.delete('1.0', tk.END)
    global airports
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    i=0
    while i<len(airports):
        airports[i].sche=SetSchengen(airports[i])    #We call the SetSchengen from the airport to look if the airport is or isn't Schengen
        i=i+1
    text_area.insert(tk.END,"Updated Schengen attribute for all airports.\n")
    return airports

def ShowAirports(): #Function to show all the current information from all the current airports in the list
    text_area.delete('1.0', tk.END)
    if len(airports)==0:
        messagebox.showwarning("No Data","No airports loaded.")
        return
    text_area.insert(tk.END,"---Airports---\n")
    i=0
    while i<len(airports):
        info=PrintAirport(airports[i])
        text_area.insert(tk.END,info)
        i=i+1
    return

def SaveSchengen(): #Function to save all the Schengen airports into a separate file of our choice
    text_area.delete('1.0', tk.END)
    if len(airports)==0:
        messagebox.showwarning("No Data","No airports loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save Schengen Airports",defaultextension=".txt")
    if filename:
        SaveSchengenAirports(airports,filename) #We call the SaveSchengenAirports from the airport to create and fill the new file
        text_area.insert(tk.END,f"Schengen airports saved to {filename}\n")
    return

def GraphAirports():    #Function to ask for the plot to create a graph of Schengen vs Non-Schengen airports
    if airports[0].sche==None:
        messagebox.showwarning("Input Error","No Schengen stablished.")
    else:
        if len(airports)==0:
            messagebox.showwarning("No Data", "No airports loaded.")
            return
        PlotAirports(airports)  #We call the PlotAirports from the airport to do the graph
    return

def ShowMap():  #Function to create the code for the Google Earth to place all the airports
    text_area.delete('1.0', tk.END)
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save the airports",defaultextension=".kml")
    MapAirports(airports,filename)  #We call the PlotAirports from the airport to do the graph
    text_area.insert(tk.END, f"{filename} generated. Open it in Google Earth.\n")
    return

#---AIRPORT SECTION---
aircrafts_file=None  #We put the aircrafts file as None so the default state is without any information, and we can add whatever file we want
aircrafts=[] #We put the airports as a list, just like it was in the aircrafts

def LoadAricrafts():
    text_area.delete('1.0', tk.END)
    global aircrafts,aircrafts_file
    filename=filedialog.askopenfilename(title="Select airports file")  # Similar to putting a variable=input(), we ask for the file, but searching in our files
    if filename:
        aircrafts=LoadArrivals(filename)  # We call the LoadAirport from the airport to give us the list we knew (and still know here) as airports
        aircrafts_file=filename  # We clarify, globally, that now there's a file for the airports
        text_area.insert(tk.END, f"Loaded {len(aircrafts)} airports from {filename}\n")
    return

def ShowAircrafts(): #Function to show all the current information from all the current airports in the list
    text_area.delete('1.0', tk.END)
    if len(aircrafts)==0:
        messagebox.showwarning("No Data","No aircrafts loaded.")
        return
    text_area.insert(tk.END,"---Aircrafts---\n")
    i=0
    while i<len(aircrafts):
        info=PrintAircrafts(aircrafts[i])
        text_area.insert(tk.END,info)
        i=i+1
    return

def SaveArrivals(): #Function to save all the Schengen airports into a separate file of our choice
    text_area.delete('1.0', tk.END)
    if len(aircrafts)==0:
        messagebox.showwarning("No Data","No arrivals loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save Arrivals",defaultextension=".txt")
    if filename:
        SaveFlights(aircrafts,filename) #We call the SaveSchengenAirports from the airport to create and fill the new file
        text_area.insert(tk.END,f"Arrivals saved to {filename}\n")
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
    if airports[0].sche==None:
        messagebox.showwarning("Input Error","No Schengen stablished.")
    else:
        if len(airports)==0:
            messagebox.showwarning("No Data", "No airports loaded.")
            return
        if len(aircrafts) == 0:
            messagebox.showwarning("No Data", "No arrivals loaded.")
            return
        PlotFlightsType(aircrafts)  #We call the PlotFlightsType from the airport to do the graph
    return

def ShowMapRoute():  #Function to create the code for the Google Earth to place all the flight routes
    text_area.delete('1.0', tk.END)
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save the route",defaultextension=".kml")
    MapFlights(aircrafts,airports,filename)  #We call the PlotAirports from the airport to do the graph
    text_area.insert(tk.END, f"{filename} generated. Open it in Google Earth.\n")
    return

def ShowMapLongDistance():  #Function to create the code for the Google Earth to place all the long distance flights
    text_area.delete('1.0', tk.END)
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save long distance",defaultextension=".kml")
    LongDistanceArrivals(aircrafts,airports,filename)  #We call the PlotAirports from the airport to do the graph
    text_area.insert(tk.END, f"{filename} generated. Open it in Google Earth.\n")
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
    tk.Label(menu_frame, text="EDIT DATA", font=("Segoe UI", 9, "bold"), bg="#f0f3f5", fg="#7f8c8d").pack(anchor="w",pady=(10, 0))
    tk.Button(menu_frame, text="➕ Add Airport", command=lambda: AddNewAirport(secondary), **button).pack(pady=5)
    tk.Button(menu_frame, text="🗑️ Delete Airport", command=lambda: DeleteAirport(secondary), **button).pack(pady=5)
    tk.Button(menu_frame, text="✈️ Set Schengen Attribute", command=SetNewSchengen, **button).pack(pady=5)
    tk.Label(menu_frame, text="VIEW & SAVE", font=("Segoe UI", 9, "bold"), bg="#f0f3f5", fg="#7f8c8d").pack(anchor="w",pady=(10, 0))
    tk.Button(menu_frame, text="📑 Show Airport Data", command=ShowAirports, **button).pack(pady=5)
    tk.Button(menu_frame, text="📑 Show Arrivals Data", command=ShowAircrafts, **button).pack(pady=5)
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