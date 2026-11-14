import argparse
from seepy.event.message_bus import *
from seepy.event.event import *
from seepy.application import load_project

parser = argparse.ArgumentParser(description="SeePy arguments")

parser.add_argument(
    "--path", type=str, help="path of project directory, such my_project/"
)
parser.add_argument(
    "--type", type=str, help="type of chart: function flow or class extension"
)
args = parser.parse_args()

print(1)
message_bus.post(OnStart({"path": args.path, "ui_type": args.type}))