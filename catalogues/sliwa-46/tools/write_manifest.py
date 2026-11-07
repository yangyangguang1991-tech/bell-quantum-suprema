from __future__ import annotations
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rows=[]
for p in ROOT.rglob('*'):
    rel=p.relative_to(ROOT)
    if not p.is_file()or any(a in {'.git','__pycache__','exports','verification_runs'}for a in rel.parts):continue
    if p.name=='MANIFEST.sha256'or p.suffix in {'.pyc','.pyo','.log'}:continue
    rows.append((rel.as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()))
(ROOT/'MANIFEST.sha256').write_text(''.join(f'{h}  {r}\n'for r,h in sorted(rows)),encoding='utf-8',newline='\n')
print(f'Wrote {len(rows)} file hashes')
