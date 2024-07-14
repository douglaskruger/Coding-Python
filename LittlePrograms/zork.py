# Welcome to the Great Underground Empire, a land of magic and mystery.
# You are an brave adventurer seeking fortune and glory.

import readline

class Player:
    def __init__(self):
        self.inventory = ["bottle of water", "pocket knife"]
        self.health = 100

    def take(self, item):
        self.inventory.append(item)

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
        else:
            print("You don't have that item.")

    def has(self, item):
        return item in self.inventory


class Room:
    def __init__(self, description, items):
        self.description = description
        self.items = items
        self.exits = {}

    def add_exit(self, direction, room):
        self.exits[direction] = room


# Create the player
player = Player()

# Create the rooms
west_of_house = Room("You are standing in a dimly lit chamber, the walls made of rough-hewn stone blocks. The air is musty and dank, and the only light comes from a small torch flickering on the wall.", ["torch"])
north_of_house = Room("You are facing the north side of a white house. There is no door here, and all the windows are boarded up. To the north a dark forest looms.", [])
south_of_house = Room("You are facing the south side of a white house. There is a small window which is slightly ajar.", [])
kitchen = Room("You are in the kitchen of the white house. A table seems to have been used recently for the preparation of a meal, but the chairs are pushed back as if the diners had left in a hurry.", ["bottle of water"])
attic = Room("You are in the attic of the white house.There is a pile of old clothes in the corner, and a trunk bolted shut.", ["trunk"])
forest_1 = Room("This is a forest, with trees in all directions. To the east, there appears to be sunlight.", [])
forest_2 = Room("This is a forest, with trees in all directions. To the west, there appears to be sunlight.", [])
cave_entrance = Room("You are standing at the entrance of a dark cave. The air is musty and dank, and the only light comes from a small torch flickering on the wall.", ["torch"])
cave_tunnel = Room("You are in a narrow tunnel. The air is musty and dank, and the only light comes from a small torch flickering on the wall.", [])
cave_chamber = Room("You are in a large underground chamber. There is a chest in the center of the room.", ["chest"])

# Connect the rooms
west_of_house.add_exit("east", north_of_house)
west_of_house.add_exit("south", south_of_house)
north_of_house.add_exit("west", west_of_house)
north_of_house.add_exit("north", forest_1)
north_of_house.add_exit("south", south_of_house)
south_of_house.add_exit("north", north_of_house)
south_of_house.add_exit("south", kitchen)
south_of_house.add_exit("west", west_of_house)
kitchen.add_exit("north", south_of_house)
kitchen.add_exit("up", attic)
attic.add_exit("down", kitchen)
forest_1.add_exit("east", forest_2)
forest_1.add_exit("south", north_of_house)
forest_2.add_exit("west", forest_1)
cave_entrance.add_exit("north", cave_tunnel)
cave_tunnel.add_exit("south", cave_entrance)
cave_tunnel.add_exit("north", cave_chamber)
cave_chamber.add_exit("south", cave_tunnel)
west_of_house.add_exit("down", cave_entrance)
cave_entrance.add_exit("up", west_of_house)

# Starting room
current_room = west_of_house

# Game loop
while True:
    try:
        # Print the current room's description
        print(current_room.description)

        # Get the player's command
        command = input("> ")

        # Add the command to the history
        readline.add_history(command)

        # Parse the command
        command = command.split()

        if command[0] == "go":
            direction = command[1]
            if direction == "n" or direction == "north":
                direction = "north"
            elif direction == "s" or direction == "south":
                direction = "south"
            elif direction == "e" or direction == "east":
                direction = "east"
            elif direction == "w" or direction == "west":
                direction = "west"
            elif direction == "u" or direction == "up":
                direction = "up"
            elif direction == "d" or direction == "down":
                direction = "down"

            if direction in current_room.exits:
                current_room = current_room.exits[direction]
            else:
                print("You can't go that way.")
        elif command[0] == "take":
            if command[1] in current_room.items:
                player.take(command[1])
                current_room.items.remove(command[1])
            else:
                print("That item is not here.")
        elif command[0] == "drop":
            player.drop(command[1])
        elif command[0] == "inventory":
            print("You have: " + str(player.inventory))
        elif command[0] == "health":
            print("Your health is: " + str(player.health))
        elif command[0] == "look":
            print(current_room.description)
        elif command[0] == "quit":
            break
        else:
            print("Invalid command. Type 'go <direction>' to move, 'take <item>' to take an item, 'drop <item>' to drop an item, 'inventory' to view your inventory, 'look' to look around, or 'quit' to quit the game.")
    except IndexError:
        print("Invalid command. Type 'go <direction>' to move, 'take <item>' to take an item, 'drop <item>' to drop an item, 'inventory' to view your inventory, 'look' to look around, or 'quit' to quit the game.")
    except Exception as e:
        print("An error occurred: " + str(e))
