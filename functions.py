from classes import *
import math


#return: vehdict, lanedict, col_info_list
def readtxt_VehData(fnum, varlist):
    f = open("data/" + str(fnum) + "_0vehicleData.txt", 'r')
    lines = f.readlines()
    lines.append("\n") #index 구분행 추가

    vehdict = {}
    lanedict = {}

    prev_index_veh_list = []
    current_index_veh_list = []
    collision_info_list = []

    indices = list(map(lambda x: (lines[13].split().index(x), x), varlist)) #varlist에 있는 각 variable의 위치

    for line in lines[14:]: #한 라인씩 읽으면서 각 vehicle object에 varlist의 항목들을 저장, lane에 시간별 차량 정보를 정렬하여 저장
        line = line.split()
        if len(line) > 1:
            #Vehicle object
            if line[2] not in vehdict:
                newveh = Vehicle(line[2])
                newveh.setVariableTypes(varlist)
                vehdict[line[2]] = newveh
            currentlineveh = vehdict[line[2]]
            for variable in indices:
                currentlineveh.appendValue(variable[1], line[variable[0]])

            current_index_veh_list.append(line[2])

            #Lane object
            if line[3] not in lanedict:
                newlane = Lane(line[3])
                lanedict[line[3]] = newlane
            lanedict[line[3]].appendVeh(float(line[1]), line[2], float(line[4]))


        else: #한 index가 끝났을 경우 충돌하여 사라진 차량 확인 후 collision 정보 저장
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

                    collision_info_list.append((col_veh_info[0], col_veh_info[1], collision_vehicle, closest_vehicle))

            prev_index_veh_list = current_index_veh_list
            current_index_veh_list = []

    f.close()

    return vehdict, lanedict, collision_info_list

#return: platoon_history
def readtxt_InConfigData(fnum):
    f = open("data/" + str(fnum) + "_0plnConfig.txt", 'r')
    lines = f.readlines()
    lines.append("\n") #index 구분행 추가

    current_time = 0

    current_index_veh_list = []
    platoon_history = []
    for line in lines[14:]:
        if len(line) > 1:
            line = line.split()
            current_index_veh_list.append(line[2])
            current_time = float(line[lines[13].split().index("timestamp")])

        elif len(current_index_veh_list) > 0:
            if len(platoon_history) == 0:
                platoon_history.append((current_time, [current_index_veh_list]))
            elif platoon_history[-1][0] == current_time:
                platoon_history[-1][1].append(current_index_veh_list)
            else:
                platoon_history.append((current_time, [current_index_veh_list]))
            current_index_veh_list = []

    f.close()

    return platoon_history

#return: target_veh_platoon_history
def tracking_plt_history_for_target_veh(target_veh, structure_history):
    history = []
    start = 0
    end = 0
    cnt = -1
    last_ind = 0
    for tick in structure_history:
        cnt += 1
        for platoon in tick[1]:
            if target_veh in platoon:
                last_ind = cnt
                current = tick[0]
                if len(history) == 0:
                    history.append((current, platoon))
                    start = current
                    end = current
                elif history[-1][1] == platoon:
                    if end == start:
                        history.append((current, platoon))
                    else:
                        history[-1] = (current, platoon)
                    end = current
                else:
                    history.append((current, platoon))
                    start = current
                    end = current

    last_platoon = history[-1][1][:]
    last_platoon.remove(target_veh)

    #Leave 확인
    if last_ind != len(structure_history) - 1:
        for tick in structure_history[last_ind+1:]:
            for platoon in tick[1]:
                for veh in last_platoon:
                    if veh in platoon:
                        history.append((tick[0], "Leave"))
                        return history

    return history

#return: time period that should be analyzed
def getTimeScope(col_time, plt_history):
    for i in range(len(plt_history) - 1):
        if plt_history[i][0] < col_time <= plt_history[i + 1][0]:
            return [plt_history[i][0], col_time]


#return: Collision type
def collision_classification(col_veh1, col_veh2, time):
    if "flow" in col_veh1:
        if "flow" in col_veh2:
            return "env-env"


#Select relatively important vehicles based on three distance
#def grouping(structure_history, lane_history, target_veh, time):


#Calculate the order distance in the platoon vehicles
def structure_distance(col_veh, target_veh, time, structure_history):
    prev_history = None
    for change_point in structure_history:
        if time >= change_point[0]:
            prev_history = change_point[1]
        else:
            break

    if target_veh in prev_history:
        return abs(prev_history.index(col_veh) - prev_history.index(target_veh))
    else:
        return -1

#Calculate the order distance in the lane
def lane_distance(col_veh, target_veh, time, lane_history):
    prev_history = None
    for tick in lane_history:
        if time >= tick[0]:
            prev_history = tick[1]
        else:
            break

    if target_veh in prev_history:
        return abs(prev_history.index(col_veh) - prev_history.index(target_veh))
    else:
        return -1

#Calculate the position distance in the lane
def position_distance(col_veh, target_veh, time, lane_history):
    prev_history = None
    for tick in lane_history:
        if time >= tick[0]:
            prev_history = tick[1]
        else:
            break

    veh_list = list(map(lambda x: x[0], prev_history))
    if target_veh in veh_list:
        return abs(prev_history[veh_list.index(col_veh)][1]-prev_history[veh_list.index(target_veh)][1])
    else:
        return -1



