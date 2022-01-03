import win32api as a
import os

def getMove():

    while True:
        wKey = a.GetKeyState(0x57)
        aKey = a.GetKeyState(0x41)
        sKey = a.GetKeyState(0x53)
        dKey = a.GetKeyState(0x44)
    
        if wKey < 0:
            move = 'W'
            break
        
        elif aKey < 0:
            move = 'A'
            break
        
        elif sKey < 0:
            move = 'S'
            break
        
        elif dKey < 0:
            move = 'D'
            break

    """while move.lower() not in ['w', 'a', 's', 'd']:
        move = input("Invalid, what is your move? ")"""

    return move.lower()

def levelLoader(currentLevel):
    
    MapsList = ['map1.txt', 'map2.txt', 'map3.txt']
    currentMap = MapsList[currentLevel - 1]
    Map = []
    
    mapFile = open(currentMap , 'r')
    
    for line in mapFile:
        for character in line.strip():
            Map.append(character)

    return Map

def displayMap(Map):
    for i in range(800):
        if((i>0) and (i %40 == 0)):
            print()
        print(Map[i], end = "")
    print()

def locatePlayer(Map):
    loc = Map.index('p')
    return loc

def isWall(Map, targetLoc):
    if Map[targetLoc] == '#':
        return True
    else:
        return False

def addKey(keysHolder, Map, targetLoc):

    if Map[targetLoc] in ['g', 'y']: #checks if there is a key on the tile where the player will move into
        keysHolder.append(Map[targetLoc]) #adds the key to the player's inventory

    return keysHolder #returns a list containing the keys

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

def checkDoor(Map, targetLoc): #checks if the destination is a door

    if Map[targetLoc] in ['G', 'Y']:
        return True

    else:
        return False

def keyAvailable(door, keysHolder):
    key = door.lower()
    if key in keysHolder:
        return True
    else:
        return False

def isImmune(immunity, hazard):
    if hazard == 'W' and 'z' in immunity:
        return True

    elif hazard == 'F' and 'f' in immunity:
        return True

    else:
        return False

def locateTarget(move, Map): #locates the desired position
    playerLoc = locatePlayer(Map) #locates the player on the map
    if move == 'w':
        targetLoc = playerLoc - 40
    elif move == 's':
        targetLoc = playerLoc + 40
    elif move == 'a':
        targetLoc = playerLoc - 1
    elif move == 'd':
        targetLoc = playerLoc + 1

    return targetLoc #returns the the index of the desired position

def slide(move, Map, targetLoc):

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

    return targetLoc


def movePlayer(Map, targetLoc, prevTile):

    playerLoc = locatePlayer(Map)

    if isWall(Map, targetLoc) == True:
        pass

    else:
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

            keysLoc.append({keyLoc: key})

            Map[keyLoc] = ' '

    for item in keysLoc:
        for i in item:
            Map[i] = item[i]

    return keysLoc

def findImmunities(Map):

    immunityLocs = []

    for item in ['z', 'f']:
        while item in Map:
            immunityLoc = Map.index(item)
            immunity = Map[immunityLoc]

            immunityLocs.append({immunityLoc: immunity})

            Map[immunityLoc] = ' '

    for item in immunityLocs:
        for i in item:
            Map[i] = item[i]

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
    
    for itemHolder in itemDicts:
        for item in itemHolder:
            for i in item:
                Map[i] = item[i]

    for i in range(len(chipsLoc)):
        Map[chipsLoc[i]] = 'c'
        
    keysHolder.clear()
    immunity.clear()
    chips.clear()
    
    #return Map

