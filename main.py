from functions import *
import pickle

filename = 'COLLISION_Cases.xlsx'
compositionbound = 2
distancebound = 200

#make_group_xlsx_from_raw_data(filename, compositionbound, distancebound)

#MTS_dataset = read_group_xlsx()

with open('groupdata/mtsdata.pickle', 'rb') as f:
    MTS_dataset = pickle.load(f)
print(MTS_dataset)

#print(position_distance('veh1.6', 'flow1.2', collision_time, lanedict['1to2_1'].hist))

