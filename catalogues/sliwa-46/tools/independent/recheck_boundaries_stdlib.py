"""Independent exact audit of the frozen S16/S46 boundary proofs.

Standard library only.  No author Python module is imported.  Source polynomial
and leaf-path data are inputs; all polynomial algebra, resultant identities,
Bernstein transforms, interval signs and branch/literal checks are recomputed.
This does not replace the common literal-characteristic check for full S16/S46
or the other 44 upper proofs.  It proves the recorded resultant identities by
integer interpolation with an explicit conservative degree bound, not sampling.
"""
from __future__ import annotations

import argparse
import ast
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import comb, factorial, isqrt
from pathlib import Path
import re
import time

NAMES = ("q", "r", "x", "y", "z", "t", "d", "h", "u", "v", "w")
IDX = {v: i for i, v in enumerate(NAMES)}
ZERO = (0,) * len(NAMES)


class P:
    def __init__(self, value=0):
        if isinstance(value, P):
            self.a = value.a
        elif isinstance(value, dict):
            self.a = {k: F(v) for k, v in value.items() if v}
        else:
            self.a = {} if not value else {ZERO: F(value)}

    def __add__(self, other):
        b = defaultdict(F, self.a)
        for k, v in P(other).a.items():
            b[k] += v
        return P(dict(b))

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.a.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        b = defaultdict(F)
        for k, v in self.a.items():
            for l, w in P(other).a.items():
                b[tuple(a + c for a, c in zip(k, l))] += v * w
        return P(dict(b))

    __rmul__ = __mul__

    def __truediv__(self, n):
        n = F(n)
        if not n:
            raise ZeroDivisionError()
        return P({k: v / n for k, v in self.a.items()})

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Only nonnegative integer powers")
        out, base = P(1), self
        while n:
            if n & 1:
                out = out * base
            n //= 2
            if n:
                base = base * base
        return out

    def degree(self, var):
        return max((k[IDX[var]] for k in self.a), default=-1)

    def coeff(self, var, n):
        i = IDX[var]
        return P({k[:i] + (0,) + k[i + 1:]: v
                  for k, v in self.a.items() if k[i] == n})

    def diff(self, var, n=1):
        out = self
        i = IDX[var]
        for _ in range(n):
            b = {}
            for k, v in out.a.items():
                if k[i]:
                    b[k[:i] + (k[i] - 1,) + k[i + 1:]] = v * k[i]
            out = P(b)
        return out

    def sub(self, **subs):
        subs = {k: P(v) for k, v in subs.items()}
        powers = {}
        out = P(0)
        for exps, c in self.a.items():
            term = P(c)
            for var, n in zip(NAMES, exps):
                if n:
                    key = (var, n)
                    if key not in powers:
                        powers[key] = subs.get(var, VAR[var]) ** n
                    term = term * powers[key]
            out += term
        return out

    def scalar(self):
        if set(self.a) - {ZERO}:
            raise ValueError("Nonconstant polynomial")
        return self.a.get(ZERO, F(0))

    def at(self, **values):
        out = F(0)
        for exps, c in self.a.items():
            for var, n in zip(NAMES, exps):
                if n:
                    c *= F(values[var]) ** n
            out += c
        return out

    def divrem(self, divisor, var):
        divisor = P(divisor)
        dv = divisor.degree(var)
        lead = divisor.coeff(var, dv).scalar()
        if dv < 0:
            raise ZeroDivisionError()
        rest, quotient = self, P(0)
        while rest.degree(var) >= dv:
            dr = rest.degree(var)
            piece = rest.coeff(var, dr) * VAR[var] ** (dr - dv) / lead
            quotient += piece
            rest -= piece * divisor
        return quotient, rest

    def rem(self, divisor, var):
        return self.divrem(divisor, var)[1]


VAR = {}
for name, index in IDX.items():
    exp = list(ZERO)
    exp[index] = 1
    VAR[name] = P({tuple(exp): 1})
q, r, x, y, z, t, d, h, u, v, w = [VAR[n] for n in NAMES]


