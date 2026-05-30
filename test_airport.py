from airport import *
list_test = [Airport("LEBL", 41.297, 2.078),Airport("LFPG", 49.009, 2.547),Airport("KJFK", 40.639, -73.778)]
i=0
while i<len(list_test):
    SetSchengen(list_test[i])
    print(PrintAirport(list_test[i]))
    i=i+1
new_airport = Airport("EDDF", 50.033, 8.570)
SetSchengen(new_airport)
AddAirport(list_test, new_airport)
repeated = Airport("LEBL", 41.0, 2.0)
AddAirport(list_test, repeated)
RemoveAirport(list_test, "LEBL")
PlotAirports(list_test)