def main():

    #desigMap = 1
    currentLevel = 1
    playAgain = True
    
    while playAgain:
        Map = levelLoader(currentLevel)
        
        displayMap(Map)
        print() #space

        keysHolder = [] #initiate keys inventory
        chips = []
        immunity = []

        #keysLoc = findKeys(Map)
        chipsLoc = findChips(Map)
        immunityLocs = findImmunities(Map)

        prevTile = ' '
        initialPos = locatePlayer(Map)
        gameOn = True

        while gameOn:
            keysLoc = findKeys(Map)
            currentLoc = locatePlayer(Map)
            
            """if prevTile in ['W', 'F']:

                move = getMove() #gets the player's desired movement
                targetLoc = locateTarget(move, Map)

                checkDoor(Map, targetLoc)
                addKey(keysHolder, Map, targetLoc)
                addChip(chips, Map, targetLoc)
                addImmunity(immunity, Map, targetLoc)

                if checkDoor(Map, targetLoc) == True: #checks if the destination is a door
                    door = Map[targetLoc]
                    key = door.lower()
                    if keyAvailable(door, keysHolder) == True:
                        print('available!')


                        movePlayer(Map, targetLoc)
                        Map[currentLoc] = prevTile
                        prevTile = ' '

                        keysHolder.remove(key)

                    else:
                        print('u need a key!')

                elif Map[targetLoc] == 'E':
                    if len(chips) == 7:

                        movePlayer(Map, targetLoc)
                        Map[currentLoc] = prevTile
                        prevTile = ' '

                        currentLevel += 1
                        break
                        
                    else:
                        print("not enough chips :(")

                elif Map[targetLoc] in ['W', 'F']:

                    hazard = Map[targetLoc]
                    if isImmune(immunity, hazard) == True:
                        prevTile = hazard
                        movePlayer(Map, targetLoc)
                        Map[currentLoc] = prevTile

                    else:
                        print('you died')
                        break

                elif Map[targetLoc] == 'T':

                    print('unlucko')
                    #keysHolder.clear()
                    #chips.clear()
                    #immunity.clear()

                    resetPos(Map,initialPos)
                    Map[currentLoc] = prevTile
                    resetItems(Map, keysLoc, immunityLocs, chipsLoc, keysHolder, immunity, chips)
                    
                    prevTile = ' '


                elif Map[targetLoc] in ['>', '<']:
                    slideLoc = slide(move, Map, targetLoc)

                    movePlayer(Map, slideLoc)
                    #Map[currentLoc] = prevTile
                    #prevTile = ' '

                else: #no door

                    movePlayer(Map, targetLoc) #moves the player
                    if isWall(Map, targetLoc) == False:
                        Map[currentLoc] = prevTile
                        prevTile = ' '


            else: #if the previous Tile was not a hazard ##########################################################################################################################
                move = getMove() #gets the player's desired movement
                targetLoc = locateTarget(move, Map)

                checkDoor(Map, targetLoc)
                addKey(keysHolder, Map, targetLoc)
                addChip(chips, Map, targetLoc)
                addImmunity(immunity, Map, targetLoc)

                if checkDoor(Map, targetLoc) == True: #checks if the destination is a door
                    door = Map[targetLoc]
                    key = door.lower()
                    if keyAvailable(door, keysHolder) == True:
                        print('available!')


                        movePlayer(Map, targetLoc)

                        keysHolder.remove(key)

                    else:
                        print('u need a key!')

                elif Map[targetLoc] == 'E':
                    if len(chips) == 7:

                        movePlayer(Map, targetLoc)
                        currentLevel += 1
                        break

                    else:
                        print("not enough chips :(")

                elif Map[targetLoc] in ['W', 'F']:

                    hazard = Map[targetLoc]
                    if isImmune(immunity, hazard) == True:
                        
                        prevTile = hazard
                        movePlayer(Map, targetLoc)

                    else:
                        print('you died')
                        break

                elif Map[targetLoc] == 'T':
                    print('unlucko')
                    
                    resetPos(Map,initialPos)
                    Map[currentLoc] = ' '
                    resetItems(Map, keysLoc, immunityLocs, chipsLoc, keysHolder, immunity, chips)

                elif Map[targetLoc] in ['>', '<']:
                    
                    slideLoc = slide(move, Map, targetLoc)
                    movePlayer(Map, slideLoc)

                else: #no door

                    movePlayer(Map, targetLoc) #moves the player"""
                    
            move = getMove() #gets the player's desired movement
            targetLoc = locateTarget(move, Map)

            #checkDoor(Map, targetLoc)
            addKey(keysHolder, Map, targetLoc)
            addChip(chips, Map, targetLoc)
            addImmunity(immunity, Map, targetLoc)

            if checkDoor(Map, targetLoc) == True: #checks if the destination is a door
                door = Map[targetLoc]
                key = door.lower()
                if keyAvailable(door, keysHolder) == True:
                    print('available!')

                    movePlayer(Map, targetLoc, prevTile)
                    prevTile = ' '
                    
                    keysHolder.remove(key)

                else:
                    print('u need a key!')

            elif Map[targetLoc] == 'E':
                if len(chips) == 7:

                    movePlayer(Map, targetLoc, prevTile)
                    prevTile = ' '
                    
                    currentLevel += 1
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

            elif Map[targetLoc] == 'T':
                print('unlucko')
                    
                resetPos(Map,initialPos)
                Map[currentLoc] = ' '
                resetItems(Map, keysLoc, immunityLocs, chipsLoc, keysHolder, immunity, chips)
                prevTile = ' '

            elif Map[targetLoc] in ['>', '<']:
                    
                slideLoc = slide(move, Map, targetLoc)
                newPrev = Map[slideLoc]
                movePlayer(Map, slideLoc, prevTile)
                prevTile = newPrev

            else: #no door

                movePlayer(Map, targetLoc, prevTile) #moves the player
                prevTile = ' '

            displayMap(Map) #displays the current map
            print()

            print("keys:", end = " ")
            print(keysHolder)

            print("chips:", end = " ")
            print(chips)

            print("immunity:", end=" ")
            print(immunity)

            #print("locations of keys: ", end = " ")
            print(prevTile)
            
        playAgain = gameReset()

    print('Thank you for playing!')

if __name__ == "__main__":
    main()
