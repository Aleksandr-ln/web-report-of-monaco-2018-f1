import os

BASE_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../data"))

START_LOG = os.path.join(BASE_DIR, "start.log")
END_LOG = os.path.join(BASE_DIR, "end.log")
ABBREVIATIONS_FILE = os.path.join(BASE_DIR, "abbreviations.txt")
