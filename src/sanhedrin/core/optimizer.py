"""Full L_total optimization for M*."""
import numpy as np
import networkx as nx
from .config import SimConfig
from .diversity import effective_diversity
from .collusion_risk import compute_collusion_risk

def L_error(M, sigma2, rho_bar, G):
    D = effective_diversity(M, rho_bar, G)
    return sigma2 / D

def L_cost(M, cfg):
    return cfg.mu_cost * (M * cfg.c_inf + cfg.c_synth * M * np.log(M + 1))

def L_trust(M, M_target, cfg):
    return cfg.nu_trust * np.exp(-((M - M_target) ** 2) / (2 * cfg.sigma_trust ** 2))

def L_coll(M, G, T, delta, S, cfg):
    return cfg.lambda_coll * compute_collusion_risk(M, G, T, delta, S, cfg)

def optimize_ensemble_size(E=0.5, S=0.5, rho_bar=0.3, p=0.0, T=10, delta=0.7, cfg=None, sigma2=1.0, enforce_odd=True):
    if cfg is None:
        cfg = SimConfig()
    M_target = cfg.M_min + int(4 * E / (1 - rho_bar + 0.01)) + int(4 * S * (1 + E))
    best_M, best_loss = cfg.M_min, float('inf')
    for M in range(cfg.M_min, cfg.M_max + 1):
        G = nx.erdos_renyi_graph(M, min(p, 0.99), seed=42)
        loss = L_error(M, sigma2, rho_bar, G) + L_cost(M, cfg) - L_trust(M, M_target, cfg) + L_coll(M, G, T, delta, S, cfg)
        if loss < best_loss:
            best_loss = loss
            best_M = M
    if enforce_odd and best_M % 2 == 0:
        best_M = min(best_M + 1, cfg.M_max)
    return best_M
