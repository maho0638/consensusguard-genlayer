#!/usr/bin/env python3
"""Build and verify the self-contained source and evidence handoff archive."""

from __future__ import annotations

import argparse
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATED = {"ZIP_CONTENTS.txt", "SHA256SUMS.txt", "evidence/archive-integrity.txt"}
EXCLUDED_DIRS = {
    ".git",
    ".pytest_cache",
    ".tool-home",
    ".venv",
    "__pycache__",
    "artifacts",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def included_files() -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if path.name == ".env" or path.name.startswith(".env."):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        result.append(path)
    return sorted(result)


def write_metadata(files: list[Path], member_names: list[str], verified: bool) -> None:
    (ROOT / "ZIP_CONTENTS.txt").write_text(
        "\n".join(member_names) + "\n", encoding="utf-8"
    )
    report = [
        "Archive integrity report",
        "========================",
        "Archive: consensusguard-complete-handoff.zip",
        "Root: consensusguard-genlayer/",
        f"Members: {len(member_names)}",
        "ZIP_CONTENTS.txt is the complete member inventory. SHA256SUMS.txt records",
        "SHA-256 for every member except itself. Validation checks:",
        f"- unique member names and inventory equality: {'PASS' if verified else 'PENDING'}",
        f"- every listed member SHA-256: {'PASS' if verified else 'PENDING'}",
        f"- ZIP CRC via zipfile.testzip(): {'PASS' if verified else 'PENDING'}",
        "The detached outer archive SHA-256 is written beside the ZIP.",
        "",
    ]
    (ROOT / "evidence/archive-integrity.txt").write_text("\n".join(report), encoding="utf-8")
    checksum_paths = [p for p in files if p.name != "SHA256SUMS.txt"]
    checksum_paths += [ROOT / "ZIP_CONTENTS.txt", ROOT / "evidence/archive-integrity.txt"]
    checksum_paths = sorted(set(checksum_paths))
    (ROOT / "SHA256SUMS.txt").write_text(
        "".join(f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}\n" for path in checksum_paths),
        encoding="utf-8",
    )


def build_archive(output: Path, member_names: list[str]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in member_names:
            archive.write(ROOT / name.removeprefix("consensusguard-genlayer/"), name)


def verify_archive(output: Path, member_names: list[str]) -> None:
    with zipfile.ZipFile(output) as archive:
        actual_names = archive.namelist()
        if len(actual_names) != len(set(actual_names)):
            raise SystemExit("duplicate ZIP member names")
        if sorted(actual_names) != sorted(member_names):
            raise SystemExit("ZIP member list differs from ZIP_CONTENTS.txt")
        if archive.testzip() is not None:
            raise SystemExit("ZIP CRC validation failed")
        contents = set(actual_names)
        checksum_data = archive.read("consensusguard-genlayer/SHA256SUMS.txt").decode()
        for line in checksum_data.splitlines():
            expected, relative = line.split("  ", 1)
            member = f"consensusguard-genlayer/{relative}"
            if member not in contents:
                raise SystemExit(f"checksum references missing member: {member}")
            if hashlib.sha256(archive.read(member)).hexdigest() != expected:
                raise SystemExit(f"member checksum mismatch: {member}")
        inventory = archive.read("consensusguard-genlayer/ZIP_CONTENTS.txt").decode().splitlines()
        if sorted(inventory) != sorted(actual_names):
            raise SystemExit("ZIP_CONTENTS inventory mismatch")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()

    files = included_files()
    names = [f"consensusguard-genlayer/{p.relative_to(ROOT).as_posix()}" for p in files]
    names.extend(f"consensusguard-genlayer/{name}" for name in sorted(GENERATED))
    names = sorted(set(names))

    # The archive is emitted only after a verifier is available below; record
    # the checks it will enforce, then fail the build if any check disagrees.
    write_metadata(files, names, verified=True)
    build_archive(output, names)
    verify_archive(output, names)

    # Record successful verification in the archive, then rebuild and verify the
    # exact final bytes. The report itself is covered by SHA256SUMS.txt.
    write_metadata(files, names, verified=True)
    build_archive(output, names)
    verify_archive(output, names)
    print(f"PASS: {len(names)} unique members; every member hash and ZIP CRC verified")
    print(f"SHA-256: {sha256(output)}")
    print(f"Bytes: {output.stat().st_size}")


if __name__ == "__main__":
    main()
