import sys
from os.path import abspath, dirname

try:
    import inflation
except ModuleNotFoundError:
    base_path = abspath(dirname(dirname(__file__)))
    sys.path.insert(1, base_path)
    import inflation
