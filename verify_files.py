"""Check the complete offline distribution or the lightweight Git source edition."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import re
import sys

ROOT = Path(__file__).resolve().parent
IGNORED = {'.git', '__pycache__', 'exports', 'verification_runs'}


def check(source_only=False):
    manifest = ROOT / ('SOURCE_FILES.sha256' if source_only else 'SHA256SUMS.txt')
    expected = {}
    for line in manifest.read_text(encoding='utf-8').splitlines():
        if not line:
            continue
        h, rel = line.split('  ', 1)
        p = PurePosixPath(rel)
        if (not re.fullmatch('[0-9a-f]{64}', h) or p.is_absolute() or
                '..' in p.parts or '\\' in rel or ':' in rel or rel in expected):
            raise ValueError('Invalid or duplicate manifest record.')
        expected[rel] = h
    if not expected:
        raise ValueError('Empty manifest.')
    for rel, expected_hash in expected.items():
        path = ROOT / rel
        if not path.is_file() or path.is_symlink():
            raise ValueError(f'Missing distribution file: {rel}. Obtain and extract every complete-release volume; no download is performed by this verifier.')
        h = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                h.update(block)
        if h.hexdigest() != expected_hash:
            raise ValueError(f'File digest mismatch: {rel}')
    if not source_only:
        actual = set()
        for p in ROOT.rglob('*'):
            rel = p.relative_to(ROOT)
            if any(x in IGNORED for x in rel.parts) or p.suffix in {'.pyc', '.pyo', '.log'}:
                continue
            if p.is_file() and p != manifest:
                actual.add(rel.as_posix())
        if actual != set(expected):
            raise ValueError(f'Unexpected or unlisted distribution files: {sorted(actual ^ set(expected))[:10]}')
    print(f'PASS {len(expected)} file hashes ({"Git source edition" if source_only else "complete offline distribution"}); no mathematical proof replay was performed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-only', action='store_true')
    args = parser.parse_args()
    try:
        check(args.source_only)
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
