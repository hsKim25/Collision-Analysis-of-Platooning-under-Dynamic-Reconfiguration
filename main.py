from classes import *
import math


def readtxt_VehData(fnum, varlist):
    f = open("data/" + str(fnum) + "_0vehicleData.txt", 'r')
    lines = f.readlines()
    vehdict = {}

    prev_index_veh_list = []
    current_index_veh_list = []
    collision_info_list = []

    indices = list(map(lambda x: (lines[13].split().index(x), x), varlist)) #varlist에 있는 각 variable의 위치

    for line in lines[14:]:
        line = line.split()
        if len(line) > 1:
            if line[2] not in vehdict:
                newveh = Vehicle(line[2])
                newveh.setVariableTypes(varlist)
                vehdict[line[2]] = newveh
            currentlineveh = vehdict[line[2]]
            for variable in indices:
                try:
                    currentlineveh.appendValue(variable[1], float(line[variable[0]]))

                except:
                    currentlineveh.appendValue(variable[1], line[variable[0]])

            current_index_veh_list.append(line[2])

        else:
            for vehicle in prev_index_veh_list: #prev와 비교해서 사라진 차량 찾기
                if vehicle not in current_index_veh_list:
                    collision_vehicle = vehicle
                    col_veh_info = []
                    for variable in varlist:
                        col_veh_info.append(vehdict[collision_vehicle].getValues(variable)[-1])

                    time = vehdict[collision_vehicle].getValues("timeStamp")[-1]
                    difference = math.inf
                    closest_vehicle = None
                    closest_veh_info = []
                    for vehid in prev_index_veh_list: #사라진 차량과 가장 근접한 차량 찾기
                        if vehid == collision_vehicle:
                            continue
                        timeindex = vehdict[vehid].getValues("timeStamp").index(time)
                        if vehdict[collision_vehicle].getValues("lane")[-1] == vehdict[vehid].getValues("lane")[timeindex]:
                            if abs(vehdict[collision_vehicle].getValues("lanepos")[-1] - vehdict[vehid].getValues("lanepos")[timeindex]) < difference:
                                difference = abs(vehdict[collision_vehicle].getValues("lanepos")[-1] - vehdict[vehid].getValues("lanepos")[timeindex])
                                closest_vehicle = vehid

                    for variable in varlist:
                        closest_veh_info.append(vehdict[closest_vehicle].getValues(variable)[timeindex])

                    collision_info_list.append(((collision_vehicle, col_veh_info), (closest_vehicle, closest_veh_info)))

            prev_index_veh_list = current_index_veh_list
            current_index_veh_list = []

    f.close()

    return vehdict, collision_info_list

def readtxt_InConfigData(fnum, varlist):
    f = open("data/" + str(fnum) + "_InConfigData.txt", 'r')
    lines = f.readlines()
    index = 0
    vehdict = {}
    print(lines[13].split())

    indices = list(map(lambda x: (lines[13].split().index(x), x), varlist)) #varlist에 있는 각 variable의 위치

    for line in lines[14:]:
        if len(line) > 1:
            line = line.split()
            if line[2] not in vehdict:
                newveh = Vehicle(line[2])
                newveh.setVariableTypes(varlist)
                vehdict[line[2]] = newveh
            currentlineveh = vehdict[line[2]]
            for variable in indices:
                currentlineveh.appendValue(variable[1], line[variable[0]])





vehdict, col_info = readtxt_VehData(5925, ["timeStamp","lane","lanepos","speed","accel"])
#col_info = collsionfinder(4900, ["timeStamp","lane","lanepos","speed","accel"])
print(col_info)



