#handles button logic
class Button():
    def __init__(self,name,state,carry):
        self.name = name
        self.state = state
        self.carry = carry

    def press(self):
        return self.carry

    def getDrawable(self):
        return self.name.format(self.carry)

    def getState(self):
        return self.state

    def istype(self):
        return "Button"
