#handles menu drawing
import curses
class Menu():
    def __init__(self,**kwargs):
        curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)#selected
        curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_BLACK)#available
        curses.init_pair(3,8,curses.COLOR_BLACK)#locked

        try:
            self.objects = kwargs["objects"]
            self.positions = kwargs["positions"]
        except KeyError:
            self.objects = []
            self.positions = []

        self.selected = kwargs.get("selected",0)
        if self.selected >= 0:
            while self.objects[self.selected].getState() == -1:
                self.selected += 1
                if self.selected >= len(self.objects):
                    self.selected = 0

    def edit(self,id,data,value):
        if data == "state":
            self.objects[id].state = value
        elif data == "selected":
            self.selected = value

    def drawItem(self,stdscr,item,pos,state):
        stdscr.addstr(pos[0],pos[1],item.getDrawable(),curses.color_pair(state))

    def drawNext(self,stdscr,item,state):
        stdscr.addstr(item.getDrawable(),curses.color_pair(state))

    def convertState(self,state):
        if state == -1:
            return 3
        return 2

    def drawAll(self,stdscr):
        i = 0
        for item,pos in zip(self.objects,self.positions):
            bufferState = self.convertState(item.getState())
            if bufferState == -2:
                i+=1
                continue
            if i == self.selected:
                bufferState = 1

            if pos == None:
                self.drawNext(stdscr,item,bufferState)
            else:
                self.drawItem(stdscr,item,pos,bufferState)
            i+=1
        stdscr.refresh()

    def call(self,*args):
        if args[0] == "Button":
            return self.objects[self.selected].press()
        elif self.objects[self.selected].istype() == "Selector" and args[0] == "Selector":
            try:
                self.objects[self.selected].add(args[1])
                return 0
            except IndexError:
                return self.objects[self.selected].getValue()
        elif self.objects[self.selected].istype() == "List" and args[0] == "List":
            try:
                if args[1] > 0:
                    self.objects[self.selected].listNext()
                elif args[1] == 0:
                    return self.objects[self.selected].getSelected()
                else:
                    self.objects[self.selected].listPrev()
                return 0
            except IndexError:
                return self.objects[self.selected].getSelPos()
        elif self.objects[self.selected].istype() == "Stringbox" and args[0] == "Stringbox":
            try:
                if args[1] == 0:
                    return "Stringbox"
                elif args[1] == 1:
                    self.objects[self.selected].removeChar()
                else:
                    self.objects[self.selected].addChar(args[1])
            except IndexError:
                return self.objects[self.selected].getString()
        return -1

    def link(self):
        i = 0
        for item in self.objects:
            if item != self.objects[self.selected] and item.press() == self.objects[self.selected].press():
                self.selected = i
                return 0
            i+=1
        return -1

    def selectDown(self):
        self.selected += 1
        if self.selected >= len(self.objects):
            self.selected = 0
        while self.objects[self.selected].getState() == -1:
            self.selected += 1
            if self.selected >= len(self.objects):
                self.selected = 0

    def selectUp(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.objects)-1
        while self.objects[self.selected].getState() == -1:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.objects)-1
