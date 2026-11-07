"""Mutations must be rejected; no changes are made to the published entries."""
from __future__ import annotations
import copy,json,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.check_strategy import check
from tools.check_exact_dag import check as check_dag

def main():
    d=ROOT/'entries/S021/attainment'
    original=json.loads((d/'strategy_numeric.json').read_text())
    exact=json.loads((d/'strategy_exact.json').read_text())
    tests=[]
    def reject(name,action):
        try:action()
        except (ArithmeticError,RuntimeError,ValueError,ZeroDivisionError,KeyError):tests.append(name);return
        raise RuntimeError(f'Mutation was accepted: {name}')
    with tempfile.TemporaryDirectory(prefix='sliwa46-negative-')as temporary:
        p=Path(temporary)/'strategy.json';ep=Path(temporary)/'exact.json'
        for name,change in [
            ('state_amplitude',lambda a:a['state_vector_real'].__setitem__(0,'0.999')),
            ('observable_reflection',lambda a:a['observables_real']['A'][0].__setitem__(0,'2')),
            ('bell_coefficient',lambda a:a.__setitem__('literal_expression','999A')),
            ('target_value',lambda a:a.__setitem__('q_display','100')),
        ]:
            mutated=copy.deepcopy(original);change(mutated);p.write_text(json.dumps(mutated))
            reject(name,lambda:check(p))
        p.write_text(json.dumps(original))
        for name,change in [
            ('dag_bad_reference',lambda a:a['nodes'].__setitem__(0,{'op':'add','args':[999999]})),
            ('dag_wrong_state_root',lambda a:a['state_vector_nodes'].__setitem__(0,a['normalization_squared_node'])),
            ('nonpositive_norm_certificate',lambda a:a.__setitem__('normalization_squared_rational_interval',['-1','0'])),
        ]:
            mutated=copy.deepcopy(exact);change(mutated);ep.write_text(json.dumps(mutated))
            reject(name,lambda:check_dag(ep,p))
    print(json.dumps({'status':'PASS_NEGATIVE_CONTROLS','rejected':tests,'count':len(tests)},indent=2))

if __name__=='__main__':main()
