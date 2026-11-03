#!/usr/bin/env python3
"""Read-only CSV structure/quality profiling with Python standard library.

WARNING: Keep generated profiles in the private task workspace. Field names,
paths and opt-in samples may expose information from confidential datasets.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import tempfile
from collections import Counter
from pathlib import Path


def analyze_csv(
    path: Path,
    *,
    encoding: str = "utf-8-sig",
    delimiter: str = ",",
    sample_values: int = 0,
    max_distinct: int = 10000,
    max_row_fingerprints: int = 200000,
) -> dict:
    """Read the CSV, without changing it; large-cardinality metrics are lower bounds."""
    if len(delimiter) != 1:
        raise ValueError("Delimiter must be one character (or 'tab' via CLI).")
    if sample_values < 0 or max_distinct < 1 or max_row_fingerprints < 1:
        raise ValueError("sample_values >= 0 and caps >= 1 are required")

    with path.open("r", encoding=encoding, newline="") as stream:
        rows = csv.reader(stream, delimiter=delimiter, strict=True)
        header = next(rows, None)
        if header is None:
            return {
                "file": str(path), "encoding": encoding, "delimiter": delimiter,
                "row_count": 0, "column_count": 0, "columns": [],
                "blank_header_positions": [], "duplicate_header_names": [],
                "rows_with_wrong_column_count": 0, "wrong_width_row_examples": [],
                "duplicate_normalized_rows_detected_lower_bound": 0,
                "duplicate_check_capped": False,
                "warnings": ["Empty CSV file (no header row)."],
                "limitations": ["No business or semantic validation performed."],
            }

        ncols = len(header)
        names = [h.strip() for h in header]
        name_counts = Counter(n for n in names if n)
        dup_names = sorted(n for n, count in name_counts.items() if count > 1)
        blanks = [i + 1 for i, n in enumerate(names) if not n]
        missing = [0] * ncols
        seen_values = [set() for _ in range(ncols)]
        distinct_capped = [False] * ncols
        seen_rows = set()
        duplicate_capped = False
        detected_duplicates = 0
        wrong_width_rows = 0
        wrong_width_examples = []
        row_count = 0

        for cells in rows:
            row_count += 1
            if len(cells) != ncols:
                wrong_width_rows += 1
                if len(wrong_width_examples) < 10:
                    wrong_width_examples.append({
                        "record_number": row_count,
                        "physical_line_number": rows.line_num,
                        "expected_fields": ncols,
                        "actual_fields": len(cells),
                    })

            normalized = [value.strip() for value in cells]
            fingerprint = hashlib.sha256(
                json.dumps(normalized, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            ).digest()
            if fingerprint in seen_rows:
                detected_duplicates += 1
            elif len(seen_rows) < max_row_fingerprints:
                seen_rows.add(fingerprint)
            else:
                duplicate_capped = True

            for idx in range(ncols):
                value = normalized[idx] if idx < len(normalized) else ""
                if value == "":
                    missing[idx] += 1
                elif value not in seen_values[idx]:
                    if len(seen_values[idx]) < max_distinct:
                        seen_values[idx].add(value)
                    else:
                        distinct_capped[idx] = True

    warnings = []
    if blanks:
        warnings.append("Blank column headers found; refer to column_index.")
    if dup_names:
        warnings.append("Repeated column header names found; refer to column_index.")
    if wrong_width_rows:
        warnings.append("Some rows do not match the header field count.")
    if duplicate_capped:
        warnings.append("Duplicate tracking cap reached: duplicate count is a lower bound.")
    if any(distinct_capped):
        warnings.append("Distinct tracking cap reached: some counts are lower bounds.")

    return {
        "file": str(path),
        "encoding": encoding,
        "delimiter": "\\t" if delimiter == "\t" else delimiter,
        "row_count": row_count,
        "column_count": ncols,
        "columns": [
            {
                "column_index": index + 1,
                "name": names[index],
                "missing_count": missing[index],
                "missing_rate": round(missing[index] / row_count, 6) if row_count else 0,
                "distinct_count_lower_bound": len(seen_values[index]),
                "distinct_check_capped": distinct_capped[index],
                **({"sample_values": sorted(seen_values[index])[:sample_values]}
                   if sample_values else {}),
            }
            for index in range(ncols)
        ],
        "blank_header_positions": blanks,
        "duplicate_header_names": dup_names,
        "rows_with_wrong_column_count": wrong_width_rows,
        "wrong_width_row_examples": wrong_width_examples,
        "duplicate_normalized_rows_detected_lower_bound": detected_duplicates,
        "duplicate_check_capped": duplicate_capped,
        "warnings": warnings,
        "limitations": [
            "Does not infer semantic types, outliers, key uniqueness, units or business validity.",
            "Duplicate rows compare trimmed cells; they are not raw-byte duplicates.",
            "Duplicate and distinct cardinality checks are capped to control memory.",
            "Wrong-width rows remain in row_count and are not silently removed.",
            "Source input is read-only; output may contain sensitive paths and headers.",
            "Sample values are omitted by default to reduce personal-data exposure.",
        ],
    }


def self_test() -> None:
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "sample.csv"
        path.write_text("id,name\n1,A\n2,\n2,\n3,C,extra\n4,D\n", encoding="utf-8")
        report = analyze_csv(path)
        assert report["row_count"] == 5, report
        assert report["column_count"] == 2, report
        assert report["duplicate_normalized_rows_detected_lower_bound"] == 1, report
        assert report["rows_with_wrong_column_count"] == 1, report
        assert report["columns"][1]["missing_count"] == 2, report
        assert all("sample_values" not in col for col in report["columns"]), report
        capped = analyze_csv(path, max_distinct=1, max_row_fingerprints=1)
        assert capped["columns"][0]["distinct_check_capped"] is True, capped
        assert capped["duplicate_check_capped"] is True, capped
        # The profiler never modifies the source.
        assert path.read_text(encoding="utf-8") == "id,name\n1,A\n2,\n2,\n3,C,extra\n4,D\n"
    print("SELF-TEST PASS: counts, missing, duplicates, widths, caps, privacy defaults, source preservation")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, nargs="?", help="source CSV (read only)")
    parser.add_argument("--out", type=Path, default=Path("outputs/data_profile.json"))
    parser.add_argument("--encoding", default="utf-8-sig")
    parser.add_argument("--delimiter", default=",", help="one character or 'tab'")
    parser.add_argument("--sample-values", type=int, default=0,
                        help="opt-in sensitive cell examples per column; default 0")
    parser.add_argument("--max-distinct", type=int, default=10000)
    parser.add_argument("--max-row-fingerprints", type=int, default=200000)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.csv_file is None:
        parser.error("csv_file is required unless --self-test is used")
    if not args.csv_file.is_file():
        parser.error(f"CSV does not exist: {args.csv_file}")
    if args.csv_file.resolve() == args.out.resolve():
        parser.error("Output path cannot be the same file as source CSV")
    delimiter = "\t" if args.delimiter == "tab" else args.delimiter
    try:
        report = analyze_csv(
            args.csv_file,
            encoding=args.encoding,
            delimiter=delimiter,
            sample_values=args.sample_values,
            max_distinct=args.max_distinct,
            max_row_fingerprints=args.max_row_fingerprints,
        )
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    except (ValueError, UnicodeError, csv.Error, OSError) as exc:
        parser.error(f"Cannot profile CSV: {exc}")
    print(f"Profile: {args.out}")
    print(f"rows={report['row_count']} columns={report['column_count']} "
          f"normalized_duplicate_rows_detected>={report['duplicate_normalized_rows_detected_lower_bound']} "
          f"wrong_width_rows={report['rows_with_wrong_column_count']}")
    if report["warnings"]:
        print("WARNINGS: " + "; ".join(report["warnings"]))


if __name__ == "__main__":
    main()
