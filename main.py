from functions import *


start_num = 2791
end_num = 2791

for filenum in range(start_num, end_num + 1):
    try:
        vehdict, lanedict, col_info = readtxt_VehData(filenum, ["timeStamp", "lane", "lanepos", "speed", "accel"])
        print("Collision Information: ", col_info)
        if len(col_info) != 0:
            structure_history = readtxt_InConfigData(filenum)

            # 두 충돌 차량의 위치를 바탕으로 뒤에 있는 차량 찾기
            first_col = col_info[0]
            col_time = first_col[0]
            col_lane = lanedict[first_col[1]]
            col_veh1 = vehdict[first_col[2]]
            col_veh2 = vehdict[first_col[3]]
            col_veh1_pos = col_veh1.getValues("lanepos", col_time)
            col_veh2_pos = col_veh2.getValues("lanepos", col_time)

            behind_veh = col_veh1
            if col_veh1_pos > col_veh2_pos:
                behind_veh = col_veh2

            front_veh_list = get_front_veh(behind_veh.vehid, col_time, col_lane)

            front_veh_numbering = []
            base_veh = behind_veh.vehid
            cnt = 0
            for veh in front_veh_list:
                current_veh_structure_history = tracking_plt_history_for_target_veh(base_veh, structure_history)
                str_dist = structure_distance(base_veh, veh[0], col_time, current_veh_structure_history)
                if str_dist == -1:
                    cnt += 1
                front_veh_numbering.append(cnt)
                base_veh = veh[0]

            print(front_veh_numbering)

            #timescope = getTimeScope(col_info)

    except FileNotFoundError:
        continue



#print(position_distance('veh1.6', 'flow1.2', collision_time, lanedict['1to2_1'].hist))

