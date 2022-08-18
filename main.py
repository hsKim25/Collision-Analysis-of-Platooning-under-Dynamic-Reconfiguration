from classes import *


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
                currentlineveh.appendValue(variable[1], line[variable[0]])

            current_index_veh_list.append(line[2])

        else:
            for vehicle in prev_index_veh_list: #prev와 비교해서 사라진 차량 찾기
                if vehicle not in current_index_veh_list:
                    collision_vehicle = vehicle
                    col_veh_info = []
                    for variable in varlist:
                        col_veh_info.append(vehdict[collision_vehicle].getValues(variable)[-1])
                    collision_info_list.append((collision_vehicle, col_veh_info))
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





vehdict, col_info = readtxt_VehData(5904, ["timeStamp","lane","lanepos","speed","accel"])
#col_info = collsionfinder(4900, ["timeStamp","lane","lanepos","speed","accel"])
print(col_info)



