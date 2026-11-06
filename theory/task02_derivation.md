# Task 02: Formal Derivation of Gustafson's Scaled Speedup

## 1. System Model & Normalization Baseline
Let $P$ represent the number of parallel processing cores. 

In Gustafson's model, performance measurement is performed on the parallel architecture executing a scaled problem instance. The total parallel execution runtime $T_P$ on $P$ processors is normalized to $1$ unit of time:

$$T_P = s + p = 1$$

where:
* $s$ is the sequential execution time fraction ($0 \le s \le 1$).
* $p$ is the parallel execution time fraction ($0 \le p \le 1$).

From normalization, the parallel execution fraction is:
$$p = 1 - s$$

---

## 2. Equivalent Single-Processor Workload Construction
If the exact same scaled workload were executed sequentially on a single processor ($P = 1$):
1. The sequential section $s$ would still require time $s$ (since it cannot be parallelized).
2. The parallel section $p$ (which was divided across $P$ cores) would require $P \times p$ time units on a single core.

Therefore, the equivalent serial execution time $T_1$ on a single processor is:

$$T_1 = s + P \cdot p$$

---

## 3. Derivation of Scaled Speedup $S(P)$
Speedup $S(P)$ is defined as the ratio of single-processor execution time to $P$-processor execution time:

$$S(P) = \frac{T_1}{T_P} = \frac{s + P \cdot p}{1} = s + P \cdot p$$

Substituting $p = 1 - s$ into the expression:

$$\begin{aligned}
S(P) &= s + P(1 - s) \\
&= s + P - s \cdot P \\
&= P - s(P - 1)
\end{aligned}$$

Replacing $s$ with $a$ (where $a$ represents the measured parallel serial fraction):

$$S(P) = P - a(P - 1)$$

Alternatively, expanding in terms of parallel fraction $p$:

$$S(P) = a + p \cdot P$$

---

## 4. Line-by-Line Mathematical Proof

$$\begin{array}{rll}
T_P &= 1 & \text{(Normalize total parallel time to 1 unit)} \\
s + p &= 1 & \text{(Partition runtime into serial and parallel components)} \\
p &= 1 - s & \text{(Express parallel fraction in terms of serial fraction)} \\
T_1 &= s + P \cdot p & \text{(Formulate total single-processor workload)} \\
S(P) &= \frac{T_1}{T_P} & \text{(Apply classical speedup definition)} \\
S(P) &= \frac{s + P \cdot p}{1} & \text{(Substitute } T_1 \text{ and } T_P = 1 \text{)} \\
S(P) &= s + P(1 - s) & \text{(Substitute } p = 1 - s \text{)} \\
S(P) &= s + P - s \cdot P & \text{(Distribute } P \text{ across terms)} \\
S(P) &= P - s(P - 1) & \text{(Factor out } s \text{ to obtain Gustafson's Law)}
\end{array}$$

Q.E.D.