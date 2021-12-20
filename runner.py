from selket import executor
from selket.sitegen import serve, state_vars
import argparse as ap
from pathlib import Path

arg = ap.ArgumentParser()
arg.add_argument(
    "-n", help="site name", required=True, type=str, default="myamazingsite"
)
arg.add_argument("-s", help="serve site", required=False, action="store_true")
arg.add_argument("-p", help="new post", required=False, action="store_true")
arg.add_argument(
    "-f",
    help="BE CAREFUL : delete everything and create fresh paths",
    required=False,
    type=bool,
    default=False,
)

ag = arg.parse_args()
print(ag)

if ag.s == False:
    executor.main(ag)
else:
    executor.main(ag)
    serve()
