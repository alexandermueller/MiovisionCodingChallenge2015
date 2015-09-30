#!/usr/bin/python

## Miovision Coding Challenge 2015
# Alexander Mueller

## data.json Results:
# Desired Answer: 22262229
# Actual Answer:  22252229

## Note: There is a missing datapoint for the vehicle with id: a51b612f. 
# { 'region': 3, 'vehicle': 'a51b612f', 'time': 1434577610.5230947 }
# The above entrance to the intersection isn't balanced by an exit from 
# the intersection, which in this case needs to be a straight trajectory
# through region 5.

import json
from math import *

dataFile = open('data.json')
dataset = json.load(dataFile)
dataFile.close()

vehicles = {}                                                               # Dictionary indexed by vehicle id, containing a list of sorted events that each car triggered.
stats = [0, 0, 0, 0]                                                        # List of turning frequencies.

for turn in dataset:                                                        # Loop through all the turns in the dataset and build a dictionary of vehicles and their events.
    vehicle = turn['vehicle']
    if vehicle in vehicles:                                                 # This vehicle has already been seen before, so place the event into its list.
        events = vehicles[vehicle]
        for i in xrange(len(events)):                                       # Iterate through the events and place the current event in the right spot.
            event = events[i]
            if event['time'] > turn['time']:                                # Place the event in order of occurance in the list.
                vehicles[vehicle] = events[:i] + [turn] + events[i:]
                break
            elif event['time'] < turn['time'] and i == (len(events) - 1):   # Otherwise, it is the last occurring event, so add it to the end.
                vehicles[vehicle] += [turn]
    else:                                                                   # This vehicle hasn't been seen before, so create a new vehicle in the dictionary.
        vehicles[vehicle] = [turn]

for vehicle in vehicles:                                                    
    events = vehicles[vehicle]    
    for i in xrange(0, len(events) / 2, 2):                                 # Loop through each pair of events for each vehicle, and determine the turn type
        eventA = events[i]
        eventB = events[i + 1]
        turnType = (abs(eventA['region'] - eventB['region']) - 1) % 4       # Calculate the difference (with offset of minus 1 to change their ordering in the list)
        stats[turnType] += 1                                                # modulo 4 in order to determine the type of turn.

print "%d%d%d%d" % (stats[0], stats[1], stats[2], stats[3])                 # Print out the resulting frequencies.