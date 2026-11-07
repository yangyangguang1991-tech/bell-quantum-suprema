"""Small in-memory positive/negative controls for the independent audit kernel."""
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
K = runpy.run_path(str(HERE / 'independent_attainment_audit.py'))


def main():
    package = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    if output.exists() or output == package or package in output.parents:
        raise RuntimeError('Use a new output path outside the original package')
    results = []
    def rejects(name, action):
        try:
            action()
        except (ArithmeticError, KeyError, ValueError) as error:
            results.append({'case': name, 'expected': 'reject', 'status': 'PASS_REJECTED', 'reason': str(error)})
        else:
            raise AssertionError(f'Control unexpectedly accepted: {name}')
    rejects('multi-character alias is not a declared parameter', lambda: K['parse_poly']('qx'))
    coeff = K['univariate'](K['parse_poly']('q**2 - 2'))
    rejects('Sturm box contains no root', lambda: K['sturm_isolate'](coeff, ['0', '1']))
    rejects('Sturm box contains two roots', lambda: K['sturm_isolate'](coeff, ['-2', '2']))
    equation = [K['parse_poly']('q**2 - 2')]
    rejects('singular zero preconditioner', lambda: K['contraction'](equation, ['q'], [(F(7, 5), F(3, 2))], [[F(0)]]))
    rejects('contractive map has no root inclusion', lambda: K['contraction'](equation, ['q'], [(F(1), F(11, 10))], [[F(1, 2)]]))
    K['contraction'](equation, ['q'], [(F(7, 5), F(3, 2))], [[F(1, 3)]])
    tower = K['QuadraticTower']()
    assert not any(tower.parse('sqrt(2)**2 - 2'))
    assert any(tower.parse('sqrt(2)**2 - 3'))
    assert not any(tower.parse('sqrt(3 + sqrt(2))**2 - 3 - sqrt(2)'))
    d = package / 'entries/S001'
    exact = json.loads((d / 'attainment/strategy_exact.json').read_text())
    literal = json.loads((d / 'functional.json').read_text())
    spec = json.loads((d / 'strategy_spec.json').read_text())
    P = K['parse_poly'](exact['characteristic_polynomial'])
    env, _, _ = K['selected_parameters'](spec, P, None)
    M, _ = K['literal_matrix'](literal['expression'])
    cc = K['complement'](P, exact['binding']['multiplicity'])
    K['audit_dag'](exact, M, cc, env)
    bad = deepcopy(exact)
    zero = next(j for j, n in enumerate(bad['nodes']) if n == {'op': 'rational', 'args': ['0']})
    bad['state_vector_nodes'][0] = zero
    rejects('one normalized state coordinate replaced by zero', lambda: K['audit_dag'](bad, M, cc, env))
    bad = deepcopy(exact)
    bad['nodes'][-1]['args'][0] = len(bad['nodes']) - 1
    rejects('self-reference in final DAG node', lambda: K['audit_dag'](bad, M, cc, env))
    bad = deepcopy(exact)
    bad['normalization_squared_rational_interval'] = ['0', '1']
    rejects('nonpositive supplied normalization certificate', lambda: K['audit_dag'](bad, M, cc, env))
    report = {'status': 'PASS_INDEPENDENT_KERNEL_CONTROLS', 'negative_controls': len(results),
              'positive_controls': ['simple contraction containing sqrt(2)', 'quadratic zero and nonzero identities',
                                    'nested radical defining identity', 'unchanged S001 complete exact DAG'],
              'scope': 'Small deterministic arithmetic and semantic controls; no claim of exhaustive software verification.',
              'original_files_written': False, 'results': results}
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
