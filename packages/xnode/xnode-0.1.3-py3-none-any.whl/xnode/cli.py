import os
import platform
import posixpath
import re
import serial.serialutil

import click
import dotenv

config = dotenv.find_dotenv(filename=".xnode", usecwd=True)
if config:
    dotenv.load_dotenv(dotenv_path=config)

import xnode.files as files
import xnode.pyboard as pyboard

_board = None

def windows_full_port_name(portname):
    m = re.match("^COM(\d+)$", portname)
    if m and int(m.group(1)) < 10:
        return portname
    else:
        return "\\\\.\\{0}".format(portname)

@click.group()
@click.option(
    "--port",
    "-p",
    envvar="XNODE_PORT",
    required=True,
    type=click.STRING,
    help="Name of serial port for connected board.",
    metavar="PORT",
)
@click.option(
    "--baud",
    "-b",
    envvar="XNODE_BAUD",
    default=115200,
    type=click.INT,
    help="Baud rate for the serial connection (default 115200).",
    metavar="BAUD",
)
@click.option(
    "--delay",
    "-d",
    envvar="XNODE_DELAY",
    default=0,
    type=click.FLOAT,
    help="Delay in seconds before entering RAW MODE (default 0).",
    metavar="DELAY",
)
@click.option(
    "--exclusive",
    "-e",
    default=False,
    type=click.BOOL,
    help="Scan Mode (default False).",
)

def cli(port, baud, delay, exclusive):
    if exclusive:
        return None

    global _board
    if platform.system() == "Windows":
        port = windows_full_port_name(port)
        
    _board = pyboard.Pyboard(port, baudrate=baud, rawdelay=delay)

@cli.command()
@click.argument("remote_file")
@click.argument("local_file", type=click.File("wb"), required=False)
def get(remote_file, local_file):
    board_files = files.Files(_board)
    contents = board_files.get(remote_file)

    if local_file is None:
        print(contents.decode("utf-8"))
    else:
        local_file.write(contents)

@cli.command()
@click.option(
    "--exists-okay", is_flag=True, help="Ignore if the directory already exists."
)
@click.argument("directory")
def mkdir(directory, exists_okay):
    board_files = files.Files(_board)
    board_files.mkdir(directory, exists_okay=exists_okay)

@cli.command()
@click.argument("directory", default="/")
@click.option(
    "--long_format",
    "-l",
    is_flag=True,
    help="Print long format info including size of files.",
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="recursively list all files and (empty) directories.",
)
def ls(directory, long_format, recursive):
    board_files = files.Files(_board)
    for f in board_files.ls(directory, long_format=long_format, recursive=recursive):
        print(f)

@cli.command()
@click.argument("local", type=click.Path(exists=True))
@click.argument("remote", required=False)
def put(local, remote):
    if remote is None:
        remote = os.path.basename(os.path.abspath(local))
    if os.path.isdir(local):
        board_files = files.Files(_board)
        for parent, child_dirs, child_files in os.walk(local, followlinks=True):
            remote_parent = posixpath.normpath(
                posixpath.join(remote, os.path.relpath(parent, local))
            )
            try:
                board_files.mkdir(remote_parent)
            except files.DirectoryExistsError:
                pass
            for filename in child_files:
                with open(os.path.join(parent, filename), "rb") as infile:
                    remote_filename = posixpath.join(remote_parent, filename)
                    board_files.put(remote_filename, infile.read())
    else:
        with open(local, "rb") as infile:
            board_files = files.Files(_board)
            board_files.put(remote, infile.read())

@cli.command()
@click.argument("remote_file")
def rm(remote_file):
    board_files = files.Files(_board)
    board_files.rm(remote_file)

@cli.command()
@click.option(
    "--missing-okay", is_flag=True, help="Ignore if the directory does not exist."
)
@click.argument("remote_folder")
def rmdir(remote_folder, missing_okay):
    board_files = files.Files(_board)
    board_files.rmdir(remote_folder, missing_okay=missing_okay)

@cli.command()
@click.argument("type")
def format(type):
    board_files = files.Files(_board)
    if type.lower() == 'a':
        board_files.format_a()
    elif type.lower() == 'b':
        board_files.format_b()
    else:
        print("failed type")

@cli.command()
@click.argument("local_file")
@click.option(
    "--no-output",
    "-n",
    is_flag=True,
    help="Run the code without waiting for it to finish and print output.",
)
@click.option(
    "--input-on",
    "-i",
    is_flag=True,
    help="Run the code with input stream.",
)
def run(local_file, no_output, input_on):
    board_files = files.Files(_board)
    try:
        board_files.run(local_file, not no_output, input_on)
    except IOError:
        click.echo(
            "Failed to find or read input file: {0}".format(local_file), err=True
        )

@cli.command()
@click.option(
    "--bootloader", "mode", flag_value="BOOTLOADER", help="Reboot into the bootloader"
)
@click.option(
    "--hard",
    "mode",
    flag_value="NORMAL",
    help="Perform a hard reboot, including running init.py",
)
@click.option(
    "--repl",
    "mode",
    flag_value="SOFT",
    default=True,
    help="Perform a soft reboot, entering the REPL  [default]",
)
@click.option(
    "--safe",
    "mode",
    flag_value="SAFE_MODE",
    help="Perform a safe-mode reboot.",
)
def reset(mode):
    _board.enter_raw_repl()
    if mode == "SOFT":
        _board.exit_raw_repl()
        return

    _board.exec_(
        """if 1:
        def reset():
            import machine
            machine.reset()
    """
    )

    try:
         _board.exec_raw_no_follow("reset()")
    except serial.serialutil.SerialException as e:
        pass

@cli.command()
def scan():
    pass

@cli.command()
def repl():
    pass
