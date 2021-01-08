#!/local/cluster/bin/python

"""
venv_man.py

Virtual ENVironment MANager. 
BLT-specific script for creating, deleting,
    viewing, editing, and activating venvs
"""

import argparse
import sys
import os

config = {
    "BASE_VENV_PATH": "/bread/venv"
}


import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list",
                        action="store_true",
                        default=False,
                        help="List all available virtual environments.")
    parser.add_argument("-n", "--name",
                        type=str,
                        default=None,
                        help="Specify the name of a virtual environment")
    parser.add_argument("-c", "--create",
                        action="store_true",
                        default=False,
                        help="Create a new virtual environment with name specified")
    parser.add_argument("-d", "--delete",
                        action="store_true",
                        default=False,
                        help="Delete the virtual environment with name specified")
    parser.add_argument("-a", "--add",
                        type=str,
                        default=None,
                        nargs="+",
                        help="Add specified python packages to specified virtual environmentwith pip.")
    parser.add_argument("-r", "--remove",
                        type=str,
                        default=None,
                        nargs="+",
                        help="Remove specified python packages from specified virtual environment with pip.")
    parser.add_argument("-e", "--activate",
                        action="store_true",
                        default=False,
                        help="Print the command to activate (engage) a virtual environment")
    args = parser.parse_args()

    if not any([args.list, args.activate, args.remove, args.add, args.delete, args.create]):
        print("ERROR: No action specified.")
        sys.exit(1)

    if not args.name and not args.list:
        print("ERROR: All arguments except `--list` require a venv name.")
        sys.exit(1)

    # At this point, we know args.name is set.
    if args.list:
        print("ERROR: Cannot list when args.name is specified.")
        sys.exit(1)

    if args.create and args.delete:
        print("ERROR: Cannot delete and create at once.")
        sys.exit(1)

    if args.add and args.remove:
        print("ERROR: Cannot add and remove packages at once.")
        sys.exit(1)

    if any([args.create, args.delete]) and any([args.add, args.remove]):
        print("ERROR: Add/Remove and Create/Delete are not supported together.")
        sys.exit(1)

    return args

if __name__ == '__main__':
    args = parse_args()