# largely based off of https://www.kosbie.net/cmu/fall-19/15-112/notes/hw4.html 

class Room(object):
    def __init__(self, name):
        self.name = name
        self.exits = [None] * 6 # north, south, east, west, core, rim
        self.items = [ ]

    def getDirection(self, dirName):
        dirName = dirName.lower()
        if (dirName in ['n', 'north']): return 0
        elif (dirName in ['s', 'south']): return 1
        elif (dirName in ['e', 'east']): return 2
        elif (dirName in ['w', 'west']): return 3
        elif (dirName in ['c', 'core']): return 4
        elif (dirName in ['r', 'rim']): return 5
        else:
            print(f'Sorry, I do not recognize the direction {dirName}')
            return None
    
    def setExit(self, dirName, room):
        direction = self.getDirection(dirName)
        self.exits[direction] = room

    def getExit(self, dirName):
        direction = self.getDirection(dirName)
        if (direction == None):
            return None
        else:
            return self.exits[direction]

    def getAvailableDirNames(self):
        availableDirections = [ ]
        for dirName in ['North', 'South', 'East', 'West', 'Core', 'Rim']:
            if (self.getExit(dirName) != None):
                availableDirections.append(dirName)
        if (availableDirections == [ ]):
            return 'None'
        else:
            return ', '.join(availableDirections)
            
class Item(object):
    def __init__(self, name, shortName):
        self.name = name
        self.shortName = shortName

