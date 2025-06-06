world = {
    "start": {
        "description": "You are at the starting point, a grassy field under a clear blue sky. A path leads north.",
        "exits": {"north": "cave"}
    },
    "cave": {
        "description": "You are at the entrance of a dark cave. It looks spooky. You can hear bats. A path leads south.",
        "exits": {"south": "start"}
    }
}

current_location = "start"

def _display_current_location_description():
    """Prints the description of the current location. Internal use."""
    if current_location in world:
        print(world[current_location]["description"])
    else:
        print("Error: Unknown location!")

def handle_look():
    """Handles the 'look' command by displaying the current location's description."""
    _display_current_location_description()

def handle_go(direction: str):
    """Handles the 'go' command by trying to move the player in the given direction."""
    global current_location

    if not direction:
        print("Go where?")
        return

    available_exits = world[current_location].get("exits", {})
    if direction in available_exits:
        current_location = available_exits[direction]
        print(f"You go {direction}.")
        _display_current_location_description()
    else:
        print(f"You can't go {direction}.")

def parse_command(raw_input: str) -> tuple[str, str]:
    """Splits the raw input into a command and an argument."""
    parts = raw_input.strip().lower().split(maxsplit=1)
    command = parts[0] if parts else ""
    argument = parts[1] if len(parts) > 1 else ""
    return command, argument

def main():
    """Main function for the text adventure game."""
    print("Welcome to the Text Adventure Game!")
    print("Commands: go [direction], look, quit")
    print("-" * 30)

    _display_current_location_description() # Display initial location

    while True:
        raw_input = input("> ")
        command, argument = parse_command(raw_input)
        print("-" * 30) # Separator for readability after input

        if command == "quit":
            print("Thanks for playing. Goodbye!")
            break
        elif command == "go":
            handle_go(argument)
        elif command == "look":
            handle_look()
        elif command == "": # Empty input
            print("Please enter a command.")
        else:
            print(f"Unknown command: '{command}'")

        print("-" * 30) # Separator after action

if __name__ == "__main__":
    main()
