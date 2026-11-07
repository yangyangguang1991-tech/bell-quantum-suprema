"""Check the byte-level integrity of the distributed files (not their mathematical claims)."""
from pathlib import Path
import argparse, hashlib, sys

ROOT = Path(__file__).resolve().parent

def check(root):
    expected = {}
    for line in (root / "SHA256SUMS.txt").read_text(encoding="utf-8-sig").splitlines():
        if not line:
            continue
        digest, name = line.split("  ", 1)
        path = root / name
        if name in expected or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("Invalid or duplicate manifest entry: " + name)
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("Manifest path outside the catalogue: " + name)
        expected[name] = digest
    for name, digest in expected.items():
        with (root / name).open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != digest:
            raise ValueError("File digest mismatch: " + name)
    print("PASS", len(expected), "distributed file hashes. Mathematical replay is separate.")

if __name__ == "__main__":
    check(ROOT)
