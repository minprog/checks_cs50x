import re
import os
import uuid

from check50 import *
import check50

room_1_name = "Outside building"
room_1_description = ("You are standing at the end of a road before a "
                      "small brick building.  A small stream flows out of "
                      "the building and down a gully to the south.  A road "
                      "runs up a small hill to the west.")

room_2_name = "End of road"
room_2_description = ("You are at the end of a road at the top of a small "
                      "hill. You can see a small building in the valley to "
                      "the east.")

room_3_name = "Inside building"
room_3_description = ("You are inside a building, a well house for a large "
                      "spring.")
room_3_items = ["KEYS", "a set of keys"]

room_8_name = "Beneath grate"
room_8_description = ("You are in a small chamber beneath a 3x3 steel "
                      "grate to the surface.  A low crawl over cobbles "
                      "leads inward to the west.")
room_8_items = ["LAMP", "a brightly shining brass lamp"]

room_14_description = ("You are in a splendid chamber thirty feet high.  "
                       "The walls are frozen rivers of orange stone.  A narrow "
                       "canyon and a good passage exit from east and west "
                       "sides of the chamber.")
room_15_description = ("You are in a splendid chamber thirty feet high.  "
                       "The walls are frozen rivers of orange stone.  A narrow "
                       "canyon and a good passage exit from east and west "
                       "sides of the chamber. High in the cavern, you see a "
                       "little bird flying around the rocks.  It takes one "
                       "look at the black rod and quickly flies out of sight.")

help_statement = ["EAST/WEST/IN/OUT", "QUIT quits", "HELP prints",
                  "INVENTORY lists", "LOOK lists", "TAKE <item>", "DROP <item>"]
no_item = "No such item"


