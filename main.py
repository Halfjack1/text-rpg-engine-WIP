import random

maxHp = 7
hp = maxHp
maxMana = 5
mana = maxMana
attention = 0
light = False
currentRoom = 0
turns = 0
inventory = ["spellbook", "dagger"]
gold = 10
currentEnemy = 0
shieldEnd = 0
shield = False
level = 1
invisibility = 0
spellList = ["light", "firebolt", "knock", "shield"]
unKnownSpells = ["fireblast", "invisibility"]
Rooms = []

#actions
def doAction(action):
  global turns
  global attention
  if action == "inventory":
    checkInv()
  elif action == "hide":
    turns += 1
    hide()
  elif action == "look":
    look()
  elif action == "wait":
    turns += 1
    print("Time passes")
  elif action.lower().startswith("take") and not currentRoom.Title == "store":
    take(action.lower()[5:])
  elif action.lower().startswith("go to"):
    goto(action.lower()[6:])
  elif action.lower() == "search":
    turns += 1
    attention += 1
    print(currentRoom.SearchDesc)
    currentRoom.SearchDesc = "you find nothing you didn't previously find"
  elif action[0:3].lower() == "use":
    obj = action[4:len(action)].lower()
    if obj in inventory:
      turns += 1
      useObject(obj)
    else:
      print("You don't have a " + obj)
  elif action[0:4].lower() == "cast":
    spell = action[5:len(action)].lower()
    if spell in spellList:
      turns += 1
      castSpell(spell)
    else:
      print("You don't have the spell " + spell)
  elif action[0:3].lower() == "buy":
    buy(action[4:len(action)].lower())
  else:
    print("you can't do that")
  print()

def checkInv():
  print("You have:")
  for i in range(0, len(inventory)):
    print(inventory[i])
  print()

def hide():
  global light
  global attention
  if not light:
    attention = max(attention-2, 0)
    print("you avoid others' attention")
  else:
    print("your floating light makes it impossible to hide")

def look():
  print(currentRoom.description)
  if currentEnemy.active:
    print("There is also a " + currentEnemy.title + " attacking you.")

def useObject(obj):
  if obj == "spellbook":
    print("Your spellbook has the spells:")
    for i in range(0, len(spellList)):
      print(spellList[i])
    print()
  elif obj == "spell scroll":
    temp = random.choice(unKnownSpells)
    unKnownSpells.remove(temp)
    spellList.append(temp)

  #potions
  elif obj == "health potion":
    inventory.remove(obj)
    global hp
    global maxHp
    hp = maxHp
  elif obj == "mana potion":
    global mana
    global maxMana
    inventory.remove(obj)
    mana = maxMana

  #weapons
  elif obj == "dagger":
    if currentEnemy.active:
      temp = random.randint(1,4)
      print("your dagger strikes the " + currentEnemy.title + ", dealing " + str(temp) + " damage.")
      if light:
        temp += level
      currentEnemy.hitPoints -= temp
    else:
      print("there is nothing to use the dagger on.")
  elif obj == "shortsword":
    if currentEnemy.active:
      temp = random.randint(1,6)
      print("your shortsword strikes the " + currentEnemy.title + ", dealing " + str(temp) + " damage.")
      if light:
        temp += level
      currentEnemy.hitPoints -= temp
    else:
      print("there is nothing to use the shortsword on.")
  elif obj == "stick":
    if currentEnemy.active:
      temp = random.randint(1000,9999)
      print("your stick strikes the " + currentEnemy.title + ", dealing " + str(temp) + " damage.")
      if light:
        temp += level
      currentEnemy.hitPoints -= temp
    else:
      print("there is nothing to use the stick on.")
  else:
    print("you can't use " + obj + " here.")

def castSpell(spell):
  global attention
  global level
  global mana
  global turns
  global shieldEnd
  global shield
  global light
  global invisibility
  if spell == "light":
    light = not light
    if light:
      print("You summon a small floating light")
      attention += 3
    else:
      print("Your light disappears")
      attention -= 3
  elif spell == "shield" and mana > 0:
    print("You summon a magical shield that will temporarily protect you")
    mana -= 1
    shieldEnd = turns + 5
    shield = True
  elif spell == "firebolt" and mana > 0:
    if currentEnemy.active:
      mana -= 1
      attention += 1
      temp = 0
      for i in range(0, 1 + level):
        temp += random.randint(1,4)
      print("Your firebolt strikes the " + currentEnemy.title + ", dealing " + str(temp) + " damage.")
      currentEnemy.hitPoints -= temp
    else:
      print("There is nothing to use firebolt on.")
  elif spell == "fireblast" and mana > 2:
    if currentEnemy.active:
      mana -= 3
      attention += 2
      temp = 0
      for i in range(0, 1 + level):
        temp += random.randint(3,6)
      print("Your fireblast strikes the " + currentEnemy.title + ", dealing " + str(temp) + " damage.")
      currentEnemy.hitPoints -= temp
    else:
      print("There is nothing to use fireblast on.")
  elif spell == "invisibility" and mana > 1:
    if light:
      print("Your floating light makes invisibility worthless")
    else:
      mana -= 2
      invisibility = turns + 5
      print("you are now temporarily invisible")
  else:
    print("You don't have enough mana")

def buy(obj):
  global turns
  global attention
  if currentRoom.Title == "store":
    targetFound = False
    for item in currentRoom.RoomInventory:
      if item.title.lower() == obj:
        targetFound = True
        turns += 1
        global inventory
        if gold >= item.cost:
          inventory.append(item.title)
          gold -= item.cost
          print("You buy the " + item.title + ".")
          attention += 1
        else:
          print("You don't have enough gold to buy that.")
    if targetFound == False:
      print ("No " + obj + " to buy here.")
  else:
    print("you can't buy anything here")

