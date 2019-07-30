from lxml import html
import requests
import time
import signal
import sys

def signal_handler(sig, frame):
        print("\n\033[94mDon't cheat again and play fairly!\033[0m\n")
        sys.exit(0)

class Player:
    name = ""
    
    Kills = []
    KilledBy = []
    
    KillsNames = []
    KillsNumbers = []
    KilledByNames = []
    KilledByNumbers = []
    lastKillsNames = []
    lastKillsNumbers = []
    lastKilledByNames = []
    lastKilledByNumbers = []
    
    KillsListEntries = []
    KilledByListEntries = []
    
    KillUrl = ""
    KilledByUrl = ""
    def __init__(self, name):
        self.name = name

deltext1 = '"\\u003ctable class=\\"table table-hover\\"\\u003e\\u003ctbody\\u003e\\u003ctr\\u003e\\u003cth\\u003ePlayer Name\\u003c/th\\u003e\\u003cth\\u003eTimes\\u003c/th\\u003e\\u003c/tr\\u003e\\u003ctr\\u003e\\u003ctd\\u003e\\u003cb\\u003e'
deltext2 = '\\u003c/b\\u003e\\u003c/td\\u003e\\u003ctd\\u003e'
deltext3 = '\\u003c/td\\u003e\\u003c/tr\\u003e\\u003ctr\\u003e\\u003ctd\\u003e\\u003cb\\u003e'
deltext4 = '\\u003c/td\\u003e\\u003c/tr\\u003e\\u003c/tbody\\u003e\\u003c/table\\u003e"'

bindedPlayers={}

try:
    fileWithPlayers = str(open("players.txt", "r").read()).replace("\n", ":").split(":")
    playersListNames = []
    playersListIds = []
    for x in range(0, len(fileWithPlayers)):
        if(x%2==0):
            playersListNames.append(fileWithPlayers[x])
        else:
            playersListIds.append(fileWithPlayers[x])
    zipObject = zip(playersListNames, playersListIds)
    bindedPlayers = dict(zipObject)
    del fileWithPlayers
    del playersListNames
    del playersListIds
    del zipObject
except FileNotFoundError:
    print("\n\033[91mCouldn't find or read players.txt file!\033[0m\n")
    sys.exit(0)

urlNameGrab = 'https://www.tgwerewolf.com/Stats/Player/'
urlKills = 'https://www.tgwerewolf.com/Stats/PlayerKills/'
urlKilledBy = 'https://www.tgwerewolf.com/Stats/PlayerKilledBy/'

players = []
amount_int = 0

def clear(r):
    text = r.text
    text = text.replace(deltext1, "")
    text = text.replace(deltext2, "|")
    text = text.replace(deltext3, "|")
    text = text.replace(deltext4, "")
    return text

def updateKills(PlayerNum):
    players[PlayerNum].KillsNames = []
    players[PlayerNum].KillsNumbers = []
    r = requests.get(players[PlayerNum].KillUrl)
    writeIntoList(PlayerNum, "Kill", r)

def updateKilledBy(PlayerNum):
    players[PlayerNum].KilledByNames = []
    players[PlayerNum].KilledByNumbers = []
    r = requests.get(players[PlayerNum].KilledByUrl)
    writeIntoList(PlayerNum, "By", r)

def writeIntoList(PlayerNum, KillOrBy, r):
    b = clear(r).split("|")
    if(KillOrBy == "Kill"):
        for x in range(0, 10):
            if(x%2 == 0):
                players[PlayerNum].KillsNames.append(b[x])
            else:
                players[PlayerNum].KillsNumbers.append(b[x])
    else:
        for x in range(0, 10):
            if(x%2 == 0):
                players[PlayerNum].KilledByNames.append(b[x])
            else:
                players[PlayerNum].KilledByNumbers.append(b[x])
    if(KillOrBy == "Kill"):
        players[PlayerNum].KillsListEntries = len(players[PlayerNum].KillsNames)
    else:
        players[PlayerNum].KilledByListEntries = len(players[PlayerNum].KilledByNames)

