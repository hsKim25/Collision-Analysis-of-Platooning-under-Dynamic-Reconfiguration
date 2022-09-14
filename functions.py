from classes import *
import math


# return: vehdict, lanedict, col_info_list
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
                    closest_vehicle_timeindex = None
                    closest_veh_info = []
                    for vehid in prev_index_veh_list: #사라진 차량과 가장 근접한 차량 찾기
                        if vehid == collision_vehicle:
                            continue
                        timeindex = vehdict[vehid].getValues("timeStamp").index(time)
                        if vehdict[collision_vehicle].getValues("lane")[-1] == vehdict[vehid].getValues("lane")[timeindex]:
                            if abs(vehdict[collision_vehicle].getValues("lanepos")[-1] - vehdict[vehid].getValues("lanepos")[timeindex]) < difference:
                                difference = abs(vehdict[collision_vehicle].getValues("lanepos")[-1] - vehdict[vehid].getValues("lanepos")[timeindex])
                                closest_vehicle = vehid
                                closest_vehicle_timeindex = timeindex

                    for variable in varlist:
                        closest_veh_info.append(vehdict[closest_vehicle].getValues(variable)[closest_vehicle_timeindex])
                    collision_info_list.append((col_veh_info[0], col_veh_info[1], collision_vehicle, closest_vehicle))

            prev_index_veh_list = current_index_veh_list
            current_index_veh_list = []

    f.close()

    return vehdict, lanedict, collision_info_list

# return: platoon_history
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

# return: target_veh_platoon_history List((Time, List(plt_veh)))
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

    if len(history) != 0:
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

# Calculate the order distance in the platoon vehicles
def structure_distance(base_veh, target_veh, time, structure_history):
    prev_history = []
    for change_point in structure_history:
        if time >= change_point[0]:
            prev_history = change_point[1]
        else:
            break
    if prev_history == "Leave":
        return -1
    elif target_veh in prev_history:
        return abs(prev_history.index(base_veh) - prev_history.index(target_veh))
    else:
        return -1

# Calculate the order distance in the lane
def lane_distance(base_veh, target_veh, time, lane_history):
    prev_history = None
    for tick in lane_history:
        if time >= tick[0]:
            prev_history = tick[1]
        else:
            break

    if target_veh in prev_history:
        return abs(prev_history.index(base_veh) - prev_history.index(target_veh))
    else:
        return -1

# Calculate the position distance in the lane
def position_distance(base_veh, target_veh, time, lane_history):
    prev_history = None
    for tick in lane_history:
        if time >= tick[0]:
            prev_history = tick[1]
        else:
            break

    veh_list = list(map(lambda x: x[0], prev_history))
    if target_veh in veh_list:
        return abs(prev_history[veh_list.index(base_veh)][1] - prev_history[veh_list.index(target_veh)][1])
    else:
        return -1

# Find front vehs based on lane_history at the specific time
def get_front_veh(base_veh, time, lane):
    lane_info = lane.getperiodinfo(time, time)[0]
    print("Lane information: ", lane_info)

    front_veh_list = []
    for i in range(len(lane_info[1])):
        if lane_info[1][i][0] == base_veh:
            front_veh_list = lane_info[1][i+1:]
            break

    print("Front vehicle list: ", front_veh_list)
    return front_veh_list

# Calculate the structure, lane composite distance
def structure_lane_composite_distance(base_veh, time, ordered_veh_list, structure_history):
    ordered_veh_numbering = []
    cnt = 0
    for veh in ordered_veh_list:
        current_veh_structure_history = tracking_plt_history_for_target_veh(base_veh, structure_history)
        str_dist = structure_distance(base_veh, veh[0], time, current_veh_structure_history)
        if str_dist == -1:
            cnt += 1
        ordered_veh_numbering.append(cnt)
        base_veh = veh[0]

    print("Front vehicle numbering: ", ordered_veh_numbering)

    return ordered_veh_numbering

