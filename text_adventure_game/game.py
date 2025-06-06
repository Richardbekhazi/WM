world = {
    "start": {
        "description": {
            "first_visit": "You find yourself in a bright, grassy field under a clear blue sky. A well-trodden path leads north, inviting adventure.",
            "subsequent_visit": "You are back at the starting field. The path to the north still beckons."
        },
        "exits": {"north": "cave"},
        "visited": False,
        "items": []
    },
    "cave": {
        "description": {
            "first_visit": "The entrance to the cave is a dark, ominous maw in the mountainside. Cold air wafts out, carrying the faint sound of dripping water and distant bat screeches. It looks spooky.",
            "subsequent_visit": "You are at the cave entrance again. The darkness within feels familiar now, but no less chilling."
        },
        "exits": {"south": "start", "north": "forest"}, # East will be added when unlocked
        "locked_exits": {
            "east": {
                "room": "treasure_room",
                "key": "rusty_key",
                "description": "A sturdy wooden door to the east seems locked."
            }
        },
        "visited": False,
        "event_on_entry": "As you step into the cave, a faint scratching sound echoes from the darkness.",
        "items": []
    },
    "forest": {
        "description": {
            "first_visit": "You are in a dense forest. Sunlight filters weakly through the canopy. Paths lead south and east.",
            "subsequent_visit": "You are back in the dense forest. Paths lead south and east."
        },
        "exits": {"south": "cave", "east": "clearing"},
        "visited": False,
        "event_on_entry": "A twig snaps nearby, but you see nothing.",
        "items": ["rusty_key"] # Key added here
    },
    "clearing": {
        "description": {
            "first_visit": "You step into a small, sunlit clearing. It feels peaceful here. A narrow path leads west.",
            "subsequent_visit": "You are in the peaceful, sunlit clearing. A path leads west."
        },
        "exits": {"west": "forest"},
        "visited": False,
        "items": ["shiny_rock"]
    },
    "treasure_room": {
        "description": {
            "first_visit": "You've found the treasure room! A small, dusty chest sits in the center.",
            "subsequent_visit": "You are back in the treasure room. The chest is still here."
        },
        "exits": {"west": "cave"},
        "visited": False,
        "items": ["gold_coins"]
    }
}

player = {
    "location": "start",
    "inventory": []
}

def _display_current_location_description():
    loc_data = world[player['location']]
    if not loc_data["visited"]:
        print(loc_data["description"]["first_visit"])
    else:
        print(loc_data["description"]["subsequent_visit"])

def handle_look():
    _display_current_location_description()
    current_items = world[player['location']].get('items', [])
    if current_items:
        print("You also see: " + ", ".join(current_items))

    # Describe locked exits if present
    if 'locked_exits' in world[player['location']]:
        for direction, details in world[player['location']]['locked_exits'].items():
            print(details['description'])


def handle_go(direction: str):
    global player
    global world

    if not direction:
        print("Go where?")
        return

    current_room_data = world[player['location']]

    if direction in current_room_data.get("exits", {}):
        player['location'] = current_room_data["exits"][direction]
        print(f"You go {direction}.")

        loc_data = world[player['location']]
        if not loc_data["visited"]:
            print(loc_data["description"]["first_visit"])
            world[player['location']]["visited"] = True
        else:
            print(loc_data["description"]["subsequent_visit"])

        if "event_on_entry" in loc_data:
            event_message = loc_data["event_on_entry"]
            print(event_message)
            del world[player['location']]["event_on_entry"]
    elif direction in current_room_data.get("locked_exits", {}):
        print(current_room_data["locked_exits"][direction]["description"])
    else:
        print(f"You can't go {direction}.")

def handle_take(item_name: str):
    global player
    global world

    if not item_name:
        print("Take what?")
        return

    location_items = world[player['location']].get('items', [])
    if item_name in location_items:
        player['inventory'].append(item_name)
        location_items.remove(item_name)
        print(f"You take the {item_name}.")
    elif not world[player['location']].get('items'): # Check if items key exists and is empty or key doesn't exist
        print("There is nothing to take here.")
    else: # Items key exists and is not empty, but specified item is not there
        print(f"You don't see a {item_name} here.")


def handle_inventory():
    if not player['inventory']:
        print("Your inventory is empty.")
    else:
        print("You are carrying: " + ", ".join(player['inventory']))

def handle_use(item_name: str):
    global player
    global world

    if not item_name:
        print("Use what?")
        return

    if item_name not in player['inventory']:
        print(f"You don't have a {item_name}.")
        return

    # Specific puzzle: using rusty_key in the cave to unlock the east door
    if player['location'] == 'cave' and item_name == 'rusty_key':
        cave_data = world['cave']
        if 'locked_exits' in cave_data and 'east' in cave_data['locked_exits']:
            if cave_data['locked_exits']['east']['key'] == item_name:
                print("The rusty_key fits the lock! You hear a click and the door swings open.")
                player['inventory'].remove(item_name) # Key is used

                # Add new exit and remove locked door
                if 'exits' not in cave_data: cave_data['exits'] = {}
                cave_data['exits']['east'] = cave_data['locked_exits']['east']['room']
                del cave_data['locked_exits']['east']

                # Remove the whole locked_exits dict if it's now empty
                if not cave_data['locked_exits']:
                    del cave_data['locked_exits']
                return

    print(f"You can't use the {item_name} here.")


def parse_command(raw_input: str) -> tuple[str, str]:
    parts = raw_input.strip().lower().split(maxsplit=1)
    command = parts[0] if parts else ""
    argument = parts[1] if len(parts) > 1 else ""
    return command, argument

def handle_help():
    print("You can use the following commands:")
    print("  go [direction] - Move to a new location (e.g., 'go north')")
    print("  look           - See the description of your current location, items, and locked doors")
    print("  take [item]    - Pick up an item (e.g., 'take shiny_rock')")
    print("  use [item]     - Use an item from your inventory (e.g., 'use rusty_key')")
    print("  inventory (i)  - Check your inventory")
    print("  quit / exit    - Exit the game")
    print("  help           - Show this help message")

def main():
    global player
    global world

    print("Welcome to the Text Adventure Game!")
    print("Commands: go [direction], look, take [item], use [item], inventory (i), quit, exit, help")
    print("-" * 30)

    loc_data_start = world[player['location']]
    if not loc_data_start["visited"]:
        print(loc_data_start["description"]["first_visit"])
        world[player['location']]["visited"] = True
    else:
        print(loc_data_start["description"]["subsequent_visit"])

    initial_items = loc_data_start.get('items', [])
    if initial_items:
        print("You also see: " + ", ".join(initial_items))
    if 'locked_exits' in loc_data_start: # For starting location, if it had locked exits
        for direction, details in loc_data_start['locked_exits'].items():
            print(details['description'])

    while True:
        raw_input = input("> ")
        command, argument = parse_command(raw_input)
        print("-" * 30)

        if command == "quit" or command == "exit":
            print("Thanks for playing. Goodbye!")
            break
        elif command == "go":
            handle_go(argument)
        elif command == "look":
            handle_look()
        elif command == "take":
            handle_take(argument)
        elif command == "use":
            handle_use(argument)
        elif command == "inventory" or command == "i":
            handle_inventory()
        elif command == "help":
            handle_help()
        elif command == "":
            print("Please enter a command.")
        else:
            print(f"Unknown command: '{command}'")

        print("-" * 30)

if __name__ == "__main__":
    main()
