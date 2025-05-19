# directory for data to main

from pathlib import Path

DATA_DIRECTORY = Path(__file__).parents[1] / "data"

print(DATA_DIRECTORY)