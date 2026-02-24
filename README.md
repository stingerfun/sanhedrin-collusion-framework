# 🏛️ Sanhedrin Collusion Framework

**Effective Diversity and Collusion Risk in Multi-Agent Bioinformatics:
A Game-Theoretic Framework for Ensemble Consensus Auditing**

> Sapielkin, S. (2026). Weizmann Institute of Science.

[![CI](https://github.com/stingerfun/sanhedrin-collusion-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/stingerfun/sanhedrin-collusion-framework/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## The Problem

When multiple computational tools agree, does their consensus reflect **independent evidence** — or **correlated biases**?

- Ensemble variant callers combine 4–13 tools under majority vote — but performance **plateaus or degrades** beyond 6 tools ([Guille et al., 2025](https://doi.org/10.1093/bib/bbae697))
- Multi-agent LLM systems for protein design (ProtAgents, BioAgents) share a common backbone — agents may **converge without independent validation**
- The Condorcet Jury Theorem promises that larger ensembles improve accuracy — **but only under independence assumptions** that are systematically violated

**Nobody has a formal theory explaining why.**

## Our Solution: Effective Diversity

We introduce **D_eff** — a theory-grounded metric for ensemble reliability:

```
D_eff = M² / Σᵢⱼ ρᵢⱼ × φ(G)
```

where:
- `M` = number of tools in the ensemble
- `ρᵢⱼ` = pairwise correlation between tools i and j
- `φ(G)` = topology discount from communication structure

**Key insight:** Adding a 7th GATK-family variant caller barely increases D_eff, because it shares algorithmic ancestry (high ρ) with existing GATK callers. Adding a FreeBayes or Strelka2 caller increases D_eff substantially.

## What This Framework Provides

| Component | What It Does |
|-----------|-------------|
| **D_eff Calculator** | Computes effective diversity from inter-tool correlation matrix |
| **M\* Optimizer** | Finds optimal ensemble size via loss function minimization |
| **Collusion Risk R_coll** | Detects phase transitions where multi-agent coordination becomes possible |
| **Bootstrap Auditing** | Circular block bootstrap tests for consensus validation (Politis-White 2004) |
| **Variant Calling Module** | Computes ρ from VCF call sets, sweeps all 2^M subsets, validates D_eff → F1 |

## Bioinformatics Applications

### 1. Ensemble Variant Calling

**Problem:** [Guille et al., 2025] tested 8,178 combinations of 15 somatic variant callers. Performance peaked at 4–6 callers, then degraded. Why?

**Our answer:** Tools sharing GATK ancestry have high ρ (~0.7). D_eff saturates at M=4–6 regardless of nominal count.

```python
from sanhedrin.core.diversity import effective_diversity_from_correlation
import numpy as np

# Real correlation matrix: 3 GATK-family + 2 independent callers
rho = np.array([
    [1.0, 0.8, 0.7, 0.2, 0.3],  # Mutect2
    [0.8, 1.0, 0.6, 0.2, 0.3],  # HaplotypeCaller
    [0.7, 0.6, 1.0, 0.3, 0.2],  # DeepVariant
    [0.2, 0.2, 0.3, 1.0, 0.3],  # Strelka2
    [0.3, 0.3, 0.2, 0.3, 1.0],  # FreeBayes
])

D_eff = effective_diversity_from_correlation(rho)
print(f"Effective diversity: {D_eff:.2f} out of {len(rho)} nominal tools")
# → Effective diversity: 2.83 out of 5 tools
```

### 2. Multi-Agent Protein Design

**Problem:** ProtAgents assigns 4 LLM agents to protein design. If all agents use GPT-4o, they share biases.

**Our answer:** Enforce heterogeneous backbones (GPT-4o + Claude + Gemini) + randomize role assignments.

```python
from sanhedrin.core.optimizer import optimize_ensemble_size

# Clinical genomics: high stakes, moderate uncertainty
M_star = optimize_ensemble_size(
    E=0.6,        # Epistemic uncertainty
    S=0.8,        # Social criticality (clinical = high)
    rho_bar=0.45, # Average inter-tool correlation
    p=0.0,        # No inter-tool communication
)
print(f"Recommended ensemble size: {M_star}")
```

### 3. Automated Bio Pipelines

**Problem:** BioMaster / BioAgents orchestrate multi-step genomic pipelines. Correlated errors cascade.

**Our answer:** Monitor agreement patterns across pipeline steps. Flag suspicious unanimity.

## Installation

```bash
git clone https://github.com/stingerfun/sanhedrin-collusion-framework.git
cd sanhedrin-collusion-framework
pip install -e ".[dev]"

# For bioinformatics experiments:
pip install -e ".[bio]"

# For protein design experiments:
pip install -e ".[protein]"

# Everything:
pip install -e ".[all]"
```

## Project Structure

```
src/sanhedrin/
├── core/                      # Theory
│   ├── config.py              # Master configuration
│   ├── diversity.py           # D_eff computation
│   ├── collusion_risk.py      # R_coll, phase transitions
│   ├── optimizer.py           # M* via L_total optimization
│   └── bootstrap.py           # Politis-White block bootstrap
│
├── games/                     # Game-theoretic simulations
│   ├── cournot.py             # Cournot oligopoly (competitive)
│   ├── dcop.py                # Graph coloring (cooperative)
│   └── stego.py               # Steganographic channel (covert)
│
├── agents/                    # Agent strategies
│   ├── gaussian_copula.py     # Correlated random agents
│   ├── q_learning.py          # Tabular Q-learning
│   ├── trigger_strategy.py    # Grim trigger
│   └── best_response.py       # Myopic best response
│
├── bio/                       # Bioinformatics applications
│   ├── variant_calling/       # VCF analysis, ensemble sweep
│   ├── protein_design/        # ProtAgents wrapper, diversity metrics
│   └── meta_analysis/         # Re-analysis of published benchmarks
│
└── viz/                       # Paper figures
```

## Experiments

| # | Experiment | Data | Cost |
|---|-----------|------|------|
| 01 | Monte Carlo simulations (625 configs × 1000 trials) | Synthetic | $0 |
| 02 | Variant calling ensemble (7 callers on GIAB HG002) | [GIAB](https://www.nist.gov/programs-projects/genome-bottle) | $0 |
| 03 | Protein design (ProtAgents homo/hetero/Sanhedrin) | [ProtAgents](https://github.com/lamm-mit/ProtAgents) | ~$100 API |
| 04 | Meta-analysis (re-analysis of 8,178 caller combos) | [Guille et al.](https://doi.org/10.1093/bib/bbae697) | $0 |

Reproduce everything:

```bash
snakemake --cores 8
```

## Comparison with Existing Approaches

| Framework | Handles Correlation? | Optimal M Theory? | Collusion Audit? |
|-----------|---------------------|-------------------|-----------------|
| Simple majority vote | ✗ | ✗ | ✗ |
| SomaticSeq | Partial (learned weights) | ✗ | ✗ |
| BAYSIC | Partial (Bayesian) | ✗ | ✗ |
| Ensemble (Guille et al.) | Empirical only | Empirical only | ✗ |
| **Sanhedrin (this work)** | **✓ D_eff theory** | **✓ L_total optimization** | **✓ R_coll + bootstrap** |

## Key Theoretical Results

1. **Effective Diversity Bound (Corollary 7):** D_eff saturates when tools share algorithmic ancestry, explaining the empirical 4–6 caller optimum.
2. **Phase Transition (Theorem 4):** Collusion risk jumps at percolation threshold p_c = 1/(M−1).
3. **Folk Theorem for Model Councils (Theorem 5):** Repeated interaction + shared backbone → tacit coordination is sustainable when δ > δ_crit.
4. **High-Stakes Paradox (Corollary 8):** Domains requiring the most reliability are most vulnerable to correlated consensus.

## Citation

```bibtex
@article{sapielkin2026sanhedrin_collusion,
  title={Effective Diversity and Collusion Risk in Multi-Agent Bioinformatics:
         A Game-Theoretic Framework for Ensemble Consensus Auditing},
  author={Sapielkin, Shaul},
  journal={Preprint},
  year={2026},
  institution={Weizmann Institute of Science}
}
```

## License

MIT License. See [LICENSE](LICENSE).
