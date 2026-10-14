#!/usr/bin/env python3
"""Build and locally verify one complete, provenance-bound phase-seven handoff.

This builds a DIRECTORY for GitHub Actions upload-artifact. The upload action
creates the ONE final downloadable ZIP. No nested ZIP is created here.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BASE = "29eff0d38a1181dff9e8a60c1e9c0eff018c87de"
REPO = "maho0638/consensusguard-genlayer"
SOURCE_CONTRACT_BLOB = "ca4df13afea4accc90e858aab5f71cb420242c57"

CI_RUNS = {
    "phase6_full_studio": (38555170256, "3c0f5391431b5f8d0e0ae6ca57a716ced047b359"),
    "phase6_quality_last_report": (38557260290, EXPECTED_BASE),
    "studio_dev_signed_receipts_readonly": (38583016128, "5058c5be46763e7b0bdb0fb6b411e64ef70b3946"),
    "phase6_dependency_advisories": (38555288470, "c16a85395e9a473c430e367f30fc6f182ca5f0e6"),
    "phase5_studio_dev_historical_read": (38553677412, "d65eed9a7899ba5b221822b5fccd5c7c34e90ba4"),
    "phase5_local_studio": (38532431448, "f3178399cc1a9e435dd75dabe7a4c86f9065ea46"),
    "phase4_real_studio": (38505860129, "e8022da8c14edf30dde0a56894e9ba1fd964c863"),
    "phase3_real_studio": (38495073179, "f75a5fab"),
    "phase1_real_studio": (38474767527, "7cb921429217ed4537f55ddbadde4fc7c19e2daa"),
}

REQUIRED_EVIDENCE = [
    "evidence/PHASE1_OPEN_CASE_DIAGNOSIS_2026-10-14.md",
    "evidence/PHASE3_REAL_STUDIO_APPEAL_VERIFIED_2026-10-14.md",
    "evidence/audit-studio-phase4-38505860129.md",
    "evidence/PHASE5_IDLE_VALIDATORS_ROOT_CAUSE_2026-10-14.md",
    "evidence/historical-studio-dev-idle-readonly-38553677412.md",
    "evidence/audit-studio-phase6-full-38555170256.md",
    "evidence/PHASE6_FINAL_SECURITY_REGRESSION_2026-10-14.md",
    "evidence/phase6-dependency-audit-38555288470.md",
    "evidence/studio-dev-live-validation.md",
    "evidence/STUDIO_DEV_PHASE7_SIGNED_APPEAL_2026-10-14.md",
    "evidence/STUDIO_DEV_SIGNED_APPEAL_RECEIPT_INDEPENDENT_AUDIT_2026-10-14.md",
    "evidence/STUDIO_DEV_SIGNED_APPEAL_FINAL_VERDICT_2026-10-14.md",
    "requirements-lock.txt",
    "contracts/consensus_guard.py",
    "tests/test_consensus_guard.py",
    "tests/test_studio_multivalidator.py",
    "tests/test_studio_phase4_disagreement.py",
    "tests/test_studio_phase4_rotation.py",
    ".github/workflows/phase6-full-audit.yml",
    ".github/workflows/quality.yml",
]
CHECKS = [
    "pip_check.log", "bundle_verify.log", "compileall.log",
    "genvm_lint.log", "contract_sdk.log", "pyright.log", "pytest.log",
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def fetch_verified_runs() -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN missing; cannot attest real CI status")
    report = {}
    for key, (runid, expected_sha) in CI_RUNS.items():
        url = f"https://api.github.com/repos/{REPO}/actions/runs/{runid}"
        request = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "ConsensusGuard-Phase7-Readonly",
            },
        )
        with urllib.request.urlopen(request, timeout=25) as response:
            item = json.load(response)
        if item.get("status") != "completed" or item.get("conclusion") != "success":
            raise RuntimeError(f"Historical CI run {runid} is not successful")
        actual_sha = str(item.get("head_sha", ""))
        if not actual_sha.startswith(expected_sha):
            raise RuntimeError(f"Historical CI run {runid} has unexpected commit")
        if item.get("repository", {}).get("full_name", REPO).lower() != REPO.lower():
            raise RuntimeError(f"Historical CI run {runid} repository mismatch")
        report[key] = {
            "run_id": runid,
            "url": item.get("html_url"),
            "status": "completed",
            "conclusion": "success",
            "head_sha": actual_sha,
            "created_at": item.get("created_at"),
        }
    return report


def check_manifest(folder: Path) -> tuple[int, int]:
    manifest = json.loads((folder / "SHA256_MANIFEST.json").read_text("utf-8"))
    listed = manifest["files"]
    actual = {
        p.relative_to(folder).as_posix()
        for p in folder.rglob("*")
        if p.is_file() and p.name != "SHA256_MANIFEST.json"
    }
    if actual != set(listed):
        raise RuntimeError(
            f"Archive inventory mismatch: missing={len(set(listed)-actual)} "
            f"extra={len(actual-set(listed))}"
        )
    size = 0
    for path, meta in listed.items():
        data = (folder / path).read_bytes()
        size += len(data)
        if len(data) != meta["bytes"] or digest(data) != meta["sha256"]:
            raise RuntimeError(f"SHA-256 file mismatch: {path}")
    return len(listed), size


def build(qa: Path, destination: Path) -> None:
    head = git("rev-parse", "HEAD")
    branch = git("symbolic-ref", "--short", "HEAD")
    if branch != "audit/studio-dev-real-appeal-20261014":
        raise RuntimeError("Unexpected branch; refuse handoff")
    if git("rev-parse", f"{EXPECTED_BASE}^{{commit}}") != EXPECTED_BASE:
        raise RuntimeError("Known phase-six base missing")
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", EXPECTED_BASE, head], cwd=ROOT
    )
    if ancestry.returncode != 0:
        raise RuntimeError("Phase seven is not descended from audited phase six")
    if git("rev-parse", "HEAD:contracts/consensus_guard.py") != SOURCE_CONTRACT_BLOB:
        raise RuntimeError("Production contract modified after audited phase six")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).strip():
        raise RuntimeError("Refuse dirty source checkout")
    if destination.exists():
        raise RuntimeError("Destination already exists; refuse stale content")

    tracked = [
        os.fsdecode(p) for p in
        subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).split(b"\x00")
        if p
    ]
    if len(tracked) < 180:
        raise RuntimeError(f"Only {len(tracked)} tracked files; expected whole repository")
    missing = sorted(set(REQUIRED_EVIDENCE) - set(tracked))
    if missing:
        raise RuntimeError("Required exact proof is missing: " + ",".join(missing))
    if not (qa / "pytest.log").exists():
        raise RuntimeError("QA artifacts missing")
    pytest_result = (qa / "pytest.log").read_text(errors="replace")
    m = re.search(r"(\d+) passed, (\d+) skipped", pytest_result)
    if not m or int(m.group(1)) < 98 or int(m.group(2)) != 3:
        raise RuntimeError("Final QA pass threshold not proven")
    for name in CHECKS:
        if not (qa / name).exists():
            raise RuntimeError(f"QA output {name} missing")
    try:
        genvm_result = json.loads((qa / "genvm_lint.log").read_text("utf-8"))
    except (ValueError, UnicodeError):
        raise RuntimeError("GenVM-lint output is not valid JSON")
    if not (isinstance(genvm_result, dict) and genvm_result.get("ok") is True
            and int(genvm_result.get("passed", -1)) >= 1):
        raise RuntimeError("GenVM-lint PASS marker absent")
    try:
        pyright_result = json.loads((qa / "pyright.log").read_text("utf-8"))
        pyright_errors = int(pyright_result["summary"]["errorCount"])
    except (ValueError, TypeError, KeyError, UnicodeError):
        raise RuntimeError("Pyright output lacks explicit error summary")
    if pyright_errors != 0:
        raise RuntimeError("Pyright reported type errors")
    if "No broken requirements found" not in (qa / "pip_check.log").read_text():
        raise RuntimeError("Pip dependency consistency not verified")

    studio = (ROOT / "evidence/audit-studio-phase6-full-38555170256.md").read_text()
    for needle in [
        "PHASE4_COMPLETE: REAL_STUDIO_DISAGREEMENT_ROLLBACK_RECOVERY_PASS",
        "PHASE4_ROTATION_COMPLETE: REAL_STUDIO_SPARE_VALIDATOR_ROTATION_ROLLBACK_RECOVERY_PASS",
        "STUDIO_PHASE5_COMPLETE: RESOLVE_AND_APPEAL_TWO_IDLE_CAUSE_PROVEN",
        "TX_STATE|FINALIZED|count=12",
        "LIFECYCLE|total=12|finalized=12|unfinalized=0|write_calls=9",
    ]:
        if needle not in studio:
            raise RuntimeError(f"Phase-six real Studio evidence is missing: {needle}")
    if not re.search(r"## Result\s+PASS", studio):
        raise RuntimeError("Real Studio report not PASS")
    deps = (ROOT / "evidence/phase6-dependency-audit-38555288470.md").read_text()
    for val in ("Known advisories: 0", "Result: **PASS**"):
        if val not in deps:
            raise RuntimeError("Dependency security proof invalid")

    # The new latest-source signed Studio Dev appeal was validated by an
    # independent read-only consensus receipt/source SHA-256 audit. Fail closed
    # if that new evidence is missing or falsely claims storage readback PASS.
    signed = (ROOT / "evidence/STUDIO_DEV_SIGNED_APPEAL_RECEIPT_INDEPENDENT_AUDIT_2026-10-14.md").read_text()
    for needle in (
        "Deployed source EXACT match: **True**",
        "FINISHED_WITH_RETURN and FINALIZED count: 4/4",
        'appeal: status=FINALIZED, execution=FINISHED_WITH_RETURN',
        "All four strong receipt gates pass: **True**",
    ):
        if needle not in signed:
            raise RuntimeError("Latest Studio Dev signed appeal proof missing: " + needle)
    finaldev = (ROOT / "evidence/STUDIO_DEV_SIGNED_APPEAL_FINAL_VERDICT_2026-10-14.md").read_text()
    if "readback remains BLOCKED" not in finaldev:
        raise RuntimeError("Latest report must explicitly distinguish unavailable state readback")
    latest_test = (ROOT / "evidence/STUDIO_DEV_PHASE7_SIGNED_APPEAL_2026-10-14.md").read_text()
    if "- appeal finalized successfully" not in latest_test:
        raise RuntimeError("Original fresh Studio Dev appeal finalization proof absent")

    run_proofs = fetch_verified_runs()
    source_root = destination / "SOURCE_CODE"
    for rel in tracked:
        source = ROOT / rel
        if not source.is_file():
            raise RuntimeError(f"Tracked source missing on disk: {rel}")
        target = source_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)

    qa_dest = destination / "CURRENT_TEST_RESULTS"
    qa_dest.mkdir(parents=True, exist_ok=True)
    for name in CHECKS:
        shutil.copyfile(qa / name, qa_dest / name)
    save_text(
        destination / "CURRENT_TEST_RESULTS" / "QA_SUMMARY.json",
        json.dumps({
            "run_commit": head,
            "passed": int(m.group(1)),
            "skipped_real_studio_in_offline_suite": int(m.group(2)),
            "real_studio_test_workflow_run": 38555170256,
            "real_studio_test_count": 3,
            "real_local_studio_finalized_transactions": 12,
            "security_vulnerability_advisory_count": 0,
        }, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    )
    save_text(
        destination / "VERIFIED_CI" / "RUNS_VERIFIED.json",
        json.dumps(run_proofs, sort_keys=True, indent=2) + "\n"
    )
    save_text(
        destination / "VERIFIED_CI" / "PROVENANCE.json",
        json.dumps({
            "repository": REPO,
            "audited_branch": branch,
            "git_commit_with_all_source_files": head,
            "parent_verified_phase6_base": EXPECTED_BASE,
            "production_contract_git_blob": SOURCE_CONTRACT_BLOB,
            "tracked_file_count": len(tracked),
            "verification_date_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "full_source_tree": "SOURCE_CODE/",
            "no_public_chain_writes_or_gen_spending": True,
            "no_merge_or_deploy_performed": True,
        }, sort_keys=True, indent=2) + "\n"
    )
    save_text(
        destination / "START_HERE_TR.txt",
        "CONSENSUSGUARD — GUNCEL KAYNAK VE GERCEK STUDIO DEV APPEAL KANITLARI\n"
        f"GitHub: https://github.com/{REPO}/tree/{head}\n"
        f"Kaynak commit: {head}\n"
        "SOURCE_CODE/ klasoru tum izlenen kaynak, evidence ve CI is akislarini icerir.\n"
        "VERIFIED_CI/ gercek basarili is akislarinin canli GitHub durum kanitidir.\n"
        "CURRENT_TEST_RESULTS/ 98+ test ve lint/SDK/typecheck kanitlarini icerir.\n"
        "GUNCEL STUDIO DEV: dort imzali islem, deploy/open_case/resolve/appeal,\n"
        "tum islem makbuzlari FINALIZED + FINISHED_WITH_RETURN, 3/5 validator onay.\n"
        "Kaniti: SOURCE_CODE/evidence/STUDIO_DEV_SIGNED_APPEAL_FINAL_VERDICT_2026-10-14.md\n"
        "AYRI SINIR: Studio Dev gen_call sunucusunda SQLAlchemy DB hatasi var;\n"
        "get_case/get_decision uzerinden bagimsiz state readback henuz mumkun degil.\n"
        "SHA256_MANIFEST.json ve verify_sha256.py tum dosyalari dogrular.\n"
        "PORTAL GONDERIMI YAPILMADI. Main veya Vercel degismedi.\n"
    )
    save_text(
        destination / "FINAL_RELEASE_DECISION_TR.md",
        f"""# ConsensusGuard — Tek ZIP ve son dogrulama (2026-10-14)

