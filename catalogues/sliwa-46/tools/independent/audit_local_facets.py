"""Independent exact audit of the 46 supplied correlator facet representatives.

Uses only Python standard-library integer/Fraction arithmetic. Does not import
the package's parser, proof libraries, vendored CAS, or saved verification logs.
It verifies facet rank and inequivalence, not an independent H-representation
enumeration of the local polytope.
"""
from __future__ import annotations

import argparse
import itertools as it
import json
import re
from fractions import Fraction
from pathlib import Path


TERMS = tuple(t for t in it.product(range(3), repeat=3) if any(t))
INDEX = {t: k for k, t in enumerate(TERMS)}
LETTERS = 'AaBbCc'


def parse(expression):
    expression = re.sub(r'\s+', '', expression)
    found = re.findall(r'([+-]?)(\d*)([AaBbCc]+)', expression)
    reconstructed = ''.join(a + b + c for a, b, c in found)
    if reconstructed != expression:
        raise ValueError('Unexpected literal syntax')
    vector = [0] * 26
    for sign, number, word in found:
        triple = [0, 0, 0]
        for letter in word:
            k = LETTERS.index(letter)
            if triple[k // 2]:
                raise ValueError('Duplicate party')
            triple[k // 2] = 1 + k % 2
        vector[INDEX[tuple(triple)]] += (-1 if sign == '-' else 1) * int(number or 1)
    return tuple(vector)


def exact_rank(rows):
    rows = [list(map(Fraction, row)) for row in rows]
    rank = 0
    for col in range(len(rows[0])):
        pivot = next((j for j in range(rank, len(rows)) if rows[j][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        a = rows[rank][col]
        rows[rank] = [t / a for t in rows[rank]]
        for j in range(rank + 1, len(rows)):
            a = rows[j][col]
            if a:
                rows[j] = [v - a * w for v, w in zip(rows[j], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def transformations():
    out = []
    for permutation in it.permutations(range(3)):
        for swaps in it.product(range(2), repeat=3):
            target = []
            masks = []
            for term in TERMS:
                mapped = [0, 0, 0]
                mask = []
                for party, setting in enumerate(term):
                    if setting:
                        mapped[permutation[party]] = 1 + ((setting - 1) ^ swaps[party])
                        mask.append(2 * party + setting - 1)
                target.append(INDEX[tuple(mapped)])
                masks.append(mask)
            for flips in it.product((-1, 1), repeat=6):
                mapping = [None] * 26
                for source, dest in enumerate(target):
                    sign = 1
                    for k in masks[source]:
                        sign *= flips[k]
                    mapping[dest] = (source, sign)
                out.append(mapping)
    if len(out) != 3072:
        raise ArithmeticError('Wrong relabeling group size')
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    vertices = []
    for assignment in it.product((-1, 1), repeat=6):
        row = []
        for term in TERMS:
            product = 1
            for party, setting in enumerate(term):
                if setting:
                    product *= assignment[2 * party + setting - 1]
            row.append(product)
        vertices.append(row)
    full_rank = exact_rank([[1] + v for v in vertices]) - 1
    if full_rank != 26:
        raise ArithmeticError('Local affine dimension differs')
    relabelings = transformations()
    representatives = set()
    records = []
    for i in range(1, 47):
        path = args.repository / 'entries' / f'S{i:03d}' / 'functional.json'
        data = json.loads(path.read_text())
        coefficients = parse(data['expression'])
        scores = [sum(a * b for a, b in zip(v, coefficients)) for v in vertices]
        maximum = max(scores)
        if maximum != data['local_bound']:
            raise ArithmeticError(f'S{i:03d}: local bound mismatch')
        saturated = [v for v, s in zip(vertices, scores) if s == maximum]
        rank = exact_rank([[1] + v for v in saturated]) - 1
        if rank != 25:
            raise ArithmeticError(f'S{i:03d}: not a facet')
        orbit = {tuple(sign * coefficients[k] for k, sign in transform)
                 for transform in relabelings}
        representative = (maximum, min(orbit))
        if representative in representatives:
            raise ArithmeticError(f'S{i:03d}: duplicated equivalence class')
        representatives.add(representative)
        records.append({'id': i, 'local_bound': maximum,
                        'tight_vertices': len(saturated), 'tight_affine_rank': rank,
                        'orbit_size': len(orbit), 'stabilizer_size': 3072 // len(orbit),
                        'nonzero_terms': sum(c != 0 for c in coefficients)})
        print(f'S{i:03d}: L={maximum}, tight rank={rank}, orbit={len(orbit)}', flush=True)
    output = {'status': 'PASS_ALL_46_LOCAL_FACETS_AND_PAIRWISE_INEQUIVALENCE',
              'local_vertices': len(vertices), 'affine_dimension': full_rank,
              'relabelings': len(relabelings), 'distinct_classes': len(representatives),
              'total_orbit_size': sum(r['orbit_size'] for r in records),
              'nonzero_literal_terms': sum(r['nonzero_terms'] for r in records),
              'scope': 'Exact local bounds, facet ranks, and symmetry orbits; no quantum upper bound is inferred.',
              'records': records}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'records'}, indent=2))


if __name__ == '__main__':
    main()
