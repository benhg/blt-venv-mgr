#!/local/cluster/bin/python
"""
venv_man.py

Virtual ENVironment MANager. 
BLT-specific script for creating, deleting,
    viewing, editing, and activating venvs
"""

import argparse
import sys
import subprocess
import os
import collections


class Config:
    def __init__(self):
        self.BASE_VENV_PATH = "/bread/venv"


config = Config()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l",
                        "--list",
                        action="store_true",
                        default=False,
                        help="List all available virtual environments.")
    parser.add_argument("-n",
                        "--name",
                        type=str,
                        default=None,
                        help="Specify the name of a virtual environment")
    parser.add_argument(
        "-c",
        "--create",
        action="store_true",
        default=False,
        help="Create a new virtual environment with name specified")
    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        default=False,
        help="Delete the virtual environment with name specified")
    parser.add_argument(
        "-a",
        "--add",
        type=str,
        default=[],
        nargs="+",
        help=
        "Add specified python packages to specified virtual environmentwith pip."
    )
    parser.add_argument(
        "-r",
        "--remove",
        type=str,
        default=[],
        nargs="+",
        help=
        "Remove specified python packages from specified virtual environment with pip."
    )
    parser.add_argument(
        "-e",
        "--activate",
        action="store_true",
        default=False,
        help="Print the command to activate (engage) a virtual environment")
    parser.add_argument(
        "-s",
        "--show",
        action="store_true",
        default=False,
        help="Show a list of packages installed in specified environment")
    parser.add_argument("-y",
                        "--yes",
                        action="store_true",
                        default=False,
                        help="Force remove, do not ask for confirmation.")
    args = parser.parse_args()

    if not any([
            args.list, args.activate, args.remove, args.add, args.delete,
            args.create, args.show
    ]):
        print("ERROR: No action specified.")
        sys.exit(1)

    if not args.name and not args.list:
        print("ERROR: All arguments except `--list` require a venv name.")
        sys.exit(1)

    if args.list:
        list_venvs()
        sys.exit(0)

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
        print(
            "ERROR: Add/Remove and Create/Delete are not supported together.")
        sys.exit(1)

    if args.show and any(
        [args.activate, args.remove, args.add, args.delete, args.create]):
        print("ERROR: Show cannot be specified with other actions")
        sys.exit(1)

    if args.create:
        create_virtualenv(args.name)

    if args.delete:
        remove_virtualenv(args.name, args.yes)

    if args.activate:
        show_activate_cmd(args.name)

    if len(args.add) > 0:
        add_pkgs(args.add, args.name)

    if len(args.remove) > 0:
        remove_pkgs(args.remove, args.name)

    return args


def list_venvs():
    """
    List all virtual environments in directory `config.BASE_VENV_PATH`
        Assume that if file is a directory and `config.BASE_VENV_PATH/bin/activate`
        both exist, it is in fact a virtual env.
    """
    print("Listing Virtual Environments:")
    directories = os.listdir(config.BASE_VENV_PATH)
    if len(directories) == 0:
        print("\tNone Found.")
        sys.exit(0)
    for directory in directories:
        if _venv_exists(directory):
            print(f"\t{directory}")


def remove_virtualenv(name, force):
    """
    Delete a virtual environment with name :param name.
    """
    if not os.path.isdir(_dir_path(name)):
        print(f"ERROR: could not find environment {name}")
        sys.exit(1)
    if not force and input(
            f"Are you sure you want to delete virtualenv {name}? y/N ").lower(
            ) != "y":
        print("Aborting.")
        sys.exit(0)
    subprocess.check_call(["rm", "-rf", _dir_path(name)])


def create_virtualenv(name):
    """
    Create an empty virtual environment with name :param name.
    """
    if os.path.exists(_dir_path(name)):
        print(f"ERROR: name {name} already taken.")
        sys.exit(1)
    subprocess.check_call(" ".join(
        ["cd", config.BASE_VENV_PATH, ";", "virtualenv", name]),
                          shell=True)


def show_activate_cmd(name):
    """
    Print the command used to activate the named virtualenv.
    """
    if not _venv_exists(name):
        print(f"ERROR: Could not find virtualenv {name}")
        sys.exit(1)
    print(f"To activate the virtualenv {name}, use the following command:")
    print(f"\t`source {_dir_path(name)}/bin/activate`")
    print("You can always deactivate a virtualenv with the command `deactivate`")


def add_pkgs(pkgs, name):
    """
    Add packages :param pkgs to virtualenv :param name
    """
    if not _venv_exists(name):
        print(f"ERROR: Could not find virtualenv {name}")
        sys.exit(1)
    cmd_base = f"\tsource {_dir_path(name)}/bin/activate;"
    for pkg in pkgs:
        cmd_base += f"pip install {pkg};"
    cmd_base += "deactivate"
    subprocess.check_call(cmd_base, shell=True)


def remove_pkgs(pkgs, name):
    """
    Remove packages :param pkgs from virtualenv :param name
    """
    if not _venv_exists(name):
        print(f"ERROR: Could not find virtualenv {name}")
        sys.exit(1)
    cmd_base = f"\tsource {_dir_path(name)}/bin/activate;"
    for pkg in pkgs:
        cmd_base += f"pip uninstall {pkg};"
    cmd_base += "deactivate"
    subprocess.check_call(cmd_base, shell=True)


def _dir_path(name):
    return f"{config.BASE_VENV_PATH}/{name}"


def _venv_exists(name):
    dir_path = f"{config.BASE_VENV_PATH}/{name}"
    return os.path.isdir(dir_path) and os.path.exists(
        f"{dir_path}/bin/activate")


if __name__ == '__main__':
    args = parse_args()
