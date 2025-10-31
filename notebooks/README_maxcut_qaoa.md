# Max-Cut Approximation Experiments using QAOA on IBM Quantum Hardware

## Overview

This notebook explores **approximate solutions to the Max-Cut problem** using both **classical** and **quantum** approaches.  
The primary objective is to test whether a commercially available quantum computer — specifically an **IBM Quantum backend** — can deliver a *practical advantage* over classical heuristics on small- to mid-scale graph instances.

The project was motivated by recent announcements from **Google Quantum AI** reporting another “quantum advantage” milestone.  
Given that Google’s *Willow* chip is not publicly accessible, the next best option was to reproduce a similar test on **IBM’s public superconducting devices** and compare their QAOA-based performance to classical approximations on a standard laptop.

---

## Goals

- Evaluate **quantum approximate optimization (QAOA)** for the Max-Cut problem under realistic conditions.  
- Compare **quantum** and **classical** approximation performance in terms of:
  - Cut quality (approximation ratio or direct cut value)
  - Execution time (simulator vs. hardware vs. classical baselines)
- Measure the scaling behavior of each method as the number of nodes grows.
- Assess the practicality of near-term QAOA hardware runs.

---

## Algorithms Implemented

| Category | Algorithm | Description |
|-----------|------------|-------------|
| **Classical** | Brute-force (exact) | Exhaustive search; used only for small graphs (≤ 20 nodes) as ground truth. |
|  | Random cut | Baseline heuristic (uniform random bit assignment). |
|  | Local search (greedy hill-climb) | Simple classical approximation benchmark. |
| **Quantum (simulated)** | QAOA (p = 1) | Standard one-layer quantum approximation algorithm. |
| **Quantum (hardware)** | QAOA (p = 1) on IBM device | Same circuit transpiled and executed via IBM Runtime (`SamplerV2`), using automatic transpilation and noise-aware backend mapping. |

---

## Design Choices and Assumptions

- **Graph model:** Undirected, integer-weighted, generated via `networkx` with configurable vertex count and edge probability.  
- **Library:** Custom `graphlib.py` built on `networkx`, `matplotlib`, and `qiskit`.  
- **Visualization:** Matplotlib with Seaborn theme; includes error bars (mean ± SEM) for statistical clarity.  
- **Environment:** Developed in **VS Code** with **Jupyter** notebooks. Dependencies are listed in `qaoa_env.yml`.  
- **Simulation backend:** Qiskit Aer for noiseless classical simulation.  
- **Hardware backend:** Smallest operational IBM Quantum system available at runtime.  
- **Shots:** 512 per QAOA execution.  
- **QAOA depth:** Fixed at p = 1 for clarity and speed.  
- **Parameter optimization:** Classical analytic expectation-based search (`optimize_qaoa1_classical`); not hybrid hardware-in-the-loop.  
- **Runtime measurement:** All timing captured in notebooks (not inside the library), including parameter optimization and quantum execution.  

---

## Notebook Organization

1. **Graph library (`graphlib.py`)**  
   - Core graph data structures  
   - Random graph generation  
   - Classical and quantum Max-Cut solvers  
   - IBM Runtime integration (`SamplerV2`, automatic transpilation)  

2. **`maxcut_qaoa_experiment.ipynb`**  
   - End-to-end simulation of classical vs. quantum algorithms  
   - Aggregated statistics, error bars, and runtime scaling plots  

3. **`maxcut_qaoa_hardware.ipynb` (planned)**  
   - Execution on real IBM hardware using the same circuits  
   - Comparison with simulator performance and noise-induced degradation  

---

## Preliminary Results

- QAOA (p = 1) on Aer simulation produces **comparable cut values** to the best classical approximations (local search, random baseline).  
- Quantum simulation runtime is **higher** and **increases rapidly** with the number of qubits.  
- Exact brute-force search remains the only ground truth for small graphs.  
- Real hardware runs succeeded on graphs up to **100 nodes**, with execution time ≈ **5 seconds** (excluding queue delays).  
- Execution timing was extracted successfully from job metadata; however, **queue delays of several hours** remain a bottleneck for practical testing.  

### TODO — Add Charts
- [ ] Mean cut values (± SEM) vs graph size  
- [ ] Runtime scaling (log scale)  
- [ ] Hardware vs simulation comparisons  

---

## Known Limitations

- Currently limited to **p = 1**; no parameter optimization on hardware yet.  
- **Analytic optimizer** assumes noiseless expectation; real devices may deviate.  
- Only **one hardware job per graph size** for cost control; statistical significance limited.  
- Hardware timing excludes IBM Cloud queue latency (measured separately).  
- No error mitigation applied beyond transpilation to backend’s ISA.  
- Large-graph tests (n > 40) remain classical-only due to circuit depth limits.  

---

## Future Directions

- Extend to multi-layer QAOA (p > 1).  
- Integrate noise models and readout-error mitigation.  
- Add hardware-in-the-loop optimizer (SPSA or COBYLA).  
- Compare multiple IBM backends for performance variability.  
- Automate data aggregation and chart generation for reproducible benchmarking.  

---

## References

1. Farhi et al., *“A Quantum Approximate Optimization Algorithm,”* arXiv:1411.4028 (2014).  
2. IBM Quantum Runtime Documentation – [https://quantum.ibm.com/docs/](https://quantum.ibm.com/docs/)  
3. Qiskit Transpilation Guide – [https://quantum.ibm.com/docs/guides/transpile](https://quantum.ibm.com/docs/guides/transpile)  
4. Google Quantum AI, *“Demonstrating quantum advantage with the Willow processor,”* Nature (2025).  
5. NetworkX Documentation – [https://networkx.org](https://networkx.org)

---

## Conclusion / Discussion

> **TODO:** Summarize comparative results between classical, simulator, and hardware runs once final data are available.  
> Include runtime scaling plots and approximation quality charts.  
> Discuss whether empirical data suggest any emerging *quantum advantage* under realistic conditions.
