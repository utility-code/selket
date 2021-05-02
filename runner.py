from selket import executor
import argparse as ap

arg = ap.ArgumentParser()
arg.add_argument(
    "-n", help="site name", required=True, type=str, default="myamazingsite"
)
arg.add_argument("-s", help="serve site", required=False, type=bool, default=False)
arg.add_argument("-p", help="new post", required=False, type=bool, default=False)
arg.add_argument(
    "-f",
    help="BE CAREFUL : delete everything and create fresh paths",
    required=False,
    type=bool,
    default=False,
)

ag = arg.parse_args()

executor.main(ag)
