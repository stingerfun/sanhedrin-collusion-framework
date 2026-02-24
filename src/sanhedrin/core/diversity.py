"""Effective diversity computation.
D_eff = M * (1 - rho_bar) * phi(G) for uniform correlation.
D_eff = M^2 / sum(Sigma) * phi(G) for heterogeneous correlation.
"""
import numpy as np
import networkx as nx
from typing import Optional

def topology_discount(G: nx.Graph, M: int) -> float:
    if M <= 1:
        return 1.0
    max_edges = M * (M - 1) / 2
    density = G.number_of_edges() / max_edges if max_edges > 0 else 0.0
    return max(0.01, 1.0 - density)

def effective_diversity(M: int, rho_bar: float, G: Optional[nx.Graph] = None) -> float:
    phi = topology_discount(G, M) if G is not None else 1.0
    return max(0.01, M * (1.0 - rho_bar) * phi)

def effective_diversity_from_correlation(Sigma: np.ndarray, G: Optional[nx.Graph] = None) -> float:
    M = Sigma.shape[0]
    total_corr = np.sum(Sigma)
    if total_corr < 1e-12:
        return float(M)
    D = M ** 2 / total_corr
    phi = topology_discount(G, M) if G is not None else 1.0
    return max(0.01, D * phi)

def build_block_correlation_matrix(family_sizes: list, rho_within: float = 0.7, rho_between: float = 0.15) -> np.ndarray:
    N = sum(family_sizes)
    Sigma = np.full((N, N), rho_between)
    idx = 0
    for size in family_sizes:
        Sigma[idx:idx + size, idx:idx + size] = rho_within
        idx += size
    np.fill_diagonal(Sigma, 1.0)
    eigvals, eigvecs = np.linalg.eigh(Sigma)
    eigvals = np.maximum(eigvals, 1e-6)
    Sigma = eigvecs @ np.diag(eigvals) @ eigvecs.T
    d = np.sqrt(np.diag(Sigma))
    Sigma = Sigma / np.outer(d, d)
    np.fill_diagonal(Sigma, 1.0)
    return Sigma