def sell(obj):
  global turns
  global gold
  if currentRoom.Title == "store":
    if obj in inventory:
      inventory.remove(obj)
      gold += 1
      print("you sell your " + obj + ".")
    else:
      print("You don't have a " + obj + " to sell.")
  else:
    print("You can't sell anything here")

def take(target):
  targetFound = False
  global turns
  for item in currentRoom.RoomInventory:
    if item.lower() == target:
      targetFound = True
      turns += 1
      global inventory
      if item == "coin":
        global gold
        gold += 1
      else:
        inventory.append(item)
      currentRoom.RoomInventory.remove(item)
      print("You take the " + item + ".")
  if targetFound == False:
    print ("No " + target + " to pick up!")

def goto(target):
  global turns
  if not currentEnemy.active:
    turns += 1
    targetFound = False
    for exit in currentRoom.Exits:
      if exit.Title.lower() == target:
        targetFound=True
        enterRoom(exit)
    if targetFound == False:
      print ("Unable to enter: " + target)
  else:
    print("A " + currentEnemy.title + " is preventing you from leaving this area")

def enterRoom(room):
  global currentRoom
  global currentEnemy
  currentRoom = room
  currentEnemy = currentRoom.enemy
  doAction("look")

def enemyAttacks(enem):
  global hp
  global shield
  global level
  
  temp = random.randint(enem.minDamage, enem.maxDamage)
  if shield:
    temp = max(temp - level, 0)
  print("The " + currentEnemy.title + " attacks, dealing " + str(temp) + " damage.")
  hp -= temp



#classes
class enemy:
  def __init__(self, ID, Title, hitPoints, minDamage, maxDamage, attention, gear):
    self.ID = ID
    self.title = Title
    self.hitPoints = hitPoints
    self.minDamage = minDamage
    self.maxDamage = maxDamage
    self.attention = attention
    self.active = False
    self.gear = gear
class room:
  def __init__(self, ID, Title, Exits, description, RoomInventory, SearchDesc, enemy):
    self.ID = ID
    self.Title = Title
    self.description = description
    self.Exits = Exits
    self.RoomInventory = RoomInventory
    self.SearchDesc = SearchDesc
    self.enemy = enemy
class purchasable:
  def __init__(self, Title, Cost):
    self.title = Title
    self.cost = Cost
#Enemies

#none/Easter egg1
noEnemy = enemy(0, "God of Death", 100, 1000, 9999, 100, ["stick"])
#thug
thug = enemy(1,"thug", 4, 1, 4, 4, ["dagger", "coin"])


#purchasables
spellScroll = purchasable("spell scroll", 5) 
shortSword = purchasable("shortsword", 3) 
hPotion = purchasable("health potion", 2) 
mPotion = purchasable("mana potion", 2) 
wFirebolt = purchasable("wand of firebolt", 20) 

#Rooms

#Home
Exits = []
RoomInventory = ["lockpicks"]
roomHome = room(1, "Home", Exits, "This is your |home|.\nIt's not a particularly nice house, but it's a house.\nOutside is the |market|.", RoomInventory, "You find the box that holds your |lockpicks|, if you haven't taken them yet", noEnemy)
Rooms.append(roomHome)
#market
Exits = []
RoomInventory = ["coin"]
roomMarket = room(2, "market", Exits, "This is the |market|.\nYou can return |home| or go to the |store| from here", RoomInventory, "You find a gold |coin| on the ground", thug)
Rooms.append(roomHome)
#store
Exits = []
RoomInventory = [spellScroll, shortSword, hPotion, mPotion, wFirebolt]
roomStore = room(3, "store", Exits, "This is a |store|.\nthere are several things for sale here, including:\nA |spell scroll|(5 gold)\nA |shortsword|(3 gold)\nA |health potion|(2 gold)\nA |mana potion|(2 gold)\nYou can return to the |market| from here", RoomInventory, "You find a |wand of firebolt|(20 gold) for sale", noEnemy)
Rooms.append(roomStore)


#Exits
roomHome.Exits.append(roomMarket)
roomMarket.Exits.append(roomHome)
roomMarket.Exits.append(roomStore)
roomStore.Exits.append(roomMarket)

enterRoom(roomHome)
while hp > 0:
  temp1 = turns
  if currentEnemy.hitPoints > 0 and attention >= currentEnemy.attention:
    if not currentEnemy.active:
      print("A " + currentEnemy.title + " appears and attacks you!\n")
    currentEnemy.active = True
  print("HP: " + str(hp) + "/" + str(maxHp) + "    Mana: " + str(mana) + "/" + str(maxMana) + "    Gold: " + str(gold) + "    Attention: " + str(attention) + "    Time: " + str(turns) + "    Level: " + str(level));
    
  action = input("\nWhat do you do?\n> ")
  doAction(action)

  if currentEnemy.hitPoints < 1 and currentEnemy.active:
    currentEnemy.active = False
    print("The " + currentEnemy.title + " dies.\n")
    for i in range(0,len(currentEnemy.gear)):
      print("The " + currentEnemy.title + " dropped a |" + currentEnemy.gear[i] + "|.")
      currentRoom.RoomInventory.append(currentEnemy.gear[i])
  if shield and shieldEnd < turns:
    shield = False
    print("Your shield spell ends")
  if invisibility > turns and not light:
    attention = 0
  if currentEnemy.active and not temp1 == turns:
    enemyAttacks(currentEnemy)
  if (turns % 5) == 0 and attention > 0 and not light:
    attention -= 1

print("\nAlas, you succumb to your wounds")