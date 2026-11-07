"""Fast standard-library checks of all delivered entries and strategies."""
from __future__ import annotations
import itertools,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from run import verify_manifest
from bellverify.proof_inputs import check as bind_inputs
from tools.check_strategy import check as score
from tools.check_exact_dag import check as dag

def require(ok,message):
    if not ok:raise RuntimeError(message)

def main():
    verify_manifest();rows=json.loads((ROOT/'catalogue.json').read_text(encoding='utf-8'))
    require([r['id']for r in rows]==list(range(1,47)),'Catalogue coverage mismatch')
    require({p.name for p in(ROOT/'entries').iterdir()if p.is_dir()}=={f'S{i:03d}'for i in range(1,47)},'Unexpected entry directory')
    results=[]
    for row in rows:
        i=row['id'];entry=ROOT/'entries'/f'S{i:03d}';bind_inputs(entry)
        f=json.loads((entry/'functional.json').read_text(encoding='utf-8'))
        n=json.loads((entry/'attainment/strategy_numeric.json').read_text(encoding='utf-8'))
        e=json.loads((entry/'attainment/strategy_exact.json').read_text(encoding='utf-8'))
        c=json.loads((entry/'upper_bound/inputs.json').read_text(encoding='utf-8'))
        require(c['id']==f['id']==n['id']==i,'Entry identity mismatch')
        require(n['literal_expression']==f['expression'],'Literal expression mismatch')
        require(e['parameters']==json.loads((entry/'strategy_spec.json').read_text(encoding='utf-8')),'Exact parameter mismatch')
        require(e['characteristic_polynomial']==(entry/'upper_bound'/c['characteristic_file']).read_text().strip(),'Characteristic mismatch')
        require(row['q_display']==n['q_display'],'Value display mismatch')
        terms=[]
        for t in re.findall(r'[+-]?[^+-]+',f['expression'].replace(' ','')):
            m=re.fullmatch(r'([+-]?)(\d*)([AaBbCc]+)',t);require(m is not None,'Malformed Bell term')
            s,k,w=m.groups();terms.append(((-1 if s=='-'else 1)*int(k or '1'),w))
        scores=[]
        for signs in itertools.product((-1,1),repeat=6):
            env=dict(zip('AaBbCc',signs));value=0
            for k,w in terms:
                term=k
                for name in w:term*=env[name]
                value+=term
            scores.append(value)
        require(max(scores)==f['local_bound']==row['local_bound'],'Local bound mismatch')
        score(entry/'attainment/strategy_numeric.json')
        dag(entry/'attainment/strategy_exact.json',entry/'attainment/strategy_numeric.json')
        # Filenames in a numbered entry cannot carry another entry's payload.
        for path in entry.rglob('*'):
            if not path.is_file():continue
            for match in re.finditer(r'S(\d{1,3})(?:_|\.|$)',path.name):
                require(int(match[1])==i,'Another numbered entry is embedded here')
        results.append({'id':i,'status':'PASS_DELIVERED_DATA_AND_STRATEGY'})
    print(json.dumps({'status':'PASS_ALL_46_DELIVERED_ENTRIES','entries':46,'checks':results,
          'scope':'Integrity, input binding, local bounds and independent supplied-strategy checks; run.py verify --all also replays exact upper proofs.'},indent=2))

if __name__=='__main__':main()
