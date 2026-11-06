\# Task 08: Cross-Over Point Determination and Model Divergence Analysis



\## 1. Problem Setup \& System Parameters



This analysis quantifies the mathematical divergence between Amdahl's Law (Strong Scaling) and Gustafson's Law (Weak Scaling) for a system operating across $P = 128$ processor cores with a baseline serial overhead of $8\\%$ ($s = \\alpha = 0.08$).



\### Key Parameters

\- \*\*Processor Count ($P$):\*\* $128$ cores

\- \*\*Serial Overhead Fraction:\*\* $s = \\alpha = 0.08$ ($8\\%$)

\- \*\*Parallel Fraction:\*\* $p = 1 - 0.08 = 0.92$ ($92\\%$)



\---



\## 2. Quantitative Speedup Calculations ($P = 128$)



\### 2.1 Amdahl's Speedup Calculation ($S\_{\\text{Amdahl}}$)

Under Amdahl's fixed-size scaling model:



$$S\_{\\text{Amdahl}}(P) = \\frac{1}{s + \\frac{1 - s}{P}}$$



Substitute $s = 0.08$ and $P = 128$:



$$\\begin{aligned}

S\_{\\text{Amdahl}}(128) \&= \\frac{1}{0.08 + \\frac{0.92}{128}} \\\\

\&= \\frac{1}{0.08 + 0.0071875} \\\\

\&= \\frac{1}{0.0871875} \\\\

\&\\approx \\mathbf{11.4695\\times}

\\end{aligned}$$



\#### Amdahl Parallel Efficiency

$$E\_{\\text{Amdahl}}(128) = \\frac{11.4695}{128} \\approx 0.089605 \\quad (\\mathbf{8.9605\\%})$$



\---



\### 2.2 Gustafson's Scaled Speedup Calculation ($S\_{\\text{Gustafson}}$)

Under Gustafson's fixed-time scaling model:



$$S\_{\\text{Gustafson}}(P) = P - \\alpha(P - 1)$$



Substitute $\\alpha = 0.08$ and $P = 128$:



$$\\begin{aligned}

S\_{\\text{Gustafson}}(128) \&= 128 - 0.08(127) \\\\

\&= 128 - 10.16 \\\\

\&= \\mathbf{117.8400\\times}

\\end{aligned}$$



\#### Gustafson Parallel Efficiency

$$E\_{\\text{Gustafson}}(128) = \\frac{117.8400}{128} = 0.920625 \\quad (\\mathbf{92.0625\\%})$$



\---



\## 3. Discrepancy \& Variance Analysis



\### 3.1 Absolute Variance

$$\\Delta S = S\_{\\text{Gustafson}}(128) - S\_{\\text{Amdahl}}(128) = 117.8400 - 11.4695 = \\mathbf{106.3705\\times}$$



\### 3.2 Percentage Discrepancy Relative to Amdahl Baseline

$$\\text{Percentage Discrepancy} = \\left( \\frac{S\_{\\text{Gustafson}} - S\_{\\text{Amdahl}}}{S\_{\\text{Amdahl}}} \\right) \\times 100\\%$$



$$\\text{Percentage Discrepancy} = \\left( \\frac{106.3705}{11.4695} \\right) \\times 100\\% \\approx \\mathbf{927.42\\%}$$



Gustafson's model predicts a speedup that is \*\*$10.27\\times$ higher\*\* (or $927.42\\%$ greater) than Amdahl's prediction on $128$ cores.



\---



\## 4. Analytical Comparison \& Cause of Divergence



| Metric | Amdahl's Law (Strong Scaling) | Gustafson's Law (Weak Scaling) | Ratio / Variance |

| :--- | :--- | :--- | :--- |

| \*\*Model Premise\*\* | Fixed Problem Size ($N = \\text{const}$) | Scaled Problem Size ($N \\propto P$) | Different Premises |

| \*\*Predicted Speedup ($S$)\*\* | \*\*$11.47\\times$\*\* | \*\*$117.84\\times$\*\* | $S\_{\\text{Gustafson}}$ is $10.27\\times$ higher |

| \*\*Parallel Efficiency ($E$)\*\* | \*\*$8.96\\%$\*\* | \*\*$92.06\\%$\*\* | Efficiency gap of $83.10\\%$ |

| \*\*Asymptotic Bound ($P \\to \\infty$)\*\* | Capped at $1/s = 12.5\\times$ | Unbounded ($\\approx 0.92 P$) | Hard ceiling vs Linear |



\### Why the Models Diverge

1\. \*\*Workload Expansion:\*\* Amdahl forces the problem to remain tiny. As $P$ increases to 128, each core processes only $1/128$th of the parallel work ($0.7187\\%$), causing the fixed $8\\%$ serial fraction to consume $91.04\\%$ of the total parallel execution time.

2\. \*\*Serial Overhead Dilution:\*\* Gustafson expands the problem size by $128\\times$. The parallel work scales to $0.92 \\times 128 = 117.76$ time units while serial overhead remains fixed at $0.08$ time units, keeping the serial component tiny relative to the expanded total workload.

