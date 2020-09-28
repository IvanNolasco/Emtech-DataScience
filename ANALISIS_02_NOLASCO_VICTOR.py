# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 16:14:48 2020

@author: navi_
"""

import csv

""" read the registers from a csv file and save them in a list """
def get_registers(name):
    registers_list = []
    csv_file = open(name, "r")
    registers = csv.reader(csv_file)
    for r in registers:
        registers_list.append(r)
    csv_file.close()
    return registers_list[1:]   # to avoid the first register (headers)



""" create a dictionary with all the diferent routes 
    route = {(origin, destination) : [total_travels, exports, imports]} """
def get_routes(registers):
    routes = {}
    for register in registers:
        # the key is a tuple with the origin and the destination of the route
        key = (register[2], register[3])
        # chek if the route alredy exists in the dictionary
        if key in routes.keys():
            aux_value = routes.get(key)
        else:
            aux_value = [0, 0, 0]
        aux_value[0] += 1
        if register[1] == "Exports":
            aux_value[1] += 1
        else:
            aux_value[2] += 1
        routes[key] = aux_value     #update the value
    return routes



""" create a dictionary with all the transport modes
    transport = {transport_mode: [exports_value, imports_value, total]} """ 
def get_transports(registers):
    transports = {}
    for register in registers:
        # register[7] is the transport mode and will be the key
        mode = register[7]
        # register[9] is the total value of the export or import
        total_value = int(register[9])
        # check if the transport mode already exists in the dictionary 
        if mode in transports.keys():
            aux_value = transports.get(mode)
        else:
            aux_value = [0, 0, 0]
        aux_value[2] += total_value
        if register[1] == "Exports":
            aux_value[0] += total_value
        else:
            aux_value[1] += total_value
        transports[mode] = aux_value    #update the value
    return transports



""" create a dictionary with the countries and their exports/imports value
    countries = { country: total_value} """
def get_countries(registers):
    countries = {}
    for register in registers:
        # if it is an export the country will be the origin
        if register[1] == "Exports":
            country = register[2]
        # if it is an import the country will be the destination
        else:
            country = register[3]
            # check if the country already exists in the dictionary
        if country in countries.keys():
            countries[country] += int(register[9]) # add the value
        else:
            countries[country] = int(register[9])    # set the value
    return countries



""" print the n most popular routes """
def print_routes(routes, n):
    # first sort the routes
    sorted_routes = sorted(routes.items(), key=lambda x: x[1][0], 
                           reverse=True)
    print("\n\t\tTOP 10 MOST POPULAR ROUTES\n")
    aux = 1
    for route in sorted_routes[:n]:
        print("Route", aux, ":  from", route[0][0], "to", route[0][1], route[1][0], "times")
        aux += 1
      
        
        
""" print the transport modes """
def print_transports(transports):
    # first sort the transports
    sorted_transports = sorted(transports.items(), key=lambda x: x[1][2], 
                               reverse=True) 
    print("\n \t \t TRANSPORT MODES TOTAL VALUE\n")
    for transport in sorted_transports:
        print("A total of  $", transport[1][2], " were transport by ", transport[0])



""" print the countries' exports/imports value """
def print_countries(countries, percent):
    #first sort the countries 
    sorted_countries = sorted(countries.items(), key=lambda x: x[1], 
                              reverse=True)
    aux = 0
    print("\n\tEXPORTS/IMPORTS VALUE PER COUNTRY\n")
    for country in sorted_countries:
        aux += country[1]
        if aux <= percent:
            print(country[0], " generated ", country[1])
        else:
            break
    print("\nThe countries listed above generated approx \nthe 80% of" 
          " exports/imports total value")
    
    

if __name__ == "__main__" :
    
    registers = get_registers("synergy_logistics_database.csv")
    
    # top 10 routes
    routes = get_routes(registers)
    print_routes(routes, 10)
    
    # best transport mode
    transports = get_transports(registers)
    print_transports(transports)
    
    # countries that represent the 80% of the exports/imports
    countries = get_countries(registers)
    # 172553038400 is the 80% of total exports/imports
    print_countries(countries, 172553038400) 
    
    
    
    
    
    
    
    