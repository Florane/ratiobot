#handles list logic
from button import Button
class List(Button):
    def __init__(self,name,state,carry,list,*args):
        self.name = name
        self.state = state
        self.carry = carry
        self.list = list
        try:
            self.selected = args[0]
        except IndexError:
            self.selected = 0

    def getSelected(self):
        return self.list(self.selected)

    def getSelPos(self):
        return self.selected

    def listNext(self):
        self.selected += 1
        if self.selected >= len(self.list):
            self.selected = 0

    def listPrev(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.list)-1

    def getDrawable(self):
        return self.name.format(self.list[self.selected])

    def istype(self):
        return "List"
