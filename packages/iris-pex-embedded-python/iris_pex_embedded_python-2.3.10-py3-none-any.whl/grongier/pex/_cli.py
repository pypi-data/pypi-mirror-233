# _manager.py is the main entry point of the pex package
# it's a command line interface to manage productions
# eg :
#   python3 -m grongier.pex -h : display help and the default production name
#   python3 -m grongier.pex -l : list productions
#   python3 -m grongier.pex -d <production_name> : set the default production to <production_name>
#   python3 -m grongier.pex -s <production_name> : start a production named <production_name> if <production_name> is not set, the default production is started
#   python3 -m grongier.pex -k <production_name> : stop a production named <production_name> if <production_name> is not set, the default production is killed
#   python3 -m grongier.pex -r <production_name> : restart a production named <production_name> if <production_name> is not set, the default production is restarted
#   python3 -m grongier.pex -m <settings_file> : migrate a production and classes with the settings file <settings_file>
#   python3 -m grongier.pex -x <production_name> : export a production named <production_name> if <production_name> is not set, the default production is exported
from grongier.pex._director import _Director
from grongier.pex._utils import _Utils

import argparse
import json
from importlib.metadata import version 

def parse_args(argv):
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--default', help='set the default production', nargs='?', const='not_set')
    parser.add_argument('-l', '--list', help='list productions', action='store_true')
    parser.add_argument('-s', '--start', help='start a production', nargs='?', const='not_set')
    parser.add_argument('-S', '--stop', help='stop a production', action='store_true')
    parser.add_argument('-k', '--kill', help='kill a production', action='store_true')
    parser.add_argument('-r', '--restart', help='restart a production', action='store_true')
    parser.add_argument('-x', '--status', help='status a production', action='store_true')
    parser.add_argument('-m', '-M', '--migrate', help='migrate production and classes with settings file')
    parser.add_argument('-e', '--export', help='export a production', nargs='?', const='not_set')
    parser.add_argument('-v', '--version', help='display version', action='store_true')
    parser.add_argument('-L', '--log', help='display log', action='store_true')
    parser.add_argument('-i', '--init', help='init the pex module in iris', nargs='?', const='not_set')
    parser.add_argument('-t', '--test', help='test the pex module in iris', nargs='?', const='not_set')
    return parser.parse_args(argv)

def main(argv=None):
    # build arguments
    args = parse_args(argv)

    if args.default:
        # set default production
        if args.default == 'not_set':
            # display default production name
            print(_Director.get_default_production())
        else:
            _Director.set_default_production(args.default)

    elif args.lists:
        # display list of productions
        dikt = _Director.list_productions()
        print(json.dumps(dikt, indent=4))

    elif args.start:
        if args.start == 'not_set':
            # start default production
            args.start = _Director.get_default_production()
        _Director.start_production_with_log(args.start)

    elif args.init:
        if args.init == 'not_set':
            # set arg to None
            args.init = None
        _Utils.setup(args.start)

    elif args.kill:
        # kill a production
        _Director.shutdown_production()

    elif args.restart:
        # restart a production
        _Director.restart_production()

    elif args.migrate:
        # migrate a production
        _Utils.migrate(args.migrate)

    elif args.version:
        # display version
        print(version('iris-pex-embedded-python'))

    elif args.log:
        # display log
        _Director.log_production()

    elif args.stop:
        # stop a production
        _Director.stop_production()

    elif args.status:
        dikt=_Director.status_production()
        print(json.dumps(dikt, indent=4))

    elif args.test:
        _Director.test_component(args.test)

    elif args.export:
        if args.export == 'not_set':
            # export default production
            args.export=_Director.get_default_production()

        dikt = _Utils.export_production(args.export)
        print(json.dumps(dikt, indent=4))

    else:
        # display help and default production name
        print("usage: python3 -m grongier.pex [-h] [-d [DEFAULT]] [-l] [-s [START]] [-S] [-k] [-r] [-x] [-m [MIGRATE]] [-e [EXPORT]] [-v] [-L] [-i [INIT]] [-t [TEST]]")
        print("")
        print("optional arguments:")
        print("  -h, --help            show this help message and exit")
        print("  -d [DEFAULT], --default [DEFAULT]")
        print("                        set the default production")
        print("  -l, --list            list productions")
        print("  -s [START], --start [START]")
        print("                        start a production")
        print("  -S, --stop            stop a production")
        print("  -k, --kill            kill a production")
        print("  -r, --restart         restart a production")
        print("  -x, --status          status a production")
        print("  -m [MIGRATE], --migrate [MIGRATE]")
        print("                        migrate production and classes with settings file")
        print("  -e [EXPORT], --export [EXPORT]")
        print("                        export a production")
        print("  -v, --version         display version")
        print("  -L, --log             display log")
        print("  -i , --init")
        print("                        init the pex module in iris")
        print("  -t [TEST], --test [TEST]")
        print("                        test the pex module in iris")
        print("")
        print("default production: " + _Director.get_default_production())


if __name__ == '__main__':
    main()
