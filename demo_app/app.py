import sys
from pathlib import Path
# Ensure the root directory is in the path so 'captchard' can be found
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import run

run()
