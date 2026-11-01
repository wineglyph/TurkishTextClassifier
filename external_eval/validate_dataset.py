#!/usr/bin/env python3
"""Non-destructive integrity and source-overlap validator for this evaluation CSV."""
from __future__ import annotations
import argparse, ast, csv, json, re, unicodedata
from collections import Counter
from pathlib import Path

EXPECTED_LABELS = {"Soru", "Şikâyet", "Öneri"}
EXPECTED_CLASSES = {"Soru": 150, "Şikâyet": 150, "Öneri": 150}
EXPECTED_TOTAL = 450
EXPECTED_COLUMNS = ["id", "text", "gold_label", "domain", "writing_style", "synthetic"]
EXPECTED_DOMAINS = {
    "E-ticaret", "Bankacılık ve finans", "Telekomünikasyon", "Yazılım ve mobil uygulamalar",
    "Ulaşım", "Sağlık hizmetleri", "Belediye hizmetleri", "Eğitim", "Kargo ve lojistik",
    "Restoran ve konaklama"
}
EXPECTED_STYLES = {
    "Resmî / kurumsal", "Günlük konuşma", "Kısa ve doğrudan", "Ayrıntılı anlatım", "Yazım varyasyonlu"
}
TR_LOWER = str.maketrans({"I": "ı", "İ": "i"})

def normalize(text: str) -> str:
    text = text.translate(TR_LOWER).lower()
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"([!?.,])\1+", r"\1", text)
    text = re.sub(r"[^\w\s!?.,]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def punctuationless(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[!?.,]+", " ", normalize(text))).strip()

def read_original_texts(root: Path) -> list[str]:
    texts: list[str] = []
    for rel in ("data/turkish_text_dataset.csv", "data/train.csv", "data/test.csv"):
        p = root / rel
        if p.exists():
            with p.open("r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames and "text" in reader.fieldnames:
                    texts.extend(row.get("text", "") for row in reader if row.get("text"))
    p = root / "data/turkish_text_dataset.jsonl"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                obj = json.loads(line)
                if isinstance(obj, dict) and isinstance(obj.get("text"), str):
                    texts.append(obj["text"])
    for rel in ("test_samples_20.json", "artifacts/reports/manual_test_results.json"):
        p = root / rel
        if p.exists():
            obj = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(obj, list):
                texts.extend(x["text"] for x in obj if isinstance(x, dict) and isinstance(x.get("text"), str))
            elif isinstance(obj, dict):
                texts.extend(x["text"] for x in obj.get("sample_evaluations", []) if isinstance(x, dict) and isinstance(x.get("text"), str))
    # Read the original hand-curated generator examples without executing project code.
    p = root / "src/dataset/generate_dataset.py"
    if p.exists():
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CURATED_EXAMPLES" for t in node.targets):
                curated = ast.literal_eval(node.value)
                texts.extend(x["text"] for x in curated if isinstance(x, dict) and isinstance(x.get("text"), str))
    return texts

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, default=Path(__file__).with_name("synthetic_test.csv"))
    ap.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1], help="Original project root; source overlap is checked when available.")
    args = ap.parse_args()
    errors: list[str] = []
    warnings: list[str] = []
    try:
        args.csv.read_bytes().decode("utf-8")
        with args.csv.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames or []
            rows = list(reader)
    except Exception as exc:
        print(f"FAIL: CSV UTF-8/readability: {exc}")
        return 2
    if fields != EXPECTED_COLUMNS:
        errors.append(f"Unexpected columns: {fields}")
    if len(rows) != EXPECTED_TOTAL:
        errors.append(f"Expected {EXPECTED_TOTAL} data rows, found {len(rows)}")
    labels = Counter(r.get("gold_label", "") for r in rows)
    if dict(labels) != EXPECTED_CLASSES:
        errors.append(f"Class distribution mismatch: {dict(labels)}")
    if any(not (r.get("text") or "").strip() for r in rows):
        errors.append("Empty text field found")
    if any(not (r.get("id") or "").strip() for r in rows):
        errors.append("Empty ID field found")
    if any(r.get("gold_label") not in EXPECTED_LABELS for r in rows):
        errors.append("Unexpected label value found")
    if any(r.get("synthetic", "").strip().lower() != "true" for r in rows):
        errors.append("One or more records are not marked synthetic=true")
    ids = [r.get("id", "") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate IDs found")
    normalized = [normalize(r.get("text", "")) for r in rows]
    punctless = [punctuationless(r.get("text", "")) for r in rows]
    if len(normalized) != len(set(normalized)):
        errors.append("Exact duplicates after project normalization found")
    if len(punctless) != len(set(punctless)):
        errors.append("Duplicates after punctuation/whitespace normalization found")
    domains = Counter(r.get("domain", "") for r in rows)
    styles = Counter(r.get("writing_style", "") for r in rows)
    if set(domains) != EXPECTED_DOMAINS or any(v != 45 for v in domains.values()):
        errors.append(f"Domain distribution mismatch: {dict(domains)}")
    if set(styles) != EXPECTED_STYLES or any(v != 90 for v in styles.values()):
        errors.append(f"Writing-style distribution mismatch: {dict(styles)}")
    # Pattern-based PII scan only; a zero result is not proof of privacy in every possible format.
    patterns = {
        "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "Turkish phone": re.compile(r"(?<!\d)(?:\+?90\s*)?(?:0\s*)?(?:5\d{2}|[2-4]\d{2})[\s().-]*\d{3}[\s.-]*\d{2}[\s.-]*\d{2}(?!\d)"),
        "long numeric identifier": re.compile(r"(?<!\d)\d{10,}(?!\d)"),
        "IBAN": re.compile(r"\bTR\d{24}\b", re.I),
    }
    for name, pat in patterns.items():
        hits = [r.get("id", "") for r in rows if pat.search(r.get("text", ""))]
        if hits:
            warnings.append(f"Possible {name} pattern in record IDs: {hits}")
    if args.project_root.exists():
        originals = read_original_texts(args.project_root)
        original_norm = {normalize(t) for t in originals if normalize(t)}
        original_punct = {punctuationless(t) for t in originals if punctuationless(t)}
        exact = [r["id"] for r in rows if normalize(r["text"]) in original_norm]
        punct = [r["id"] for r in rows if punctuationless(r["text"]) in original_punct]
        if exact:
            errors.append(f"Original normalized overlap found in IDs: {exact}")
        if punct:
            errors.append(f"Original punctuation-insensitive overlap found in IDs: {punct}")
        print(f"Original source entries checked: {len(originals)}; unique normalized references: {len(original_norm)}; exact overlaps={len(exact)}; punctuation-insensitive overlaps={len(punct)}")
    else:
        warnings.append("Original project root unavailable; source-overlap check skipped")
    print(f"CSV: {args.csv}")
    print(f"UTF-8: PASS | rows={len(rows)} | columns={fields}")
    print(f"Class distribution: {dict(labels)}")
    print(f"Domain distribution: {dict(domains)}")
    print(f"Writing-style distribution: {dict(styles)}")
    print(f"Exact duplicates after project normalization: {len(normalized) - len(set(normalized))}")
    print(f"Duplicates after punctuation/whitespace normalization: {len(punctless) - len(set(punctless))}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"VALIDATION FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"VALIDATION PASSED: {len(rows)} rows, balanced classes/domains/styles, no exact duplicates, no confirmed source overlap; {len(warnings)} warning(s)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
