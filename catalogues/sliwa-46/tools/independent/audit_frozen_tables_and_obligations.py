"""Independent structural and manuscript audit of the frozen Sliwa archive.

Uses only the Python standard library and never imports a package verifier.
This checks mathematical obligation inventories and finite cover topology,
not Bernstein coefficient signs, root existence, or eigenvector equality.
Run: python audit_frozen_tables_and_obligations.py PACKAGE --output RESULT.json
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def literal_terms(text):
    text = text.replace(" ", "").replace("\n", "")
    parts = re.findall(r"[+-]?[^+-]+", text)
    result = Counter()
    for part in parts:
        match = re.fullmatch(r"([+-]?)(\d*)([AaBbCc]+)", part)
        require(match is not None, "Malformed literal term: " + part)
        sign, coefficient, word = match.groups()
        require(len({c.upper() for c in word}) == len(word), "Same-party product")
        result[word] += (-1 if sign == "-" else 1) * int(coefficient or 1)
    return dict(result)


def polynomial_coefficients(text):
    text = text.replace(" ", "").replace("\n", "").replace("**", "^")
    text = text.replace("*", "").replace("{", "").replace("}", "")
    result = Counter()
    for part in re.findall(r"[+-]?[^+-]+", text):
        sign = -1 if part.startswith("-") else 1
        part = part.lstrip("+-")
        if "q" in part:
            before, after = part.split("q")
            require(not after or re.fullmatch(r"\^\d+", after), "Bad q power")
            degree = int(after[1:]) if after else 1
            coefficient = int(before or "1")
        else:
            degree, coefficient = 0, int(part)
        result[degree] += sign * coefficient
    return {degree: c for degree, c in result.items() if c}


def exact_cover(paths, dimensions, simultaneous=False):
    """Check each leaf once and all children of each internal node."""
    if simultaneous:
        converted = [tuple(int(c) for c in path) for path in paths]
        require(all(all(0 <= c < 2**dimensions for c in path) for path in converted), "Invalid simultaneous split")
    else:
        converted = []
        for path in paths:
            if isinstance(path, str):
                require(len(path) % 2 == 0, "Odd path length")
                path = [(int(path[i]), int(path[i + 1])) for i in range(0, len(path), 2)]
            path = tuple(tuple(p) for p in path)
            require(all(len(p) == 2 and 0 <= p[0] < dimensions and p[1] in (0, 1) for p in path), "Invalid binary split")
            converted.append(path)
    require(len(converted) == len(set(converted)), "Duplicate leaf")

    def visit(tails):
        require(bool(tails), "Missing complete branch")
        if () in tails:
            require(len(tails) == 1, "Ancestor/descendant leaves overlap")
            return
        if simultaneous:
            require({p[0] for p in tails} == set(range(2**dimensions)), "Missing simultaneous child")
            children = range(2**dimensions)
        else:
            axes = {p[0][0] for p in tails}
            require(len(axes) == 1, "Incoherent split axis")
            axis = next(iter(axes))
            require({p[0] for p in tails} == {(axis, 0), (axis, 1)}, "Missing binary child")
            children = ((axis, 0), (axis, 1))
        for child in children:
            visit([p[1:] for p in tails if p[0] == child])

    visit(converted)
    return len(converted)


def box(value):
    return [tuple(map(Q, pair)) for pair in value]


def slabs(center):
    require(len(center) == 3 and all(-1 < lo < hi < 1 for lo, hi in center), "Invalid contact box")
    result = []
    for axis in range(3):
        for interval in ((Q(-1), center[axis][0]), (center[axis][1], Q(1))):
            current = [center[j] if j < axis else (Q(-1), Q(1)) for j in range(3)]
            current[axis] = interval
            result.append(current)
    # The disjoint interiors plus the central box must fill the cube exactly.
    volume = lambda b: (b[0][1] - b[0][0]) * (b[1][1] - b[1][0]) * (b[2][1] - b[2][0])
    require(sum(map(volume, result), volume(center)) == 8, "Slab volume mismatch")
    return result


def counted_cover(records, leaf_key="leaves", dimensions=3, simultaneous=False):
    count = 0
    for record in records:
        leaves = record[leaf_key]
        paths = [a["path"] if isinstance(a, dict) else a for a in leaves]
        count += exact_cover(paths, dimensions, simultaneous)
    return count


def audit_upper(entry, inputs):
    i, engine = inputs["id"], inputs["engine"]
    upper = entry / "upper_bound"
    commands = inputs["commands"]
    require(commands, f"S{i}: no upper command")
    require((upper / inputs["characteristic_file"]).is_file(), "Missing characteristic")
    for command in commands:
        path = entry.parents[1] / "prooflib" / (command[1:] + ".py") if command.startswith("@") else upper / command
        require(path.is_file(), "Missing command " + command)
    count, obligations = 0, []
    if engine == "analytic":
        data = load(upper / "certificate.json")
        require(len(data["rows"]) == 1 and data["rows"][0]["id"] == i, "Analytic row identity")
        row = data["rows"][0]
        require(literal_terms(row["literal"]) == literal_terms(load(entry / "functional.json")["expression"]), "Analytic literal differs")
        if i in (1, 2, 3, 4):
            require(row["method"] == "elementary_operator", "Wrong operator family")
            obligations = ["direct operator identity"]
        else:
            expected = set(map(str, range(1, 7 if i == 13 else 8 if i in (6, 7, 8, 9, 15, 26) else 9)))
            require(set(row["elementary_coefficients"]) == expected, "Analytic coefficient inventory")
            for name, rec in row["elementary_coefficients"].items():
                require(len(rec["parity"]) == 3, "Parity dimension")
                count += counted_cover([rec])
                obligations.append("e" + name)
            require(("identity_determinant" in row) == (i in (6, 9, 13)), "Determinant identity inventory")
            require(("interior_determinant" in row) == (i in (7, 8, 15, 26)), "Contact determinant inventory")
            if "identity_determinant" in row:
                obligations.append("factor/determinant identity")
            if "interior_determinant" in row:
                rec = row["interior_determinant"]
                expected_slabs = slabs(box(rec["H"]))
                require(len(rec["outer"]) == 6, "Analytic outer slab count")
                require({(a["axis"], a["side"]) for a in rec["outer"]} == {(j, k) for j in range(3) for k in range(2)}, "Analytic slab keys")
                for leaf_rec in rec["outer"]:
                    require(box(leaf_rec["box"]) == expected_slabs[2 * leaf_rec["axis"] + leaf_rec["side"]], "Analytic slab domain")
                count += counted_cover(rec["outer"])
                obligations.append("contact Hessian and six exterior slabs")
    elif i in (21, 27, 28, 33):
        data = load(upper / f"S{i}_global_certificate.json")
        expected = {f"P_q_derivative_order_{j}" for j in range(1, 9)} | {f"P_exterior_box_{j}" for j in range(6)}
        require(len(data["records"]) == 14 and {r["name"] for r in data["records"]} == expected, "Named global obligation inventory")
        expected_slabs = slabs(box(data["local_convexity_box"]))
        for rec in data["records"]:
            expected_box = expected_slabs[int(rec["name"].rsplit("_", 1)[1])] if rec["name"].startswith("P_exterior") else [(Q(-1), Q(1))] * 3
            require(box(rec["box"]) == expected_box, "Named obligation domain")
        count += counted_cover(data["records"], "positive_leaf_cover")
        obligations = sorted(expected) + ["contact Hessian"]
    elif i == 16:
        data = load(upper / "certificate_16_field_bernstein.json")
        expected = {f"shifted_e{j}_whole_cube" for j in range(1, 4)} | {"det_x_nonnegative", "d_derivative_x_negative_t_nonnegative", "d_derivative_x_negative_t_nonpositive"}
        require(len(data["records"]) == 6 and {r["name"] for r in data["records"]} == expected, "S16 field obligations")
        count += counted_cover(data["records"], simultaneous=True)
        obligations = sorted(expected) + ["diagonal slice resultant and boundary factors"]
    elif i == 23:
        data = load(upper / "S23_full_certificate.json")
        require(len(data["certificates"]) == 4 and {r["name"] for r in data["certificates"]} == {"z0_constant", "e1", "e2", "e3"}, "S23 obligation names")
        for rec in data["certificates"]:
            count += counted_cover([rec], dimensions=2 if rec["name"] == "z0_constant" else 3)
        obligations = ["z0_constant", "e1", "e2", "e3", "z1 determinant identity", "full determinant = quartic squared"]
    elif i == 46:
        data = load(upper / "certificate_46_full_bernstein.json")
        expected = {f"e{k}:zBernstein{j}/{k//2}" for k in range(1, 8) for j in range(k//2 + 1)}
        expected |= {f"e8:segment{s}:zBernstein{j}/4" for s in range(4) for j in range(5) if (s, j) != (0, 0)}
        require(len(data["records"]) == 38 and {r["name"] for r in data["records"]} == expected, "S46 named obligations")
        require(box(data["w_segments"]) == [(Q(0), Q(1, 16)), (Q(1, 16), Q(1, 4)), (Q(1, 4), Q(1, 2)), (Q(1, 2), Q(1))], "S46 Charlie domain")
        count += counted_cover(data["records"], "positive_leaf_subdivision", dimensions=2, simultaneous=True)
        obligations = sorted(expected) + ["z=1 full determinant from two proven branches"]
    else:
        data = load(upper / f"S{i}_full_certificate.json")
        center = data["central_box"]
        if i in (22, 39):
            center = [center] * 3
        expected_slabs = slabs(box(center))
        require(len(data["outer_boxes"]) == 6, "All six outer slabs required")
        require([box(r["box"]) for r in data["outer_boxes"]] == expected_slabs, "Full-certificate slab domains")
        require(len(data["elementary_coefficients"]) == 7 and {r["k"] for r in data["elementary_coefficients"]} == set(range(1, 8)), "All seven coefficients required once")
        count += counted_cover(data["outer_boxes"]) + counted_cover(data["elementary_coefficients"])
        obligations = [f"e{j}" for j in range(1, 8)] + ["contact Hessian", "six exterior determinant slabs"]
    return {"id": i, "engine": engine, "commands": commands, "obligations": obligations, "cover_leaves": count}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root, output = args.package.resolve(), args.output.resolve()
    require(not output.is_relative_to(root), "Output must be outside the original archive")
    manifest = {path: digest for digest, path in (line.split("  ", 1) for line in (root / "MANIFEST.sha256").read_text().splitlines())}
    def immutable_snapshot():
        actual = {path: hashlib.sha256((root / path).read_bytes()).hexdigest() for path in manifest}
        require(actual == manifest, "Original manifest inputs changed")
        return hashlib.sha256(json.dumps(actual, sort_keys=True).encode()).hexdigest()
    before = immutable_snapshot()
    catalogue = {r["id"]: r for r in load(root / "catalogue.json")}
    history = {r["id"]: r for r in load(root / "data/prior_work_and_contributions.json")["records"]}
    selectors = {r["id"]: r for r in load(root / "data/compact_root_selectors.json")["records"]}
    table = {}
    for line in (root / "manuscript/catalogue_table.tex").read_text().splitlines():
        if re.match(r"^\d+ &", line):
            fields = [x.strip().rstrip("\\") for x in line.split("&")]
            i, local, display, kind, old, multiplicity, column = fields
            require(int(i) not in table, "Duplicate manuscript row")
            table[int(i)] = (int(local), Q(display), kind, old, int(multiplicity), int(column))
    require(set(table) == set(catalogue) == set(history) == set(range(1, 47)), "Catalogue index completeness")
    literal_appendix = (root / "manuscript/bell_functionals.tex").read_text()
    latex_literals = {}
    for match in re.finditer(r"\\paragraph\{Index (\d+).*?\\begin\{align\*\}(.*?)\\end\{align\*\}", literal_appendix, re.S):
        i = int(match[1]); body = re.sub(r"\\B_\{\d+\}=\{\}&", "", match[2])
        body = body.replace("&{}", "").replace("\\\\", "").replace(".", "")
        latex_literals[i] = literal_terms(body)
    require(set(latex_literals) == set(table), "Literal appendix completeness")
    uni_tex = (root / "manuscript/univariate_values.tex").read_text()
    latex_uni = {}
    for match in re.finditer(r"\\paragraph\{Index (\d+)\.\}.*?\\begin\{align\*\}(.*?)\\end\{align\*\}.*?\$\(([^,]+),([^\)]+)\)\$", uni_tex, re.S):
        i = int(match[1]); body = re.sub(r"p_\{\d+\}\(q\)=\{\}&", "", match[2])
        body = body.replace("&{}", "").replace("\\\\", "").replace(".", "")
        latex_uni[i] = (polynomial_coefficients(body), (Q(match[3]), Q(match[4])))
    system_table = {}
    for line in (root / "manuscript/system_centres.tex").read_text().splitlines():
        if re.match(r"^\d+ &", line):
            fields = [a.strip().rstrip("\\") for a in line.split("&")]
            i = int(fields[0]); system_table[i] = list(map(Q, fields[1:-1] if i == 28 else fields[1:]))
            if i == 28:
                require(fields[-1] == "$y$", "S28 omitted-coordinate presentation")
    records, kinds, multiplicities, endpoints = [], Counter(), Counter(), []
    for i in range(1, 47):
        entry = root / "entries" / f"S{i:03d}"
        functional, spec, exact, inputs = [load(entry / name) for name in ("functional.json", "strategy_spec.json", "attainment/strategy_exact.json", "upper_bound/inputs.json")]
        local, display, kind, old, multiplicity, column = table[i]
        require(local == functional["local_bound"] == catalogue[i]["local_bound"], "Local-bound transcription")
        require(latex_literals[i] == literal_terms(functional["expression"]), "Bell appendix transcription")
        require(kind == {"radicals": "R", "univariate": "U", "system": "S"}[spec["kind"]], "Value-kind transcription")
        require(old == ("A" if history[i]["lopez_rosa_2016"]["report_type"] == "analytic_expression" else "D"), "Historical classification transcription")
        require(multiplicity == exact["binding"]["multiplicity"] == history[i]["eigenvalue_multiplicity"], "Multiplicity transcription")
        require(column == exact["column_index_zero_based"] == history[i]["attaining_state_column"], "State-column transcription")
        qlo, qhi = map(Q, exact["binding"]["parameter_intervals"]["q"])
        require(display - Q(1, 2 * 10**10) <= qlo <= qhi <= display + Q(1, 2 * 10**10), "Rounded catalogue value inconsistent with certified interval")
        require(history[i]["upper_verifiers"] == inputs["commands"], "Historical command list transcription")
        if spec["kind"] == "univariate":
            polynomial, interval = latex_uni[i]
            require(polynomial == polynomial_coefficients(spec["polynomial"]) == polynomial_coefficients(selectors[i]["polynomial"]), "Univariate polynomial transcription")
            require(interval == tuple(map(Q, selectors[i]["interval"])), "Univariate selecting-interval transcription")
        elif spec["kind"] == "system":
            require(len(system_table[i]) == len(spec["box"]) == (3 if i == 28 else 4), "System selecting-box dimension")
            require(system_table[i] == list(map(Q, selectors[i]["centers"])), "System centre transcription")
            require(Q(selectors[i]["radius"]) == Q(1, 10**11), "System radius transcription")
            require(all(c - Q(1, 10**11) <= Q(b[0]) <= Q(b[1]) <= c + Q(1, 10**11) for c, b in zip(system_table[i], spec["box"])), "Original system box not inside displayed cube")
        for variable in "xyz":
            lo, hi = map(Q, exact["binding"]["parameter_intervals"][variable])
            if lo == hi and lo in (-1, 1):
                endpoints.append({"id": i, "variable": variable, "overlap": str(lo), "square_root": "0"})
        records.append(audit_upper(entry, inputs))
        kinds[spec["kind"]] += 1; multiplicities[multiplicity] += 1
    require(set(latex_uni) == {i for i, r in selectors.items() if r["kind"] == "univariate"}, "Univariate appendix coverage")
    require(set(system_table) == {i for i, r in selectors.items() if r["kind"] == "system"}, "System appendix coverage")
    after = immutable_snapshot()
    require(before == after, "Read-only audit changed inputs")
    result = {"status": "PASS_INDEPENDENT_TABLES_AND_OBLIGATION_STRUCTURE_ONLY", "entries": 46,
              "scope": "Independent standard-library parsing of catalogue, Bell literals, all 8 univariate polynomials/intervals, all 10 system centres and root-box containment; complete mathematical obligation names and every cover tree. Does not recompute coefficient signs, exact roots, or states.",
              "counts": dict(kinds), "multiplicity_counts": dict(multiplicities),
              "upper_invocations": sum(len(r["commands"]) for r in records),
              "cover_leaves": sum(r["cover_leaves"] for r in records),
              "endpoint_overlap_parameters": endpoints, "original_input_count": len(manifest),
              "original_snapshot_before": before, "original_snapshot_after": after, "records": records}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("status", "entries", "counts", "multiplicity_counts", "upper_invocations", "cover_leaves", "original_input_count")}, indent=2))


if __name__ == "__main__":
    main()
