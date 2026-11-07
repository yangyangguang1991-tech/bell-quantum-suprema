"""Exact symbolic binding must reject wrong Bell targets and root definitions."""
from __future__ import annotations
import json,shutil,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'third_party/vendor'),str(ROOT)]
from bellverify.exact import verify_binding,characteristic_path

def main():
    rejected=[]
    with tempfile.TemporaryDirectory(prefix='sliwa-exact-negative-')as temp:
        for name,i,change in [
            ('changed_literal_functional',21,lambda d:modify(d/'functional.json','expression',lambda a:a+'+abc')),
            ('wrong_isolating_interval',21,lambda d:modify(d/'strategy_spec.json','interval',lambda a:['0','1'])),
            ('illegal_measurement_overlap',21,lambda d:modify(d/'strategy_spec.json','overlaps',lambda a:['2','2','2'])),
            ('wrong_system_characteristic_factor',28,lambda d:modify(d/'strategy_spec.json','equations',lambda a:[a[0]+'+1',*a[1:]])),
        ]:
            dest=Path(temp)/name;dest.mkdir()
            for f in ['functional.json','strategy_spec.json']:
                shutil.copy2(ROOT/'entries'/f'S{i:03d}'/f,dest/f)
            shutil.copy2(characteristic_path(ROOT/'entries'/f'S{i:03d}'),dest/'characteristic_polynomial.txt')
            change(dest)
            try:verify_binding(dest)
            except (ArithmeticError,RuntimeError,ValueError):rejected.append(name);continue
            raise RuntimeError(f'Exact mutation accepted: {name}')
    print(json.dumps({'status':'PASS_EXACT_BINDING_NEGATIVE_CONTROLS','count':len(rejected),'rejected':rejected},indent=2))

def modify(path,key,change):
    d=json.loads(path.read_text(encoding='utf-8'));d[key]=change(d[key]);path.write_text(json.dumps(d),encoding='utf-8')

if __name__=='__main__':main()
