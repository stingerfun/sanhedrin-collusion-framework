"""Compute inter-caller correlation from VCF call sets.

Estimates rho_ij between variant callers using:
- Jaccard similarity on variant call sets
- Cohen's kappa on per-site agreement

These serve as the empirical correlation matrix for D_eff computation.
"""

import numpy as np
from typing import Dict, List, Set, Tuple
from pathlib import Path
import warnings

try:
    from cyvcf2 import VCF
    HAS_CYVCF2 = True
except ImportError:
    HAS_CYVCF2 = False
    warnings.warn("cyvcf2 not installed. Install with: pip install cyvcf2")


def load_variant_positions(vcf_path: str | Path,
                           min_qual: float = 0.0,
                           pass_only: bool = True) -> Set[Tuple[str, int, str, str]]:
    """Load variant positions from VCF as set of (chrom, pos, ref, alt)."""
    if not HAS_CYVCF2:
        raise ImportError("cyvcf2 required for VCF parsing")

    variants = set()
    for v in VCF(str(vcf_path)):
        if pass_only and v.FILTER is not None:
            continue
        if v.QUAL is not None and v.QUAL < min_qual:
            continue
        for alt in v.ALT:
            variants.add((v.CHROM, v.POS, v.REF, alt))
    return variants


def jaccard_similarity(set_a: set, set_b: set) -> float:
    """Jaccard similarity: |A ∩ B| / |A ∪ B|."""
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def compute_correlation_matrix(
    vcf_paths: Dict[str, str | Path],
    min_qual: float = 0.0,
    pass_only: bool = True,
    method: str = "jaccard",
) -> Tuple[np.ndarray, List[str]]:
    """Compute pairwise correlation matrix from variant caller VCFs.

    Parameters
    ----------
    vcf_paths : dict
        Mapping of caller name -> VCF file path.
    method : str
        'jaccard' (default) or 'kappa'.

    Returns
    -------
    rho : np.ndarray
        M x M correlation matrix.
    caller_names : list[str]
        Ordered list of caller names.
    """
    caller_names = sorted(vcf_paths.keys())
    M = len(caller_names)

    # Load all call sets
    call_sets = {}
    for name in caller_names:
        call_sets[name] = load_variant_positions(
            vcf_paths[name], min_qual=min_qual, pass_only=pass_only
        )

    rho = np.eye(M)
    for i in range(M):
        for j in range(i + 1, M):
            if method == "jaccard":
                sim = jaccard_similarity(
                    call_sets[caller_names[i]],
                    call_sets[caller_names[j]],
                )
            else:
                raise ValueError(f"Unknown method: {method}")
            rho[i, j] = sim
            rho[j, i] = sim

    return rho, caller_names