class Adventure(Checks):
    def spawn_tiny(self):
        return self.spawn("python3 adventure.py Tiny")

    def spawn_small(self):
        return self.spawn("python3 adventure.py Small")

    def spawn_crowther(self):
        return self.spawn("python3 adventure.py Crowther")

    @check()
    def exists(self):
        """Checking if all files exist."""
        self.require("adventure.py", "room.py")

        # self.add can't create directories :(
        # give v3 pls
        cwd = os.getcwd()
        dest = os.path.join(cwd, "data")
        if os.path.exists(dest):
            os.rename(dest, dest + str(uuid.uuid4()))
        os.mkdir(dest)
        with check50.cd(check50.config.check_dir):
            data_files = [os.path.join("data", data_file) for data_file in os.listdir("data")]
            for path in data_files:
                check50.copy(path, dest)

    @check("exists")
    def handles_argument(self):
        """Starting adventure with command line argument 'Tiny'."""
        try:
            self.spawn_tiny().stdout(re.escape(room_1_description), str_output=room_1_description)
        except Error as error:
            raise Error(rationale=f"Expected the description of initial "
                                  f"room when Adventure starts.\n    {error}")

    @check("handles_argument")
    def rejects_incorrect_arguments(self):
        """Rejects incorrect amount of arguments or wrong filename."""
        try:
            self.spawn("python3 adventure.py").exit(1)
        except Error as error:
            raise Error(rationale=f"Expected an exit code of 1. Not {error}")

        try:
            self.spawn("python3 adventure.py Tiny CS50").exit(1)
        except Error as error:
            raise Error(rationale=f"Expected an exit code of 1. Not {error}")

        try:
            self.spawn("python3 adventure.py CS50").exit(1)
        except Error as error:
            raise Error(rationale=f"Expected an exit code of 1. Not {error}")

    @check("handles_argument")
    def move_once(self):
        """Starting Adventure then moving once to the WEST."""
        try:
            self.spawn_tiny().stdout(re.escape(room_1_description), str_output=room_1_description)
        except Error as error:
            raise Error(rationale=f"Expected the description of initial "
                                  f"room when Adventure starts.\n    {error}")

        self.spawn_tiny().stdin("WEST").stdout(re.escape(room_2_description), str_output=room_2_description)


    @check("move_once")
    def move_invalid(self):
        """Attempt to move EAST into an unconnected room."""
        self.spawn_tiny().stdin("EAST").stdout("Invalid command")


    @check("move_once")
    def move_repeatedly(self):
        """Moving WEST, EAST, WEST in succession."""
        check = self.spawn_tiny()
        check.stdin("WEST").stdout(re.escape(room_2_description), str_output=room_2_description)
        check.stdin("EAST").stdout(re.escape(room_1_name), str_output=room_1_name)
        check.stdin("WEST").stdout(re.escape(room_2_name), str_output=room_2_name)


    @check("move_repeatedly")
    def move_mixed_case(self):
        """Move with mixed case command."""
        self.spawn_tiny().stdin("west").stdout(re.escape(room_2_description), str_output=room_2_description)
        self.spawn_tiny().stdin("wESt").stdout(re.escape(room_2_description), str_output=room_2_description)
        self.spawn_tiny().stdin("west").stdin("EAST").stdout(re.escape(room_1_name), str_output=room_1_name)


    @check("move_mixed_case")
    def helper_commands(self):
        """Testing helper commands; HELP, LOOK, QUIT."""
        # Test HELP
        try:
            check = self.spawn_tiny().stdin("HELP")
            for help in help_statement:
                check.stdout(help)
        except Error as error:
            raise Error(rationale=f"HELP did not print the expected message.\n"
                                  f"    {error}")

        # Test LOOK command
        try:
            self.spawn_tiny().stdin("LOOK").stdout(re.escape(room_1_description), str_output=room_1_description)
            self.spawn_tiny().stdin("look").stdout(re.escape(room_1_description), str_output=room_1_description)
        except Error as error:
            raise Error(rationale=f"LOOK/look did not print the expected room"
                                  f"description.\n    {error}")

        # Test QUIT
        try:
            self.spawn_tiny().stdin("QUIT").stdout(re.escape("Thanks for playing!"), str_output="Thanks for playing!").exit(0)
        except Error as error:
            raise Error(rationale=f"QUIT did not function as expected.\n"
                                  f"    {error}")


    @check("helper_commands")
    def commands(self):
        """Test if program handles invalid commands."""
        # Check invalid command
        check = self.spawn_tiny().stdin("cs50")
        check.stdout(re.escape("Invalid command"), str_output="Invalid command")


    @check("helper_commands")
    def find_items(self):
        """Finds items in rooms."""
        self.require("item.py")

        # Check initial description
        try:
            check = self.spawn_tiny().stdin("in")
            check.stdout(re.escape(room_3_description), str_output=room_3_description)

            for item in room_3_items:
                check.stdout(re.escape(item), str_output=item)
        except Error as error:
            raise Error(rationale=f"Could not find items upon first entering room.\n"
                                  f"    Remember to seperate multiple items by a "
                                  f"single newline.\n"
                                  f"    {error}")

        # Check for look command
        try:
            check = self.spawn_tiny()
            moves = ["IN", "OUT", "IN", "LOOK"]

            for move in moves:
                check.stdout("> ")
                check.stdin(move, prompt=False)

            for item in room_3_items:
                check.stdout(re.escape(item), str_output=item)
        except Error as error:
            raise Error(rationale=f"Could not find items when using LOOK.\n"
                                  f"    {error}")


    @check("find_items")
    def handle_items(self):
        """Take and drop items."""
        self.require("inventory.py")

        # Take keys check
        check = self.spawn_tiny()
        moves = ["IN", "TAKE keys"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape("KEYS taken"), str_output="KEYS taken")

        # Drop keys check then look for dropped keys check
        check = self.spawn_tiny()
        moves = ["IN", "TAKE keys", "OUT", "DROP keys"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape("KEYS dropped"), str_output="KEYS dropped")
        check.stdin("look").stdout(re.escape("KEYS"), str_output="KEYS")
        check.stdout(re.escape("a set of keys"), str_output="a set of keys")


    @check("handle_items")
    def handle_invalid_items(self):
        """Take and drop nonexistent items."""
        # Take a non-existent item.
        check = self.spawn_tiny().stdin("TAKE kes")
        check.stdout(re.escape(no_item), str_output=no_item)

        # Take an item twice.
        check = self.spawn_tiny()
        moves = ["IN", "TAKE keys", "TAKE keys"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)
        check.stdout(re.escape(no_item), str_output=no_item)

        # Drop non-existent item.
        check = self.spawn_tiny().stdin("DROP something")
        check.stdout(re.escape(no_item), str_output=no_item)


    @check("handle_items")
    def inventory(self):
        """Using the INVENTORY command."""
        # Check empty inventory.
        try:
            check = self.spawn_tiny().stdin("INVENTORY")
            check.stdout(re.escape("Your inventory is empty"), str_output="Your inventory is empty")
        except Error as error:
            raise Error(rationale=f"Let the player know they have no items.\n"
                                  f"    {error}")

        # Check having keys.
        check = self.spawn_tiny()
        moves = ["IN", "TAKE keys", "INVENTORY"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape("KEYS"), str_output="KEYS")
        check.stdout(re.escape("a set of keys"), str_output="KEYS")


    @check("handle_items")
    def conditional_move(self):
        """Check if holding an item affects conditional movement."""
        check = self.spawn_small()
        moves = ["DOWN", "DOWN", "DOWN", "DOWN"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape("The grate is locked and you don't have any keys."),
                     str_output="The grate is locked and you don't have any keys.")

        check = self.spawn_small()
        moves = ["IN", "TAKE keys", "OUT",
                 "DOWN", "DOWN", "DOWN", "DOWN"
                 ]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape(room_8_description), str_output=room_8_description)
        for item in room_8_items:
            check.stdout(re.escape(item), str_output=item)


    @check("conditional_move")
    def forced_move(self):
        """Checking if FORCED immediately moves the player."""
        check = self.spawn_small()
        moves = ["DOWN", "DOWN", "DOWN", "DOWN"]

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        check.stdout(re.escape("The grate is locked and you don't have any keys."),
                     str_output="The grate is locked and you don't have any keys.")
        check.stdout(re.escape("Outside grate"), str_output="Outside grate")


    @check("conditional_move")
    def multiple_conditional_move(self):
        """Check if holding multiple items affects conditional movement."""
        try:
            check = self.spawn_crowther()
            moves = ["IN", "TAKE KEYS", "OUT", "DOWN", "DOWN",
                     "DOWN", "DOWN", "TAKE LAMP", "IN", "WEST",
                     "WEST", "WEST", "TAKE BIRD", "WEST", "DOWN",
                     "SOUTH", "TAKE NUGGET", "OUT", "DROP NUGGET", "UP",
                     "EAST", "EAST", "EAST", "TAKE ROD", "WEST",
                     "WEST", "LOOK"
                     ]

            for move in moves:
                check.stdout("> ")
                check.stdin(move, prompt=False)
            check.stdout(re.escape(room_14_description), str_output=room_14_description)

            moves = ["EAST", "DROP BIRD", "WEST", "LOOK"]

            for move in moves:
                check.stdout("> ")
                check.stdin(move, prompt=False)
            check.stdout(re.escape(room_15_description), str_output=room_15_description)

        except Error as error:
            raise Error(rationale="Did not find correct room description when "
                                  "going WEST from room 13 holding either BIRD & "
                                  "ROD or just ROD.\n"
                                  f"    {error}")


    @check("move_repeatedly")
    def special_move(self):
        """Performing special moves such as JUMP or XYZZY."""
        try:
            check = self.spawn_crowther()
            moves = ["IN", "XYZZY"]

            for move in moves:
                check.stdout("> ")
                check.stdin(move, prompt=False)

            text = "It is now pitch dark.  If you proceed you will "\
                   "likely fall into a pit."
            check.stdout(re.escape(text), str_output=text)
        except Error as error:
            raise Error(rationale="Could not perform XYZZY. Check "
                                  "CrowtherRooms.txt for all the different"
                                  "connections.")


    @check("special_move")
    def won(self):
        """Testing Crowther Adventure win condition."""
        moves = ["IN", "TAKE KEYS", "OUT", "DOWN", "DOWN",
                 "DOWN", "DOWN", "TAKE LAMP", "IN", "WEST",
                 "WEST", "WEST", "TAKE BIRD", "WEST", "DOWN",
                 "SOUTH", "TAKE NUGGET", "OUT", "DROP NUGGET", "UP",
                 "EAST", "EAST", "EAST", "TAKE ROD", "WEST",
                 "WEST", "WEST", "DOWN", "TAKE NUGGET", "WEST",
                 "WAVE", "TAKE DIAMOND", "WEST", "SOUTH", "SOUTH",
                 "EAST", "NORTH", "NORTH", "TAKE CHEST", "OUT",
                 "WEST", "DOWN", "WEST", "DOWN", "NORTH",
                 "EAST", "TAKE COINS", "OUT", "NORTH", "DOWN",
                 "EAST", "DROP LAMP", "DROP BIRD", "DROP NUGGET", "DROP COINS",
                 "NORTH", "TAKE EMERALD", "OUT", "TAKE LAMP", "TAKE BIRD",
                 "TAKE NUGGET", "TAKE COINS", "WEST", "WEST", "WEST",
                 "DOWN", "WATER", "TAKE EGGS", "NORTH", "DOWN",
                 "OUT", "EAST", "EAST", "EAST", "UP",
                 "SOUTH", "SOUTH", "WEST", "WAVE", "WEST",
                 "SOUTH", "NORTH", "NORTH", "EAST", "DOWN",
                 "EAST", "EAST", "XYZZY", "NORTH"
                 ]
        check = self.spawn_crowther()

        for move in moves:
            check.stdout("> ")
            check.stdin(move, prompt=False)

        text = "You have collected all the treasures and are admitted to "\
                     "the Adventurer's Hall of Fame.  Congratulations!"
        check.stdout(re.escape(text), str_output=text)
        #check.stdout("\n")
        check.exit(0)
