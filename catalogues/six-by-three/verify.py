"""Reproduce one entry or the complete seven-class catalogue offline."""

if not __debug__:
    raise RuntimeError("Run without -O or -OO: exact verification requires assertions.")

import argparse, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'common'))
from census import check_facet
from classification import run as classify

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('entry',nargs='?',default='all',help='0 to 6, or all (default)')
    args=parser.parse_args()
    entries=sorted((ROOT/'entries').iterdir())
    assert [p.name[:2] for p in entries]==[f'{i:02d}' for i in range(7)]
    if args.entry!='all':
        try:i=int(args.entry)
        except ValueError:parser.error('entry must be all or an integer from 0 to 6')
        if not 0<=i<=6:parser.error('entry must be all or an integer from 0 to 6')
        entries=[entries[i]]
    for entry in entries:
        data=json.loads((entry/'definition.json').read_text(encoding='utf-8'))
        meta=json.loads((entry/'proof.json').read_text(encoding='utf-8'))
        assert meta['entry']==entry.name and meta['label']==data['label']
        assert meta['command']==['python','-B','verify.py']
        assert all((entry/name).is_file() for name in meta['materials'])
        check_facet(data['active_table'])
        subprocess.run([sys.executable,'-I','-B',str(entry/'verify.py')],check=True)
    if args.entry=='all':classify()
    print('PASS:', 'all seven entries and exact catalogue completeness' if args.entry=='all' else entries[0].name)
if __name__=='__main__':main()
