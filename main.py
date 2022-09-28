from functions import *
import pickle


filename = 'COLLISION_Cases.xlsx'
compositionbound = 2
distancebound = 200

#make_group_xlsx_from_raw_data(filename, compositionbound, distancebound)

#filelist, MTS_dataset = read_group_xlsx()

with open('groupdata/mtsdata.pickle', 'rb') as f:
    filelist, MTS_dataset = pickle.load(f)
print("FileList: ", filelist)

MTS_dataset_preprocessed = preprocess(MTS_dataset[:], distancebound)

cluster_result, centers = dtwKMeans(MTS_dataset_preprocessed, 10, compositionbound)

with open('outputdata/clusterdata.pickle', 'rb') as f:
    nearest_center_index, centers = pickle.load(f)

print(nearest_center_index)

visualization(MTS_dataset_preprocessed, nearest_center_index, centers)
