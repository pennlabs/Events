import subprocess

import fabric


SCRIPTS_DIR = "app/static/scripts"
STYLESHEETS_DIR = "app/static/stylesheets"


# TODO: Make some kind of way to kill background processes.


def _local(command, capture=False, shell=False, bg=False):
    if bg:
        print command
        with open("/dev/null", "w") as f:
            subprocess.Popen(command.split(), stdout=f, shell=False)
    else:
        return fabric.api.local(command, capture, shell)


def make_static(capture=True, bg=True):
    """Build static files and update on change."""
    _local("coffee -cw %s" % SCRIPTS_DIR, capture=capture, bg=bg)
    _local("sass -w %s" % STYLESHEETS_DIR, capture=capture, bg=bg)


def run_server(capture=True, bg=True):
    """Start the database and the server."""
    _local("mongod", capture=capture, bg=bg)
    _local("python run.py", capture=capture, bg=bg)


def run():
    """Run the server and compile static files."""
    make_static()
    run_server()
