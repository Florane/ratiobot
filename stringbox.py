#handles string box logic
from button import Button
class Stringbox(Button):
    def __init__(self,name,state,carry,string):
        self.name = name
        self.state = state
        self.carry = carry
        self.string = string

    def setString(self,string):
        self.string = string

    def getString(self):
        return self.string

    def addChar(self,char):
        self.string += char

    def removeChar(self):
        self.string = self.string [:-1]

    def istype(self):
        return "Stringbox"

    def getDrawable(self):
        return self.name.format(self.string)