**Tek ZIP teslimi: TAMAMLANDI.**
**Gerçek Studio Dev imzalı appeal: PASS.**
**GenLayer Portal / kamuya gönderim: HAZIR DEĞİL; ayrı son state readback sunucuda engellendi.**

## Kanıtlanan teknik koşular

- Kaynak: `{head}`; **{len(tracked)} tam izlenen dosya**.
- Üretim kontrat kodu Git blob: `{SOURCE_CONTRACT_BLOB}`.
- Direct Mode ve güvenlik regresyonu: **{m.group(1)} PASS, {m.group(2)} lokal Studio ayrı çalıştırılmış SKIP**.
- Gerçek yerel Studio entegrasyonu: üç PASS senaryosu, 12 FINALIZED işlem;
  anlaşmazlık, rollback, rotasyon ve appeal.
- Studio Dev eski imzalı işlem kaydındaki 2 IDLE'ın nedeni doğrulandı.
- **YENİ gerçek Studio Dev 61997:** Yeni kontrat deploy, open_case, resolve,
  appeal; dört özgün imzalı işlem `FINALIZED + FINISHED_WITH_RETURN`.
- Yeni deploy'un kaynak SHA-256 değeri GitHub sözleşmesiyle **birebir eşleşti**.
- Gerçek appeal: 3 agree / 1 disagree / 1 idle, başarılı kabul edilmiş tam consensus.
- Gerçek işlem dökümü: `SOURCE_CODE/evidence/STUDIO_DEV_PHASE7_SIGNED_APPEAL_2026-10-14.md`.
- Bağımsız makbuzlar ve SHA-256:
  `SOURCE_CODE/evidence/STUDIO_DEV_SIGNED_APPEAL_RECEIPT_INDEPENDENT_AUDIT_2026-10-14.md`.
