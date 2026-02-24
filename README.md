# 🏛️ Sanhedrin Collusion Framework

**Effective Diversity and Collusion Risk in Multi-Agent Bioinformatics:
A Game-Theoretic Framework for Ensemble Consensus Auditing**

> Sapielkin, S. (2026). Weizmann Institute of Science.

[![Status: Development](https://img.shields.io/badge/status-development-yellow)](https://github.com/stingerfun/sanhedrin-collusion-framework)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🚧 Project Status

**This repository is under active development.**

- ✅ Core mathematical library implemented and unit tested
- ✅ Game-theoretic simulation framework complete
- 🔄 Bioinformatics experiments in progress
- 📝 Manuscript in preparation
- 🎯 Target: PNAS / Nature Communications

### Reproducibility Roadmap

| Experiment | Data Source | Status | ETA |
|-----------|------------|--------|-----|
| **01. Monte Carlo** | Synthetic (625 configs × 1000 trials) | Ready to run | Week 6 |
| **02. Variant Calling** | [GIAB HG002](https://www.nist.gov/programs-projects/genome-bottle) (7 callers) | Setup in progress | Week 2-3 |
| **03. Protein Design** | [ProtAgents](https://github.com/lamm-mit/ProtAgents) benchmark | Planned | Week 4 |
| **04. Meta-analysis** | [Guille et al., 2025](https://doi.org/10.1093/bib/bbae697) (8,178 combos) | Planned | Week 5 |

**Current focus:** Variant calling experiment on GIAB truth set (Experiment 02).

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
| **M* Optimizer** | Finds optimal ensemble size via loss function minimization |
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

# Example correlation matrix: 3 GATK-family + 2 independent callers
# (Synthetic data for illustration — real experiment in progress)
rho = np.array([
    [1.0, 0.8, 0.7, 0.2, 0.3],  # Mutect2
    [0.8, 1.0, 0.6, 0.2, 0.3],  # HaplotypeCaller
    [0.7, 0.6, 1.0, 0.3, 0.2],  # DeepVariant
    [0.2, 0.2, 0.3, 1.0, 0.3],  # Strelka2
    [0.3, 0.3, 0.2, 0.3, 1.0],  # FreeBayes
])

D_eff = effective_diversity_from_correlation(rho)
print(f"Effective diversity: {D_eff:.2f} out of {len(rho)} nominal tools")
# → Effective diversity: ~2.8 out of 5 tools (illustrative)
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
# → Typical output: M* = 7-9 for these parameters
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

**Requirements:** Python 3.10+, see `pyproject.toml` for dependencies.

## Quick Start

### Compute Effective Diversity

```python
from sanhedrin.core.diversity import effective_diversity
import numpy as np

# 5 tools with average correlation 0.4
D_eff = effective_diversity(M=5, rho_bar=0.4)
print(f"D_eff = {D_eff:.2f}")  # → ~3.0

# Independent tools (rho_bar = 0)
D_eff_indep = effective_diversity(M=5, rho_bar=0.0)
print(f"D_eff (independent) = {D_eff_indep:.2f}")  # → 5.0
```

### Optimize Ensemble Size

```python
from sanhedrin.core.optimizer import optimize_ensemble_size

M_star = optimize_ensemble_size(
    E=0.5,        # Moderate uncertainty
    S=0.6,        # Moderate criticality
    rho_bar=0.3,  # Low-moderate correlation
    p=0.0,        # No communication topology
)
print(f"Optimal M* = {M_star}")
```

### Run Unit Tests

```bash
pytest tests/ -v
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

## Planned Experiments

### Experiment 02: Variant Calling Ensemble (GIAB HG002)

**Goal:** Validate that D_eff predicts optimal ensemble size from real variant caller correlations.

**Data:** [GIAB HG002 truth set v4.2.1](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/GRCh38/) (public)

**Callers:**
- GATK family: Mutect2, HaplotypeCaller, DeepVariant
- Independent: Strelka2, FreeBayes, Octopus
- Deep learning: Clair3

**Plan:**
1. Run all 7 callers on HG002 (30X WGS)
2. Compute ρ_ij from Jaccard similarity on call sets
3. Sweep all 2^7 - 1 = 127 subsets
4. Show: D_eff strongly correlates with ensemble F1
5. Show: Optimal M* ≈ 4-6 from D_eff matches empirical optimum

**Status:** Setup in progress (Week 2-3)

### Experiment 03: Protein Design Convergence

**Goal:** Demonstrate that homogeneous LLM agents converge; heterogeneous + randomization increases diversity.

**Data:** [ProtAgents benchmark](https://github.com/lamm-mit/ProtAgents) (10 design tasks)

**Conditions:**
- Homogeneous: 4 × GPT-4o agents
- Heterogeneous: GPT-4o + Claude + Gemini + GPT-4o
- Sanhedrin: Heterogeneous + randomized role assignments

**Metrics:** Structural diversity (RMSD), novelty (TM-score to PDB), pLDDT

**Status:** Planned (Week 4)

### Experiment 04: Meta-Analysis of Published Data

**Goal:** Re-analyze [Guille et al., 2025] data (8,178 caller combinations) to fit D_eff → F1 relationship.

**Data:** Supplementary Table S4 from [DOI:10.1093/bib/bbae697](https://doi.org/10.1093/bib/bbae697)

**Plan:**
1. Extract F1 for all 8,178 combinations
2. Estimate ρ matrix from pairwise agreement
3. Compute D_eff for each combination
4. Fit regression: F1 ~ D_eff
5. Show: D_eff explains performance plateau

**Status:** Planned (Week 5)

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

## Contributing

This is an active research project. Contributions, feedback, and collaboration inquiries are welcome:

- 📧 Email: shaul.sapielkin@weizmann.ac.il
- 🐛 Issues: [GitHub Issues](https://github.com/stingerfun/sanhedrin-collusion-framework/issues)
- 📝 Pull requests welcome (see `CONTRIBUTING.md` — coming soon)

## Citation

**Preprint in preparation.** Please cite as:

```bibtex
@misc{sapielkin2026sanhedrin_collusion,
  title={Effective Diversity and Collusion Risk in Multi-Agent Bioinformatics:
         A Game-Theoretic Framework for Ensemble Consensus Auditing},
  author={Sapielkin, Shaul},
  year={2026},
  note={Manuscript in preparation},
  institution={Weizmann Institute of Science},
  url={https://github.com/stingerfun/sanhedrin-collusion-framework}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.

---

**Acknowledgments:** This work builds on the Sanhedrin Architecture framework ([Sapielkin, 2026](https://github.com/stingerfun)) and draws on econometric cartel detection methods, evolutionary game theory, and bioinformatics benchmarking literature.
