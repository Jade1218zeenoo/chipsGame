import win32api as a
import time
import os


def getMove():
    '''
    Description:        takes desired move of player (w, a, s, d)
    Argument:           None
    Return:
        move.lower()    returns desired move of player in lowercase
    '''

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
    '''
    Description:        retrieves the .txt file where the maps are stored
    Argument:
        currentLevel    used to dictate which .txt file to be used
    Return:
        Map             returns contents of the .txt file as a list
    '''

    MapsList = ['map1.txt', 'map2.txt', 'map3.txt']
    currentMap = MapsList[currentLevel - 1]
    Map = []

    mapFile = open(currentMap, 'r')

    for line in mapFile:
        for character in line.strip():
            Map.append(character)

    return Map


def displayMap(Map):
    '''
    Description:        prints the contents of Map in a 40 x 20 format
    Argument:
        Map             map used for the game
    Return:             None
    '''
    print()
    for i in range(800):
        if ((i > 0) and (i % 40 == 0)):
            print()
        print(Map[i], end="")
    print()


def locatePlayer(Map):
    '''
    Description:        locates player in map
    Argument:
        Map             map used for the game
    Return:
        loc             returns player index
    '''
    loc = Map.index('p')
    return loc


def isWall(Map, targetLoc):
    '''
    Description:        checks if the desired destination is a wall
    Argument:
        Map             map used for the game
        targetLoc       index of player's desired location
    Return:
        True            returns boolean indicating desired location is a wall
        False           returns boolean indicating desired location is not a wall
    '''
    if Map[targetLoc] == '#':
        return True
    else:
        return False


def isGate(Map, targetLoc):
    '''
    Description:        checks if the desired destination is a gate
    Argument:
        Map             map used for the game
        targetLoc       index of player's desired location
    Return:
        True            returns boolean indicating desired location is a gate
        False           returns boolean indicating desired location is not a gate
    '''
    if Map[targetLoc] == 'O':
        return True
    else:
        return False


def switching(switcher):
    '''
    Description:        switches the direction of the gate
    Argument:
        switcher        indicates if the direction of the gate
    Return:
        switcher        returns boolean that indicates new direction of the gate
    '''
    if switcher == True:
        switcher = False
    else:
        switcher = True

    return switcher


def moveGate(Map, switcher):
    '''
    Description:        moves gate to the left or right
    Argument:
        Map             map used for the game
        switcher        used to check if the gate is to move left or right
    Return:             None
    '''
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
    '''
    Description:        adds available key to list
    Argument:
        keysHolder      list that will contain keys
        Map             map used for the game
        targetLoc       index of player's desired location
    Return:
        keysHolder      returns list containing new keys
    '''
    if Map[targetLoc] in ['g', 'y']:  # checks if there is a key on the tile where the player will move into
        keysHolder.append({"location": targetLoc, "value": Map[targetLoc]})  # adds the key to the player's inventory

    return keysHolder


def addChip(chips, Map, targetLoc):
    '''
    Description:        adds available chips to list
    Argument:
        chips           list that will contain chips
        Map             map used for the game
        targetLoc       index of player's desired location
    Return:
        chips           returns list containing new chips
    '''
    if Map[targetLoc] == 'c':
        chips.append('c')
    return chips


def addImmunity(immunity, Map, targetLoc):
    '''
    Description:        adds available immunities to list
    Argument:
        immunity        list that will contain immunities
        Map             map used for the game
        targetLoc       index of player's desired location
    Return:
        immunity        returns list containing new immunities
    '''
    if Map[targetLoc] in ['z']:
        immunity.append(Map[targetLoc])
    if Map[targetLoc] in ['f']:
        immunity.append(Map[targetLoc])

    return immunity


def checkDoor(Map, targetLoc):  # checks if the destination is a door
    '''
    Description:        checks if the desired destination is a door
    Argument:
        Map             map used for the game
        targetLoc       index of player's desired location
    Return:
        True            returns boolean indicating desired location is a door
        False           returns boolean indicating desired location is not a door
    '''
    if Map[targetLoc] in ['G', 'Y']:
        return True

    else:
        return False


def keyAvailable(door, keysHolder):
    '''
    Description:        checks if the appropriate key is available in the list
    Argument:
        door            desired location of player is a door
        keysHolder      list of available keys
    Return:
        True            returns boolean indicating appropriate key is available
        False           returns boolean indicating appropriate key is not available
    '''
    key = door.lower()
    for item in keysHolder:
        if item["value"] == key:
            return True

    return False


def isImmune(immunity, hazard):
    '''
    Description:        checks if appropriate immunity is available for an element tile
    Argument:
        immunity        list of available immunities
        hazard          desired location of player is an element tile
    Return:
        True            returns boolean indicating appropriate immunity is available
        False           returns boolean indicating appropriate immunity is not available
    '''
    if hazard == 'W' and 'z' in immunity:
        return True

    elif hazard == 'F' and 'f' in immunity:
        return True

    else:
        return False


def locateTarget(move, Map):
    '''
    Description:        locates player's desired move in map
    Argument:
        move            player's desired move
        Map             map used for the game
    Return:
        targetLoc       returns index of desired position
    '''
    playerLoc = locatePlayer(Map)  # locates the player on the map
    if move == 'w':
        targetLoc = playerLoc - 40
    elif move == 's':
        targetLoc = playerLoc + 40
    elif move == 'a':
        targetLoc = playerLoc - 1
    elif move == 'd':
        targetLoc = playerLoc + 1

    return targetLoc

