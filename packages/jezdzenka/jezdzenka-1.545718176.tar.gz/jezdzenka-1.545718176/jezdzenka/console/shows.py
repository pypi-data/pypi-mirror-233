import os
import subprocess
import sys

from jezdzenka.database import collection
from jezdzenka.application import app as jezdzenka


def show_object(doc_id: int):
    directory = jezdzenka.configuration
    if collection.get_archived_status_by_id(doc_id):
        directory += jezdzenka.archived_directory
    path = os.path.join(directory, collection.get_filename_by_id(doc_id))
    if sys.platform == "win32":
        os.startfile(path)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.run([opener, path], check=True)