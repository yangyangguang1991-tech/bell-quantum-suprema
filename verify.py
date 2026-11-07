"""Run the catalogue proof programs through one offline entry point."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CATALOGUES = {
    'sliwa': ROOT / 'catalogues/sliwa-46',
    'six-by-three': ROOT / 'catalogues/six-by-three',
    'york': ROOT / 'catalogues/york-4422',
}
UNKNOWN = frozenset((83, 92, 125, 128))


def invoke(path, *args, no_site=False):
    env = dict(os.environ)
    env.update(PYTHONOPTIMIZE='', PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1',
               PYTHONNOUSERSITE='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', OMP_NUM_THREADS='1')
    command = [sys.executable, '-B']
    if no_site:
        command.append('-S')
    command.extend([str(path), *map(str, args)])
    print('Running:', path.relative_to(ROOT).as_posix(), *args, flush=True)
    subprocess.run(command, cwd=path.parent, env=env, check=True)


def definitions():
    s = CATALOGUES['sliwa']
    rows = json.loads((s / 'catalogue.json').read_text(encoding='utf-8'))
    if [r['id'] for r in rows] != list(range(1, 47)):
        raise ValueError('The Sliwa index must contain S001 through S046.')
    for n in range(1, 47):
        entry = s / 'entries' / f'S{n:03d}'
        for name in ('README.md', 'functional.json', 'strategy_spec.json', 'verify.py'):
            if not (entry / name).is_file():
                raise ValueError(f'Missing Sliwa entry document: {n}/{name}')
        json.loads((entry / 'functional.json').read_text(encoding='utf-8'))
    six = CATALOGUES['six-by-three'] / 'entries'
    entries = sorted(p for p in six.iterdir() if p.is_dir())
    if [e.name[:2] for e in entries] != [f'{i:02d}' for i in range(7)]:
        raise ValueError('The six-by-three index must contain seven entries.')
    for entry in entries:
        data = json.loads((entry / 'definition.json').read_text(encoding='utf-8'))
        if data['scenario'] != [6, 3, 2, 2]:
            raise ValueError('Incorrect six-by-three scenario.')
        for name in ('README.md', 'PROOF.md', 'proof.json', 'verify.py'):
            if not (entry / name).is_file():
                raise ValueError(f'Missing six-by-three entry document: {entry.name}/{name}')
    york = CATALOGUES['york'] / 'entries'
    if sorted(p.name for p in york.iterdir() if p.is_dir()) != [f'Y{i:03d}' for i in range(1, 176)]:
        raise ValueError('The York index must contain Y001 through Y175.')
    for n in range(1, 176):
        entry = york / f'Y{n:03d}'
        data = json.loads((entry / 'definition.json').read_text(encoding='utf-8'))
        if data['york_number'] != n:
            raise ValueError('York entry identifier mismatch.')
        if n in UNKNOWN:
            if (entry / 'proof.json').exists():
                raise ValueError('An unresolved entry unexpectedly has a proof descriptor.')
            if 'Exact unrestricted quantum supremum: unknown.' not in (entry / 'README.md').read_text(encoding='utf-8'):
                raise ValueError('An unresolved entry is not clearly identified.')
        else:
            for name in ('README.md', 'PROOF.md', 'proof.json'):
                if not (entry / name).is_file():
                    raise ValueError(f'Missing York entry document: {n}/{name}')
    invoke(ROOT / 'verify_crosswalk.py')
    invoke(CATALOGUES['york'] / 'verify_names.py')
    print('PASS catalogue definitions and exact coefficient correspondences; no global proof replay was requested.', flush=True)


def entry(name, number):
    path = CATALOGUES[name]
    if name == 'sliwa':
        invoke(path / 'run.py', 'verify', '--id', number, no_site=True)
    elif name == 'six-by-three':
        invoke(path / 'verify.py', number)
    else:
        if number not in UNKNOWN:
            directory = path / 'entries' / f'Y{number:03d}'
            config = json.loads((directory / 'proof.json').read_text(encoding='utf-8'))
            if any(not (directory / part).is_file() for part in config['parts']):
                raise ValueError('This source tree lacks York certificate payloads. Extract every complete-release volume before mathematical replay; no files are downloaded automatically.')
        invoke(path / 'verify.py', number)


def all_entries(name):
    if name == 'sliwa':
        for n in range(1, 47):
            entry(name, n)
    elif name == 'six-by-three':
        # The original default command also checks complete facet classification.
        invoke(CATALOGUES[name] / 'verify.py')
    else:
        for n in range(1, 176):
            entry(name, n)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--catalogue', choices=tuple(CATALOGUES))
    action = p.add_mutually_exclusive_group(required=True)
    action.add_argument('--all', action='store_true', help='Replay all supplied proofs, retaining unknown statements.')
    action.add_argument('--entry', type=int, help='Replay one numbered entry; requires --catalogue.')
    action.add_argument('--definitions-only', action='store_true', help='Check indices and coefficient maps, without global proof replay.')
    action.add_argument('--files', action='store_true', help='Check complete-distribution file hashes only.')
    a = p.parse_args()
    if not __debug__:
        p.error('Use ordinary Python without -O or -OO; exact checks require assertions.')
    if a.entry is not None:
        if a.catalogue is None:
            p.error('--entry requires --catalogue.')
        lo, hi = (0, 6) if a.catalogue == 'six-by-three' else (1, 46) if a.catalogue == 'sliwa' else (1, 175)
        if not lo <= a.entry <= hi:
            p.error(f'This catalogue uses entry numbers {lo} through {hi}.')
    elif a.catalogue is not None and not a.all:
        p.error('--catalogue is used with --entry or --all.')
    if a.files:
        invoke(ROOT / 'verify_files.py')
    elif a.definitions_only:
        definitions()
    elif a.entry is not None:
        entry(a.catalogue, a.entry)
    else:
        names = [a.catalogue] if a.catalogue else list(CATALOGUES)
        if 'york' in names:
            for n in range(1, 176):
                if n in UNKNOWN:
                    continue
                directory = CATALOGUES['york'] / 'entries' / f'Y{n:03d}'
                config = json.loads((directory / 'proof.json').read_text(encoding='utf-8'))
                if any(not (directory / part).is_file() for part in config['parts']):
                    raise ValueError('The full replay requires every complete-release volume. The lightweight source tree alone lacks York certificates.')
        definitions()
        for name in names:
            all_entries(name)
        print('All requested supplied proof commands completed; unresolved York entries remain unknown.', flush=True)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'Verification did not complete: {error}', file=sys.stderr)
        sys.exit(1)