def movePlayer(Map, targetLoc, prevTile):
    '''
    Description:        moves player to the desired destination
    Argument:
        Map             map used for the game
        targetLoc       index of player's desired location
        prevTile        character that will replace player's current position
    Return:
        Map             returns map with player moved to desired destination
    '''
    playerLoc = locatePlayer(Map)

    Map[playerLoc] = prevTile
    Map[targetLoc] = 'p'

    return Map


def resetPos(Map, initialPos):
    '''
    Description:        resets player position
    Argument:
        Map             map used for the game
        initialPos      index of player at the beginning of the game
    Return:
        targetLoc       returns map wherein player is at its starting position
    '''
    # playerLoc = locatePlayer(Map)
    Map[initialPos] = 'p'
    return Map


def gameReset():
    '''
    Description:        resets whole map
    Argument:           None
    Return:
        True            returns boolean that activates while loop again
    '''
    return True


def findKeys(Map):
    '''
    Description:        locates keys within map
    Argument:
        Map             map used for the game
    Return:
        keysLocs        returns index of each key
    '''
    keysLoc = []

    for item in ['y', 'g']:
        while item in Map:
            keyLoc = Map.index(item)
            key = Map[keyLoc]

            keysLoc.append({"location": keyLoc, "value": key})

            Map[keyLoc] = ' '

    for item in keysLoc:
        Map[item["location"]] = item["value"]

    return keysLoc


def findImmunities(Map):
    '''
    Description:        locates immunities within map
    Argument:
        Map             map used for the game
    Return:
        immunityLocs    returns the index of each immunity
    '''
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
    '''
    Description:        locates chips within map
    Argument:
        Map             map used for the game
    Return:
        chipsLoc        returns list of chips' indeces
    '''
    chipsLoc = []

    while 'c' in Map:
        chipLoc = Map.index('c')

        chipsLoc.append(chipLoc)

        Map[chipLoc] = ' '

    for i in range(len(chipsLoc)):
        Map[chipsLoc[i]] = 'c'

    return chipsLoc


def resetItems(Map, keysLoc, immunityLocs, chipsLoc, keysHolder, immunity, chips):
    '''
    Description:        removes all items in player's inventory
    Argument:
        Map             map used for the game
        keysLoc         indeces of keys' initial location
        immunityLocs    indeces of immunities' initial location
        chipsLoc        indeces of chips' initial location
        keysHolder      list of available keys
        immunity        list of available immunities
        chips           list of available chips
    Return:             None
    '''
    # itemDicts = [keysLoc, immunityLocs]

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
    '''
    Description:        serves as the timer for the game
    Argument:
        initialtime     starting time of the game
    Return:
        targetLoc       returns gameplay time in seconds
    '''
    endtime = time.time()
    laptime = round((endtime - initialtime), 2)

    return laptime


def game():
    '''
    Description:        contains while loops which keeps the game running until the last map
    Argument:           None
    Return:             None
    '''
    currentLevel = 1
    playAgain = True
    starttime = time.time()

    if currentLevel > 3:
        print("Congratulations! You finished the game. ")

    while playAgain:
        if currentLevel == 4:
            break
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
            # keysLoc = findKeys(Map)
            currentLoc = locatePlayer(Map)

            move = getMove()  # gets the player's desired movement
            targetLoc = locateTarget(move, Map)

            addKey(keysHolder, Map, targetLoc)
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
                    print('You need a key!')

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
                    print("Your score is " + str(score))
                    break

                else:
                    print("You don't have enough chips. :(")

            elif Map[targetLoc] in ['W', 'F']:

                hazard = Map[targetLoc]

                if isImmune(immunity, hazard) == True:

                    movePlayer(Map, targetLoc, prevTile)
                    prevTile = hazard

                else:
                    print('You died. :(')
                    break

            elif isWall(Map, targetLoc):
                pass

            elif isGate(Map, targetLoc):
                pass

            elif Map[targetLoc] == 'o':
                temp = Map[targetLoc]
                moveGate(Map, switcher)
                movePlayer(Map, targetLoc, prevTile)
                switcher = switching(switcher)
                prevTile = temp

            elif Map[targetLoc] == 'T':
                print('Your items were stolen, unlocko. :(')

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

            else:  # blank tile

                movePlayer(Map, targetLoc, prevTile)  # moves the player
                prevTile = ' '

            os.system('cls')
            displayMap(Map)  # displays the current map
            print()

            print("keys:", end=" ")
            print(keysHolder)

            print("chips:", end=" ")
            print(chips)
            print(f'You now have {len(chips)} chip/s. ' + 'You need 7 chips to exit this map.')

            print("immunity:", end=" ")
            print(immunity)

        playAgain = gameReset()

    print('Thank you for playing!')

def main():
    '''
    Description:        displays the main screen; asks the player to press the enter key to start the game
    Argument:           none
    Return:             none
        
    '''
    gameStart = False

    print("Welcome to Chips Game!")
    print("Press the enter key to start.")

    while True:
        enterKey = a.GetKeyState(0x0D)

        if enterKey < 0:
            gameStart = True
            time.sleep(0.15)
            break

    if gameStart == True:
        os.system('cls')
        game()

if __name__ == "__main__":
    main()