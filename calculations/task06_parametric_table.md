\# Task 06: Parametric Speedup and Parallel Efficiency Across Processor Densities



\## 1. Mathematical Model \& Parameter Definitions



Under Gustafson's Law (Weak Scaling), performance is modeled with a fixed parallel wall-clock runtime $T\_P = 1$. Given the observed parallel serial fraction $\\alpha = 0.04$ ($4\\%$), the remaining parallel fraction is $p = 1 - \\alpha = 0.96$ ($96\\%$).



The governing formulas for scaled speedup $S(P)$ and parallel efficiency $E(P)$ are:



$$S(P) = P - \\alpha(P - 1) = \\alpha + (1 - \\alpha)P = 0.04 + 0.96P$$



$$E(P) = \\frac{S(P)}{P} = 1 - \\alpha\\left(\\frac{P - 1}{P}\\right) = 1 - 0.04\\left(1 - \\frac{1}{P}\\right)$$



\---



\## 2. Step-by-Step Numerical Calculations ($\\alpha = 0.04$)



\### 1. Core Topology $P = 16$

\- \*\*Speedup:\*\* $S(16) = 16 - 0.04(15) = 16 - 0.6 = 15.4000\\times$

\- \*\*Efficiency:\*\* $E(16) = \\frac{15.4000}{16} = 0.9625 \\quad (96.2500\\%)$



\### 2. Core Topology $P = 64$

\- \*\*Speedup:\*\* $S(64) = 64 - 0.04(63) = 64 - 2.52 = 61.4800\\times$

\- \*\*Efficiency:\*\* $E(64) = \\frac{61.4800}{64} = 0.960625 \\quad (96.0625\\%)$



\### 3. Core Topology $P = 256$

\- \*\*Speedup:\*\* $S(256) = 256 - 0.04(255) = 256 - 10.20 = 245.8000\\times$

\- \*\*Efficiency:\*\* $E(256) = \\frac{245.8000}{256} = 0.960156 \\quad (96.0156\\%)$



\### 4. Core Topology $P = 1024$

\- \*\*Speedup:\*\* $S(1024) = 1024 - 0.04(1023) = 1024 - 40.92 = 983.0800\\times$

\- \*\*Efficiency:\*\* $E(1024) = \\frac{983.0800}{1024} \\approx 0.960039 \\quad (96.0039\\%)$



\### 5. Core Topology $P = 4096$

\- \*\*Speedup:\*\* $S(4096) = 4096 - 0.04(4095) = 4096 - 163.80 = 3932.2000\\times$

\- \*\*Efficiency:\*\* $E(4096) = \\frac{3932.2000}{4096} \\approx 0.960010 \\quad (96.0010\\%)$



\### 6. Core Topology $P = 16384$

\- \*\*Speedup:\*\* $S(16384) = 16384 - 0.04(16383) = 16384 - 655.32 = 15728.6800\\times$

\- \*\*Efficiency:\*\* $E(16384) = \\frac{15728.6800}{16384} \\approx 0.960002 \\quad (96.0002\\%)$



\---



\## 3. Parametric Evaluation Table



| Processors ($P$) | Serial Work ($\\alpha$) | Parallel Work ($P(1-\\alpha)$) | Equivalent Work ($T\_1$) | Scaled Speedup $S(P)$ | Parallel Efficiency $E(P)$ | Efficiency Loss ($1 - E$) |

| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

| \*\*1\*\* | 0.04 | 0.96 | 1.0000 | \*\*1.0000×\*\* | \*\*100.0000%\*\* | 0.0000% |

| \*\*16\*\* | 0.04 | 15.36 | 15.4000 | \*\*15.4000×\*\* | \*\*96.2500%\*\* | 3.7500% |

| \*\*64\*\* | 0.04 | 61.44 | 61.4800 | \*\*61.4800×\*\* | \*\*96.0625%\*\* | 3.9375% |

| \*\*256\*\* | 0.04 | 245.76 | 245.8000 | \*\*245.8000×\*\* | \*\*96.0156%\*\* | 3.9844% |

| \*\*1024\*\* | 0.04 | 983.04 | 983.0800 | \*\*983.0800×\*\* | \*\*96.0039%\*\* | 3.9961% |

| \*\*4096\*\* | 0.04 | 3932.16 | 3932.2000 | \*\*3932.2000×\*\* | \*\*96.0010%\*\* | 3.9990% |

| \*\*16384\*\* | 0.04 | 15728.64 | 15728.6800 | \*\*15728.6800×\*\* | \*\*96.0002%\*\* | 3.9998% |

| \*\*$\\infty$\*\* | 0.04 | $\\infty$ | $\\infty$ | \*\*$\\infty$\*\* | \*\*96.0000%\*\* | \*\*4.0000%\*\* |



\---



\## 4. Analytical Evaluation \& Efficiency Degradation Profile



1\. \*\*Monotonic Convergence to $1 - \\alpha$:\*\* 

&#x20;  As core count expands exponentially from $P = 16$ to $P = 16384$ ($1024\\times$ scale-up), efficiency smoothly drops by a tiny fraction of a percent (from $96.25\\%$ down to $96.0002\\%$). It strictly converges toward the asymptotic lower bound:



&#x20;  $$\\lim\_{P \\to \\infty} E(P) = 1 - \\alpha = 1 - 0.04 = 0.9600 \\quad (96.00\\%)$$



2\. \*\*Contrast with Amdahl's Collapse:\*\* 

&#x20;  Under Amdahl's Law with the same $4\\%$ serial fraction, efficiency collapses catastrophically as $P$ grows:

&#x20;  - Amdahl $E(16) = 62.50\\%$

&#x20;  - Amdahl $E(256) = 9.53\\%$

&#x20;  - Amdahl $E(16384) = 0.15\\%$



&#x20;  Under Gustafson's weak scaling model, resource utilization remains nearly optimal ($>96\\%$) across all core counts because computational workload expands proportionally with added processor hardware.

