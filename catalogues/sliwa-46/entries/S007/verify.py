from pathlib import Path
import subprocess,sys
if not __debug__:raise SystemExit('Exact verification requires assertions; omit -O and -OO.')
if len(sys.argv)!=1:raise SystemExit('Use root run.py for additional options.')
root=Path(__file__).resolve().parents[2]
raise SystemExit(subprocess.call([sys.executable,'-S',str(root/'run.py'),'verify','--id','7'],cwd=root))
