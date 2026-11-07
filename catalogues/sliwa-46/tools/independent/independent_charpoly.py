#!/usr/bin/env python3
"""Exact independent literal/characteristic-polynomial check using only stdlib.

No author code, SymPy, determinant routine, floating point, or stored numerical
values are imported.  A degree proof turns the 5^3 integer grid into an exact
polynomial identity check, not a numerical sampling argument.

For tr(M^k), each local word in two reflections reduces to an alternating word.
Odd words have zero trace; an even word of length 2m has trace 2*T_m(t).
Hence every overlap degree is at most floor(k/2).  Newton identities preserve
this bound for the k-th characteristic coefficient.  For an 8 by 8 matrix the
degree is at most four in each overlap.  Five distinct points per coordinate
therefore determine each coefficient exactly.  The polynomial gauge extends
the characteristic identity from the physical open cube to all real overlaps.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import platform
import re
import time
from pathlib import Path

ZERO = (0, 0, 0, 0)
GRID = (-2, -1, 0, 1, 2)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def poly_add(a, b, sign=1):
    out = dict(a)
    for powers, coeff in b.items():
        out[powers] = out.get(powers, 0) + sign * coeff
        if out[powers] == 0:
            del out[powers]
    return out


def poly_mul(a, b):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            key = tuple(x + y for x, y in zip(ea, eb))
            out[key] = out.get(key, 0) + ca * cb
    return {key: val for key, val in out.items() if val}


def parse_polynomial(text):
    def parse(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return {ZERO: node.value} if node.value else {}
        if isinstance(node, ast.Name) and node.id in ('q', 'x', 'y', 'z'):
            exponents = [0, 0, 0, 0]
            exponents['qxyz'.index(node.id)] = 1
            return {tuple(exponents): 1}
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            out = parse(node.operand)
            return out if isinstance(node.op, ast.UAdd) else {e: -v for e, v in out.items()}
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Add):
                return poly_add(parse(node.left), parse(node.right))
            if isinstance(node.op, ast.Sub):
                return poly_add(parse(node.left), parse(node.right), -1)
            if isinstance(node.op, ast.Mult):
                return poly_mul(parse(node.left), parse(node.right))
            if isinstance(node.op, ast.Pow):
                require(isinstance(node.right, ast.Constant) and type(node.right.value) is int
                        and 0 <= node.right.value <= 8, 'Unsupported polynomial exponent')
                out = {ZERO: 1}
                for _ in range(node.right.value):
                    out = poly_mul(out, parse(node.left))
                return out
        raise ValueError(f'Unsupported polynomial syntax: {ast.dump(node)}')
    return parse(ast.parse(text.strip(), mode='eval').body)


def parse_literal(text):
    compact = ''.join(text.split())
    require(compact, 'Empty literal')
    if compact[0] not in '+-':
        compact = '+' + compact
    tokens = re.findall(r'([+-])(\d*)([AaBbCc]+)', compact)
    require(''.join(sign + number + word for sign, number, word in tokens) == compact,
            'Unparsed literal content')
    out = []
    for sign, number, word in tokens:
        parties = ['ABC'.index(letter.upper()) for letter in word]
        require(len(parties) == len(set(parties)), 'Repeated party in a literal term')
        coefficient = int(number or '1') * (-1 if sign == '-' else 1)
        require(coefficient != 0, 'Zero literal coefficient')
        settings = ['I'] * 3
        for party, letter in zip(parties, word):
            settings[party] = 'S' if letter.islower() else 'R'
        out.append((coefficient, tuple(settings)))
    return out


def kron(a, b):
    return [[av * bv for av in rowa for bv in rowb]
            for rowa in a for rowb in b]


def bell_matrix(terms, overlaps):
    identity = [[1, 0], [0, 1]]
    reflection = [[1, 0], [0, -1]]
    locals_ = [{'I': identity, 'R': reflection,
                'S': [[t, 1], [1 - t*t, -t]]} for t in overlaps]
    matrix = [[0] * 8 for _ in range(8)]
    for coefficient, settings in terms:
        term = [[1]]
        for party, setting in enumerate(settings):
            term = kron(term, locals_[party][setting])
        for row in range(8):
            for col in range(8):
                matrix[row][col] += coefficient * term[row][col]
    return matrix


def charpoly_faddeev(matrix):
    """Return monic coefficients, descending, checking every integer division."""
    n = len(matrix)
    rows = [[(j, a) for j, a in enumerate(row) if a] for row in matrix]
    current = [[int(i == j) for j in range(n)] for i in range(n)]
    coefficients = [1]
    for k in range(1, n + 1):
        product = [[sum(a * current[j][col] for j, a in rows[row])
                    for col in range(n)] for row in range(n)]
        trace = sum(product[i][i] for i in range(n))
        require(trace % k == 0, f'Nonintegral Faddeev coefficient at order {k}')
        coefficient = -trace // k
        coefficients.append(coefficient)
        for i in range(n):
            product[i][i] += coefficient
        current = product
    require(all(value == 0 for row in current for value in row),
            'Final Faddeev matrix is not zero')
    return coefficients


def evaluate_stored(poly, overlaps):
    powers = [[t**j for j in range(5)] for t in overlaps]
    coefficients = [0] * 9
    for (eq, ex, ey, ez), value in poly.items():
        coefficients[8 - eq] += value * powers[0][ex] * powers[1][ey] * powers[2][ez]
    return coefficients


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    package = args.package.resolve(strict=True)
    output = args.output.resolve()
    require(not output.is_relative_to(package), 'Output must be outside the original package')
    started = time.monotonic()
    records = []
    for i in range(1, 47):
        entry = package / 'entries' / f'S{i:03d}'
        literal_path = entry / 'functional.json'
        raw_literal = literal_path.read_bytes()
        functional = json.loads(raw_literal)
        require(functional['id'] == i, 'Entry/literal identity mismatch')
        terms = parse_literal(functional['expression'])
        config = json.loads((entry / 'upper_bound' / 'inputs.json').read_bytes())
        polynomial_path = entry / 'upper_bound' / config['characteristic_file']
        require(polynomial_path.resolve().is_relative_to(entry.resolve()),
                'Characteristic file escapes its entry')
        raw_polynomial = polynomial_path.read_bytes()
        polynomial = parse_polynomial(raw_polynomial.decode('utf-8'))
        require(polynomial.get((8, 0, 0, 0)) == 1, 'Nonmonic degree-eight polynomial')
        require(all(0 <= ex[0] <= 8 and all(0 <= a <= 4 for a in ex[1:])
                    for ex in polynomial), 'Stored polynomial exceeds proved degree bounds')
        require(all(all(a <= (8-ex[0])//2 for a in ex[1:]) for ex in polynomial),
                'Stored coefficient exceeds sharper Newton degree bounds')
        evaluated = hashlib.sha256()
        for overlaps in itertools.product(GRID, repeat=3):
            actual = charpoly_faddeev(bell_matrix(terms, overlaps))
            expected = evaluate_stored(polynomial, overlaps)
            require(actual == expected, f'S{i:03d} coefficient mismatch at {overlaps}')
            evaluated.update(json.dumps([overlaps, actual], separators=(',', ':')).encode())
        require(literal_path.read_bytes() == raw_literal and
                polynomial_path.read_bytes() == raw_polynomial, 'An input changed during checking')
        records.append({
            'id': i, 'status': 'PASS_EXACT_CHARACTERISTIC_IDENTITY',
            'literal_terms': len(terms), 'stored_monomials': len(polynomial),
            'stored_overlap_degrees': [max(e[k] for e in polynomial) for k in (1, 2, 3)],
            'integer_grid_points': 125, 'monic_coefficients_per_point': 9,
            'literal_sha256': hashlib.sha256(raw_literal).hexdigest(),
            'characteristic_file': polynomial_path.relative_to(package).as_posix(),
            'characteristic_sha256': hashlib.sha256(raw_polynomial).hexdigest(),
            'grid_evaluation_sha256': evaluated.hexdigest(),
        })
        print(f'S{i:03d}: exact identity PASS (125 integer points with proved degree bounds)', flush=True)
    report = {
        'schema': 'sliwa-independent-integer-charpoly-v1',
        'status': 'PASS_ALL_46_EXACT_CHARACTERISTIC_IDENTITIES',
        'python': platform.python_version(), 'entry_count': len(records),
        'total_integer_grid_points': sum(r['integer_grid_points'] for r in records),
        'total_integer_coefficient_equalities': sum(r['integer_grid_points'] * 9 for r in records),
        'algorithm': 'Faddeev-LeVerrier over integers, restricted AST polynomial parser, tensor-product gauge matrices',
        'trusted_runtime': 'Python standard library and exact integer arithmetic; no author code or CAS imported',
        'scope': 'Exact literal/characteristic polynomial identities only; does not prove upper-bound coefficient signs or attainment',
        'degree_argument': 'Local reflection words give tr(M^k) degree at most floor(k/2) per overlap; Newton identities give the same bound for coefficient k. At k<=8, each overlap degree<=4. Equality at a tensor grid of five distinct integers per axis is therefore a polynomial identity.',
        'grid': list(GRID), 'seconds': round(time.monotonic() - started, 6),
        'records': records,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'records'}, indent=2))


if __name__ == '__main__':
    main()
