if not __debug__:
    raise RuntimeError("Run without -O or -OO: exact verification requires assertions.")

from pathlib import Path
import sys
entry=Path(__file__).resolve().parent
sys.path.insert(0,str(entry.parents[1]/"common"))
from check_entry import run
run(entry)
