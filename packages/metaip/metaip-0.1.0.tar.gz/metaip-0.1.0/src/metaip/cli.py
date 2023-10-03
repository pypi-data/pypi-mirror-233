# Core Library modules
import argparse


def _parse_args(args: list) -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    """Function to return the ArgumentParser object created from all the args.

    Args:
        args:   A list of arguments from the commandline
                e.g. ['metaip', '-r',]
    """
    parser = argparse.ArgumentParser(
        prog="metaip",
        description="Return the latitude and longitude for a given IP address",
    )
    parser.add_argument(
        "ip_address",
        default="None",
        help="IP address to query",
    )
    parser.add_argument(
        "-k",
        "--key",
        help="Manually specify a new key to use.",
    )

    return parser.parse_args(args), parser