- İlgili CI başarı kaydı:
  https://github.com/maho0638/consensusguard-genlayer/actions/runs/38583016128
- İlk dört gerçek işlem zincirde başarıyla sonuçlandı, fakat ilk E2E CI koşusu
  yalnızca son readback kapısında başarısız olarak raporlandı. Bu olgu gizlenmedi.
- 67 kilitli bağımlılık; sıfır bilinen güvenlik uyarısı.
- ZIP `SHA256_MANIFEST.json` içindeki bütün dosyalar tekrar hesaplanarak doğrulanır.

## Eksik olan, sözleşme işlem hatası olmayan kontrol

GenLayer'ın barındırdığı Studio Dev `gen_call` endpoint'i hâlâ `-32603`
SQLAlchemy oturumunda geri alma hatası veriyor. Bu nedenle gerçek kontratın
`get_case(0)`, `get_decision(0/1)` ve `decision_count()` JSON readback
sonuçları erişilemiyor. Gerçek imzalı ve başarılı `appeal` makbuzu
`PASS` olsa da bu **ayrı readback doğrulaması PASS değildir.**
Kontrat kaynak kodundan başarılı `appeal` sonucunun `APPEALED` state'i
ve ikinci değişmez karar kaydı yazması beklenir; bu doğrudan storage okuması
ile **ayrıca kanıtlanmış değildir**.

