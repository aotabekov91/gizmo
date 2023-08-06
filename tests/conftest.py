import sys
from pathlib import Path

dir_path=Path(Path(__file__).parent.parent)
sys.path.insert(0, str(dir_path.joinpath('src')))
