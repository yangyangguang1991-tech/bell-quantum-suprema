"""Check the integrity of every listed release file using the standard library."""
if not __debug__:
    raise RuntimeError("Run without -O or -OO: verification requires assertions.")

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    lines = (ROOT / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines()
    seen = set()
    for line in lines:
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        if match is None:
            raise ValueError('Malformed checksum record')
        digest, relative = match.groups()
        if relative in seen:
            raise ValueError('Duplicate checksum path')
        seen.add(relative)
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError('Missing or invalid release path: ' + relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Checksum mismatch: ' + relative)
    if not seen:
        raise ValueError('Empty checksum manifest')
    print('PASS: integrity of', len(seen), 'listed release files')


if __name__ == '__main__':
    main()
