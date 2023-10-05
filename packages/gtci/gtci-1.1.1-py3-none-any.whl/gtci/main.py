#!/usr/bin/python
# This line is called a shebang and specifies the path to the Python interpreter that should be used to run the script.
# The shebang is followed by the location of the interpreter executable on the system.
# In this case, it is pointing to the default Python executable that is installed in the /usr/bin directory.

# -*- coding: UTF-8 -*-
# This line specifies the encoding of the source code file.

# Auther : MR_GT
# This line is a comment that indicates the author of the script.

import sys           # This module provides access to system-specific parameters and functions.
from utils import * # This imports all functions from the utils module in the current package (indicated by the period before "utils").


def Main():
    try: commands = sys.argv[1]  # Get the first command-line argument
    except IndexError: commands = False  # If no argument is provided, set 'commands' to False

    try: options = sys.argv[2:]  # Get the command-line arguments starting from the second argument
    except IndexError: options = False  # If no arguments are provided, set 'options' to False

    try: arguments = sys.argv[3:]  # Get the command-line arguments starting from the third argument
    except IndexError: arguments = ""  # If no arguments are provided, set 'arguments' to an empty string

    if (commands):
        if (commands == "i") or (commands == "-i") or (commands == "--i") or (commands == "install") or (commands == "-install") or (commands == "--install") or (commands == "--clone") or (commands == "--clone") or (commands == "--clone"):
            if (internet()):
                if (len(options) != 1):
                    print(f"\n{bold}{magenta}[{red}!{magenta}] {white}The install command requires 1 argument, but {len(options)} were provided.")
                else: install(options[0])
            else: print(f"{bold}{magenta}[{red}!{magenta}] {white}Check your internet connection...{reset}"), exit()
        elif (commands == "r") or (commands == "-r") or (commands == "--r") or (commands == "run") or (commands == "-run") or (commands == "--run") or (commands == "--start") or (commands == "--start") or (commands == "--start"):
            run(options[0], arguments)
        elif (commands == "remove") or (commands == "-remove") or (commands == "--remove") or (commands == "uninstall") or (commands == "-uninstall") or (commands == "--uninstall"):
            if (len(options) != 1):
                print(f"\n{bold}{magenta}[{red}!{magenta}] {white}The uninstall command requires 1 argument, but {len(options)} were provided.")
            else: uninstall(options[0])
        elif (commands == "d") or (commands == "-d") or (commands == "--d") or (commands == "download") or (commands == "-download") or (commands == "--download"):
            if (len(options) != 1):
                print(f"\n{bold}{magenta}[{red}!{magenta}] {white}The download command requires 1 argument, but {len(options)} were provided.")
            else: download(options[0])
        elif (commands == "l") or (commands == "-l") or (commands == "--l") or (commands == "list") or (commands == "-list") or (commands == "--list"):
            list()
        elif (commands == "v") or (commands == "-v") or (commands == "--v") or (commands == "version") or (commands == "-version") or (commands == "--version"):
            version()
        elif (commands == "h") or (commands == "-h") or (commands == "--h") or (commands == "help") or (commands == "-help") or (commands == "--help"):
            help()
    else: help()


if (__name__ == "__main__"):
    # Check if the module is being run as the main program
    try: Main()  # Call the Main() function
    except KeyboardInterrupt:
         # If the user interrupts the program (e.g., by pressing Ctrl+C), exit the program
        print(f"\n\n{bold}{magenta}[{red}!{magenta}] {white}Program Interrupted...{yellow}!!{reset}")
        exit()
    except Exception as exc:
        # If an exception occurs during the execution of the Main() function, capture the exception in the variable 'e'
        # Print an error message with the captured exception
        print(f"\n\n{bold}{magenta}[{red}!{magenta}] {cyan}{exc}")
        print(f"{bold}{magenta}[{yellow}+{magenta}] {white}Repost this issue at {blue}github.com/GreyTechno/gtci/issues")