# Select the vehicles that might be related to the collision
def select_related_vehicles(front_veh_list, front_veh_numbering, upperbound):
    try:
        ind = front_veh_numbering.index(upperbound + 1)
        return front_veh_list[:ind], front_veh_numbering[:ind]
    except ValueError:
        return front_veh_list, front_veh_numbering

# return: time period that should be analyzed
def getTimeScope(col_time, plt_history):
    for i in range(len(plt_history) - 1):
        if plt_history[i][0] < col_time <= plt_history[i + 1][0]:
            return [plt_history[i][0], col_time]

#
def generate_group_object(col_veh, veh_list, veh_numbering, vehdict, lanedict, timescope):
    groups = []
    col_veh = Group([col_veh])
    groups.append(col_veh)

    current_numbering = veh_numbering[0]
    current_list = []
    for i in range(len(veh_list)):
        if current_numbering == veh_numbering[i]:
            current_list.append(vehdict[veh_list[i][0]])
        else:
            new_group = Group(current_list)
            groups.append(new_group)
            current_numbering = veh_numbering[i]
            current_list = [vehdict[veh_list[i][0]]]
    new_group = Group(current_list)
    groups.append(new_group)


    for i in range(len(groups)):
        group = groups[i]
        if len(group.vehlist) == 1:
            veh = group.vehlist[0]
            start_ind = veh.vardict["timeStamp"].index(timescope[0])
            end_ind = veh.vardict["timeStamp"].index(timescope[1])
            group.timestamp = veh.getValues("timeStamp")[start_ind:end_ind + 1]
            group.lane = veh.getValues("lane")[start_ind:end_ind + 1]
            group.capacity = [0 for i in range(end_ind - start_ind)]
            group.speed = veh.getValues("speed")[start_ind:end_ind + 1]

            for i in range(len(group.timestamp)):
                lane_info = lanedict[group.lane[i]].getperiodinfo(group.timestamp[i], group.timestamp[i])[0][1]
                lane_vehs = list(map(lambda x: x[0], lane_info))

                veh_index = lane_vehs.index(veh.vehid)
                if veh_index != len(lane_vehs) - 1:
                    group.distance.append(round(lane_info[veh_index + 1][1] - lane_info[veh_index][1], 2))
                else:
                    group.distance.append(math.inf)

        else:
            back_veh = group.vehlist[0]
            front_veh = group.vehlist[-1]
            start_ind = front_veh.vardict["timeStamp"].index(timescope[0])
            end_ind = front_veh.vardict["timeStamp"].index(timescope[1])
            group.timestamp = front_veh.getValues("timeStamp")[start_ind:end_ind + 1]
            group.lane = front_veh.getValues("lane")[start_ind:end_ind + 1]
            group.speed = back_veh.getValues("speed")[start_ind:end_ind + 1]

            for i in range(len(group.timestamp)):
                lane_info = lanedict[group.lane[i]].getperiodinfo(group.timestamp[i], group.timestamp[i])[0][1]
                lane_vehs = list(map(lambda x: x[0], lane_info))

                front_veh_index = lane_vehs.index(front_veh.vehid)
                back_veh_index = lane_vehs.index(back_veh.vehid)
                print(lane_info[front_veh_index][1], lane_info[back_veh_index][1])
                group.capacity.append(round(lane_info[front_veh_index][1] - lane_info[back_veh_index][1], 2))
                if front_veh_index != len(lane_vehs) - 1:
                    group.distance.append(round(lane_info[front_veh_index + 1][1] - lane_info[front_veh_index][1], 2))
                else:
                    group.distance.append(math.inf)

    return groups

# return: Collision type
def collision_classification(col_veh1, col_veh2, time):
    if "flow" in col_veh1:
        if "flow" in col_veh2:
            return "env-env"


# Select relatively important vehicles based on three distance
#def grouping(structure_history, lane_history, target_veh, time):






