"""Validate the publication catalogue and file provenance; no network or SDK runs."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import csv
import hashlib
import json
import re

root = Path(__file__).resolve().parents[1]
papers = json.loads((root / "catalog/papers.json").read_text())
manifest = json.loads((root / "catalog/pdf-manifest.json").read_text())
errors = []

def check(condition, message):
    if not condition:
        errors.append(message)

ids = [p["id"] for p in papers]
check(len(ids) == len(set(ids)), "Duplicate catalogue IDs")
jsonl = [json.loads(line) for line in (root / "catalog/papers.jsonl").read_text().splitlines()]
check(jsonl == papers, "JSON and JSONL differ")
with (root / "catalog/papers.csv").open(newline="") as file:
    rows = list(csv.DictReader(file))
check([r["id"] for r in rows] == ids, "CSV IDs/order differ")
keys = re.findall(r"@\w+\{([^,]+),", (root / "references.bib").read_text())
check(set(keys) == {p["citation_key"] for p in papers}, "BibTeX coverage differs")
check(len(keys) == len(set(keys)), "Duplicate BibTeX keys")
readme = (root / "README.md").read_text()
for p in papers:
    for field in ("title", "authors", "year", "venue", "url", "summary", "reading_depth"):
        check(bool(p.get(field)), f"Missing {field}: {p['id']}")
    check(p["title"] in readme, f"README omits {p['id']}")
    check(p["summary"] in readme, f"README omits summary: {p['id']}")
    check(p["reading_depth"] in {"discovery", "targeted", "full_main_text"}, f"Invalid review label: {p['id']}")
    check(p["publication_status"] in {"published", "preprint", "workshop"}, f"Invalid publication status: {p['id']}")

expected = {p["local_pdf"] for p in papers if p["local_pdf"]}
actual = {str(p.relative_to(root)) for p in (root / "papers").rglob("*.pdf")}
check(expected == actual, "Unindexed or missing public PDF")
check({p["file"] for p in manifest} == expected, "PDF manifest coverage differs")
check(len(manifest) == len(expected), "Duplicate PDF manifest records")
for p in manifest:
    file = root / p["file"]
    if not file.exists():
        errors.append(f"Missing {p['file']}")
        continue
    content = file.read_bytes()
    check(content.startswith(b"%PDF-"), f"Invalid PDF header: {p['file']}")
    check(len(content) == p["bytes"], f"Size differs: {p['file']}")
    check(hashlib.sha256(content).hexdigest() == p["sha256"], f"Hash differs: {p['file']}")
    check(p["license"] in {"CC-BY-4.0", "CC0-1.0"}, f"Review mirror policy: {p['file']}")
    check(bool(p.get("license_evidence")), f"Missing licence evidence: {p['file']}")

for file in root.rglob("*.md"):
    text = file.read_text()
    for link in re.findall(r"\]\(([^)]+)\)", text):
        url = urlsplit(link.strip("<>"))
        if url.scheme or not url.path:
            continue
        target = (file.parent / unquote(url.path)).resolve()
        check(target.is_relative_to(root), f"Local link leaves repository: {file.name}: {link}")
        check(target.exists(), f"Broken local link: {file.name}: {link}")
    check("/Users/" not in text, f"Private local path in {file.name}")

if errors:
    raise SystemExit("\n".join(errors))
print(f"Validated {len(papers)} catalogue entries, {len(manifest)} PDF hashes, metadata coverage and local file links.")
print("External availability, research claims and SDK/hardware execution are separate checks.")
