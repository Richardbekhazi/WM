from adventurelib import Room, Bag, Item, when, start, say
# Removed 'exit as a_exit_builtin_conflict_resolver'

# Global variable to keep track of the current room
current_room = None

# Player inventory
inventory = Bag()

# --- AdventureLib Room definitions ---

start_location = Room("Initial description for start_location") # Temp, overwritten below
cave = Room("Initial description for cave")
forest = Room("Initial description for forest")
clearing = Room("Initial description for clearing")
treasure_room = Room("Initial description for treasure_room")

# Assigning custom data using the .data dictionary
start_location.data = {
    "desc_first_visit": "You find yourself in a bright, grassy field under a clear blue sky. A well-trodden path leads north, inviting adventure.",
    "desc_subsequent_visit": "You are back at the starting field. The path to the north still beckons.",
    "visited": False,
    "items": Bag()
}
# Set initial description for AdventureLib's start()
start_location.description = start_location.data["desc_first_visit"]

cave.data = {
    "desc_first_visit": "The entrance to the cave is a dark, ominous maw in the mountainside. Cold air wafts out, carrying the faint sound of dripping water and distant bat screeches. It looks spooky.",
    "desc_subsequent_visit": "You are at the cave entrance again. The darkness within feels familiar now, but no less chilling.",
    "visited": False,
    "event_on_entry": "As you step into the cave, a faint scratching sound echoes from the darkness.",
    "locked_exit_direction": 'east',
    "locked_exit_room": treasure_room,
    "locked_exit_key_name": 'rusty key',
    "locked_exit_description": 'A sturdy wooden door to the east seems locked.',
    "locked_exit_unlocked": False,
    "items": Bag()
}
cave.description = cave.data["desc_first_visit"]

forest.data = {
    "desc_first_visit": "You are in a dense forest. Sunlight filters weakly through the canopy. Paths lead south and east.",
    "desc_subsequent_visit": "You are back in the dense forest. Paths lead south and east.",
    "visited": False,
    "event_on_entry": "A twig snaps nearby, but you see nothing.",
    "items": Bag([
        Item('rusty key', 'key')
    ])
}
forest.description = forest.data["desc_first_visit"]

clearing.data = {
    "desc_first_visit": "You step into a small, sunlit clearing. It feels peaceful here. A narrow path leads west.",
    "desc_subsequent_visit": "You are in the peaceful, sunlit clearing. A path leads west.",
    "visited": False,
    "items": Bag([
        Item('shiny rock', 'rock')
    ])
}
clearing.description = clearing.data["desc_first_visit"]

treasure_room.data = {
    "desc_first_visit": "You've found the treasure room! A small, dusty chest sits in the center.",
    "desc_subsequent_visit": "You are back in the treasure room. The chest is still here.",
    "visited": False,
    "items": Bag([
        Item('gold coins', 'coins', 'gold')
    ])
}
treasure_room.description = treasure_room.data["desc_first_visit"]

# Define Exits
start_location.north = cave
cave.south = start_location
cave.north = forest
forest.south = cave
forest.east = clearing
clearing.west = forest
treasure_room.west = cave

# Set initial current_room for AdventureLib
current_room = start_location

# --- AdventureLib Command Functions ---

@when('look')
@when('l')
def look_around():
    global current_room
    room_data = current_room.data

    # Determine appropriate description based on visited status
    if not room_data.get("visited"):
        # This is the first time 'look' is effectively called for this room by the player,
        # or by 'go' into this room.
        display_description = room_data.get("desc_first_visit", current_room.description)
        room_data["visited"] = True # Mark visited AFTER deciding description
    else:
        display_description = room_data.get("desc_subsequent_visit", current_room.description)

    # Update current_room.description so if AdventureLib reuses it (e.g. after no-match), it's the "correct" one.
    current_room.description = display_description
    say(display_description) # Output the chosen description

    room_items_bag = current_room.data.get('items')
    if room_items_bag:
        say("You see:")
        for item_obj in room_items_bag:
            say(f"- {item_obj.name}")

    exits = []
    for direction in ['north', 'south', 'east', 'west', 'northeast', 'northwest', 'southeast', 'southwest', 'up', 'down', 'in', 'out']:
        # Check if the room has an attribute for this direction and it's a Room (an exit)
        if hasattr(current_room, direction) and isinstance(getattr(current_room, direction, None), Room):
            exits.append(f"{direction.capitalize()}")

    if current_room == cave and not current_room.data.get('locked_exit_unlocked', False):
        if 'locked_exit_description' in current_room.data:
            say(current_room.data['locked_exit_description'])

    if exits:
        say("Exits: " + ", ".join(exits))
    else:
        say("There are no obvious exits.")

