import argparse

from src.core.domain.parse_code import *

parser = argparse.ArgumentParser(description="SeePy arguments")

parser.add_argument(
    "--path", type=str, help="path of project directory, such my_project/"
)
parser.add_argument(
    "--type", type=str, help="type of chart: function flow or class extension"
)
args = parser.parse_args()

if args.path and args.type in ["flow", "class"]:
    parse_output = parse_project(args.path)
    if args.type == "flow":
        extract = parse_output.func_net
    else:
        extract = parse_output.class_net
