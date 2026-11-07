"""Reject deliberately corrupted manuscript root selectors."""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.dont_write_bytecode=True
from tools.verify_root_selectors import check_record

def main():
    records=json.loads((ROOT/'data/compact_root_selectors.json').read_text(encoding='utf-8'))['records']
    uni=next(r for r in records if r['kind']=='univariate')
    system=next(r for r in records if r['kind']=='system')
    cases=[]
    r=deepcopy(uni);r['interval']=['0','1'];cases.append(('wrong_univariate_root',r))
    r=deepcopy(uni);r['polynomial']='q-1';cases.append(('changed_defining_polynomial',r))
    r=deepcopy(system);r['centers'][0]='0';cases.append(('displaced_contact_box',r))
    r=deepcopy(system);r['preconditioner'][0][0]='0';cases.append(('false_rational_preconditioner',r))
    r=deepcopy(system);r['radius']='-1';cases.append(('negative_box_radius',r))
    for name,record in cases:
        try:check_record(record)
        except ArithmeticError:continue
        raise ArithmeticError('Corrupted selector was accepted: '+name)
    print(json.dumps({'status':'PASS_ALL_5_SELECTOR_MUTATION_CONTROLS',
        'rejected':[name for name,r in cases]},indent=2))

if __name__=='__main__':main()
