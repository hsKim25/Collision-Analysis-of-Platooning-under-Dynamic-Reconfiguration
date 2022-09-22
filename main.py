from functions import *
import pickle

filename = 'COLLISION_Cases.xlsx'
compositionbound = 2
distancebound = 200

#make_group_xlsx_from_raw_data(filename, compositionbound, distancebound)

#MTS_dataset = read_group_xlsx()

with open('groupdata/mtsdata.pickle', 'rb') as f:
    MTS_dataset = pickle.load(f)
print(MTS_dataset[0])
print(MTS_dataset[1])
#MTS_dataset_preprocessed = preprocess(MTS_dataset[:], distancebound)
calculate_distance_btw_two_MTS([[0,1,2,3,4,5,6,7,8,9,10,11],[8,9,10,11,12,13,14,15,16,17,18,19]],[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]])

#print(position_distance('veh1.6', 'flow1.2', collision_time, lanedict['1to2_1'].hist))

