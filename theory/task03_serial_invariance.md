# Task 03: The Serial Fraction Invariance Paradox

## 1. Executive Summary

A fundamental point of confusion in parallel computing performance analysis is the apparent paradox between Amdahl's Law and Gustafson's Law regarding the impact of serial overhead. Amdahl's Law asserts that even a tiny serial fraction (e.g., $s = 1\%$) severely throttles speedup as processor count scales toward infinity. Conversely, Gustafson's Law demonstrates that real-world parallel applications achieve massive, near-linear speedups despite containing sequential code components.

This paradox is analytically resolved by examining the **frame of reference** and **point of measurement** for the serial fraction:
- **Amdahl's Frame ($s$):** Serial fraction measured on a single processor running a fixed problem size $W$.
- **Gustafson's Frame ($\alpha$ or $s'$):** Serial fraction observed on the fully scaled parallel system running a expanded problem size $W(P)$.

---

## 2. Analytical Comparison of Frames of Reference

### 2.1 Amdahl's Fixed-Size Frame ($s$)
In Amdahl's formulation, total problem workload $W$ is held strictly constant. Let uniprocessor execution time $T(1)$ be normalized to 1, partitioned into sequential time $s$ and parallelizable time $p = 1 - s$.

When distributed across $P$ processors, total parallel execution time shrinks to:

$$T(P) = s + \frac{1 - s}{P}$$

The proportion of total execution time spent running sequential code on $P$ processors is:

$$\text{Fraction}_{\text{serial}}(P) = \frac{s}{T(P)} = \frac{s}{s + \frac{1 - s}{P}}$$

Taking the limit as $P \to \infty$:

$$\lim_{P \to \infty} \frac{s}{s + \frac{1 - s}{P}} = 1 \quad (100\%)$$

Because the problem size is fixed, the parallel portion shrinks to zero ($\frac{1-s}{P} \to 0$), forcing the static serial overhead $s$ to monopolize $100\%$ of the remaining wall-clock time and capping speedup at $S_{\text{Amdahl}} \le \frac{1}{s}$.

---

## 2.2 Gustafson's Scaled Parallel Frame ($\alpha$)
In Gustafson's formulation, total parallel execution time on $P$ processors is normalized to 1 unit of time: $T_P = \alpha + (1 - \alpha) = 1$, where $\alpha$ is the observed parallel serial fraction and $(1 - \alpha)$ is the parallel computation time.

The equivalent single-processor execution time required to execute this scaled problem size $W(P)$ is:

$$T_1 = \alpha + P(1 - \alpha)$$

Here, as processor count $P$ increases, the absolute serial execution time $\alpha$ remains fixed while total computational work scales as $O(P)$. Expressing the serial work as a fraction of the total workload $T_1$:

$$\text{Fraction}_{\text{work}}(\alpha) = \frac{\alpha}{T_1} = \frac{\alpha}{\alpha + P(1 - \alpha)}$$

Taking the limit as $P \to \infty$:

$$\lim_{P \to \infty} \frac{\alpha}{\alpha + P(1 - \alpha)} = 0$$

Because problem workload scales linearly with core count ($W(P) \propto P$), the relative contribution of the serial component vanishes relative to the expanded parallel workload, preventing serial overhead from choking system throughput.

---

## 3. Mathematical Reconciliation of $s$ and $\alpha$

The transformation between Amdahl's uniprocessor serial fraction $s$ and Gustafson's parallel serial fraction $\alpha$ for a scaled problem size demonstrates why no physical contradiction exists.

Equating the single-processor workload definitions:

$$s_{\text{scaled}} = \frac{\alpha}{\alpha + P(1 - \alpha)}$$

Solving for $\alpha$ in terms of $s$:

$$\alpha = \frac{s \cdot P}{1 + s(P - 1)}$$

### Core Deduction
Measuring the serial fraction directly on a parallel machine running a scaled workload ($\alpha$) reflects the operational reality of high-performance computing: as memory and core capacity grow, scientific problems expand, and parallel work dominates total system energy. The frame of reference shifts from "speeding up a tiny static code" to "expanding resolution in a fixed runtime window," proving that serial overhead does not throttle weak-scaling applications.

---

## 4. Frame of Reference Comparison Matrix

| Property | Amdahl's Model ($s$) | Gustafson's Model ($\alpha$) |
| :--- | :--- | :--- |
| **Point of Measurement** | Uniprocessor system | Parallel execution environment |
| **Workload Assumption** | Fixed problem size ($N = \text{const}$) | Weak scaling ($N(P) \propto P$) |
| **Serial Overhead Ratio vs $P$** | Dominates runtime as $P \to \infty$ | Dilutes relative to total work as $P \to \infty$ |
| **Scalability Limit** | Hard speedup ceiling ($S \le 1/s$) | Linear scaling ($S(P) = P - \alpha(P-1)$) |