class Game(object):
    def __init__(self, name, goal, startingRoom, startingInventory):
        self.name = name
        self.goal = goal
        self.room = startingRoom
        self.commandCounter = 0
        self.inventory = startingInventory
        self.gameOver = False

    def getCommand(self):
        self.commandCounter += 1
        response = input(f'[{self.commandCounter}] Your command --> ')
        print()
        if (response == ''): response = 'help'
        responseParts = response.split(' ')
        command = responseParts[0]
        target = '' if (len(responseParts) == 1) else responseParts[1]
        return command, target

    def play(self):
        print(f'Welcome to {self.name}!')
        print(f'Your goal: {self.goal}!')
        print('Just press enter for help.')
        while (not self.gameOver):
            self.doLook()
            command, target = self.getCommand()
            if (command == 'help'): self.doHelp()
            elif (command == 'look'): self.doLook()
            elif (command == 'go'): self.doGo(target)
            elif (command == 'get'): self.doGet(target)
            elif (command == 'put'): self.doPut(target)
            elif (command == 'call'): self.doCall(target)
            elif (command == 'pay'): self.doPay(target)
            elif (command == 'build'): self.doBuild(target)
            elif (command == 'read'): self.doRead(target)
            elif (command == 'quit'): break
            else: print(f'Unknown command: {command}. Enter "help" for help.')
        print('Goodbye!')

    def doHelp(self):
        print('''
Welcome to this fine game!  Here are some commands I know:
    help (print this message)
    look (see what's around you)
    go north (or just 'go n'), go south, go east, go west
    get thing
    put thing
    call thing
    pay thing
    build thing
    read thing
    quit
Have fun!''')

    def printItems(self, items):
        if (len(items) == 0):
            print('Nothing.')
        else:
            itemNames = [item.name for item in items]
            print(', '.join(itemNames))

    def findItem(self, targetItemName, itemList):
        for item in itemList:
            if (item.shortName == targetItemName):
                return item
        return None

    def doLook(self):
        print(f'\nI am in {self.room.name}')
        print(f'I can go these directions: {self.room.getAvailableDirNames()}')
        print('I can see these things: ', end='')
        self.printItems(self.room.items)
        print('I am carrying these things: ', end='')
        self.printItems(self.inventory)
        print()

    def doGo(self, dirName):
        newRoom = self.room.getExit(dirName)
        if (newRoom == None):
            print(f'Sorry, I cannot go in that direction.')
        else:
            self.room = newRoom

    def doGet(self, itemName):
        item = self.findItem(itemName, self.room.items)
        if (item == None):
            print('Sorry, but I do not see that here.')
        elif (itemName == 'sign'):
            print('Try as I might, I cannot pull the sign out of\n'
                    'the ground. It is stuck firmly into Mars\'s\n'
                    'rocky surface. I collapse, out of breath, and\n'
                    'find myself covered in red dust.')
        else:
            self.room.items.remove(item)
            self.inventory.append(item)

    def doPut(self, itemName):
        item = self.findItem(itemName, self.inventory)
        if (item == None):
            print('Sorry, but I do not seem to be carrying that!')
        else:
            self.inventory.remove(item)
            self.room.items.append(item)

    def doCall(self, itemName):
        phone = self.findItem('phone', self.inventory)
        if (itemName.lower() != 'mcdonalds'):
            print('I do not know how to call that!')
        elif (phone == None):
            print('I am not holding a phone!')
        else:
            print('Hello, this is McDonalds. It costs $100 to open a',
                    'franchise. \nLook for your bill to pay.')
            bill = Item('bill for franchise certificate', 'bill')
            self.room.items.append(bill)
            
    def doPay(self, itemName):
        money = self.findItem('money', self.inventory)
        bill = self.findItem('bill', self.inventory)
        if (itemName in ['money', '$100']):
            print('Who do you want to pay?')
        elif (itemName.lower() != 'mcdonalds' and itemName.lower() != 'bill'):
            print('I do not know how to pay that.')
        elif (money == None):
            print('I do not have any money.')
        elif (bill == None):
            print('I do not have the bill.')
        else:
            print('Thank you for your payment! You will receive your'
                    'certificate for your franchise shortly!')
            certificate = Item('certificate for franchise', 'certificate')
            self.inventory.append(certificate)
            self.inventory.remove(money)
    
    def doBuild(self, itemName):
        certificate = self.findItem('certificate', self.inventory)
        if (certificate == None):
            print('I don\'t have a certificate for a franchise.')
        elif (itemName.lower() != 'mcdonalds'):
            print('That won\'t help me save Pluto!')
        elif ('Pluto Save' not in self.room.name):
            print('You can\'t build here!')
        else:
            print('Great job! You saved Pluto by building McDonalds!!!')
            self.gameOver = True
    
    def doRead(self, itemName):
        if (itemName != 'sign'):
            print('I don\'t know how to read that.')
        elif ('Mars Save' not in self.room.name):
            print('I can\'t read that here.')
        else:
            print('The sign reads:\n\n'
                    '"CHEESEBURGERS: THE MORE THE BETTER"\n\n',
                    (' ' * 16) + '-- the Martians')

def playSimpleGame():
    # make rooms
    earthLaunch = Room('Earth Launch Room')
    earthChapter = Room('Earth Save Pluto Chapter HQ')

    marsLaunch = Room('Mars Launch Room')
    marsChapter = Room('Mars Save Pluto Chapter HQ')

    plutoLaunch = Room('Pluto Launch Room')
    plutoChapter = Room('Pluto Save Pluto Chapter HQ')

    # make map
    earthLaunch.setExit('North', earthChapter)
    earthLaunch.setExit('Rim', marsLaunch)
    earthChapter.setExit('South', earthLaunch)

    marsLaunch.setExit('East', marsChapter)
    marsLaunch.setExit('Rim', plutoLaunch)
    marsLaunch.setExit('Core', earthLaunch)
    marsChapter.setExit('West', marsLaunch)

    plutoLaunch.setExit('South', plutoChapter)
    plutoLaunch.setExit('Core', marsLaunch)
    plutoChapter.setExit('North', plutoLaunch)    

    # make items
    money = Item('a $100 bill', 'money')
    phone = Item('a cell phone', 'phone')
    earthChapter.items.append(phone)

    sign = Item('a random sign', 'sign')
    marsChapter.items.append(sign)

    # run game
    game = Game('Saving Pluto',
                'Put Pluto Back on the Map!',
                earthChapter,
                [money])
    game.play()

playSimpleGame()

