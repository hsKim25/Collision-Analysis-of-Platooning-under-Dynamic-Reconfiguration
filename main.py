from functions import *
import pandas as pd

filename = 'COLLISION_Cases.xlsx'
col_file = pd.read_excel("data/" + filename, sheet_name='Falselog', engine='openpyxl')
print(col_file['file'])
col_file_num = list(map(lambda x: int(x[0:4]), col_file['file']))

for filenum in col_file_num[857:858]:
    try:
        print("filenum: ", filenum)
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
            front_veh_numbering = structure_lane_composite_distance(behind_veh.vehid, col_time, front_veh_list, structure_history)

            upperbound = 2
            col_related_veh_list, col_related_veh_numbering = select_related_vehicles(front_veh_list, front_veh_numbering, upperbound)




            if front_veh_numbering == 0:
                print("Plt-Plt Collision: ", filenum)


            #timescope = getTimeScope(col_info)



    except FileNotFoundError:
        continue



#print(position_distance('veh1.6', 'flow1.2', collision_time, lanedict['1to2_1'].hist))

