\# Task 09: Multi-Component Workload Partitioning and Composite Speedup Analysis



\## 1. Workload Partitioning \& Aggregate Serial Overhead



In complex scientific simulations, total execution time on a parallel machine is distributed across multiple operational phases. To compute the aggregate serial fraction $\\alpha$, phases must be categorized by their execution characteristics under scaling.



\### Phase Breakdown \& Classification

\- \*\*Phase A (Initial Disk I/O \& Parameter Broadcast):\*\* Consumes $2\\%$ of parallel execution time. This phase is non-parallelizable and sequential ($\\alpha\_A = 0.02$).

\- \*\*Phase B (Boundary Message-Passing Synchronization):\*\* Consumes $6\\%$ of parallel execution time. Inter-node synchronization and communication overhead scale serially relative to computation, representing non-parallelizable overhead ($\\alpha\_B = 0.06$).

\- \*\*Phase C (Core Domain Flux Computation):\*\* Consumes $92\\%$ of parallel execution time. Fully parallel domain computation that scales across available cores ($p = 0.92$).



\### Aggregate Serial Fraction ($\\alpha$)

The aggregate serial overhead fraction observed on the parallel system is the sum of all non-parallelizable phase fractions:



$$\\alpha = \\alpha\_A + \\alpha\_B = 0.02 + 0.06 = 0.08 \\quad (8\\%)$$



The scalable parallel computational fraction is:



$$p = 1 - \\alpha = 0.92 \\quad (92\\%)$$



\---



\## 2. Mathematical Formulation \& Speedup Evaluation



Under Gustafson's Scaled Speedup Model (Weak Scaling), total parallel execution time is normalized to $T\_P = 1$. The scaled speedup formula is:



$$S(P) = P - \\alpha(P - 1) = \\alpha + (1 - \\alpha)P = 0.08 + 0.92P$$



Parallel efficiency is given by:



$$E(P) = \\frac{S(P)}{P} = 1 - \\alpha\\left(\\frac{P - 1}{P}\\right)$$



\---



\## 3. Detailed Numerical Calculations



\### 3.1 Processor Topology $P = 512$

Substituting $P = 512$ and $\\alpha = 0.08$:



$$\\begin{aligned}

S(512) \&= 512 - 0.08(512 - 1) \\\\

\&= 512 - 0.08(511) \\\\

\&= 512 - 40.88 \\\\

\&= \\mathbf{471.1200\\times}

\\end{aligned}$$



\#### Parallel Efficiency:

$$E(512) = \\frac{471.1200}{512} = 0.92015625 \\quad (\\mathbf{92.0156\\%})$$



\---



\### 3.2 Processor Topology $P = 2,048$

Substituting $P = 2048$ and $\\alpha = 0.08$:



$$\\begin{aligned}

S(2048) \&= 2048 - 0.08(2048 - 1) \\\\

\&= 2048 - 0.08(2047) \\\\

\&= 2048 - 163.76 \\\\

\&= \\mathbf{1884.2400\\times}

\\end{aligned}$$



\#### Parallel Efficiency:

$$E(2048) = \\frac{1884.2400}{2048} \\approx 0.92003906 \\quad (\\mathbf{92.0039\\%})$$



\---



\## 4. Summary \& Analytical Breakdown



| Metric / Parameter | Core Topology $P = 512$ | Core Topology $P = 2,048$ |

| :--- | :--- | :--- |

| \*\*Phase A Overhead (I/O)\*\* | $0.02$ time units | $0.02$ time units |

| \*\*Phase B Overhead (Sync)\*\* | $0.06$ time units | $0.06$ time units |

| \*\*Phase C Work (Flux Comp)\*\* | $471.04$ equivalent work units | $1884.16$ equivalent work units |

| \*\*Aggregate Serial Fraction ($\\alpha$)\*\* | \*\*$0.08$\*\* ($8\\%$) | \*\*$0.08$\*\* ($8\\%$) |

| \*\*Total Equivalent Work ($T\_1$)\*\* | $471.12$ units | $1884.24$ units |

| \*\*Scaled Speedup ($S(P)$)\*\* | \*\*$471.12\\times$\*\* | \*\*$1884.24\\times$\*\* |

| \*\*Parallel Efficiency ($E(P)$)\*\* | \*\*$92.0156\\%$\*\* | \*\*$92.0039\\%$\*\* |



\### Key Insight

Even with combined I/O and communication synchronization overhead accounting for $8\\%$ of total parallel execution time ($\\alpha = 0.08$), weak scaling allows the simulation to scale efficiently. As processor count expands fourfold from $P = 512$ to $P = 2048$, parallel efficiency stays above \*\*$92\\%$\*\*, bounded by the theoretical asymptotic limit of $1 - \\alpha = 92\\%$.

