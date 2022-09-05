class Platoon:
    def __init__(self, vehlist):
        self.vehlist = vehlist


class Vehicle:
    def __init__(self, vehid):
        self.vehid = vehid
        self.vardict = {}

    def setVariableTypes(self, varlist):
        for label in varlist:
             self.vardict[label] = []

    def appendValue(self, key, newvalue):
        try:
            self.vardict[key] = self.vardict[key] + [float(newvalue)]

        except:
            self.vardict[key] = self.vardict[key] + [newvalue]

    def getValues(self, key, time= -1):
        if time == -1:
            return self.vardict[key]
        else:
            ind = self.vardict["timeStamp"].index(time)
            return self.vardict[key][ind]


class Lane:
    def __init__(self, lanenum):
        self.lanenum = lanenum
        self.hist = []

    def appendVeh(self, time, vehid, pos):
        timestamps = list(map(lambda x: x[0], self.hist))
        if time in timestamps:
            ind = timestamps.index(time)
            currentlist = self.hist[ind][1]
            start = 0
            end = len(currentlist) - 1
            while start < end:
                mid = (start + end) // 2
                if currentlist[mid][1] < pos:
                    start = mid + 1
                else:
                    end = mid - 1

            if currentlist[start][1] < pos:
                self.hist[ind][1].insert(start + 1, (vehid, pos))

            else:
                self.hist[ind][1].insert(start, (vehid, pos))

        else:
            self.hist.append((time, [(vehid, pos)]))

    def getperiodinfo(self, starttime, endtime):
        timestamps = list(map(lambda x: x[0], self.hist))
        startind = timestamps.index(starttime)
        endind = timestamps.index(endtime)

        return self.hist[startind:endind+1]

