#handles config load/save
class Config():
    def __init__(self):
        self.parameters = {}

    def loadConfig(self,name):
        self.parameters = {}
        with open(name+".cfg") as cfg:
            for line in cfg:
                buffer = line.split("=")
                id = buffer[0].strip()
                value = buffer[1].strip()
                if value.isdigit():
                    value = int(value)
                self.parameters[id] = value

    def get(self,id):
        return self.parameters.get(id)

    def set(self,id,value):
        self.parameters[id] = value

    def saveConfig(self,name):
        with open(name+".cfg","w") as cfg:
            for id, value in self.parameters.items():
                cfg.write(str(id)+" = "+str(value)+"\n")
