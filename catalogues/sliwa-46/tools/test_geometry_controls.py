"""Exact controls for the contact-box and signed-power input premises.

Uses only the Python standard library. Original entries remain unchanged;
altered copies are created in a temporary directory and removed afterwards.
These controls complement, and do not replace, the complete upper proofs.
"""
from __future__ import annotations
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from bellverify.proof_inputs import check


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def snapshot(directory):
    return {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in directory.rglob('*') if p.is_file()}


def main():
    originals = {i: ROOT / 'entries' / f'S{i:03d}' for i in (21, 27, 33)}
    before = {i: snapshot(p) for i, p in originals.items()}
    for i, directory in originals.items():
        require(check(directory, i)['status'] == 'PASS_UPPER_ATTAINMENT_INPUT_BINDING',
                f'Original S{i:03d} binding failed')
    cases = [(21, 'unequal_contact_intervals')]
    cases += [(i, mode) for i in (27, 33) for mode in ('negative_q_interval', 'reversed_q_interval')]
    records = []
    with tempfile.TemporaryDirectory(prefix='sliwa-geometry-') as temporary:
        for i, mode in cases:
            copied = Path(temporary) / f'S{i:03d}_{mode}'
            shutil.copytree(originals[i], copied)
            if i == 21:
                path = copied / 'upper_bound' / 'S21_global_certificate.json'
                data = json.loads(path.read_text(encoding='utf-8'))
                data['local_convexity_box'][1][0] = str(
                    Fraction(data['local_convexity_box'][1][0]) - Fraction(1, 100))
                expected = 'S21 symmetric slab construction requires equal first two contact intervals'
            else:
                path = copied / 'upper_bound' / f'S{i}_exact_algebraic_point.json'
                data = json.loads(path.read_text(encoding='utf-8'))
                interval = ['-2', '-1'] if mode == 'negative_q_interval' else ['2', '1']
                data['q_root_isolating_interval'] = interval
                # Keep the exported selector in agreement, so rejection tests
                # the signed-power premise rather than a selector mismatch.
                spec_path = copied / 'strategy_spec.json'
                spec = json.loads(spec_path.read_text(encoding='utf-8'))
                spec['interval'] = interval
                spec_path.write_text(json.dumps(spec), encoding='utf-8')
                expected = 'Signed q-power bounds require a positive ordered root interval'
            path.write_text(json.dumps(data), encoding='utf-8')
            try:
                check(copied, i)
            except RuntimeError as error:
                require(str(error) == expected, f'Unexpected rejection for {i}: {error}')
            else:
                raise RuntimeError(f'Altered S{i:03d} was accepted: {mode}')
            records.append({'id': i, 'mutation': mode, 'rejected': True})
    require(all(snapshot(p) == before[i] for i, p in originals.items()), 'An original entry changed')
    print(json.dumps({'status': 'PASS_SPECIFIED_GEOMETRY_CONTROLS',
                      'original_bindings': len(originals), 'negative_controls': len(records),
                      'original_entries_unchanged': True, 'records': records}, indent=2))


if __name__ == '__main__':
    main()
