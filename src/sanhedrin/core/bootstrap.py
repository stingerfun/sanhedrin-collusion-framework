"""Circular block bootstrap with Politis-White (2004) auto block length."""
import numpy as np
from typing import Tuple

try:
    import pandas as pd
    from arch.bootstrap import optimal_block_length as arch_obl
    HAS_ARCH = True
except ImportError:
    HAS_ARCH = False

def optimal_block_length(series: np.ndarray) -> int:
    T = len(series)
    if T < 10:
        return max(1, T // 3)
    if HAS_ARCH:
        try:
            result = arch_obl(pd.Series(series))
            b_cb = result['circular'].values[0]
            return max(1, int(np.round(b_cb)))
        except Exception:
            pass
    return max(1, int(T ** (1 / 3)))

def circular_block_bootstrap(series: np.ndarray, block_length: int, n_bootstrap: int = 10000, statistic: str = 'mean') -> np.ndarray:
    T = len(series)
    bl = min(block_length, T)
    n_blocks = int(np.ceil(T / bl))
    results = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        starts = np.random.randint(0, T, size=n_blocks)
        sample = np.concatenate([series[np.arange(s, s + bl) % T] for s in starts])[:T]
        results[i] = np.mean(sample) if statistic == 'mean' else np.var(sample)
    return results

def bootstrap_one_sided_test(observed_stat: float, series: np.ndarray, null_value: float, n_bootstrap: int = 10000, alpha: float = 0.05) -> Tuple[bool, float]:
    bl = optimal_block_length(series)
    centered = series - np.mean(series) + null_value
    boot_dist = circular_block_bootstrap(centered, bl, n_bootstrap)
    p_value = np.mean(boot_dist >= observed_stat)
    return p_value < alpha, float(p_value)
