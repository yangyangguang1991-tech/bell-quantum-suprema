"""Fresh 46-entry replay from a supplied release ZIP, with an immutable input audit.

Uses each entry's public `run.py verify --id` command. Four commands
run concurrently; their export directories and temporary proof directories are
disjoint. The supplied ZIP and any previous extraction remain unchanged.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import subprocess
import sys
import time
import zipfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def filesystem_path(path):
    """Use an absolute extended-length path on Windows, without changing data."""
    path = path.resolve()
    if os.name != "nt":
        return path
    slash = chr(92)
    prefix = slash * 2 + "?" + slash
    value = str(path)
    if value.startswith(prefix):
        return path
    if value.startswith(slash * 2):
        return Path(prefix + "UNC" + slash + value[2:])
    return Path(prefix + value)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("archive", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    archive = filesystem_path(args.archive)
    out = filesystem_path(args.output)
    if out.exists():
        raise SystemExit("Refusing to reuse an existing replay output directory")
    if not 1 <= args.workers <= 8:
        raise SystemExit("worker count must lie in 1..8")
    out.mkdir(parents=True)
    extracted = out / "extracted"
    original = {}
    with zipfile.ZipFile(archive) as zf:
        for info in zf.infolist():
            rel = PurePosixPath(info.filename)
            if rel.is_absolute() or ".." in rel.parts or info.is_dir():
                raise SystemExit(f"Unexpected archive path: {info.filename}")
            if info.filename in original:
                raise SystemExit("Duplicate ZIP entry")
            original[info.filename] = sha(zf.read(info))
        zf.extractall(extracted)
    roots = {PurePosixPath(name).parts[0] for name in original}
    if len(roots) != 1:
        raise SystemExit("The archive must contain one complete repository directory")
    package = extracted / next(iter(roots))
    if not (package / "run.py").is_file() or not (package / "entries").is_dir():
        raise SystemExit("The archive does not contain the documented repository layout")
    logs = out / "logs"
    reports = out / "reports"
    logs.mkdir()
    reports.mkdir()
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    started = time.monotonic()
    launch = {
        "source_archive": archive.name,
        "source_archive_sha256": sha(archive.read_bytes()),
        "extracted_original_file_count": len(original),
        "python": sys.version,
        "platform": platform.platform(),
        "workers": args.workers,
        "scope": "46 fresh public run.py verify --id commands; not one run.py --all invocation",
    }
    dump(out / "launch.json", launch)
    dump(out / "original_archive_files.json", original)

    def run_one(i):
        report = reports / f"S{i:03d}.json"
        log = logs / f"S{i:03d}.log"
        cmd = [sys.executable, "-S", str(package / "run.py"), "verify", "--id", str(i), "--report", str(report)]
        t = time.monotonic()
        with log.open("w", encoding="utf-8") as stream:
            p = subprocess.run(cmd, cwd=package, env=env, stdout=stream, stderr=subprocess.STDOUT)
        rec = {"id": i, "argv": cmd, "exit_code": p.returncode,
               "wall_seconds": round(time.monotonic()-t, 6), "log": str(log.relative_to(out))}
        if report.exists():
            payload = json.loads(report.read_text())
            rec["reported_status"] = payload.get("status")
            rec["upper_commands"] = [command for row in payload.get("upper_bounds", []) for command in row["commands"]]
            rec["attainment_count"] = len(payload.get("strategy_exports", []))
            rec["report"] = str(report.relative_to(out))
        return rec

    # Long characteristic/contact cases first, to reduce the final tail.
    order = [24, 25, 31, 32, 34, 35, 36, 41, 42, 5, 18, 16, 28, 40, 46]
    order += [i for i in range(1, 47) if i not in order]
    records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(run_one, i): i for i in order}
        for f in concurrent.futures.as_completed(futures):
            rec = f.result()
            records.append(rec)
            dump(out / "progress.json", {"completed": len(records), "total": 46,
                                        "elapsed_seconds": round(time.monotonic()-started, 3),
                                        "records": sorted(records, key=lambda r:r["id"])})
            print(f"COMPLETE {len(records):02d}/46 S{rec['id']:03d} exit={rec['exit_code']} wall={rec['wall_seconds']:.3f}s", flush=True)

    integrity = []
    for rel, digest in original.items():
        p = extracted / rel
        if not p.is_file() or sha(p.read_bytes()) != digest:
            integrity.append(rel)
    entries = []
    for i in range(1, 47):
        d = package / "entries" / f"S{i:03d}"
        paths = list(d.rglob("strategy_exact.json"))
        exported = package / "exports" / f"S{i:03d}" / "strategy_exact.json"
        if len(paths) != 1 or not exported.exists():
            entries.append({"id": i, "exact_export_identical": False,
                            "reason": "Missing or ambiguous strategy_exact.json"})
        else:
            entries.append({"id": i, "exact_export_identical": paths[0].read_bytes() == exported.read_bytes(),
                            "original_sha256": sha(paths[0].read_bytes()), "export_sha256": sha(exported.read_bytes())})
    good = (len(records)==46 and all(r["exit_code"]==0 and r.get("reported_status")=="PASS_EXACT_GLOBAL_UPPER_AND_CONSTRUCTIVE_ATTAINMENT"
                                   and r.get("attainment_count")==1 for r in records)
            and sum(len(r.get("upper_commands", [])) for r in records)==52
            and not integrity and all(r["exact_export_identical"] for r in entries))
    result = {**launch, "status": "PASS_FRESH_46_CHAINS_52_UPPER_CALLS" if good else "CHECK_FAILURES",
              "wall_seconds": round(time.monotonic()-started, 6),
              "entry_count": len(records), "upper_command_count": sum(len(r.get("upper_commands", [])) for r in records),
              "original_files_unchanged": not integrity, "changed_original_files": integrity,
              "exact_exports_byte_identical": all(r["exact_export_identical"] for r in entries),
              "entries": sorted(records, key=lambda r:r["id"]), "export_comparison": entries}
    dump(out / "fresh_replay_summary.json", result)
    print(json.dumps({k:v for k,v in result.items() if k not in {"entries","export_comparison"}}, ensure_ascii=False), flush=True)
    raise SystemExit(0 if good else 1)


if __name__ == "__main__":
    main()
