#handles number selector logic
from button import Button
class Selector(Button):
    def __init__(self,name,state,carry,value,boundry):
        self.name = name
        self.state = state
        self.carry = carry
        self.value = value
        self.boundry = boundry

    def getDrawable(self):
        return self.name.format(self.value)

    def getValue(self):
        return self.value

    def add(self,amount):
        self.value += amount
        if self.value < self.boundry[0]:
            self.value = self.boundry[0]
        elif self.value > self.boundry[1]:
            self.value = self.boundry[1]


    def istype(self):
        return "Selector"
