# run.py
import argparse
import logging

from app import create_app

parser = argparse.ArgumentParser()
parser.add_argument(
    "--debug",
    action="store_true",
    help="Enable debug logging",
)
args = parser.parse_args()

logging.basicConfig(
    level=logging.DEBUG if args.debug else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = create_app()
print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)
