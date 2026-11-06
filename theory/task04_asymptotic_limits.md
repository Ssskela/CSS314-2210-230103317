\# Task 04: Asymptotic Analysis of Parallel Efficiency



\## 1. Executive Summary



Parallel efficiency $E(P) = \\frac{S(P)}{P}$ quantifies the fraction of total processor capacity effectively utilized during parallel execution. This analysis mathematically derives and contrasts the asymptotic limit of parallel efficiency as processor concurrency scales to infinity ($P \\to \\infty$) under:

1\. \*\*Gustafson's Law (Weak Scaling)\*\*

2\. \*\*Amdahl's Law (Strong Scaling)\*\*



While Amdahl's Law predicts an efficiency decay to zero for any non-zero serial fraction, Gustafson's Law proves that weak scaling sustains parallel efficiency at a positive, non-zero constant limit ($1 - \\alpha$).



\---



\## 2. Asymptotic Analysis under Gustafson's Law



\### 2.1 Formal Definition

Under Gustafson's weak scaling model, parallel speedup $S\_{\\text{Gustafson}}(P)$ is defined as:



$$S(P) = P - \\alpha(P - 1) = \\alpha + (1 - \\alpha)P$$



where $\\alpha$ is the observed parallel serial fraction ($0 \\le \\alpha < 1$).



Parallel efficiency $E\_{\\text{Gustafson}}(P)$ is formulated as:



$$E(P) = \\frac{S(P)}{P} = \\frac{P - \\alpha(P - 1)}{P} = 1 - \\alpha\\left(\\frac{P - 1}{P}\\right)$$



\---



\### 2.2 Limit Proof as $P \\to \\infty$



$$\\begin{aligned}

\\lim\_{P \\to \\infty} E\_{\\text{Gustafson}}(P) \&= \\lim\_{P \\to \\infty} \\left\[ 1 - \\alpha\\left(\\frac{P - 1}{P}\\right) \\right] \\\\

\&= \\lim\_{P \\to \\infty} \\left\[ 1 - \\alpha\\left(1 - \\frac{1}{P}\\right) \\right] \\\\

\&= 1 - \\alpha \\cdot \\lim\_{P \\to \\infty} \\left(1 - \\frac{1}{P}\\right) \\\\

\&= 1 - \\alpha (1 - 0) \\\\

\&= 1 - \\alpha

\\end{aligned}$$



\### Deduction

As processor count expands infinitely under weak scaling, parallel efficiency asymptotically approaches $1 - \\alpha$. For an empirical serial fraction of $\\alpha = 4\\%$ ($0.04$), parallel efficiency remains bounded at a massive $96\\%$, regardless of whether $P = 1,024$ or $P = 1,000,000$.



\---



\## 3. Asymptotic Analysis under Amdahl's Law



\### 3.1 Formal Definition

Under Amdahl's fixed-size scaling model, parallel speedup $S\_{\\text{Amdahl}}(P)$ is defined as:



$$S(P) = \\frac{1}{s + \\frac{1 - s}{P}}$$



where $s$ is the uniprocessor serial fraction ($0 < s \\le 1$).



Parallel efficiency $E\_{\\text{Amdahl}}(P)$ is formulated as:



$$E(P) = \\frac{S(P)}{P} = \\frac{1}{P \\cdot s + (1 - s)}$$



\---



\### 3.2 Limit Proof as $P \\to \\infty$



$$\\begin{aligned}

\\lim\_{P \\to \\infty} E\_{\\text{Amdahl}}(P) \&= \\lim\_{P \\to \\infty} \\left\[ \\frac{1}{P \\cdot s + (1 - s)} \\right] \\\\

\&= \\frac{1}{\\lim\_{P \\to \\infty} \[P \\cdot s + (1 - s)]} \\\\

\&= \\frac{1}{\\infty + (1 - s)} \\\\

\&= 0

\\end{aligned}$$



\### Deduction

Under strong scaling with a fixed problem size, parallel efficiency decays monotonically to zero as $P \\to \\infty$. Adding more processing cores yields diminishing returns and eventually renders the hardware idle for the majority of wall-clock time.



\---



\## 4. Analytical \& Visual Contrast



$$\\begin{array}{rcc}

\\hline

\\text{Model} \& \\text{Efficiency Formulation } E(P) \& \\text{Asymptotic Limit } \\lim\_{P \\to \\infty} E(P) \\\\

\\hline

\\text{Gustafson (Weak Scaling)} \& 1 - \\alpha\\left(1 - \\frac{1}{P}\\right) \& 1 - \\alpha \\quad (\\text{Non-Zero Constant}) \\\\

\\text{Amdahl (Strong Scaling)} \& \\frac{1}{P \\cdot s + (1 - s)} \& 0 \\quad (\\text{Total Efficiency Decay}) \\\\

\\hline

\\end{array}$$



\### Physical Interpretation

\- \*\*Amdahl's Collapse:\*\* Under strong scaling, fixed problem granularity per core shrinks ($\\frac{N}{P} \\to 0$), making execution time overwhelmingly dominated by the unscalable serial tail.

\- \*\*Gustafson's Sustainability:\*\* Under weak scaling, problem size scales dynamically with hardware expansion ($N(P) \\propto P$). Per-core workload stays constant ($\\frac{N(P)}{P} = \\text{const}$), ensuring that parallel processing units continue doing useful computational work at scale.

