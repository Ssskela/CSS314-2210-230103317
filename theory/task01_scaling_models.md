\# Task 01: Strong Scaling vs. Weak Scaling Foundations



\## 1. Executive Summary \& Philosophical Divergence



Parallel computing performance models evaluate how application runtime and speedup evolve as hardware concurrency ($P$) increases. The primary philosophical divergence between Gene Amdahl (1967) and John Gustafson (1988) lies in how the problem dimension ($N$) is treated relative to processor count ($P$).



\- \*\*Amdahl's Law (Strong Scaling):\*\* Assumes a fixed problem size ($N = \\text{const}$). The goal is to minimize total execution time ($T\_P$) for a fixed computational load by distributing it across a growing number of processors.

\- \*\*Gustafson's Law (Weak Scaling):\*\* Assumes a fixed execution time ($T\_P = \\text{const}$). The goal is to maximize solution resolution or problem capacity ($N(P) \\propto P$) by leveraging additional computing resources to perform more work within the same time window.



\---



\## 2. Mathematical Formulations \& Asymptotic Limits



\### 2.1 Amdahl's Fixed-Size Scaling Model

Let total uniprocessor execution time $T(1)$ be partitioned into a sequential fraction $s$ and a parallelizable fraction $p$, where $s + p = 1$. Under strong scaling, the total workload remains constant while the parallel component is divided across $P$ processors:



$$T(P) = s \\cdot T(1) + \\frac{(1 - s) \\cdot T(1)}{P}$$



The strong scaling speedup $S\_{\\text{Amdahl}}(P)$ is formulated as:



$$S\_{\\text{Amdahl}}(P) = \\frac{T(1)}{T(P)} = \\frac{1}{s + \\frac{1 - s}{P}}$$



\#### Asymptotic Limit as $P \\to \\infty$

As processor density scales to infinity, the parallel portion per processor shrinks to zero ($\\frac{1-s}{P} \\to 0$), causing the sequential fraction $s$ to dominate runtime:



$$\\lim\_{P \\to \\infty} S\_{\\text{Amdahl}}(P) = \\frac{1}{s}$$



$$\\lim\_{P \\to \\infty} E\_{\\text{Amdahl}}(P) = \\lim\_{P \\to \\infty} \\frac{S\_{\\text{Amdahl}}(P)}{P} = 0$$



Under Amdahl's Law, parallel speedup hits a strict theoretical ceiling dictated by $1/s$, and parallel efficiency asymptotically decays to zero.



\---



\### 2.2 Gustafson's Fixed-Time Scaling Model

Let execution time on $P$ processors be normalized to 1 time unit: $T\_P = s' + p' = 1$, where $s'$ is the observed parallel serial fraction and $p' = 1 - s'$ is the parallel fraction. The equivalent single-processor workload $T(1)$ required to complete the scaled problem instance is:



$$T(1) = s' + P \\cdot p' = s' + P(1 - s')$$



The weak scaling scaled speedup $S\_{\\text{Gustafson}}(P)$ is derived as:



$$S\_{\\text{Gustafson}}(P) = \\frac{T(1)}{T\_P} = s' + P(1 - s') = P - s'(P - 1)$$



\#### Asymptotic Limit as $P \\to \\infty$

Assuming the serial fraction $s'$ remains small and invariant with respect to workload expansion:



$$\\lim\_{P \\to \\infty} S\_{\\text{Gustafson}}(P) = \\infty \\quad (\\text{linear speedup } S \\approx P(1-s'))$$



$$\\lim\_{P \\to \\infty} E\_{\\text{Gustafson}}(P) = \\lim\_{P \\to \\infty} \\left(1 - s'\\left(\\frac{P-1}{P}\\right)\\right) = 1 - s'$$



Under Gustafson's Law, parallel speedup scales near-linearly with processor count, and parallel efficiency stabilizes at a non-zero constant ($1 - s'$).



\---



\## 3. Physical Realities \& Application Domains



\### 3.1 Amdahl's Fixed-Size Applications

Strong scaling applies to time-constrained operations where delivering an exact numerical answer in minimal wall-clock time is paramount:

\- Real-time video encoding and frame rendering

\- Interactive database query execution

\- Short-range operational weather forecasting (e.g., producing a 24-hour prediction in under 30 minutes)



\### 3.2 Gustafson's Fixed-Time Applications

Weak scaling models capacity-constrained computational science where available HPC hardware determines problem fidelity:

\- High-resolution climate modeling (increasing 3D spatial grid resolution)

\- Molecular dynamics and N-body gravitational simulations (increasing particle counts)

\- Deep learning neural network training (expanding dataset size and model parameter counts)



\---



\## 4. Analytical Comparison Matrix



| Metric / Dimension | Amdahl's Law (Strong Scaling) | Gustafson's Law (Weak Scaling) |

| :--- | :--- | :--- |

| \*\*Problem Workload ($N$)\*\* | Constant ($N = \\text{const}$) | Scaled linearly ($N(P) \\propto P$) |

| \*\*Target Variable\*\* | Minimize execution time ($T\_P \\to \\text{min}$) | Maintain constant time ($T\_P = \\text{const}$) |

| \*\*Work per Processor ($N/P$)\*\* | Shrinks to zero ($\\frac{N}{P} \\to 0$) | Constant ($\\frac{N(P)}{P} = \\text{const}$) |

| \*\*Serial Overhead Point of Origin\*\* | Measured on single core ($s$) | Observed on parallel machine ($s'$) |

| \*\*Speedup Ceiling ($P \\to \\infty$)\*\* | Capped at $1/s$ | Unbounded ($S \\approx P(1-s')$) |

| \*\*Parallel Efficiency ($P \\to \\infty$)\*\* | Decays to $0$ | Sustained at $1 - s'$ |

| \*\*Primary Compute Domain\*\* | Real-time \& interactive tasks | Large-scale HPC scientific simulations |