def parse(source):
    def go(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return P(node.value)
        if isinstance(node, ast.Name) and node.id in VAR:
            return VAR[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -go(node.operand)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
            return go(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = go(node.left), go(node.right)
            if isinstance(node.op, ast.Add):
                return a + b
            if isinstance(node.op, ast.Sub):
                return a - b
            if isinstance(node.op, ast.Mult):
                return a * b
            if isinstance(node.op, ast.Div):
                return a / b.scalar()
            if isinstance(node.op, ast.Pow):
                n = b.scalar()
                if n.denominator != 1:
                    raise ValueError("Noninteger power")
                return a ** int(n)
        raise ValueError("Unsupported syntax: " + ast.dump(node))
    return go(ast.parse(source.strip(), mode="eval").body)


CHECKS = []


def equal(name, a, b=0):
    if (P(a) - P(b)).a:
        raise ArithmeticError(name)
    CHECKS.append(name)


def require(name, value):
    if not value:
        raise ArithmeticError(name)
    CHECKS.append(name)


def det_integer(matrix):
    """Fraction-free Bareiss determinant, including row pivots and zero cases."""
    a = [list(row) for row in matrix]
    n, sign, previous = len(a), 1, 1
    if not n:
        return 1
    for k in range(n - 1):
        pivot_row = next((j for j in range(k, n) if a[j][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = a[i][j] * pivot - a[i][k] * a[k][j]
                quotient, remainder = divmod(num, previous)
                if remainder:
                    raise ArithmeticError("Nonexact Bareiss division")
                a[i][j] = quotient
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def resultant_value(a, b, elim, parameter, value):
    da, db = a.degree(elim), b.degree(elim)
    ca = [a.coeff(elim, j).at(**{parameter: value}) for j in range(da, -1, -1)]
    cb = [b.coeff(elim, j).at(**{parameter: value}) for j in range(db, -1, -1)]
    if any(c.denominator != 1 for c in ca + cb):
        raise ArithmeticError("Noninteger Sylvester coefficient")
    ca, cb = list(map(int, ca)), list(map(int, cb))
    rows = []
    for shift in range(db):
        rows.append([0] * shift + ca + [0] * (db - 1 - shift))
    for shift in range(da):
        rows.append([0] * shift + cb + [0] * (da - 1 - shift))
    return det_integer(rows)


def check_resultant(name, a, b, rhs, elim, parameter):
    # A Sylvester determinant has size deg(a)+deg(b). Each entry's parameter
    # degree is bounded by max(deg_parameter a, deg_parameter b), so this
    # conservative product bounds its degree without relying on cancellations.
    bound = (a.degree(elim) + b.degree(elim)) * max(a.degree(parameter), b.degree(parameter))
    require(name + ": right degree within bound", rhs.degree(parameter) <= bound)
    for value in range(bound + 1):
        if resultant_value(a, b, elim, parameter, value) != rhs.at(**{parameter: value}):
            raise ArithmeticError(name + ": coefficient identity failed")
    CHECKS.append(name)
    return {"name": name, "degree_bound": bound, "exact_integer_points": bound + 1,
            "method": "Sylvester/Bareiss determinant plus exact polynomial interpolation"}


def tree_boxes(paths, dimensions):
    if len(paths) != len(set(paths)):
        raise ArithmeticError("Duplicate leaf")
    choices = [str(i) for i in range(1 << dimensions)]
    if any(type(p) is not str or any(c not in choices for c in p) for p in paths):
        raise ArithmeticError("Invalid path")
    paths = set(paths)
    stack = [""]
    while stack:
        prefix = stack.pop()
        if prefix in paths:
            if any(p != prefix and p.startswith(prefix) for p in paths):
                raise ArithmeticError("Overlapping leaf")
        else:
            if not any(p.startswith(prefix) for p in paths):
                raise ArithmeticError("Missing branch")
            stack.extend(prefix + c for c in choices)
    answer = []
    for path in sorted(paths):
        box = [(F(0), F(1))] * dimensions
        for c in path:
            bits = int(c)
            for i, (lo, hi) in enumerate(box):
                mid = (lo + hi) / 2
                box[i] = (mid, hi) if bits & (1 << (dimensions - 1 - i)) else (lo, mid)
        answer.append((path, box))
    return answer


def bernstein_signs(poly, axes, parameter, interval, strict):
    degrees = [poly.degree(a) for a in axes]
    if any(k < 0 for k in degrees):
        raise ArithmeticError("Unexpected zero polynomial")
    allowed = {IDX[v] for v in axes + [parameter]}
    for exps in poly.a:
        if any(exps[j] for j in range(len(NAMES)) if j not in allowed):
            raise ArithmeticError("Uneliminated variable")
    lo, hi = interval
    if not 0 < lo < hi:
        raise ArithmeticError("Positive ordered parameter interval required")
    positive = zero = 0
    minimum = None
    for powers in product(*(range(k + 1) for k in degrees)):
        coeff = defaultdict(F)
        for exps, scalar in poly.a.items():
            mon = [exps[IDX[a]] for a in axes]
            if any(k > j for k, j in zip(mon, powers)):
                continue
            for j, k, degree in zip(powers, mon, degrees):
                scalar *= F(comb(j, k), comb(degree, k))
            coeff[exps[IDX[parameter]]] += scalar
        coeff = {k: c for k, c in coeff.items() if c}
        if not coeff:
            if strict:
                raise ArithmeticError("Zero strict Bernstein coefficient")
            zero += 1
            continue
        lower = sum(c * (lo ** k if c > 0 else hi ** k) for k, c in coeff.items())
        if lower <= 0:
            raise ArithmeticError("Nonpositive independently computed Bernstein coefficient")
        positive += 1
        minimum = lower if minimum is None else min(minimum, lower)
    return positive, zero, minimum


def run_covers(cases, records, axes, parameter, interval, leaf_key, field=None):
    names = [a["name"] for a in records]
    if len(names) != len(set(names)) or set(names) != set(cases):
        raise ArithmeticError("Exact complete obligation-name set required")
    results = []
    for record in records:
        name = record["name"]
        base, strict = cases[name]
        if "strict" in record and strict is not record["strict"]:
            raise ArithmeticError("Incorrect strictness")
        if field is not None:
            base = base.rem(field, parameter)
        paths = [a["path"] for a in record[leaf_key]]
        positives = zeros = 0
        minimum = None
        boxes = tree_boxes(paths, len(axes))
        for path, box in boxes:
            leaf = base.sub(**{axis: lo + (hi - lo) * VAR[axis]
                               for axis, (lo, hi) in zip(axes, box)})
            pos, zero, low = bernstein_signs(leaf, axes, parameter, interval, strict)
            positives += pos
            zeros += zero
            if low is not None:
                minimum = low if minimum is None else min(minimum, low)
        results.append({"name": name, "leaf_count": len(boxes),
                        "positive_coefficient_count": positives, "zero_coefficient_count": zeros,
                        "minimum_positive_lower_bound": str(minimum)})
    return {"case_count": len(results), "leaf_count": sum(a["leaf_count"] for a in results),
            "positive_coefficient_count": sum(a["positive_coefficient_count"] for a in results),
            "zero_coefficient_count": sum(a["zero_coefficient_count"] for a in results),
            "cases": results}


def literal_branch_check(expression, plus, minus):
    source = expression.replace(" ", "")
    matches = list(re.finditer(r"([+-]?)(\d*)([AaBbCc]+)", source))
    if "".join(m.group(0) for m in matches) != source:
        raise ArithmeticError("Unsupported Bell literal")
    terms = []
    for m in matches:
        coefficient = (-1 if m[1] == "-" else 1) * int(m[2] or 1)
        letters = m[3]
        if any(sum(c in pair for c in letters) > 1 for pair in ["Aa", "Bb", "Cc"]):
            raise ArithmeticError("More than one same-party setting")
        terms.append((coefficient, letters))
    ident = [[1, 0], [0, 1]]
    zz = [[1, 0], [0, -1]]
    total = 0
    for epsilon, polynomial in [(1, plus), (-1, minus)]:
        for xx, yy in product(range(-4, 5), repeat=2):
            matrices = {"A": zz, "a": [[xx, 1], [1 - xx * xx, -xx]],
                        "B": zz, "b": [[yy, 1], [1 - yy * yy, -yy]]}
            bell = [[0] * 4 for _ in range(4)]
            for coefficient, letters in terms:
                coefficient *= epsilon ** sum(c in "Cc" for c in letters)
                aa = next((matrices[c] for c in letters if c in "Aa"), ident)
                bb = next((matrices[c] for c in letters if c in "Bb"), ident)
                for i, j, k, l in product(range(2), repeat=4):
                    bell[2 * i + k][2 * j + l] += coefficient * aa[i][j] * bb[k][l]
            for qq in range(5):
                matrix = [[qq * (i == j) - bell[i][j] for j in range(4)] for i in range(4)]
                if det_integer(matrix) != polynomial.at(q=qq, x=xx, y=yy):
                    raise ArithmeticError("Literal branch characteristic identity failed")
                total += 1
    return {"branches": 2, "determinant_equality_count": total,
            "grid_lengths": {"q": 5, "x": 9, "y": 9},
            "degree_bounds": {"q": 4, "x": 8, "y": 8},
            "degree_bound_reason": "A 4x4 determinant: each entry has degree at most q:1, x:2, y:2.",
            "method": "Exact integer determinant interpolation; no floating point or CAS"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package, output = args.package.resolve(), args.output.resolve()
    if output.exists() or output.is_relative_to(package):
        raise ValueError("Output must be new and outside the source package")
    started = time.monotonic()
    used = {}
    def read(relative):
        data = (package / relative).read_bytes()
        used[relative] = sha256(data).hexdigest()
        return data.decode("utf-8")

    equal("Bareiss determinant sign control", det_integer([[0, 1], [1, 0]]), -1)
    equal("Sylvester resultant sign control", resultant_value(t*t-2, 2*t, "t", "q", 0), -8)
    base16 = "entries/S016/upper_bound/"
    full16 = parse(read(base16 + "charpoly_16_full.txt"))
    require("S16 polynomial even in q", all(exps[IDX["q"]] % 2 == 0 for exps in full16.a))
    rr = P(0)
    for exps, c in full16.a.items():
        k = exps[IDX["q"]]
        rr += P({exps[:IDX["q"]] + (0,) + exps[IDX["q"] + 1:]: c}) * r ** (k // 2)
    equal("S16 even characteristic substitution", full16, rr.sub(r=q*q))
    equal("S16 monic quartic", rr.coeff("r", 4), 1)
    equal("S16 y/z symmetry", rr, rr.sub(y=z, z=y))
    equal("S16 x=1 boundary", rr.sub(x=1), (r-16)**4)
    equal("S16 y=1 boundary", rr.sub(y=1), (r-16)**4)
    equal("S16 x=-1 boundary", rr.sub(x=-1), (r*r-32*r+256*(y*y+z*z-y*y*z*z))**2)
    equal("S16 y=-1 boundary", rr.sub(y=-1), (r-16)**2*(r*r-32*r+256*(x*x+z*z-x*x*z*z)))
    equal("S16 boundary quadratic root range identity", y*y+z*z-y*y*z*z, 1-(1-y*y)*(1-z*z))
    small = r+8*x*y*y-8*x-8*y*y-8
    cc, rem = rr.sub(z=y).divrem(small, "r")
    equal("S16 diagonal factor division", rem)
    equal("S16 small root bounded by 16", 16+small.sub(r=0), 8*(1-x)*(1-y*y))
    hh = r+8*y*y+16*y-8
    alpha = -128*(y-1)**3*(y+1)*hh
    beta = 8*(y-1)*(y+1)*(-r*r+16*r*y*y+16*r+256*y**4-768*y*y+256)
    equal("S16 quadratic coefficient alpha", cc.coeff("x", 2), alpha)
    equal("S16 linear coefficient beta", cc.coeff("x", 1), beta)
    require("S16 C has degree two in x", cc.degree("x") == 2)
    equal("S16 H positivity form", hh, r+8*(y+1)**2-16)
    ee = 9*r*r*y-7*r*r+96*r*y**3-32*r*y*y-384*r*y+256*r+256*y**5-1792*y**4+2048*y**3
    equal("S16 eliminated C identity with denominators cleared",
          (4*alpha*cc.coeff("x", 0)-beta*beta)*8*(y-1)*hh,
          4*alpha*(r-16)**2*ee)
    ff = 243*r*r-12256*r+117504
    resultants = [check_resultant("S16 resultant(E,E_y)", ee, ee.diff("y"),
                                 (2**56)*r*r*(r-16)**5*ff, "y", "r")]
    require("S16 f(32)<0", ff.at(r=32) < 0)
    require("S16 f'(32)>0", ff.diff("r").at(r=32) > 0)
    require("S16 f'' positive constant", ff.diff("r", 2).scalar() > 0)
    sqrt_lo = F(isqrt(13 * 10**120), 10**60)
    sqrt_hi = sqrt_lo + F(1, 10**60)
    require("S16 fresh sqrt13 isolation", sqrt_lo**2 < 13 < sqrt_hi**2)
    rho_lo, rho_hi = ((6128+832*a)/243 for a in (sqrt_lo, sqrt_hi))
    require("S16 rho interval above32", 32 < rho_lo < rho_hi)
    # Exact radical identities are checked modulo h^2-13 independently of
    # the interval; the interval serves only to select signs and legality.
    equal("S16 rho radical satisfies f", ff.sub(r=(6128+832*h)/243).rem(h*h-13, "h"))
    equal("S16 displayed square-root value squares to rho",
          F(16, 729)*(1149+156*h), (6128+832*h)/243)
    xstar, ystar = (2320-81*r)/1664, (912-27*r)/416
    equal("S16 xstar radical form", xstar.sub(r=(6128+832*h)/243), (1-h)/6)
    equal("S16 ystar radical form", ystar.sub(r=(6128+832*h)/243), (5-2*h)/9)
    require("S16 x witness legal", -1 < (1-sqrt_hi)/6 < (1-sqrt_lo)/6 < 0)
    require("S16 y/z witnesses legal", -1 < (5-2*sqrt_hi)/9 < (5-2*sqrt_lo)/9 < 0)
    for name, expression in [("C", cc), ("C_x", cc.diff("x")), ("C_y", cc.diff("y"))]:
        equal("S16 witness " + name, expression.sub(x=xstar, y=ystar).rem(ff, "r"))
    symmetric = rr.sub(y=t+h, z=t-h)
    require("S16 unequal-overlap polynomial even in h", all(exps[IDX["h"]] % 2 == 0 for exps in symmetric.a))
    td = P(0)
    for exps, coefficient in symmetric.a.items():
        k = exps[IDX["h"]] // 2
        new = list(exps)
        new[IDX["h"]] = 0
        td += P({tuple(new): coefficient / 4**k}) * d**k
    derivative = parse(read(base16 + "charpoly_16_derivative.txt"))
    equal("S16 derivative over full physical asymmetry domain", td.diff("d"), (1-x)*derivative)
    equal("S16 d=0 is diagonal slice", td.sub(d=0), rr.sub(y=t, z=t))
    cert16 = json.loads(read(base16 + "certificate_16_field_bernstein.json"))
    cases16 = {}
    for k in range(1, 4):
        cases16[f"shifted_e{k}_whole_cube"] = (rr.diff("r", 4-k).sub(x=2*u-1, y=2*v-1, z=2*w-1) / factorial(4-k), True)
    cases16["det_x_nonnegative"] = (rr.sub(x=u, y=2*v-1, z=2*w-1), True)
    cases16["d_derivative_x_negative_t_nonnegative"] = (derivative.sub(x=u-1, t=v, d=4*w*(1-v)**2), False)
    cases16["d_derivative_x_negative_t_nonpositive"] = (derivative.sub(x=u-1, t=-v, d=4*w*(1-v)**2), False)
    signs16 = run_covers(cases16, cert16["records"], ["u", "v", "w"], "r", (rho_lo, rho_hi), "leaves", ff)
    print("PASS independently recomputed S16 algebra and complete field covers", flush=True)

    base46 = "entries/S046/upper_bound/"
    full46 = parse(read(base46 + "charpoly_46_full.txt"))
    plus = parse("q**4+48*q*q*x*y+48*q*q*x+48*q*q*y-296*q*q-576*q*x*y-576*q*x-576*q*y+2304*q-1024*x*x*y*y+1024*x*x+960*x*y+960*x+1024*y*y+960*y-4464")
    minus = parse("q**4+32*q*q*x*y-32*q*q*x-32*q*q*y-184*q*q-128*q*x*y+128*q*x+128*q*y+192*q-6144*x*x*y*y+6144*x*x-1920*x*y+1920*x+6144*y*y+1920*y+336")
    equal("S46 full z=1 determinant is both branches", full46.sub(z=1), plus*minus)
    for name, pp in [("plus", plus), ("minus", minus)]:
        equal("S46 " + name + " x/y symmetry", pp, pp.sub(x=y, y=x))
    uvplus = q**4-296*q*q+2304*q+1024*u*u+(48*q*q-576*q+960)*u-1024*v*v+(48*q*q-576*q-1088)*v-4464
    uvminus = q**4-184*q*q+192*q+6144*u*u+u*(-32*q*q+128*q+1920)-6144*v*v+v*(32*q*q-128*q-14208)+336
    for name, pp, uv, us, vs, edge in [
        ("plus", plus, uvplus, (-3*q*q+36*q-60)/128, (3*q*q-36*q-68)/128, 1+u+v),
        ("minus", minus, uvminus, (q*q-4*q-60)/384, (q*q-4*q-444)/384, 1-u+v),
    ]:
        equal("S46 " + name + " symmetric coordinate identity", uv.sub(u=x+y, v=x*y), pp)
        equal("S46 " + name + " stationary u", uv.diff("u").sub(u=us, v=vs))
        equal("S46 " + name + " stationary v", uv.diff("v").sub(u=us, v=vs))
        equal("S46 " + name + " stationary point forced to boundary", edge.sub(u=us, v=vs))
        require("S46 " + name + " uv Hessian invertible", uv.diff("u", 2).scalar() * uv.diff("v", 2).scalar() != 0)
        equal("S46 " + name + " mixed uv derivative zero", uv.diff("u").diff("v"))
    equal("S46 plus y=1 edge", plus.sub(y=1), (q-10)*(q-2)*(q*q+12*q+96*x-124))
    equal("S46 plus y=-1 edge", plus.sub(y=-1), (q-10)**2*(q-2)*(q+22))
    equal("S46 minus y=1 edge", minus.sub(y=1), (q-10)**2*(q+6)*(q+14))
    equal("S46 minus y=-1 edge", minus.sub(y=-1), (q-10)*(q+6)*(q*q+4*q-64*x-76))
    # At q=10 the two varying edge quadratics shift to monic quadratics
    # with nonnegative coefficients throughout x in [-1,1].
    equal("S46 plus edge shift at cap10", (q*q+12*q+96*x-124).sub(q=10+t), t*t+32*t+96*(1+x))
    equal("S46 minus edge shift at cap10", (q*q+4*q-64*x-76).sub(q=10+t), t*t+24*t+64*(1-x))
    cp = q**3+(-4*t+6)*q*q+(64*t*t+48*t-260)*q-256*t**3-384*t*t+176*t+744
    cm = q**3+(8*t+2)*q*q+(96*t*t-32*t-180)*q+768*t**3-192*t*t-1248*t-168
    gp = 25*q**3+98*q*q-6068*q+19736
    gm = 25*q**3-46*q*q-4788*q+15192
    equal("S46 plus diagonal factor", plus.sub(x=t, y=t), (q+4*t-6)*cp)
    equal("S46 minus diagonal factor", minus.sub(x=t, y=t), (q-8*t-2)*cm)
    resultants.append(check_resultant("S46 plus resultant", cp, cp.diff("t"),
                                      -(2**24)*(q-10)*(q-2)*(q+22)*gp, "t", "q"))
    resultants.append(check_resultant("S46 minus resultant", cm, cm.diff("t"),
                                      301989888*(q-10)*(q+6)*(q+14)*gm, "t", "q"))
    for name, gg, lo_test, hi_test in [("plus", gp, 10, 12), ("minus", gm, 12, 13)]:
        require("S46 " + name + " cubic selected-root endpoint signs", gg.at(q=lo_test) < 0 < gg.at(q=hi_test))
        require("S46 " + name + " cubic derivative positive at10", gg.diff("q").at(q=10) > 0)
        require("S46 " + name + " cubic second derivative positive at10", gg.diff("q", 2).at(q=10) > 0)
        require("S46 " + name + " cubic third derivative positive", gg.diff("q", 3).scalar() > 0)
    reduced46 = json.loads(read(base46 + "certificate_46_reduced.json"))
    cert46 = json.loads(read(base46 + "certificate_46_full_bernstein.json"))
    equal("S46 reduced root polynomial is proven branch cubic", parse(reduced46["polynomial"]), gm)
    displayed_root_polynomial = re.sub(r"(?<=\d)(?=[A-Za-z])", "*", cert46["root_polynomial"].replace("^", "**"))
    equal("S46 full root polynomial is proven branch cubic", parse(displayed_root_polynomial), gm)
    qlo, qhi = map(F, cert46["q_interval"])
    require("S46 frozen reduced/full selecting intervals equal", list(map(F, reduced46["isolating_interval"])) == [qlo, qhi])
    require("S46 original exact interval lies above12", 12 < qlo < qhi < 13)
    require("S46 original exact interval has opposite cubic signs", gm.at(q=qlo) < 0 < gm.at(q=qhi))
    witness = (25*q*q-4*q-3612)/4224
    equal("S46 attaining t matches original reduced input", parse(reduced46["attaining_t"]), witness)
    equal("S46 attaining cubic zero", cm.sub(t=witness).rem(gm, "q"))
    equal("S46 attaining derivative zero", cm.diff("t").sub(t=witness).rem(gm, "q"))
    require("S46 witness t legal on whole selecting interval", 0 < witness.at(q=qlo) < witness.at(q=qhi) < 1)
    require("S46 witness formula increasing on interval", witness.diff("q").at(q=qlo) > 0 and witness.diff("q", 2).scalar() > 0)
    functional = json.loads(read("entries/S046/functional.json"))
    branch_identity = literal_branch_check(functional["expression"], plus, minus)
    cases46 = {}
    for k in range(1, 8):
        ep = full46.diff("q", 8-k).sub(z=1-2*r) / factorial(8-k)
        n = ep.degree("r")
        for i in range(n+1):
            coefficient = sum((ep.coeff("r", j)*F(comb(i, j), comb(n, j)) for j in range(i+1)), P(0))
            cases46[f"e{k}:zBernstein{i}/{n}"] = (coefficient.sub(x=2*u-1, y=2*v-1), True)
    segments = [(F(0), F(1, 16)), (F(1, 16), F(1, 4)), (F(1, 4), F(1, 2)), (F(1, 2), F(1))]
    require("S46 four recorded Charlie segments exactly match full cover", [tuple(map(F, a)) for a in cert46["w_segments"]] == segments)
    for si, (aa, bb) in enumerate(segments):
        ep = full46.sub(z=1-2*(aa+(bb-aa)*r))
        require("S46 Charlie determinant degree4 segment" + str(si), ep.degree("r") == 4)
        for i in range(5):
            coefficient = sum((ep.coeff("r", j)*F(comb(i, j), comb(4, j)) for j in range(i+1)), P(0))
            if si == 0 and i == 0:
                equal("S46 sole omitted coefficient is exactly proven z=1 face", coefficient, plus*minus)
                continue
            cases46[f"e8:segment{si}:zBernstein{i}/4"] = (coefficient.sub(x=2*u-1, y=2*v-1), True)
    signs46 = run_covers(cases46, cert46["records"], ["u", "v"], "q", (qlo, qhi), "positive_leaf_subdivision")
    print("PASS independently recomputed S46 algebra, branch literal identities and complete covers", flush=True)
    require("All source inputs unchanged", all(sha256((package / p).read_bytes()).hexdigest() == digest for p, digest in used.items()))
    report = {
        "status": "PASS_INDEPENDENT_S16_S46_BOUNDARY_AND_FULL_COEFFICIENT_AUDIT",
        "standard_library_only": True, "author_code_imported": False,
        "floating_point_used_for_acceptance": False,
        "scope": "S16/S46 certificate polynomial identities (mathematical inputs retained from v1.0.0), all boundary eliminants, actual field/Bernstein coefficient signs and complete covers; S46 literal-to-branch identities. Other entry proofs and full literal-to-characteristic binding are outside this script.",
        "algebra_and_domain_checks": CHECKS,
        "algebra_and_domain_check_count": len(CHECKS),
        "resultant_identity_checks": resultants,
        "s16_rho_interval": [str(rho_lo), str(rho_hi)],
        "s16_positivity": signs16,
        "s46_q_interval": [str(qlo), str(qhi)],
        "s46_literal_branch_identity": branch_identity,
        "s46_positivity": signs46,
        "input_sha256": used,
        "original_inputs_unchanged": True,
        "seconds": time.monotonic()-started,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ["status", "algebra_and_domain_check_count", "seconds"]}), flush=True)


if __name__ == "__main__":
    main()
