from airport import *
from aircraft import *
import tkinter as tk
from tkinter import filedialog, messagebox

#---AIRPORT SECTION---
airports_file=None  #We put the airport file as None so the default state is without any information, and we can add whatever file we want
airports=[] #We put the airports as a list, just like it was in the airport

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
    add_window=tk.Toplevel(principal,padx=20,pady=20)
    add_window.title("Add Airport")
    tk.Label(add_window,text="ICAO Code:").grid(row=0,column=0)
    code_entry=tk.Entry(add_window)
    code_entry.grid(row=0,column=1,pady=2)
    tk.Label(add_window,text="Latitude:").grid(row=1,column=0)
    lat_entry=tk.Entry(add_window)
    lat_entry.grid(row=1,column=1,pady=2)
    tk.Label(add_window,text="Longitude:").grid(row=2,column=0)
    lon_entry=tk.Entry(add_window)
    lon_entry.grid(row=2,column=1,pady=2)
    tk.Button(add_window,text="Add",command=AddAction).grid(row=3,column=0,columnspan=2,pady=10) #Button that call the function to try and add the airport
    return

def DeleteAirport(principal):   #Function to have the button to ask to delete an airport
    text_area.delete('1.0', tk.END)
    if len(airports)==0:
        messagebox.showwarning("No Data","No airports loaded.")
        return
    def DeleteAction(): #Function to actually do the work of deleting the airport
        global airports,airports_file
        code=code_entry.get().strip()
        if len(list(code))!=4:
            messagebox.showwarning("Input Error","Incorrect ICAO code.")
        elif code:
            airports=RemoveAirport(LoadAirport(airports_file),code)   #We call the AddAirport from the airport to remove it
            text_area.insert(tk.END,f"Deleted airport {code}\n")
            del_window.destroy()
        else:
            messagebox.showwarning("Input Error","ICAO code required.")
    #We decorate the interface
    del_window = tk.Toplevel(principal,padx=20,pady=20)
    del_window.title("Delete Airport")
    tk.Label(del_window,text="ICAO Code:").grid(row=0,column=0)
    code_entry = tk.Entry(del_window)
    code_entry.grid(row=0,column=1,pady=2)
    tk.Button(del_window,text="Delete",command=DeleteAction).grid(row=1,column=0,columnspan=2,pady=10)
    return

def SetNewSchengen():   #Function to make the current airports get their Schengen/Non-Schengen information
    text_area.delete('1.0', tk.END)
    global airports
    if len(airports)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    i=0
    while i<len(airports):
        SetSchengen(airports[i])    #We call the SetSchengen from the airport to look if the airport is or isn't Schengen
        i=i+1
    text_area.insert(tk.END,"Updated Schengen attribute for all airports.\n")
    return

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
    if len(aircrafts) == 0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    PlotFlightsType(aircrafts)  #We call the PlotFlightsType from the airport to do the graph
    return

def ShowMapRoute():  #Function to create the code for the Google Earth to place all the airports
    text_area.delete('1.0', tk.END)
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save the route",defaultextension=".kml")
    MapFlights(aircrafts,filename)  #We call the PlotAirports from the airport to do the graph
    text_area.insert(tk.END, f"{filename} generated. Open it in Google Earth.\n")
    return

def ShowMapLongDistance():  #Function to create the code for the Google Earth to place all the airports
    text_area.delete('1.0', tk.END)
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No airports loaded.")
        return
    if len(aircrafts)==0:
        messagebox.showwarning("No Data", "No arrivals loaded.")
        return
    filename=filedialog.asksaveasfilename(title="Save long distance",defaultextension=".kml")
    LongDistanceArrivals(aircrafts,filename)  #We call the PlotAirports from the airport to do the graph
    text_area.insert(tk.END, f"{filename} generated. Open it in Google Earth.\n")
    return

#---INTERFACE AESTHETICS---
text_area=None  # We start with an empty text interface
button={"width":25,"pady":5}

def Main(): #The main page where we see all the buttons and possibilities
    global text_area,button
    secondary=tk.Tk()
    secondary.title("Airport Manager")
    secondary.geometry("1000x800")
    #We decorate the interface
    #Main menu to the left
    menu_frame=tk.Frame(secondary,padx=20,pady=20)
    menu_frame.pack(side="left",fill="x")
    #The buttons
    tk.Button(menu_frame,text="📂 Load Airports",command=LoadAirports,**button).pack(pady=5)
    tk.Button(menu_frame, text="📂 Load Arrivals", command=LoadAricrafts, **button).pack(pady=5)
    tk.Button(menu_frame,text="➕ Add Airport",command=lambda: AddNewAirport(secondary),**button).pack(pady=5)
    tk.Button(menu_frame,text="🗑️ Delete Airport",command=lambda: DeleteAirport(secondary),**button).pack(pady=5)
    tk.Button(menu_frame,text="✈️ Set Schengen Attribute",command=SetNewSchengen,**button).pack(pady=5)
    tk.Button(menu_frame,text="📑 Show Airport Data",command=ShowAirports,**button).pack(pady=5)
    tk.Button(menu_frame, text="📑 Show Arrivals Data", command=ShowAircrafts, **button).pack(pady=5)
    tk.Button(menu_frame,text="💾 Save Schengen Airports to File",command=SaveSchengen,**button).pack(pady=5)
    tk.Button(menu_frame,text="📈 Plot Schengen/No Schengen",command=GraphAirports,**button).pack(pady=5)
    tk.Button(menu_frame, text="📈 Plot Airlines' flights", command=GraphAirlines, **button).pack(pady=5)
    tk.Button(menu_frame, text="📈 Plot type of Flight", command=GraphFlightType, **button).pack(pady=5)
    tk.Button(menu_frame,text="📍 Show Airports in Google Earth",command=ShowMap,**button).pack(pady=5)
    tk.Button(menu_frame, text="📍 Show Routes in Google Earth", command=ShowMapRoute, **button).pack(pady=5)
    tk.Button(menu_frame, text="📍 Show Long distance flights in Google Earth", command=ShowMapLongDistance, **button).pack(pady=5)
    #The text area to the right
    display_frame=tk.Frame(secondary,padx=20,pady=20)
    display_frame.pack(side="right",fill="both",expand=True)
    text_area=tk.Text(display_frame,height=15,width=80)
    text_area.pack(fill="both",expand=True)
    secondary.mainloop()
    return

if __name__ == "__main__":
    Main()