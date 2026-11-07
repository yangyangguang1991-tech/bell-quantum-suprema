"""Replay three historical defects through the actual public verify command.

Each case uses a fresh complete temporary package copy. Only the listed JSON
inputs are changed, the copy's manifest is rebuilt and publicly checked, and
python -S run.py verify --id N must reject the intended binding/contract
defect. This script never imports or directly calls the input binder. Logs and
the changed JSON inputs are retained outside the source package.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def snapshot(directory):
    return {
        path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in directory.rglob("*") if path.is_file()
    }


def snapshot_digest(files):
    return hashlib.sha256(json.dumps(files, sort_keys=True).encode("utf-8")).hexdigest()


def mutate(package, case):
    if case == "s46_false_ten":
        changes = {
            "entries/S046/strategy_spec.json": {
                "polynomial": "q-10", "interval": ["9", "11"], "overlaps": ["1", "1", "1"]
            },
            "entries/S046/upper_bound/certificate_46_reduced.json": {
                "polynomial": "q-10", "isolating_interval": ["9", "11"], "attaining_t": "1"
            },
        }
    elif case == "s2_empty_commands":
        changes = {"entries/S002/upper_bound/inputs.json": {"commands": []}}
    elif case == "s40_interval_below":
        relative = "entries/S040/upper_bound/S40_full_certificate.json"
        original = load(package / relative)
        changes = {relative: {
            "q_interval": [str(Fraction(value) - Fraction(1, 10**20)) for value in original["q_interval"]]
        }}
    else:
        raise ArithmeticError("Unknown regression case: " + case)
    for relative, updates in changes.items():
        path = package / relative
        data = load(path)
        data.update(updates)
        save(path, data)
    return changes


def execute(package, output, label, arguments):
    env = os.environ.copy()
    env.update(PYTHONPATH=str(package / "third_party/vendor"), PYTHONUTF8="1",
               PYTHONDONTWRITEBYTECODE="1", PYTHONOPTIMIZE="0")
    command = [sys.executable, "-S", *arguments]
    log = output / (label + ".log")
    started = time.monotonic()
    with log.open("w", encoding="utf-8") as handle:
        result = subprocess.run(command, cwd=package, env=env, stdout=handle,
                                stderr=subprocess.STDOUT, timeout=60)
    return {
        "command": ["python", "-S", *arguments],
        "returncode": result.returncode,
        "seconds": round(time.monotonic() - started, 6),
        "log": log.name,
    }, log.read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="New directory outside the package for retained evidence")
    args = parser.parse_args()
    output = (args.output if args.output else ROOT.parent / (ROOT.name + "-public-regressions")).resolve()
    require(output != ROOT and ROOT not in output.parents, "Public regression output must be outside the package")
    require(not output.exists(), "Use a new output directory")
    output.mkdir(parents=True)
    started = time.monotonic()
    source_files = snapshot(ROOT)
    cases = [
        ("s46_false_ten", 46, "S46 reduced and full upper targets have different q intervals"),
        ("s2_empty_commands", 2, "S2: upper engine, characteristic file and ordered commands must match the fixed replay contract"),
        ("s40_interval_below", 40, "S40 global q interval differs from selected-root q box"),
    ]
    records = []
    with tempfile.TemporaryDirectory(prefix="sliwa-public-regressions-") as temporary:
        for name, entry_id, expected_reason in cases:
            case_output = output / name
            case_output.mkdir()
            package = Path(temporary) / name / ROOT.name
            shutil.copytree(ROOT, package)
            require(snapshot(package) == source_files, name + ": the complete package copy differs from its source")
            changes = mutate(package, name)
            mutated_files = snapshot(package)
            differences = sorted(path for path in source_files if source_files[path] != mutated_files.get(path))
            require(differences == sorted(changes) and source_files.keys() == mutated_files.keys(),
                    name + ": the mutation changed files outside the intended inputs")
            for relative in changes:
                save(case_output / "mutated_inputs" / relative, load(package / relative))

            rebuild, rebuild_text = execute(package, case_output, "01_rebuild_manifest", ["tools/write_manifest.py"])
            require(rebuild["returncode"] == 0 and "Wrote " in rebuild_text,
                    name + ": manifest rebuild failed")
            manifest, manifest_text = execute(package, case_output, "02_manifest", ["run.py", "manifest"])
            require(manifest["returncode"] == 0 and manifest_text.strip() == "PASS_MANIFEST",
                    name + ": public manifest command did not pass")
            before_verify = snapshot(package)
            verify, verify_text = execute(package, case_output, "03_verify", ["run.py", "verify", "--id", str(entry_id)])
            exception_line = "RuntimeError: " + expected_reason
            require(verify["returncode"] != 0 and verify_text.rstrip().endswith(exception_line),
                    name + ": public verify did not reject the intended binding/contract defect")
            started_prefixes = (f"S{entry_id:03d}: exact attaining strategy PASS", f"S{entry_id:03d}: upper ")
            require(not any(line.startswith(started_prefixes) for line in verify_text.splitlines()),
                    name + ": rejection happened after construction or upper replay started")
            require(snapshot(package) == before_verify, name + ": public verify changed the rejected package")
            record = {
                "case": name, "id": entry_id, "status": "PASS_PUBLIC_REJECTION",
                "changed_input_fields": changes,
                "changed_input_sha256": {path: mutated_files[path] for path in changes},
                "manifest_sha256": before_verify["MANIFEST.sha256"],
                "rebuild_manifest": rebuild, "public_manifest": manifest, "public_verify": verify,
                "rejection_reason": exception_line, "manifest_passed_before_public_verify": True,
                "rejected_before_constructive_export_and_upper": True,
                "rejected_package_unchanged": True,
            }
            save(case_output / "result.json", record)
            records.append(record)
            print(name + ": PASS_MANIFEST, then PASS_PUBLIC_REJECTION", flush=True)
    require(snapshot(ROOT) == source_files, "Source package changed during the public regression controls")
    report = {
        "status": "PASS_PUBLIC_ENTRY_POINT_REGRESSIONS", "negative_controls": len(records),
        "source_file_count": len(source_files), "source_snapshot_sha256": snapshot_digest(source_files),
        "source_package_unchanged": True, "python_executable": sys.executable,
        "scope": "Three historical mutations, each in a fresh complete package copy; manifest rebuild and public manifest PASS precede actual public verify rejection. No direct binder calls and no upper-proof replay.",
        "controls": records, "seconds": round(time.monotonic() - started, 6),
    }
    save(output / "public_regressions.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
