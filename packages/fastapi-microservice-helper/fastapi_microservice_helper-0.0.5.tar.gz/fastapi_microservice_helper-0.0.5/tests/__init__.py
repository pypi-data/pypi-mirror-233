import os
import sys

app_dir = os.path.abspath(os.path.dirname(__file__)) + '/../src'
if app_dir not in sys.path:
    sys.path.append(app_dir)