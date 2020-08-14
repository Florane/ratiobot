import curses
from config import Config
from menu import Menu
from button import Button
from selector import Selector
from list import List
from stringbox import Stringbox
from spammer import Spammer
from stoner import Stoner
from curses import wrapper
from enum import Enum, auto
from sys import exit as shutdown
from time import sleep
import glob, os

class State(Enum):
    MAIN_MENU = auto()
    SETTINGS = auto()
    EXIT = auto()
    CREATE_CFG = auto()
    START = auto()
    LOADING = auto()
    RUNNING = auto()

start_settings = Config()
buffer_file = ""

def main(stdscr):
    curses.curs_set(0)
    current = State.MAIN_MENU
    start_settings.loadConfig("general")
    while True:
        stdscr.clear()
        if current == State.MAIN_MENU:
            current = mainMenu(stdscr)
        elif current == State.SETTINGS:
            current = settings(stdscr)
        elif current == State.CREATE_CFG:
            current = new_cfg(stdscr)
        elif current == State.START:
            if start_settings.get("SAVE_LP") == 1:
                current = addPassword(stdscr)
            else:
                current = State.RUNNING
        elif current == State.RUNNING:
            current = spamBody(stdscr)
        elif current == State.LOADING:
            current = loader(stdscr)
        elif current == State.EXIT:
            shutdown()

def mainMenu(stdscr):
    if len(os.listdir("save")) == 0:
        canLoad = -1
    else:
        canLoad = 0
    menu = Menu(objects = [Button("New Config",0,State.CREATE_CFG)
    ,Button("Load config",canLoad,State.LOADING)
    ,Button("Settings",0,State.SETTINGS)
    ,Button("Exit",0,State.EXIT)]
    ,positions = [(i,0) for i in range(0,4)])
    while True:
        stdscr.clear()
        menu.drawAll(stdscr)
        getch = stdscr.getch()
        if getch == curses.KEY_DOWN:
            menu.selectDown()
        elif getch == curses.KEY_UP:
            menu.selectUp()
        elif getch == ord(' ') or getch == curses.KEY_ENTER or getch == 10 or getch == 13:
            if isinstance(menu.call("Button"),State):
                return menu.call("Button")

