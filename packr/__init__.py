import sys
from basecommand import Command
import commands
import os




def get_commands():
    """Return list of Command sub classes from current module.
    """
    classes = []
    for attr in [getattr(commands, name) for name in dir(commands)]:
        if Command in getattr(attr, '__bases__', []):
            classes.append(attr)
    return classes


def register_commands(arg_parser):
    """Register all subclasses of Command.
    """
    cmd_parsers = arg_parser.add_subparsers()
    for cmd in get_commands():
        # use first line of docstring as help
        help = (cmd.__doc__ or 'no help').strip().splitlines()[0]

        cmd_parser = cmd_parsers.add_parser(cmd.__name__.lower(), help=help)

        # add optional command-specific arguments
        for (args, kw) in cmd.args:
            cmd_parser.add_argument(*args, **kw)
        # This is really, really important!
        # Without it we won't know which command to execute.
        cmd_parser.set_defaults(command_class=cmd)

def bootstrap():
    # check if the folder exists

    # create it if it doesnt exist

    #
    DEFAULT_FOLDER_NAME = ".debvenvs"
    DEFAULT_FOLDER_LOCATION = os.path.join(os.path.expanduser('~'),DEFAULT_FOLDER_NAME)
    packr_HOME = os.getenv('packr_HOME', DEFAULT_FOLDER_LOCATION)

    os.environ['packr_HOME'] = packr_HOME

    if not os.path.exists(packr_HOME):
        os.makedirs(packr_HOME)




def main():
    import argparse

    #env.settings
    bootstrap()

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-v', '--verbose', action='store_false')

    # register commands
    register_commands(arg_parser)

    if len(sys.argv)==1:
            arg_parser.print_help()
            sys.exit(1)


    # parse args including which command to run
    args = arg_parser.parse_args(sys.argv[1:])



    # create instance of command and execute
    command = args.command_class()
    command.execute(args)


if __name__ == '__main__':

    exit = main()
    if exit:
        sys.exit()
