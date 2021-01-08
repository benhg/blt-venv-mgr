# blt-venv-mgr
Manage the python virtual environments in BLT

## How do I use it?

Here is the help menu:
```
usage: venv_man.py [-h] [-l] [-n NAME] [-c] [-d] [-a ADD [ADD ...]] [-r REMOVE [REMOVE ...]]
                   [-e] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List all available virtual environments.
  -n NAME, --name NAME  Specify the name of a virtual environment
  -c, --create          Create a new virtual environment with name specified
  -d, --delete          Delete the virtual environment with name specified
  -a ADD [ADD ...], --add ADD [ADD ...]
                        Add specified python packages to specified virtual environmentwith
                        pip.
  -r REMOVE [REMOVE ...], --remove REMOVE [REMOVE ...]
                        Remove specified python packages from specified virtual environment
                        with pip.
  -e, --activate        Print the command to activate (engage) a virtual environment
  -s, --show            Show a list of packages installed in specified environment
```
NOTES:

- `create` and `delete` may not be used together.
- `add` and `remove` may not be used together.
- `create`/`delete` cannot be used with `add/remove`.
- All arguments except `list` require `name` to be passed in
- `list` should not have a `name` provided.