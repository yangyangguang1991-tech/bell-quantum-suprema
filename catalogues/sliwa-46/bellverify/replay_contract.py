"""Fixed replay steps and per-step result files for the 46-entry corpus.

The command list and writable result names belong to the verifier, not to
certificate data. Everything else in the executed entry is frozen for each
step. In particular, S28_root_independent_replay.json may be produced by the
root step, but is a frozen input when the next global step consumes it.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ANALYTIC_IDS = (1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 20,
                26, 29, 30, 37, 38, 43, 44, 45)
RADICAL_IDS = (5, 18, 23)
INDIVIDUAL_COMMANDS = {
    16: ('verify_16_algebra.py', 'verify_16_field_independent.py'),
    19: ('verify_19_independent.py',),
    21: ('verify_21_global_independent.py',),
    22: ('verify_22_independent.py',),
    24: ('verify_24_independent.py',),
    25: ('verify_25_independent.py',),
    27: ('verify_s27_global_independent.py',),
    28: ('verify_s28_root_independent.py', 'verify_s28_global_independent.py'),
    31: ('verify_31_independent.py',),
    32: ('verify_32_independent.py',),
    33: ('verify_s33_global_independent.py',),
    34: ('verify_34_independent.py',),
    35: ('verify_35_independent.py',),
    36: ('verify_36_independent.py',),
    39: ('verify_39_independent.py',),
    40: ('verify_40_independent.py', 'verify_40_single_field.py'),
    41: ('verify_41_independent.py',),
    42: ('verify_42_independent.py',),
    46: ('verify_46_plus.py', 'verify_46_reduced.py', 'verify_boundary.py',
         'verify_sliwa46_bernstein_independent.py'),
}

# Exact, finite names audited against each verifier's reads and writes.
# A file is exempt only while its own producer runs. No certificate, selector,
# characteristic polynomial, program, or entry definition is exempt.
COMMAND_RESULTS = {
    '@analytic': ('result.json',),
    '@radical': ('result.json',),
    'verify_16_algebra.py': (),
    'verify_16_field_independent.py': ('verification_16_field_independent.json',),
    'verify_19_independent.py': ('S19_independent_replay.json',),
    'verify_21_global_independent.py': ('S21_global_independent_replay.json',),
    'verify_22_independent.py': ('S22_independent_replay.json',),
    'verify_24_independent.py': ('S24_independent_replay.json',),
    'verify_25_independent.py': ('S25_independent_replay.json',),
    'verify_s27_global_independent.py': ('S27_global_independent_replay.json',),
    'verify_s28_root_independent.py': ('S28_root_independent_replay.json',),
    'verify_s28_global_independent.py': ('S28_global_independent_replay.json',),
    'verify_31_independent.py': ('S31_independent_replay.json',),
    'verify_32_independent.py': ('S32_independent_replay.json',),
    'verify_s33_global_independent.py': ('S33_global_independent_replay.json',),
    'verify_34_independent.py': ('S34_independent_replay.json',),
    'verify_35_independent.py': ('S35_independent_replay.json',),
    'verify_36_independent.py': ('S36_independent_replay.json',),
    'verify_39_independent.py': ('S39_independent_replay.json',),
    'verify_40_independent.py': ('S40_independent_replay.json',),
    'verify_40_single_field.py': ('S40_single_field_verified.json',),
    'verify_41_independent.py': ('S41_independent_replay.json',),
    'verify_42_independent.py': ('S42_independent_replay.json',),
    'verify_46_plus.py': ('verification_46_plus.json',),
    'verify_46_reduced.py': ('verification_46_reduced.json',),
    'verify_boundary.py': (),
    'verify_sliwa46_bernstein_independent.py': ('independent_sliwa46_bernstein_replay.json',),
}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def expected_config(i):
    require(type(i) is int and 1 <= i <= 46, 'Invalid entry identifier')
    if i in ANALYTIC_IDS:
        engine, commands, characteristic = 'analytic', ('@analytic',), f'S{i:02d}_charpoly.txt'
    elif i in RADICAL_IDS:
        engine, commands, characteristic = 'radical', ('@radical',), f'S{i}_charpoly.txt'
    else:
        engine, commands = 'individual', INDIVIDUAL_COMMANDS[i]
        characteristic = f'charpoly_{i}_full.txt' if i in (16, 46) else f'S{i}_charpoly.txt'
    return {'id': i, 'engine': engine, 'characteristic_file': characteristic,
            'commands': list(commands)}


def check_entry(directory, expected_id=None):
    directory = Path(directory)
    functional = json.loads((directory / 'functional.json').read_text(encoding='utf-8'))
    i = functional['id']
    if expected_id is not None:
        require(i == expected_id, 'Requested entry and Bell functional identifiers disagree')
    expected = expected_config(i)
    actual = json.loads((directory / 'upper_bound/inputs.json').read_text(encoding='utf-8'))
    require(actual == expected,
            f'S{i}: upper engine, characteristic file and ordered commands must match the fixed replay contract')
    return expected


def command_result_paths(i, command):
    require(command in expected_config(i)['commands'], 'Unexpected upper command')
    return tuple('upper_bound/' + name for name in COMMAND_RESULTS[command])


def snapshot(directory, result_paths=()):
    """Hash every regular file except the current command's exact result names."""
    directory = Path(directory)
    excluded = frozenset(result_paths)
    files = {}
    for path in directory.rglob('*'):
        require(not path.is_symlink(), 'Symlinks are not supported inside a proof entry')
        if path.is_file():
            relative = path.relative_to(directory).as_posix()
            if relative not in excluded:
                files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def require_unchanged(directory, before, result_paths=(), context='Proof inputs'):
    after = snapshot(directory, result_paths)
    changed = sorted(name for name in before.keys() | after.keys()
                     if before.get(name) != after.get(name))
    require(not changed, context + ' changed during replay: ' + ', '.join(changed[:8]))


def snapshot_digest(files):
    return hashlib.sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
