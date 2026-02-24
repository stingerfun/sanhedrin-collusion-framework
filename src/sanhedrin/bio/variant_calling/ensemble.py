"""Ensemble variant calling strategies.

Supports:
- Majority vote (k-of-M)
- Union (any caller)
- Intersection (all callers)
- Weighted vote (by individual F1)
"""

import numpy as np
from typing import Dict, List, Set
from collections import Counter


def majority_vote(
    call_sets: Dict[str, set],
    threshold: int | None = None,
) -> set:
    """Majority vote ensemble: keep variants called by >= threshold callers.

    Default threshold: ceil(M/2).
    """
    M = len(call_sets)
    if threshold is None:
        threshold = (M + 1) // 2

    counts: Counter = Counter()
    for variants in call_sets.values():
        for v in variants:
            counts[v] += 1

    return {v for v, c in counts.items() if c >= threshold}


def union_vote(call_sets: Dict[str, set]) -> set:
    """Union: keep any variant called by at least one caller."""
    result: set = set()
    for variants in call_sets.values():
        result |= variants
    return result


def intersection_vote(call_sets: Dict[str, set]) -> set:
    """Intersection: keep only variants called by all callers."""
    sets = list(call_sets.values())
    if not sets:
        return set()
    result = sets[0].copy()
    for s in sets[1:]:
        result &= s
    return result


def evaluate_ensemble(
    ensemble_calls: set,
    truth_set: set,
) -> Dict[str, float]:
    """Evaluate ensemble against truth set.

    Returns precision, recall, F1.
    """
    tp = len(ensemble_calls & truth_set)
    fp = len(ensemble_calls - truth_set)
    fn = len(truth_set - ensemble_calls)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {"precision": precision, "recall": recall, "f1": f1, "tp": tp, "fp": fp, "fn": fn}
