import random

def start_game():
    print("Welcome to the Text Adventure!")
    print("You find yourself in a dark forest. There's a faint path to the north.")
    global current_room  # Declare current_room as global
    current_room = "forest"
    inventory = []
    max_inventory_size = 4  # Set the max inventory size
    troll_appearance_range = (10, 25)  # Range for troll appearance (inclusive)
    troll_move_counter = 0
    lamp_lit = False
    lamp_duration = 20  # Number of moves the lamp stays lit

    while True:
        action = input("What would you like to do? (n, s, e, w, u, d, get [item], inventory, quit): ").lower()

        if action == "quit":
            print("Thanks for playing!")
            break
        if lamp_lit:
            lamp_duration -= 1
            if lamp_duration == 0:
                lamp_lit = False
                print("Your lamp flickers and goes out.")

        if action in ["n", "s", "e", "w", "u", "d"]:
            move_player(action)
        elif action.startswith("get "):
            item = action[4:]
            get_item(item, inventory, max_inventory_size) # Add max_inventory_size
        elif action == "inventory":
            show_inventory(inventory)
        elif action == "light lamp" and "lamp" in inventory and "matches" in inventory:
            if not lamp_lit:
                lamp_lit = True
                lamp_duration = 20  # Reset duration
                inventory.remove("matches")  # Consume the matches
                print("You light the lamp.")
            else:
                print("The lamp is already lit.")
        else:
            print("I don't understand that command.")
        troll_move_counter += 1
        if troll_move_counter in range(*troll_appearance_range):  # Check for troll appearance
            troll_attack(inventory)
            troll_move_counter = 0  # Reset troll counter

def troll_attack(inventory):
    if inventory:
        print("A troll jumps out from the shadows and snatches your belongings!")
        stolen_items = inventory.copy()  # Copy the inventory for troll loot
        inventory.clear()  # Empty the player's inventory
        rooms["building_room1"]["items"].extend(stolen_items)  # Add stolen items to room 1
        print("The troll laughs maniacally before disappearing with your treasures!")
    else:
        print("A troll appears, but seeing your empty pockets, lets out a disappointed growl and vanishes.")

def move_player(direction):
    global current_room  # Declare current_room as global
    global rooms

    new_room = rooms[current_room].get(direction)
    if 'cavern' in new_room and not lamp_lit:
        print("The cave is too dark to enter. You need a light source.")
        return  # Prevent movement into the cave

    if new_room is not None:
        current_room = new_room
        print(rooms[current_room]["description"])
    else:
        print("You can't go that way.")


def get_item(item, inventory, max_inventory_size):
    global current_room
    global rooms

    if item in rooms[current_room]["items"]:
        if len(inventory) < max_inventory_size:  # Check if inventory has space
            inventory.append(item)
            rooms[current_room]["items"].remove(item)
            print(f"You picked up the {item}.")
        else:
            print("Your inventory is full. You can't carry any more items.")
    else:
        print(f"I don't see a {item} here.")


def show_inventory(inventory):
    if inventory:
        print("You are carrying:")
        for item in inventory:
            print(item)
    else:
        print("Your inventory is empty.")


# ------------------- Game Setup ----------------------
rooms = {
    "forest": {
        "description": "You are in a dark forest. A path leads north. Sunlight barely peeks through the dense leaves above.",
        "items": ["stick"],
        "n": "clearing"
    },
    "clearing": {
        "description": "You are in a small clearing. There is a well to the east, a path back into the forest to the south, and a rickety old building to the west.",
        "items": ["rope"],
        "e": "well",
        "s": "forest",
        "w": "building_entrance"
    },
    "well": {
        "description": "You stand at the edge of an old well. It looks deep and dark. The path leads back west. A crack in the side of the well leads downward into darkness. There's a box of matches here.",
        "items": ["matches"],  # Add matches
        "w": "clearing",
        "d": "cavern"
    },
    "cavern": {
        "description": "You have descended into a damp, musty cavern. Faint light filters in from above.",
        "items": ["shiny rock"],
        "u": "well"
    },
    # Building Rooms
    "building_entrance": {
        "description": "You're in the entrance of a dilapidated building. The floor is covered in dust and debris. There are doors to the north, east, and west.",
        "items": [],
        "n": "building_room1",
        "e": "building_room2",
        "w": "building_room3"
    },
    "building_room1": {
        "description": "This room is empty except for a broken table in the corner. There's a lamp on the floor.",
        "items": ["lamp"],  # Add the lamp here
        "s": "building_entrance"
    },
    "building_room2": {
        "description": "Old cobwebs fill this room. There's a rusty key and a shovel on the floor.",
        "items": ["rusty key", "shovel"],  # Add the shovel here
        "w": "building_entrance"
    },
    "building_room3": {
        "description": "This room looks like it was a kitchen. A locked chest sits against the far wall.",
        "items": ["locked chest"],
        "e": "building_entrance"
    },
    # Labyrinth
    "cavern_chamber1": {
        "description": "The cavern opens into a wider chamber. There are passages leading west and south.",
        "items": [],
        "w": "cavern_chamber2",
        "s": "cavern_chamber3"
    },
    "cavern_chamber2": {
        "description": "Odd symbols are scratched onto the walls of this chamber.",
        "items": [],
        "e": "cavern_chamber1"
    },
    "cavern_chamber3": {
        "description": "A faint breeze comes from a passage to the east.",
        "items": [],
        "n": "cavern_chamber1",
        "e": "cavern_chamber4"
    },
    "cavern_chamber4": {
        "description": "The air is colder here. You see a glimmer of light ahead.",
        "items": ["glowing orb"],
        "w": "cavern_chamber3"
    }
}

# Start the game
start_game()