from classes import *


def readtxt_VehData(fname, varlist):
    f = open("data/" + fname, 'r')
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

    print(vehdict["veh.1"].getValues('lanepos'))




readtxt_VehData("671_0vehicleData.txt", ["timeStamp","lane","lanepos","speed","accel"])