Studio Dev sunucusu düzeldikten sonra bu kontrat adresinden salt-okunur
`get_case(0)`, `get_decision(0)`, `get_decision(1)` ve
`decision_count()` okunup state ve değişmezlik tekrar doğrulanmalıdır.
Bunun için yeni deploy, GEN harcaması veya başka imzalı itiraz gerekmez.

**GitHub main değişmedi; Vercel ve Portal'a dokunulmadı.**
"""
    )
    verifier = r'''#!/usr/bin/env python3
"""Offline package verifier: run from anywhere with Python 3.8+."""
import hashlib, json
from pathlib import Path
root=Path(__file__).resolve().parent
metadata=json.loads((root/"SHA256_MANIFEST.json").read_text("utf-8"))
files=metadata["files"]
actual={p.relative_to(root).as_posix() for p in root.rglob("*")
        if p.is_file() and p.name != "SHA256_MANIFEST.json"}
assert set(files)==actual, "Missing or unexpected files"
for name,meta in files.items():
    blob=(root/name).read_bytes()
    assert len(blob)==meta["bytes"], "Length mismatch: "+name
    assert hashlib.sha256(blob).hexdigest()==meta["sha256"], "SHA mismatch: "+name
print("SHA256_ALL_FILES_PASS",len(files),"commit",metadata["source_git_commit"])
'''
    save_text(destination / "verify_sha256.py", verifier)
    items = {}
    for item in sorted(destination.rglob("*")):
        if not item.is_file():
            continue
        rel = item.relative_to(destination).as_posix()
        if rel == "SHA256_MANIFEST.json":
            raise RuntimeError("Manifest unexpectedly exists before creation")
        data = item.read_bytes()
        items[rel] = {"bytes": len(data), "sha256": digest(data)}
    manifest = {
        "format": "ConsensusGuard.Package.SHA256.v1",
        "source_git_commit": head,
        "source_repository": REPO,
        "source_tracked_files": len(tracked),
        "packaged_file_count_excluding_manifest": len(items),
        "files": items,
    }
    save_text(destination / "SHA256_MANIFEST.json",
              json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)+"\n")
    count, total = check_manifest(destination)
    required_controls = {
        "CURRENT_TEST_RESULTS/QA_SUMMARY.json",
        "VERIFIED_CI/RUNS_VERIFIED.json",
        "VERIFIED_CI/PROVENANCE.json",
        "START_HERE_TR.txt",
        "FINAL_RELEASE_DECISION_TR.md",
        "verify_sha256.py",
    }
    listed = json.loads((destination / "SHA256_MANIFEST.json").read_text("utf-8"))["files"]
    missing_controls = required_controls - set(listed)
    if missing_controls:
        raise RuntimeError("Handoff controls missing: " + ", ".join(sorted(missing_controls)))
    expected_count = len(tracked) + len(CHECKS) + len(required_controls)
    if count != expected_count:
        raise RuntimeError(
            f"Handoff inventory count mismatch: actual={count} expected={expected_count}"
        )
    print("PHASE7_ALL_SHA256_PASS count=",count,"bytes=",total)
    print("PHASE7_GIT_SOURCE=",head)
    print("PHASE7_SOURCE_TRACKED=",len(tracked))
    print("PHASE7_ZIP_RELEASE_GATE=SIGNED_STUDIO_DEV_APPEAL_PASS_READBACK_BLOCKED")
    print("PHASE7_READY_TO_UPLOAD_SINGLE_ARTIFACT_DIRECTORY")


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--qa-dir",required=True,type=Path)
    p.add_argument("--destination",required=True,type=Path)
    args=p.parse_args()
    build(args.qa_dir,args.destination)