@when('go DIRECTION')
@when('go to DIRECTION')
@when('move DIRECTION')
def go(direction):
    global current_room

    if current_room == cave and direction == current_room.data.get("locked_exit_direction") and \
       not current_room.data.get("locked_exit_unlocked", False):
        say(current_room.data.get("locked_exit_description", "It's locked."))
        return

    if hasattr(current_room, direction):
        next_room_obj = getattr(current_room, direction)
        if isinstance(next_room_obj, Room):
            current_room = next_room_obj
            say(f"You go {direction}.")
            look_around() # This will handle description and visited status

            if "event_on_entry" in current_room.data and current_room.data["event_on_entry"]:
                say(current_room.data["event_on_entry"])
                current_room.data["event_on_entry"] = None
        else:
            say(f"You can't go {direction} from here.") # Attribute exists but not a room
    else:
        say(f"You can't go {direction}.") # No such exit attribute

@when('n')
def go_north(): go('north')
@when('s')
def go_south(): go('south')
@when('e')
def go_east(): go('east')
@when('w')
def go_west(): go('west')

@when('take ITEM')
@when('get ITEM')
@when('pick up ITEM')
def take_item(item: str):
    global current_room

    room_items_bag = current_room.data.get('items')
    if not room_items_bag:
        say("There is nothing to take here.")
        return

    item_to_take = room_items_bag.find(item)
    if item_to_take:
        inventory.add(item_to_take)
        room_items_bag.remove(item_to_take)
        say(f"You take the {item_to_take.name}.")
    else:
        say(f"You don't see a {item} here.")

@when('inventory')
@when('i')
def show_inventory():
    if not inventory:
        say("Your inventory is empty.")
    else:
        say("You are carrying:")
        for item_obj in inventory:
            say(f"- {item_obj.name}")

@when('use ITEM')
def use_item(item):
    global current_room

    if not item:
        say("Error: Item not found in inventory by AdventureLib.")
        return

    if current_room == cave and item.name == cave.data.get('locked_exit_key_name'):
        if not cave.data.get('locked_exit_unlocked', False):
            say("The rusty key fits the lock! You hear a click and the door swings open.")

            target_room_object = cave.data.get('locked_exit_room')
            exit_direction = cave.data.get('locked_exit_direction')
            if target_room_object and exit_direction:
                setattr(cave, exit_direction, target_room_object)

            cave.data['locked_exit_unlocked'] = True
            inventory.remove(item)
        else:
            say("The door is already unlocked.")
    else:
        say(f"You can't use the {item.name} here.")

@when('help')
@when('h')
def show_help():
    say("--- Help ---")
    say("Available commands:")
    say("- look (or l): Describe the current room and items.")
    say("- go <direction> (or n, s, e, w): Move to a new room.")
    say("- take <item_name>: Pick up an item.")
    say("- inventory (or i): Show items you are carrying.")
    say("- use <item_name>: Use an item you are carrying.")
    say("- help (or h): Show this help message.")
    say("- quit (or exit): Exit the game.")
    say("------------")

@when('quit')
@when('exit')
def quit_game():
    say("Goodbye! Thanks for playing.")
    # Using a more AdventureLib-idiomatic way to signal exit if possible,
    # but standard exit() is often fine.
    # Forcing AdventureLib's loop to stop:
    # start.running = False # This is a hypothetical way, actual might differ
    # The most reliable is Python's own exit:
    exit() # Using Python's built-in exit

# --- Old game code commented out ---
"""
... (rest of old code remains commented) ...
"""

if __name__ == '__main__':
    # current_room is already set to start_location
    # start_location.description is already set to its desc_first_visit
    # AdventureLib's start() will print this initial description.
    start()