def new_cfg(stdscr):
    global buffer_file
    newSave = Config()
    newSave.loadConfig("preset")
    mode = Menu(objects = [Button("Mode: ",-1,"")
    ,List("<{}>",0,"MODE",["File","Stonetoss"],0)]
    ,positions = [(0,0),None])
    modeSelected = 0
    menuSelected = 0

    fileMenu = Menu(objects = [Button("Config name: ",0,"CFG_NAME")
    ,Stringbox("{}",-1,"CFG_NAME","save/new")
    ,Button("Spam text file: ",0,"SPAM_NAME")
    ,Stringbox("{}",-1,"SPAM_NAME","spam/transrights.txt")
    ,Button("Target username: ",0,"TARGET_USER")
    ,Stringbox("{}",-1,"TARGET_USER","okyeahcorrect")
    ,Button("Target tweet: ",0,"TARGET_TWEET")
    ,Stringbox("{}",-1,"TARGET_TWEET","1282129396124585984")
    ,Button("Start",0,State.START)]
    ,positions = [(2,0),None,(3,0),None,(7,0),None,(8,0),None,(10,0)]
    ,selected = -1)

    stonetossMenu = Menu(objects = [Button("Config name: ",0,"CFG_NAME")
    ,Stringbox("{}",-1,"CFG_NAME","save/new")
    ,Button("Spam text folder: ",0,"SPAM_STONE")
    ,Stringbox("{}",-1,"SPAM_STONE","spam/stonetoss/")
    ,Button("Stone filename: ",0,"STONE_NAME")
    ,Stringbox("{}",-1,"STONE_NAME","stone.txt")
    ,Button("Toss filename: ",0,"TOSS_NAME")
    ,Stringbox("{}",-1,"TOSS_NAME","toss.txt")
    ,Button("Nazi filename: ",0,"FASH_NAME")
    ,Stringbox("{}",-1,"FASH_NAME","notsee.txt")
    ,Button("Target username: ",0,"TARGET_USER")
    ,Stringbox("{}",-1,"TARGET_USER","okyeahcorrect")
    ,Button("Target tweet: ",0,"TARGET_TWEET")
    ,Stringbox("{}",-1,"TARGET_TWEET","1282129396124585984")
    ,Button("Start",0,State.START)]
    ,positions = [(2,0),None,(3,0),None,(4,0),None,(5,0),None,(6,0),None,(7,0),None,(8,0),None,(10,0)]
    ,selected = -1)

    def changeState(menu,number):
        nonlocal menuSelected
        if menu.call("Selector",number) == 0:
            newSave.set(menu.call("Button"),menu.call("Selector"))
        elif menu.call("List",number) == 0:
            newSave.set(menu.call("Button"),menu.call("List"))
            if menu.call("Button") == "MODE":
                menuSelected = menu.call("List")

    while True:
        stdscr.clear()
        mode.drawAll(stdscr)
        if menuSelected == 0:
            fileMenu.drawAll(stdscr)
        elif menuSelected == 1:
            stonetossMenu.drawAll(stdscr)

        getch = stdscr.getch()
        if modeSelected == 0:
            if getch == 27:
                return State.MAIN_MENU
            elif getch == curses.KEY_RIGHT:
                changeState(mode,1)
            elif getch == curses.KEY_LEFT:
                changeState(mode,-1)
            elif getch == ord(' ') or getch == curses.KEY_ENTER or getch == 10 or getch == 13:
                fileMenu.edit(0,"selected",0)
                stonetossMenu.edit(0,"selected",0)
                mode.edit(0,"selected",-1)
                modeSelected = 1
        elif modeSelected == 1:
            if menuSelected == 0:
                reference = fileMenu
            elif menuSelected == 1:
                reference = stonetossMenu
            if getch == 27:
                fileMenu.edit(0,"selected",-1)
                stonetossMenu.edit(0,"selected",-1)
                mode.edit(0,"selected",1)
                modeSelected = 0
            elif getch == curses.KEY_DOWN:
                reference.selectDown()
            elif getch == curses.KEY_UP:
                reference.selectUp()
            elif getch == curses.KEY_RIGHT:
                changeState(reference,1)
            elif getch == curses.KEY_LEFT:
                changeState(reference,-1)
            elif getch == ord(' ') or getch == curses.KEY_ENTER or getch == 10 or getch == 13:
                if isinstance(reference.call("Button"),State):
                    newSave.saveConfig(newSave.get("CFG_NAME"))
                    buffer_file = newSave.get("CFG_NAME")
                    return reference.call("Button")
                reference.link()
                if reference.call("Stringbox",0) == "Stringbox":
                    reference.call("Stringbox","")
                    stringBuffer = 0
                    while stringBuffer != ord(' ') and stringBuffer != curses.KEY_ENTER and stringBuffer != 10 and stringBuffer != 13:
                        stdscr.clear()
                        mode.drawAll(stdscr)
                        reference.drawAll(stdscr)
                        stringBuffer = stdscr.getch()
                        if stringBuffer == 8:
                            reference.call("Stringbox",1)
                        elif stringBuffer != ord(' ') and stringBuffer != curses.KEY_ENTER and stringBuffer != 10 and stringBuffer != 13:
                            reference.call("Stringbox",chr(stringBuffer))
                        start_settings.set(reference.call("Button"),reference.call("Stringbox"))
                    reference.link()

def addPassword(stdscr):
    sides = stdscr.getmaxyx()
    menu = Menu(objects = [Button("Login: ",0,"LOGIN")
    ,Stringbox("{}",-1,"LOGIN","")
    ,Button("Password: ",0,"PASSWORD")
    ,Stringbox("{}",-1,"PASSWORD","")
    ,Button("Start",0,State.RUNNING)]
    ,positions = [(int(sides[0]/2),int(sides[1]/2-10)),None,(int(sides[0]/2+1),int(sides[1]/2-10)),None,(int(sides[0]/2+2),int(sides[1]/2-2))])

    def changeState(number):
        if menu.call("Selector",number) == 0:
            start_settings.set(menu.call("Button"),menu.call("Selector"))
        elif menu.call("List",number) == 0:
            start_settings.set(menu.call("Button"),menu.call("List"))

    while True:
        stdscr.clear()
        menu.drawAll(stdscr)
        getch = stdscr.getch()
        if getch == 27:
            return State.CREATE_CFG
        elif getch == curses.KEY_DOWN:
            menu.selectDown()
        elif getch == curses.KEY_UP:
            menu.selectUp()
        elif getch == curses.KEY_RIGHT:
            changeState(1)
        elif getch == curses.KEY_LEFT:
            changeState(-1)
        elif getch == ord(' ') or getch == curses.KEY_ENTER or getch == 10 or getch == 13:
            if isinstance(menu.call("Button"),State):
                stdscr.clear()
                return menu.call("Button")
            menu.link()
            if menu.call("Stringbox",0) == "Stringbox":
                menu.call("Stringbox","")
                stringBuffer = 0
                while stringBuffer != ord(' ') and stringBuffer != curses.KEY_ENTER and stringBuffer != 10 and stringBuffer != 13:
                    stdscr.clear()
                    menu.drawAll(stdscr)
                    stringBuffer = stdscr.getch()
                    if stringBuffer == 8:
                        menu.call("Stringbox",1)
                    elif stringBuffer != ord(' ') and stringBuffer != curses.KEY_ENTER and stringBuffer != 10 and stringBuffer != 13:
                        menu.call("Stringbox",chr(stringBuffer))
                    start_settings.set(menu.call("Button"),menu.call("Stringbox"))
                menu.link()

