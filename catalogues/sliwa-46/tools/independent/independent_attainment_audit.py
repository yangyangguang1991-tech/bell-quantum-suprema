"""Read-only, standard-library exact audit of the 46 exported attainment recipes.

This imports no author code, SymPy, mpmath or numerical package.  It checks
univariate roots by a rational Sturm sequence, system roots by a freshly
evaluated rational contraction, radical identities in explicit quadratic
extension algebras, characteristic zeros and multiplicities, the complete
state DAG's agreement with its spectral-polynomial recipe, and a new positive
interval bound on the chosen column norm.  Characteristic-polynomial identity
with the literal Bell operator and the global upper bounds are separate tasks.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from math import gcd, isqrt, lcm
from pathlib import Path
import re
import time

NAMES = 'qxyzuvw'
NV = len(NAMES)
ZERO = (0,) * NV
BITS = 384
DEN = 1 << BITS


def require(test, message):
    if not test:
        raise ArithmeticError(message)


def constant(a):
    a = F(a)
    return {ZERO: a} if a else {}


def variable(name):
    p = list(ZERO)
    p[NAMES.index(name)] = 1
    return {tuple(p): F(1)}


def padd(a, b):
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, F(0)) + c
        if not out[m]:
            del out[m]
    return out


def pscale(a, c):
    c = F(c)
    return {m: v * c for m, v in a.items() if v * c}


def pmul(a, b):
    out = {}
    for m, c in a.items():
        for n, d in b.items():
            k = tuple(i + j for i, j in zip(m, n))
            out[k] = out.get(k, F(0)) + c * d
    return {m: c for m, c in out.items() if c}


def ppow(a, k):
    require(isinstance(k, int) and k >= 0, 'Not a polynomial power')
    out = constant(1)
    while k:
        if k & 1:
            out = pmul(out, a)
        k >>= 1
        if k:
            a = pmul(a, a)
    return out


def derivative(a, name):
    j = NAMES.index(name)
    out = {}
    for m, c in a.items():
        if m[j]:
            n = list(m)
            n[j] -= 1
            out[tuple(n)] = c * m[j]
    return out


def poly_key(p):
    return tuple(sorted(p.items()))


def tree(text):
    return ast.parse(text.replace('^', '**'), mode='eval').body


def parse_poly(text):
    def walk(n):
        if isinstance(n, ast.Constant) and type(n.value) is int:
            return constant(n.value)
        if isinstance(n, ast.Name) and n.id in tuple(NAMES):
            return variable(n.id)
        if isinstance(n, ast.UnaryOp):
            require(isinstance(n.op, (ast.UAdd, ast.USub)), 'Bad unary operation')
            return pscale(walk(n.operand), -1 if isinstance(n.op, ast.USub) else 1)
        require(isinstance(n, ast.BinOp), 'Unsupported polynomial expression')
        a, b = walk(n.left), walk(n.right)
        if isinstance(n.op, ast.Add):
            return padd(a, b)
        if isinstance(n.op, ast.Sub):
            return padd(a, pscale(b, -1))
        if isinstance(n.op, ast.Mult):
            return pmul(a, b)
        require(set(b) <= {ZERO}, 'Nonconstant division or exponent')
        value = b.get(ZERO, F(0))
        if isinstance(n.op, ast.Div):
            require(value != 0, 'Division by zero')
            return pscale(a, 1 / value)
        require(isinstance(n.op, ast.Pow) and value.denominator == 1, 'Bad exponent')
        return ppow(a, value.numerator)
    return walk(tree(text))


def substitute_z_y(p):
    out = {}
    for m, c in p.items():
        n = list(m)
        n[2] += n[3]
        n[3] = 0
        key = tuple(n)
        out[key] = out.get(key, F(0)) + c
    return {m: c for m, c in out.items() if c}


def round_iv(a, b):
    return F((a * DEN).__floor__(), DEN), F((b * DEN).__ceil__(), DEN)


def iadd(a, b):
    return round_iv(a[0] + b[0], a[1] + b[1])


def ineg(a):
    return -a[1], -a[0]


def imul(a, b):
    products = [i * j for i in a for j in b]
    return round_iv(min(products), max(products))


def ipow(a, n):
    if n < 0:
        require(not a[0] <= 0 <= a[1], 'Interval division crosses zero')
        return ipow(round_iv(1 / a[1], 1 / a[0]), -n)
    if n == 0:
        return F(1), F(1)
    lo, hi = a[0] ** n, a[1] ** n
    if n % 2 == 0:
        lo = F(0) if a[0] <= 0 <= a[1] else min(lo, hi)
        hi = max(a[0] ** n, a[1] ** n)
    return round_iv(lo, hi)


def isqrt_iv(a):
    require(a[0] >= 0, 'Square root interval crosses the negative axis')
    lo = isqrt((a[0] * DEN * DEN).__floor__())
    hi = isqrt((a[1] * DEN * DEN).__floor__())
    if F(hi * hi, DEN * DEN) < a[1]:
        hi += 1
    return F(lo, DEN), F(hi, DEN)


def eval_poly_iv(p, env):
    degrees = [max((m[j] for m in p), default=0) for j in range(NV)]
    powers = [[ipow(env.get(n, (F(0), F(0))), k) for k in range(d + 1)]
              for n, d in zip(NAMES, degrees)]
    out = F(0), F(0)
    for m, c in p.items():
        term = c, c
        for j, k in enumerate(m):
            if k:
                term = imul(term, powers[j][k])
        out = iadd(out, term)
    return out


def eval_expression_iv(text, env):
    def walk(n):
        if isinstance(n, ast.Constant) and type(n.value) is int:
            return F(n.value), F(n.value)
        if isinstance(n, ast.Name):
            return env[n.id]
        if isinstance(n, ast.UnaryOp):
            return ineg(walk(n.operand)) if isinstance(n.op, ast.USub) else walk(n.operand)
        if isinstance(n, ast.Call):
            require(isinstance(n.func, ast.Name) and n.func.id == 'sqrt' and len(n.args) == 1,
                    'Unsupported function')
            return isqrt_iv(walk(n.args[0]))
        require(isinstance(n, ast.BinOp), 'Unsupported interval expression')
        a, b = walk(n.left), walk(n.right)
        if isinstance(n.op, ast.Add):
            return iadd(a, b)
        if isinstance(n.op, ast.Sub):
            return iadd(a, ineg(b))
        if isinstance(n.op, ast.Mult):
            return imul(a, b)
        if isinstance(n.op, ast.Div):
            return imul(a, ipow(b, -1))
        require(isinstance(n.op, ast.Pow) and b[0] == b[1] and b[0].denominator == 1,
                'Unsupported interval power')
        return ipow(a, b[0].numerator)
    return walk(tree(text))


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def urem(a, b):
    a, b = trim(a), trim(b)
    require(b, 'Zero modulus')
    while len(a) >= len(b):
        shift = len(a) - len(b)
        c = a[-1] / b[-1]
        for j, d in enumerate(b):
            a[shift + j] -= c * d
        a = trim(a)
    return a


def primitive(a):
    if not a:
        return []
    den = lcm(*(c.denominator for c in a))
    nums = [int(c * den) for c in a]
    g = gcd(*nums)
    return [F(n // g) for n in nums]


def univariate(p):
    require(all(not any(m[1:]) for m in p), 'Multivariate input to Sturm')
    return [p.get((k,) + ZERO[1:], F(0)) for k in range(max((m[0] for m in p), default=0) + 1)]


def ueval(a, t):
    out = F(0)
    for c in reversed(a):
        out = out * t + c
    return out


def sturm_isolate(coeff, bounds):
    a, b = map(F, bounds)
    require(a < b, 'Reversed root interval')
    seq = [primitive(coeff), primitive([k * c for k, c in enumerate(coeff)][1:])]
    while seq[-1]:
        seq.append(primitive([-c for c in urem(seq[-2], seq[-1])]))
    seq.pop()
    def variations(t):
        signs = [1 if v > 0 else -1 for p in seq if (v := ueval(p, t))]
        return sum(x != y for x, y in zip(signs, signs[1:]))
    fa, fb = ueval(coeff, a), ueval(coeff, b)
    require(fa * fb < 0 and variations(a) - variations(b) == 1, 'Root is not uniquely isolated')
    initial = [str(a), str(b)]
    steps = 0
    while b - a > F(1, 1 << 330):
        m = (a + b) / 2
        fm = ueval(coeff, m)
        steps += 1
        if not fm:
            a = b = m
            break
        if fa * fm < 0:
            b = m
        else:
            a, fa = m, fm
    return (a, b), {'method': 'rational Sturm sequence and bisection', 'degree': len(coeff) - 1,
                    'root_count': 1, 'initial_interval': initial, 'bisections': steps}


def umulmod(a, b, modulus):
    out = [F(0)] * max(0, len(a) + len(b) - 1)
    for j, c in enumerate(a):
        for k, d in enumerate(b):
            out[j + k] += c * d
    return urem(out, modulus)


def composition_remainder(p, coordinates, modulus):
    degrees = [max((m[j] for m in p), default=0) for j in range(4)]
    powers = []
    for coordinate, degree in zip(coordinates, degrees):
        pp = [[F(1)]]
        for _ in range(degree):
            pp.append(umulmod(pp[-1], coordinate, modulus))
        powers.append(pp)
    out = [F(0)] * (len(modulus) - 1)
    for m, c in p.items():
        require(not any(m[4:]), 'Unexpected characteristic variable')
        term = [c]
        for j, k in enumerate(m[:4]):
            if k:
                term = umulmod(term, powers[j][k], modulus)
        for j, value in enumerate(term):
            out[j] += value
    return trim(out)


class QuadraticTower:
    """Successively adjoin s_j with s_j**2 = an earlier tower element.

    Zero in this quotient algebra implies zero at the specified positive
    radical values.  Irreducibility of the successive quadratics is not needed
    for that sufficient implication; no division by an algebraic element occurs.
    """
    def __init__(self):
        self.relations = []
        self.radicands = {}

    def pad(self, a, n=None):
        d = 1 << (len(self.relations) if n is None else n)
        return tuple(a) + (F(0),) * (d - len(a))

    def add(self, a, b):
        return tuple(x + y for x, y in zip(self.pad(a), self.pad(b)))

    def scale(self, a, c):
        return tuple(c * x for x in self.pad(a))

    def mul(self, a, b, n=None):
        n = len(self.relations) if n is None else n
        a, b = self.pad(a, n), self.pad(b, n)
        if not n:
            return (a[0] * b[0],)
        d = 1 << (n - 1)
        ac, bd = self.mul(a[:d], b[:d], n - 1), self.mul(a[d:], b[d:], n - 1)
        bd = self.mul(bd, self.relations[n - 1], n - 1)
        ad, bc = self.mul(a[:d], b[d:], n - 1), self.mul(a[d:], b[:d], n - 1)
        return tuple(x + y for x, y in zip(ac, bd)) + tuple(x + y for x, y in zip(ad, bc))

    def power(self, a, n):
        require(n >= 0, 'Negative power in radical algebra')
        out = (F(1),)
        while n:
            if n & 1:
                out = self.mul(out, a)
            n >>= 1
            if n:
                a = self.mul(a, a)
        return self.pad(out)

    def parse(self, text):
        def walk(n):
            if isinstance(n, ast.Constant) and type(n.value) is int:
                return (F(n.value),)
            if isinstance(n, ast.UnaryOp):
                return self.scale(walk(n.operand), -1 if isinstance(n.op, ast.USub) else 1)
            if isinstance(n, ast.Call):
                require(isinstance(n.func, ast.Name) and n.func.id == 'sqrt' and len(n.args) == 1,
                        'Unsupported radical function')
                a = self.pad(walk(n.args[0]))
                canonical = tuple(a)
                while len(canonical) > 1 and canonical[-1] == 0:
                    canonical = canonical[:-1]
                if canonical in self.radicands:
                    return self.pad(self.radicands[canonical])
                self.relations.append(a)
                root = (F(0),) * len(a) + (F(1),) + (F(0),) * (len(a) - 1)
                self.radicands[canonical] = root
                return root
            require(isinstance(n, ast.BinOp), 'Unsupported radical expression')
            a, b = walk(n.left), walk(n.right)
            if isinstance(n.op, ast.Add):
                return self.add(a, b)
            if isinstance(n.op, ast.Sub):
                return self.add(a, self.scale(b, -1))
            if isinstance(n.op, ast.Mult):
                return self.mul(a, b)
            require(not any(b[1:]), 'Nonrational radical denominator/exponent')
            if isinstance(n.op, ast.Div):
                require(b[0] != 0, 'Zero radical denominator')
                return self.scale(a, 1 / b[0])
            require(isinstance(n.op, ast.Pow) and b[0].denominator == 1, 'Unsupported radical exponent')
            return self.power(a, b[0].numerator)
        return self.pad(walk(tree(text)))

    def evaluate_poly(self, p, coordinates):
        powers = []
        for j, a in enumerate(coordinates):
            powers.append([self.power(a, k) for k in range(max((m[j] for m in p), default=0) + 1)])
        out = (F(0),)
        for m, c in p.items():
            require(not any(m[4:]), 'Unexpected characteristic variable')
            term = (c,)
            for j, k in enumerate(m[:4]):
                if k:
                    term = self.mul(term, powers[j][k])
            out = self.add(out, term)
        return self.pad(out)


def contraction(eq, names, box, C):
    n = len(names)
    center = [(a + b) / 2 for a, b in box]
    radii = [(b - a) / 2 for a, b in box]
    require(all(r > 0 for r in radii), 'Degenerate root box')
    point_env = {name: (c, c) for name, c in zip(names, center)}
    env = dict(zip(names, box))
    J = [[eval_poly_iv(derivative(eq[i], name), env) for name in names] for i in range(n)]
    E = []
    for i in range(n):
        row = []
        for j in range(n):
            v = F(0), F(0)
            for k in range(n):
                v = iadd(v, imul((C[i][k], C[i][k]), J[k][j]))
            row.append(iadd((F(i == j), F(i == j)), ineg(v)))
        E.append(row)
    norm = max(sum(max(abs(a), abs(b)) for a, b in row) for row in E)
    f = [eval_poly_iv(p, point_env) for p in eq]
    image = []
    for i in range(n):
        v = center[i], center[i]
        for j in range(n):
            v = iadd(v, ineg(imul((C[i][j], C[i][j]), f[j])))
            v = iadd(v, imul(E[i][j], (-radii[j], radii[j])))
        image.append(v)
    require(norm < 1, 'Root map is not contractive')
    require(all(a < u <= v < b for (a, b), (u, v) in zip(box, image)), 'Root map fails strict inclusion')
    # ||I-CJ|| < 1 also proves the square matrix C is nonsingular.  A fixed
    # point of v-CF(v) is therefore a zero of F, not merely a zero of CF.
    return {'norm_upper': str(norm), 'strict_inclusion': True,
            'image': [[str(a), str(b)] for a, b in image]}


def selected_parameters(spec, P, compact):
    kind = spec['kind']
    if kind == 'radicals':
        tower = QuadraticTower()
        texts = [spec['q'], *spec['overlaps']]
        coords = [tower.parse(t) for t in texts]
        env = {n: eval_expression_iv(t, {}) for n, t in zip('qxyz', texts)}
        vanishes = lambda p: not any(tower.evaluate_poly(p, coords))
        return env, vanishes, {'method': 'explicit quadratic extension algebra', 'tower_dimension': 1 << len(tower.relations)}
    if kind == 'univariate':
        modulus = univariate(parse_poly(spec['polynomial']))
        qr, proof = sturm_isolate(modulus, spec['interval'])
        env = {'q': qr}
        env.update({n: eval_expression_iv(t, env) for n, t in zip('xyz', spec['overlaps'])})
        coords = [[F(0), F(1)], *[univariate(parse_poly(t)) for t in spec['overlaps']]]
        return env, lambda p: not composition_remainder(p, coords, modulus), proof
    require(kind == 'system', 'Unknown selector type')
    names = spec['variables']
    eq = [parse_poly(t) for t in spec['equations']]
    require(len(names) == len(eq), 'Nonsquare selected system')
    if names == ['q', 'x', 'y']:
        require(spec['overlaps'] == ['x', 'y', 'y'], 'Wrong reduced witness coordinates')
        quotient = parse_poly(compact['complementary_factor'])
        require(pmul(eq[0], quotient) == substitute_z_y(P), 'Reduced selected factor does not divide P')
        require(eq[1:] == [derivative(eq[0], n) for n in names[1:]], 'Incorrect reduced derivatives')
    else:
        require(names == ['q', 'x', 'y', 'z'] and spec['overlaps'] == ['x', 'y', 'z'], 'Wrong full witness coordinates')
        require(eq == [P, *[derivative(P, n) for n in names[1:]]], 'Incorrect full contact system')
    C = [[F(t) for t in row] for row in compact['preconditioner']]
    require(len(C) == len(names) and all(len(row) == len(names) for row in C), 'Wrong root preconditioner dimensions')
    old = [tuple(map(F, b)) for b in spec['box']]
    centers, radius = list(map(F, compact['centers'])), F(compact['radius'])
    large = [(c - radius, c + radius) for c in centers]
    require(all(a <= c < d <= b for (a, b), (c, d) in zip(large, old)), 'Original root box not nested')
    old_proof = contraction(eq, names, old, C)
    compact_proof = contraction(eq, names, large, C)
    raw = dict(zip(names, old))
    env = {'q': raw['q'], **{n: eval_expression_iv(t, raw) for n, t in zip('xyz', spec['overlaps'])}}
    # Current system entries all have multiplicity one.  The first selected
    # equation proves the only required zero without any ideal-membership heuristic.
    return env, lambda p: p == P, {'method': 'fresh 384-bit outward rational contraction on BOTH boxes',
                                'original_box': old_proof, 'compact_box': compact_proof}


def literal_matrix(text):
    I = [[constant(1), {}], [{}, constant(1)]]
    Z = [[constant(1), {}], [{}, constant(-1)]]
    obs = {}
    for capital, small, angle, transverse in zip('ABC', 'abc', 'xyz', 'uvw'):
        obs[capital] = Z
        obs[small] = [[variable(angle), variable(transverse)], [variable(transverse), pscale(variable(angle), -1)]]
    M = [[{} for _ in range(8)] for _ in range(8)]
    for token in re.findall(r'[+-]?[^+-]+', text.replace(' ', '')):
        match = re.fullmatch(r'([+-]?)([0-9]*)([AaBbCc]+)', token)
        require(match is not None, 'Invalid Bell literal')
        sign, number, word = match.groups()
        require(len(set(c.upper() for c in word)) == len(word), 'Same-party Bell product')
        coefficient = (-1 if sign == '-' else 1) * int(number or 1)
        settings = {c.upper(): obs[c] for c in word}
        local = [settings.get(party, I) for party in 'ABC']
        for row in range(8):
            for column in range(8):
                term = constant(coefficient)
                for party, shift in enumerate((2, 1, 0)):
                    term = pmul(term, local[party][(row >> shift) & 1][(column >> shift) & 1])
                M[row][column] = padd(M[row][column], term)
    return M, obs


def complement(P, multiplicity):
    degree = max(m[0] for m in P)
    require(degree == 8, 'Not an eighth degree characteristic polynomial')
    coeff = [{} for _ in range(degree + 1)]
    for m, c in P.items():
        n = (0,) + m[1:]
        coeff[degree - m[0]][n] = c
    require(coeff[0] == constant(1), 'Nonmonic characteristic polynomial')
    for _ in range(multiplicity):
        quotient = [coeff[0]]
        for c in coeff[1:-1]:
            quotient.append(padd(c, pmul(variable('q'), quotient[-1])))
        coeff = quotient
    return coeff


def audit_dag(exact, M, coefficients, env):
    """Prove exported circuit = R(M)e_j / ||R(M)e_j|| by circuit induction.

    First evaluate the matrix/coefficient prefix as exact sparse polynomials.
    Then interpret the remaining graph as an interned arithmetic circuit and
    match the full Horner recurrence and the normalization formula.  This is
    an exact syntactic proof of that recipe, not equality inferred from decimal
    evaluations.  No author DAG builder is imported or executed.
    """
    nodes = exact['nodes']
    required = {poly_key(p) for row in M for p in row} | {poly_key(p) for p in coefficients} | {poly_key({})}
    prefix_values, prefix_count, seen = [], None, set()
    for j, node in enumerate(nodes):
        op, args = node['op'], node['args']
        if op == 'rational':
            require(len(args) == 1, 'Bad rational node')
            p = constant(F(args[0]))
        elif op == 'parameter':
            require(len(args) == 1 and args[0] in tuple(NAMES), 'Bad parameter node')
            p = variable(args[0])
        else:
            refs = args[:1] if op == 'integer_power' else args
            require(all(type(a) is int and 0 <= a < j for a in refs), 'DAG has bad references')
            if op == 'integer_power':
                require(len(args) == 2 and type(args[1]) is int and args[1] >= 0, 'Bad prefix power')
                p = ppow(prefix_values[args[0]], args[1])
            else:
                require(op in ('add', 'multiply'), 'Unexpected operation in polynomial prefix')
                p = constant(0 if op == 'add' else 1)
                for a in args:
                    p = (padd if op == 'add' else pmul)(p, prefix_values[a])
        prefix_values.append(p)
        seen.add(poly_key(p))
        if required <= seen:
            prefix_count = j + 1
            break
    require(prefix_count is not None, 'DAG lacks a matrix or complementary coefficient')
    pool, operations = {}, {}
    def intern(key):
        if key not in pool:
            pool[key] = len(pool)
        return pool[key]
    def atom(p):
        return intern(('polynomial', poly_key(p)))
    def operation_key(op, values, exponent=None):
        if op in ('add', 'multiply'):
            return op, tuple(sorted(values))
        if op == 'integer_power':
            return op, values[0], exponent
        return op, values[0]
    circuit = [atom(p) for p in prefix_values]
    # A prefix expression already collapsed to a polynomial must have the
    # same meaning if the later recurrence reuses that operation.
    for j, node in enumerate(nodes[:prefix_count]):
        op, args = node['op'], node['args']
        if op not in ('rational', 'parameter'):
            refs = args[:1] if op == 'integer_power' else args
            key = operation_key(op, [circuit[a] for a in refs], args[1] if op == 'integer_power' else None)
            require(key not in operations or operations[key] == circuit[j], 'Inconsistent polynomial prefix')
            operations[key] = circuit[j]
    def make(op, refs, exponent=None):
        key = operation_key(op, refs, exponent)
        if key not in operations:
            operations[key] = intern(('operation', key))
        return operations[key]
    for j in range(prefix_count, len(nodes)):
        op, args = nodes[j]['op'], nodes[j]['args']
        if op == 'rational':
            require(len(args) == 1, 'Bad rational node')
            value = atom(constant(F(args[0])))
        elif op == 'parameter':
            require(len(args) == 1 and args[0] in tuple(NAMES), 'Bad parameter node')
            value = atom(variable(args[0]))
        else:
            require(op in ('add', 'multiply', 'integer_power', 'sqrt'), 'Unknown DAG operation')
            refs = args[:1] if op in ('integer_power', 'sqrt') else args
            require(all(type(a) is int and 0 <= a < j for a in refs), 'DAG has invalid references')
            if op == 'integer_power':
                require(len(args) == 2 and type(args[1]) is int, 'Bad integer power')
            if op == 'sqrt':
                require(len(args) == 1, 'Bad square root')
            value = make(op, [circuit[a] for a in refs], args[1] if op == 'integer_power' else None)
        circuit.append(value)
    column = exact['column_index_zero_based']
    require(type(column) is int and 0 <= column < 8, 'Invalid state column')
    zero = atom({})
    matrix = [[atom(p) for p in row] for row in M]
    cc = [atom(p) for p in coefficients]
    vector = [cc[0] if k == column else zero for k in range(8)]
    for c in cc[1:]:
        vector = [make('add', [make('multiply', [matrix[i][k], vector[k]]) for k in range(8)]
                       + ([c] if i == column else [])) for i in range(8)]
    raw = exact['unnormalized_vector_nodes']
    roots = exact['state_vector_nodes']
    require(len(raw) == len(roots) == 8 and all(type(a) is int and 0 <= a < len(nodes) for a in raw + roots), 'Bad output references')
    require([circuit[a] for a in raw] == vector, 'Exported raw state is not R(M)e_j')
    norm2 = make('add', [make('integer_power', [a], 2) for a in vector])
    norm = make('sqrt', [norm2])
    inverse = make('integer_power', [norm], -1)
    expected = [make('multiply', [a, inverse]) for a in vector]
    require([circuit[a] for a in roots] == expected, 'Incorrect exact normalization graph')
    norm_index = exact['normalization_squared_node']
    require(type(norm_index) is int and 0 <= norm_index < len(nodes) and circuit[norm_index] == norm2, 'Wrong norm certificate node')
    full_env = dict(env)
    for transverse, angle in zip('uvw', 'xyz'):
        full_env[transverse] = isqrt_iv(iadd((F(1), F(1)), ineg(ipow(env[angle], 2))))
    intervals = []
    for node in nodes:
        op, args = node['op'], node['args']
        if op == 'rational':
            a = F(args[0])
            val = a, a
        elif op == 'parameter':
            val = full_env[args[0]]
        elif op == 'integer_power':
            val = ipow(intervals[args[0]], args[1])
        elif op == 'sqrt':
            val = isqrt_iv(intervals[args[0]])
        else:
            val = (F(0), F(0)) if op == 'add' else (F(1), F(1))
            for a in args:
                val = (iadd if op == 'add' else imul)(val, intervals[a])
        intervals.append(val)
    fresh_norm = intervals[norm_index]
    require(fresh_norm[0] > 0, 'Chosen exact column not independently certified nonzero')
    claimed_lo, claimed_hi = map(F, exact['normalization_squared_rational_interval'])
    require(0 < claimed_lo <= claimed_hi and max(claimed_lo, fresh_norm[0]) <= min(claimed_hi, fresh_norm[1]), 'Norm enclosures disagree')
    return {'node_count': len(nodes), 'polynomial_prefix_node_count': prefix_count,
            'state_recipe_identity': 'exact circuit induction: R(M)e_j / sqrt(sum_i (R(M)e_j)_i^2)',
            'fresh_normalization_squared_interval': [str(a) for a in fresh_norm],
            'all_divisions_and_square_roots_legal': True}


def audit_entry(package, i, compact):
    started = time.monotonic()
    directory = package / 'entries' / f'S{i:03d}'
    read = lambda p: json.loads(p.read_text(encoding='utf-8'))
    literal = read(directory / 'functional.json')
    spec = read(directory / 'strategy_spec.json')
    exact = read(directory / 'attainment/strategy_exact.json')
    inputs = read(directory / 'upper_bound/inputs.json')
    source = (directory / 'upper_bound' / inputs['characteristic_file']).read_text()
    P = parse_poly(source)
    require(exact['id'] == literal['id'] == i and exact['parameters'] == spec, 'Parameter identity mismatch')
    require(parse_poly(exact['characteristic_polynomial']) == P, 'Exported characteristic polynomial mismatch')
    env, vanishes, root_proof = selected_parameters(spec, P, compact.get(i))
    require(all(-1 <= env[n][0] <= env[n][1] <= 1 for n in 'xyz'), 'Illegal exact overlap')
    m = exact['binding']['multiplicity']
    require(type(m) is int and 1 <= m <= 8, 'Invalid multiplicity')
    d = P
    for k in range(m):
        require(vanishes(d), f'Nonzero characteristic derivative {k}')
        d = derivative(d, 'q')
    nonzero = eval_poly_iv(d, env)
    require(nonzero[0] > 0 or nonzero[1] < 0, 'First nonzero characteristic derivative unresolved')
    coefficients = complement(P, m)
    require(coefficients == [parse_poly(s) for s in exact['binding']['complementary_factor_coefficients_descending']], 'Synthetic division coefficient mismatch')
    M, obs = literal_matrix(literal['expression'])
    require(M == [[parse_poly(t) for t in row] for row in exact['bell_matrix']], 'Exported physical Bell matrix mismatch')
    require(obs == {name: [[parse_poly(t) for t in row] for row in O] for name, O in exact['observables'].items()}, 'Exported observables mismatch')
    dag_proof = audit_dag(exact, M, coefficients, env)
    return {'id': i, 'status': 'PASS_INDEPENDENT_EXACT_ATTAINMENT_RECIPE', 'selector_kind': spec['kind'],
            'multiplicity': m, 'column_index_zero_based': exact['column_index_zero_based'],
            'root_proof': root_proof, 'multiplicity_derivative_interval': [str(a) for a in nonzero],
            'dag_proof': dag_proof, 'seconds': round(time.monotonic() - started, 6)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('package', type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--ids', nargs='+', type=int, default=list(range(1, 47)))
    a = p.parse_args()
    package, output = a.package.resolve(), a.output.resolve()
    require(len(set(a.ids)) == len(a.ids) and all(1 <= i <= 46 for i in a.ids), 'Invalid or duplicate requested entries')
    require(output != package and package not in output.parents, 'Output must be outside original package')
    require(not output.exists(), 'Refusing to overwrite an existing report')
    compact = {r['id']: r for r in json.loads((package / 'data/compact_root_selectors.json').read_text())['records']}
    before = {str(f.relative_to(package)): hashlib.sha256(f.read_bytes()).hexdigest() for f in package.rglob('*') if f.is_file()}
    started = time.monotonic()
    results = []
    for i in a.ids:
        r = audit_entry(package, i, compact)
        results.append(r)
        print(f"S{i:03d} exact independent attainment PASS ({r['seconds']:.3f}s)", flush=True)
    after = {str(f.relative_to(package)): hashlib.sha256(f.read_bytes()).hexdigest() for f in package.rglob('*') if f.is_file()}
    require(before == after, 'Original package changed during audit')
    report = {'status': 'PASS_ALL_REQUESTED_INDEPENDENT_EXACT_ATTAINMENT_RECIPES',
              'entry_count': len(results), 'standard_library_only': True, 'author_code_imported': False,
              'floating_point_used_for_acceptance': False, 'original_files_unchanged': True,
              'original_file_count': len(before), 'counts': dict(Counter(r['selector_kind'] for r in results)),
              'original_inventory_sha256': hashlib.sha256(json.dumps(before, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
              'audit_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'total_dag_nodes': sum(r['dag_proof']['node_count'] for r in results),
              'interval_precision_bits': BITS, 'seconds': round(time.monotonic() - started, 6),
              'scope': 'Exact selector existence/uniqueness, legal overlaps, characteristic zero and multiplicity, exported observable/Bell matrix, complementary coefficients, exact DAG recipe semantics, positive column norm. Literal characteristic identity and global upper bounds are separate obligations.',
              'entries': results}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'entries'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