#Start of the program

signal.signal(signal.SIGINT, signal_handler)
print("\n\033[94mWelcome to WereWolf win script for Telegram!\033[0m")

print("Avialable names: ")
for key in bindedPlayers.keys():
  print("\033[92m" + key, end = ' ' + "\033[0m")

#mode = input("Do you want (1)Bind new names, (2)Play by Urls, (3)Play with already binded names?")

while True:
    tempvar = input("\nEnter player's binded name: ")
    if((tempvar not in bindedPlayers.keys()) and (tempvar != "")):
        print("Typo?", end='')
        continue
    if(tempvar == ""):
        if(amount_int < 5):
            continue
        else:
            print("\033[91mGame starts\033[0m\n")
            break
    else:
        players.append(Player(tempvar))
        amount_int += 1
        print("Amount of players: " + str(amount_int), end = '')
        
del tempvar

for x in range(0, amount_int):
    players[x].KillUrl = urlKills + bindedPlayers[players[x].name] + "?pid=" + bindedPlayers[players[x].name]
    players[x].KilledByUrl = urlKilledBy + bindedPlayers[players[x].name] + "?pid=" + bindedPlayers[players[x].name]
    
    r = requests.get("https://www.tgwerewolf.com/Stats/Player/" + bindedPlayers[players[x].name])
    getName = (html.fromstring(r.text).xpath('.//div[@class="box-title margin-bottom-30"]/p/text()'))
    players[x].name = ("".join(getName))
    print("Got new name: " + "".join(getName))
    
    updateKills(x)
    updateKilledBy(x)
    players[x].lastKillsNames = players[x].KillsNames
    players[x].lastKillsNumbers = players[x].KillsNumbers
    players[x].lastKilledByNames = players[x].KilledByNames
    players[x].lastKilledByNumbers = players[x].KilledByNumbers

del getName

while True:
    for x in range(0, amount_int):
        updateKills(x)
        updateKilledBy(x)
    for x in range(0, amount_int):
        
        for y in range(0, players[x].KillsListEntries):
            
            try:
                if((players[x].KillsNames.index(players[x].KillsNames[y]) < players[x].lastKillsNames.index(players[x].KillsNames[y]))):
                    print("It seems " + players[x].name + " killed " + players[x].KillsNames[y])
            except ValueError:
                for z in range(0, players[x].KillsListEntries):
                    if(players[x].KillsNames[z] not in players[x].lastKillsNames):
                        print("It seems " + players[x].name + " killed " + players[x].KillsNames[z])
                        
            if((int(players[x].KillsNumbers[y]) > int(players[x].lastKillsNumbers[y])) and (players[x].KillsNames[y] == players[x].lastKillsNames[y])):
                print("It seems " + players[x].name + " killed " + players[x].KillsNames[y])
                
        for y in range(0, players[x].KilledByListEntries):
            
            try:
                if((players[x].KilledByNames.index(players[x].KilledByNames[y]) < players[x].lastKilledByNames.index(players[x].KilledByNames[y]))):
                    print("It seems " + players[x].KilledByNames[y] + " killed " + players[x].name)
            except ValueError:
                for z in range(0, players[x].KilledByListEntries):
                    if(players[x].KilledByNames[z] not in players[x].lastKilledByNames):
                        print("It seems " + players[x].KilledByNames[z] + " killed " + players[x].name)
                        
            if(int(players[x].KilledByNumbers[y]) > int(players[x].lastKilledByNumbers[y]) and (players[x].KilledByNames[y] == players[x].lastKilledByNames[y])):
                print("It seems " + players[x].KilledByNames[y] + " killed " + players[x].name)
                
        players[x].lastKillsNames = players[x].KillsNames
        players[x].lastKillsNumbers = players[x].KillsNumbers
        players[x].lastKilledByNames = players[x].KilledByNames
        players[x].lastKilledByNumbers = players[x].KilledByNumbers
            
    time.sleep(3)
