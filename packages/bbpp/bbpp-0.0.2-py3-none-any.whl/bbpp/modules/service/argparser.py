import argparse

class ArgParser:
    @classmethod
    def parse(cls, args):
        parser = argparse.ArgumentParser(
            prog='bbpp'
        )

        subparsers = parser.add_subparsers(help='options')
        parser.add_argument('-p', '--pipeline', help='Pipeline regex to match')
        config_parser = subparsers.add_parser('config', help='Configure authentication file')
        config_parser.add_argument('-u', '--username', required=True)
        config_parser.add_argument('-p', '--password', required=True)

        return parser.parse_args(args)
