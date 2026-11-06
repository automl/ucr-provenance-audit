#!/usr/bin/env python3
"""Cross-split value-identical duplicate check on the shipped data of every drafted dataset.

For each dataset: load the raw TRAIN and TEST files (variable length kept, NaNs kept),
hash every series (all channels, float64 bytes; NaN canonicalised), and report
  n_train, n_test, n_unique_total, n_duplicate_groups, group-size histogram,
  n_test_identical_to_train (test series whose exact values appear in train),
  n_test_dup_within_test, n_train_dup_within_train,
  n_label_mixed_groups (a duplicate group carrying more than one label),
  test_dup_class_counts (per-class count of test series identical to a train series).
Writes duplicates.csv.

Usage: python duplicates/duplicates_check.py [--cache DIR] [--names A B ...]
       (default: all 128 datasets of ../ucr_provenance_audit.csv; aeon downloads the data into DIR)
"""
import csv
import hashlib
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from aeon.datasets import load_classification

HERE = Path(__file__).resolve().parent
CACHE = Path(sys.argv[sys.argv.index("--cache") + 1]) if "--cache" in sys.argv else HERE / "data_cache"
OUT = HERE / "duplicates.csv"


def series_hash(x):
    a = np.ascontiguousarray(np.asarray(x, dtype=np.float64))
    a = np.where(np.isnan(a), np.float64(-1e300), a)  # canonical NaN so equal padding hashes equal
    return hashlib.blake2b(a.tobytes() + bytes(str(a.shape), "ascii"), digest_size=16).hexdigest()


def load(name, split):
    X, y = load_classification(name, split=split, extract_path=str(CACHE),
                               load_equal_length=False, load_no_missing=False)
    return X, np.asarray(y).astype(str)


def check(name):
    Xtr, ytr = load(name, "train")
    Xte, yte = load(name, "test")
    htr = [series_hash(x) for x in Xtr]
    hte = [series_hash(x) for x in Xte]
    groups = defaultdict(list)  # hash -> list of (split, idx, label)
    for i, (h, l) in enumerate(zip(htr, ytr)):
        groups[h].append(("train", i, l))
    for i, (h, l) in enumerate(zip(hte, yte)):
        groups[h].append(("test", i, l))
    dup_groups = {h: g for h, g in groups.items() if len(g) > 1}
    hist = Counter(len(g) for g in dup_groups.values())
    train_hashes = set(htr)
    test_identical = [i for i, h in enumerate(hte) if h in train_hashes]
    test_within = sum(1 for h, c in Counter(hte).items() if c > 1 for _ in range(c - 1))
    train_within = sum(1 for h, c in Counter(htr).items() if c > 1 for _ in range(c - 1))
    mixed = sum(1 for g in dup_groups.values() if len({l for _, _, l in g}) > 1)
    class_counts = Counter(yte[i] for i in test_identical)
    return {
        "name": name, "n_train": len(Xtr), "n_test": len(Xte),
        "n_unique_total": len(groups), "n_duplicate_groups": len(dup_groups),
        "group_size_histogram": ";".join(f"{k}:{v}" for k, v in sorted(hist.items())),
        "n_test_identical_to_train": len(test_identical),
        "frac_test_identical_to_train": round(len(test_identical) / len(Xte), 4),
        "n_test_dup_within_test": test_within, "n_train_dup_within_train": train_within,
        "n_label_mixed_groups": mixed,
        "test_dup_class_counts": ";".join(f"{k}:{v}" for k, v in sorted(class_counts.items())),
    }, sorted(test_identical)


def main():
    names = sys.argv[sys.argv.index("--names") + 1:] if "--names" in sys.argv else \
        sorted(pd.read_csv(HERE.parent / "ucr_provenance_audit.csv").dataset)
    rows = []
    for i, name in enumerate(names, 1):
        t0 = time.time()
        try:
            row, _ = check(name)
            rows.append(row)
            print(f"[{i}/{len(names)}] {name}: unique {row['n_unique_total']}/{row['n_train']+row['n_test']}, "
                  f"test=train {row['n_test_identical_to_train']}, mixed {row['n_label_mixed_groups']} "
                  f"({time.time()-t0:.0f}s)", flush=True)
        except Exception as e:  # noqa: BLE001
            rows.append({"name": name, "error": f"{type(e).__name__}: {e}"})
            print(f"[{i}/{len(names)}] {name}: FAILED {type(e).__name__}: {e}", flush=True)
    cols = ["name", "n_train", "n_test", "n_unique_total", "n_duplicate_groups", "group_size_histogram",
            "n_test_identical_to_train", "frac_test_identical_to_train", "n_test_dup_within_test",
            "n_train_dup_within_train", "n_label_mixed_groups", "test_dup_class_counts", "error"]
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
