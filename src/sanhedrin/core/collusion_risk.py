"""Collusion risk: R_coll = f_topology * f_repetition * f_stakes."""
import numpy as np
import networkx as nx
from .config import SimConfig

def f_topology(G: nx.Graph, M: int, cfg: SimConfig) -> float:
    if M <= 1:
        return 0.0
    max_edges = M * (M - 1) / 2
    edge_density = G.number_of_edges() / max_edges if max_edges > 0 else 0.0
    try:
        clustering = nx.average_clustering(G)
    except Exception:
        clustering = 0.0
    return min(1.0, cfg.alpha_edge * edge_density + cfg.alpha_clust * clustering)

def f_repetition(T: int, delta: float, cfg: SimConfig) -> float:
    if delta < cfg.delta_crit:
        return 0.0
    g_delta = ((delta - cfg.delta_crit) / (1.0 - cfg.delta_crit)) ** 2
    h_T = 1.0 - np.exp(-T / cfg.T_stab)
    return g_delta * h_T

def f_stakes(S: float, cfg: SimConfig) -> float:
    if S < cfg.S_min:
        return 0.0
    return (S - cfg.S_min) ** cfg.gamma_stakes

def compute_collusion_risk(M: int, G: nx.Graph, T: int, delta: float, S: float, cfg: SimConfig) -> float:
    return f_topology(G, M, cfg) * f_repetition(T, delta, cfg) * f_stakes(S, cfg)

def percolation_threshold(M: int) -> float:
    return 1.0 / max(M - 1, 1)
