import win32api as a
import time

def getMove():
    while True:
        wKey = a.GetKeyState(0x57)
        aKey = a.GetKeyState(0x41)
        sKey = a.GetKeyState(0x53)
        dKey = a.GetKeyState(0x44)

        if wKey < 0:
            move = 'W'
            time.sleep(.15)
            break

        elif aKey < 0:
            move = 'A'
            time.sleep(.15)
            break

        elif sKey < 0:
            move = 'S'
            time.sleep(.15)
            break

        elif dKey < 0:
            move = 'D'
            time.sleep(.15)
            break

    """while move.lower() not in ['w', 'a', 's', 'd']:
        move = input("Invalid, what is your move? ")"""

    return move.lower()


def levelLoader(currentLevel):
    MapsList = ['map1.txt', 'map2.txt', 'map3.txt']
    currentMap = MapsList[currentLevel - 1]
    Map = []

    mapFile = open(currentMap, 'r')

    for line in mapFile:
        for character in line.strip():
            Map.append(character)

    return Map


def displayMap(Map):
    for i in range(800):
        if ((i > 0) and (i % 40 == 0)):
            print()
        print(Map[i], end="")
    print()


def locatePlayer(Map):
    loc = Map.index('p')
    return loc


def isWall(Map, targetLoc):
    if Map[targetLoc] == '#':
        return True
    else:
        return False

def isDoor(Map, targetLod):
    if Map[targetLod] == 'O':
        return True
    else:
        return False

def switching(switcher):
    if switcher == True:
        switcher = False
    else:
        switcher = True

    return switcher

def moveDoor(Map, switcher):
    counter = Map.count('O')
    if switcher == True:
        for i in range(counter):
            indx = Map.index('O')
            Map.pop(indx)
            Map.insert(indx, ' ')
            Map[indx + 2] = 'O'
    elif switcher == False:
        for i in range(counter):
            Map.reverse()
            indx = Map.index('O')
            Map.pop(indx)
            Map.insert(indx, ' ')
            Map[indx + 2] = 'O'
            Map.reverse()

def addKey(keysHolder, Map, targetLoc):
    if Map[targetLoc] in ['g', 'y']:  # checks if there is a key on the tile where the player will move into
        keysHolder.append({"location": targetLoc, "value": Map[targetLoc]})  # adds the key to the player's inventory

    return keysHolder  # returns a list containing the keys


def addChip(chips, Map, targetLoc):
    if Map[targetLoc] == 'c':
        chips.append('c')
    return chips


def addImmunity(immunity, Map, targetLoc):
    if Map[targetLoc] in ['z']:
        immunity.append(Map[targetLoc])
    if Map[targetLoc] in ['f']:
        immunity.append(Map[targetLoc])

    return immunity


def checkDoor(Map, targetLoc):  # checks if the destination is a door

    if Map[targetLoc] in ['G', 'Y']:
        return True

    else:
        return False


def keyAvailable(door, keysHolder):
    key = door.lower()
    for item in keysHolder:
        if item["value"] == key:
            return True
    
    return False


def isImmune(immunity, hazard):
    if hazard == 'W' and 'z' in immunity:
        return True

    elif hazard == 'F' and 'f' in immunity:
        return True

    else:
        return False


def locateTarget(move, Map):  # locates the desired position
    playerLoc = locatePlayer(Map)  # locates the player on the map
    if move == 'w':
        targetLoc = playerLoc - 40
    elif move == 's':
        targetLoc = playerLoc + 40
    elif move == 'a':
        targetLoc = playerLoc - 1
    elif move == 'd':
        targetLoc = playerLoc + 1

    return targetLoc  # returns the the index of the desired position


"""def slide(move, Map, targetLoc):
    if move == 'd':
        if Map[targetLoc] == '<':
            targetLoc -= 1
        while Map[targetLoc] == '>':
            targetLoc += 1

    elif move == 'a':
        if Map[targetLoc] == '>':
            targetLoc += 1

        while Map[targetLoc] == '<':
            targetLoc -= 1

    elif move == 'w':
        targetLoc += 40

    elif move == 's':
        targetLoc -= 40

    return targetLoc"""


def movePlayer(Map, targetLoc, prevTile):
    playerLoc = locatePlayer(Map)

    Map[playerLoc] = prevTile
    Map[targetLoc] = 'p'

    return Map


def resetPos(Map, initialPos):
    playerLoc = locatePlayer(Map)
    Map[initialPos] = 'p'
    return Map


def gameReset():
    return True


def findKeys(Map):
    keysLoc = []

    for item in ['y', 'g']:
        while item in Map:
            keyLoc = Map.index(item)
            key = Map[keyLoc]

            keysLoc.append({"location":keyLoc, "value": key})

            Map[keyLoc] = ' '

    for item in keysLoc:
        Map[item["location"]] = item["value"]

    return keysLoc


def findImmunities(Map):
    immunityLocs = []

    for item in ['z', 'f']:
        while item in Map:
            immunityLoc = Map.index(item)
            immunity = Map[immunityLoc]

            immunityLocs.append({"location": immunityLoc, "value": immunity})

            Map[immunityLoc] = ' '

    for item in immunityLocs:
        Map[item["location"]] = item["value"]

    return immunityLocs


