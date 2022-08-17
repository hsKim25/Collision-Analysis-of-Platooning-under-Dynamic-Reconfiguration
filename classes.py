class Vehicle:
    def __init__(self, vehid):
        self.vehid = vehid
        self.vardict = {}

    def setVariableTypes(self, varlist):
        for label in varlist:
             self.vardict[label] = []

    def appendValue(self, key, newvalue):
        valuehist = self.vardict[key]
        self.vardict[key] = valuehist + [newvalue]

    def getValues(self, key):
        return self.vardict[key]

