"""Master configuration for simulations and experiments."""
from dataclasses import dataclass, field
from typing import List
from enum import Enum

class DomainType(Enum):
    I = "Established"
    II = "Procedural"
    III = "Contested"
    IV = "Insufficient"

class AgentStrategy(Enum):
    GAUSSIAN_COPULA = "gaussian_copula"
    Q_LEARNING = "q_learning"
    TRIGGER = "trigger_strategy"
    BEST_RESPONSE = "myopic_best_response"

@dataclass
class SimConfig:
    E_vals: List[float] = field(default_factory=lambda: [0.2, 0.4, 0.6, 0.8, 1.0])
    S_vals: List[float] = field(default_factory=lambda: [0.2, 0.4, 0.6, 0.8, 1.0])
    rho_vals: List[float] = field(default_factory=lambda: [0.1, 0.3, 0.5, 0.7, 0.9])
    p_vals: List[float] = field(default_factory=lambda: [0.0, 0.1, 0.2, 0.3, 0.5])
    T_vals: List[int] = field(default_factory=lambda: [1, 5, 10, 20, 50])
    N: int = 20
    M_max: int = 15
    M_min: int = 3
    n_trials: int = 1000
    n_families: int = 4
    family_sizes: List[int] = field(default_factory=lambda: [5, 5, 5, 5])
    rho_within: float = 0.7
    rho_between: float = 0.15
    alpha_edge: float = 0.7
    alpha_clust: float = 0.3
    delta_crit: float = 0.6
    T_stab: float = 5.0
    S_min: float = 0.2
    gamma_stakes: float = 1.5
    a: float = 100.0
    b: float = 1.0
    c_marginal: float = 10.0
    ql_alpha: float = 0.15
    ql_gamma_discount: float = 0.95
    ql_epsilon_start: float = 1.0
    ql_epsilon_end: float = 0.01
    ql_epsilon_decay: float = 0.995
    ql_n_actions: int = 15
    c_inf: float = 1.0
    c_synth: float = 0.5
    mu_cost: float = 0.05
    nu_trust: float = 0.1
    sigma_trust: float = 3.0
    lambda_coll: float = 1.0
    B: int = 10_000
    alpha_test: float = 0.05
    delta_mean: float = 0.7
    delta_std: float = 0.1
    context_window_factor: float = 0.1
    tau1: float = 0.25
    tau2: float = 0.55
    tau3: float = 0.80
    output_dir: str = "results"
    n_jobs: int = -1
    verbose: int = 1

    @property
    def n_configs(self) -> int:
        return len(self.E_vals) * len(self.S_vals) * len(self.rho_vals) * len(self.p_vals)