def findChips(Map):
    chipsLoc = []

    while 'c' in Map:
        chipLoc = Map.index('c')

        chipsLoc.append(chipLoc)

        Map[chipLoc] = ' '

    for i in range(len(chipsLoc)):
        Map[chipsLoc[i]] = 'c'

    return chipsLoc


def resetItems(Map, keysLoc, immunityLocs, chipsLoc, keysHolder, immunity, chips):
    itemDicts = [keysLoc, immunityLocs]

    for item in immunityLocs:
        Map[item["location"]] = item["value"]

    for item in keysHolder:
        Map[item["location"]] = item["value"]

    for i in range(len(chipsLoc)):
        Map[chipsLoc[i]] = 'c'

    keysHolder.clear()
    immunity.clear()
    chips.clear()

    # return Map

def timer(initialtime):
    endtime = time.time()
    laptime = round((endtime - initialtime), 2)

    return laptime

def Menu():
    print("welcome to Chips Game!")

def main():
    
    currentLevel = 1
    playAgain = True
    starttime = time.time()

    while playAgain:
        Map = levelLoader(currentLevel)

        displayMap(Map)
        print()  # space

        keysHolder = []  # initiate keys inventory
        chips = []
        immunity = []

        keysLoc = findKeys(Map)
        chipsLoc = findChips(Map)
        immunityLocs = findImmunities(Map)
        

        prevTile = ' '
        initialPos = locatePlayer(Map)
        gameOn = True
        levelTime = time.time()
        switcher = True

        while gameOn:
            #keysLoc = findKeys(Map)
            currentLoc = locatePlayer(Map)

            move = getMove()  # gets the player's desired movement
            targetLoc = locateTarget(move, Map)

            addKey(keysHolder, Map, targetLoc)
            #addChip(chips, Map, targetLoc)
            addImmunity(immunity, Map, targetLoc)

            if checkDoor(Map, targetLoc) == True:  # checks if the destination is a door
                door = Map[targetLoc]
                key = door.lower()
                if keyAvailable(door, keysHolder) == True:
                    print('available!')

                    movePlayer(Map, targetLoc, prevTile)
                    prevTile = ' '

                    for item in keysHolder:
                        if item["value"] == key:
                            keysHolder.remove(item)
                            break

                else:
                    print('u need a key!')

            elif Map[targetLoc] == 'c':
                chips.append('c')
                movePlayer(Map, targetLoc, prevTile)
                prevTile = ' '

            elif Map[targetLoc] == 'E':
                if len(chips) == 7:

                    movePlayer(Map, targetLoc, prevTile)
                    prevTile = ' '

                    gameTimeT = timer(starttime)
                    print('\nYour total time is ' + str(gameTimeT))

                    gameTimeI = timer(levelTime)
                    print('Your time for this level is ' + str(gameTimeI))

                    currentLevel += 1

                    score = 600 - gameTimeT
                    print("Your score is" + str(score))
                    break

                else:
                    print("not enough chips :(")

            elif Map[targetLoc] in ['W', 'F']:

                hazard = Map[targetLoc]

                if isImmune(immunity, hazard) == True:

                    movePlayer(Map, targetLoc, prevTile)
                    prevTile = hazard

                else:
                    print('you died')
                    break

            elif isWall(Map, targetLoc):
                pass

            elif Map[targetLoc] == 'o':
                temp = Map[targetLoc]
                moveDoor(Map, switcher)
                movePlayer(Map, targetLoc, prevTile)
                switcher = switching(switcher)
                prevTile = temp

            elif Map[targetLoc] == 'T':
                print('unlucko')

                resetPos(Map, initialPos)
                Map[currentLoc] = ' '
                resetItems(Map, keysLoc, immunityLocs, chipsLoc, keysHolder, immunity, chips)
                prevTile = ' '

            elif Map[targetLoc] in ['>', '<']:
                if move == 'd':
                    if Map[targetLoc] == '<':
                        targetLoc -= 1
                        movePlayer(Map, targetLoc, prevTile)
                    else:
                        while Map[targetLoc] == '>':
                            targetLoc += 1
                        newPrev = Map[targetLoc]
                        movePlayer(Map, targetLoc, prevTile)
                        prevTile = newPrev
                elif move == 'a':
                    if Map[targetLoc] == '>':
                        targetLoc += 1
                    else:
                        while Map[targetLoc] == '<':
                            targetLoc -= 1
                        newPrev = Map[targetLoc]
                        movePlayer(Map, targetLoc, prevTile)
                        prevTile = newPrev

                elif move == 'w':
                    pass
                elif move == 's':
                    pass

            else:  # no door

                movePlayer(Map, targetLoc, prevTile)  # moves the player
                prevTile = ' '

            displayMap(Map)  # displays the current map
            print()

            print("keys:", end=" ")
            print(keysHolder)

            print("chips:", end=" ")
            print(chips)

            print("immunity:", end=" ")
            print(immunity)

            # print("locations of keys: ", end = " ")
            print(prevTile)

        playAgain = gameReset()

    print('Thank you for playing!')


if __name__ == "__main__":
    main()