def spamBody(stdscr):
    global buffer_file
    settings = Config()
    settings.loadConfig(buffer_file)
    sides = stdscr.getmaxyx()
    if settings.get("MODE") == 0:
        spam = Spammer(settings,start_settings)
    elif settings.get("MODE") == 1:
        spam = Stoner(settings,start_settings)
    spam.generate()
    length = spam.length()
    spam.begin()
    line = "Progress: 0/{}".format(length)
    while True:
        stdscr.clear()
        stdscr.addstr(int(sides[0]/2),int(sides[1]/2)-int(len(line)/2),line,curses.color_pair(2))
        iter = spam.step()
        line = "Progress: {0}/{1}".format(iter,length)
        if iter >= length and settings.get("MODE") == 0:
            return State.MAIN_MENU
        sleep(start_settings.get("SPAM_SPEED"))

def loader(stdscr):
    global buffer_file
    objects = []
    for file in os.listdir("save"):
        objects.append(Button(file,0,file))
    menu = Menu(objects = objects,positions = [(i,0) for i in range(0,len(objects))])

    while True:
        stdscr.clear()
        menu.drawAll(stdscr)
        getch = stdscr.getch()
        if getch == 27:
            return State.MAIN_MENU
        elif getch == curses.KEY_DOWN:
            menu.selectDown()
        elif getch == curses.KEY_UP:
            menu.selectUp()
        elif getch == ord(' ') or getch == curses.KEY_ENTER or getch == 10 or getch == 13:
            buffer_file = "save/"+file.strip(".cfg")
            return State.START


def settings(stdscr):
    menu = Menu(objects = [Button("Spam Speed: ",0,"SPAM_SPEED")
    ,Selector("<{}>",-1,"SPAM_SPEED",start_settings.get("SPAM_SPEED"),(1,120))
    ,Button("Save Login/Password: ",0,"SAVE_LP")
    ,List("<{}>",-1,"SAVE_LP",["Yes","No"],start_settings.get("SAVE_LP"))
    ,Button("Login: ",start_settings.get("SAVE_LP")*-1,"LOGIN")
    ,Stringbox("{}",-1,"LOGIN",str(start_settings.get("LOGIN")))
    ,Button("Password: ",start_settings.get("SAVE_LP")*-1,"PASSWORD")
    ,Stringbox("{}",-1,"PASSWORD",str(start_settings.get("PASSWORD")))
    ,Button("<Save and Back",0,"SAVE")
    ,Button("<Back",0,State.MAIN_MENU)]
    ,positions = [(0,0),None,(1,0),None,(2,0),None,(3,0),None,(10,0),(11,0)])

    def changeState(number):
        if menu.call("Selector",number) == 0:
            start_settings.set(menu.call("Button"),menu.call("Selector"))
        elif menu.call("List",number) == 0:
            start_settings.set(menu.call("Button"),menu.call("List"))
            if start_settings.get("SAVE_LP") == 0:
                menu.edit(4,"state",0)
                menu.edit(6,"state",0)
            else:
                menu.edit(4,"state",-1)
                menu.edit(6,"state",-1)

    while True:
        stdscr.clear()
        menu.drawAll(stdscr)
        getch = stdscr.getch()
        if getch == 27:
            return State.MAIN_MENU
        elif getch == curses.KEY_DOWN:
            menu.selectDown()
        elif getch == curses.KEY_UP:
            menu.selectUp()
        elif getch == curses.KEY_RIGHT:
            changeState(1)
        elif getch == curses.KEY_LEFT:
            changeState(-1)
        elif getch == ord(' ') or getch == curses.KEY_ENTER or getch == 10 or getch == 13:
            if isinstance(menu.call("Button"),State):
                return menu.call("Button")
            elif menu.call("Button") == "SAVE":
                if start_settings.get("SAVE_LP") == 1:
                    start_settings.set("LOGIN","")
                    start_settings.set("PASSWORD","")
                start_settings.saveConfig("general")
                return State.MAIN_MENU
            menu.link()
            if menu.call("Stringbox",0) == "Stringbox":
                menu.call("Stringbox","")
                stringBuffer = 0
                while stringBuffer != ord(' ') and stringBuffer != curses.KEY_ENTER and stringBuffer != 10 and stringBuffer != 13:
                    stdscr.clear()
                    menu.drawAll(stdscr)
                    stringBuffer = stdscr.getch()
                    if stringBuffer == 8:
                        menu.call("Stringbox",1)
                    elif stringBuffer != ord(' ') and stringBuffer != curses.KEY_ENTER and stringBuffer != 10 and stringBuffer != 13:
                        menu.call("Stringbox",chr(stringBuffer))
                    start_settings.set(menu.call("Button"),menu.call("Stringbox"))
                menu.link()

wrapper(main)
