\# Task 10: Memory Growth Rate vs. Scaled Speedup — 3D Grid Capacity Analysis



\## 1. Executive Summary \& Parameter Specifications



Under pure weak scaling, aggregate problem workload and memory footprint scale linearly with processor count $P$: 



$$M(P) = c \\cdot P$$



For a 3D grid-based solver operating on a domain of dimension $N \\times N \\times N$, total computational memory footprint scales cubicly with spatial grid resolution ($M \\propto N^3$). This analysis formulates aggregate system memory ceilings and derives maximum allowable grid dimensions $N$ across 64-node and 512-node cluster configurations under a strict 32 GB per-node RAM constraint.



\---



\## 2. Mathematical Formulation of Memory Ceilings



\### 2.1 Per-Node and System Aggregate Capacity Limits

Let $M\_{\\text{node}}$ represent the strict memory cap per node:



$$M\_{\\text{node}} = 32 \\text{ GB} = 32 \\times 10^9 \\text{ bytes} \\quad (\\text{or } 32 \\times 2^{30} \\text{ bytes} = 34,359,738,368 \\text{ bytes})$$



For a system with $P$ processing nodes, total aggregate system memory capacity $M\_{\\text{sys}}(P)$ is:



$$M\_{\\text{sys}}(P) = P \\cdot M\_{\\text{node}}$$



\### 2.2 3D Grid Memory Footprint Relation

For a 3D grid with linear dimension $N$ along each axis (total grid cells $= N^3$), assuming $k$ bytes of memory allocated per grid point (accounting for double-precision state variables, flux vectors, and solver buffers):



$$M(N) = k \\cdot N^3$$



Under full memory saturation ($M(N) = M\_{\\text{sys}}(P)$):



$$k \\cdot N^3 = P \\cdot M\_{\\text{node}}$$



Solving for maximum 3D grid dimension $N(P)$:



$$N(P) = \\sqrt\[3]{\\frac{P \\cdot M\_{\\text{node}}}{k}}$$



Using standard IEEE 754 double-precision floats ($8 \\text{ bytes/variable}$) with an exemplary solver state allocation of $k = 64 \\text{ bytes per grid cell}$ ($8$ double-precision variables per mesh point):



$$\\text{Per-cell capacity } c\_{\\text{cells/node}} = \\frac{32 \\times 10^9 \\text{ bytes}}{64 \\text{ bytes/cell}} = 500,000,000 \\text{ cells/node}$$



$$\\text{System Total Cells } C(P) = P \\cdot c\_{\\text{cells/node}} = 500,000,000 \\cdot P$$



Maximum grid dimension $N$:



$$N(P) = \\sqrt\[3]{C(P)} = \\sqrt\[3]{500,000,000 \\cdot P}$$



\---



\## 3. Step-by-Step Numerical Calculations



\### 3.1 64-Node Topology ($P = 64$)



\#### 1. Aggregate Memory Capacity

$$M\_{\\text{sys}}(64) = 64 \\times 32 \\text{ GB} = \\mathbf{2,048 \\text{ GB}} \\quad (2.048 \\text{ TB})$$



\#### 2. Aggregate Grid Cell Capacity ($k = 64 \\text{ bytes/cell}$)

$$C(64) = 64 \\times 500,000,000 = 32,000,000,000 \\text{ total cells}$$



\#### 3. Maximum 3D Grid Dimension $N$

$$N(64) = \\sqrt\[3]{32,000,000,000}$$



$$\\begin{aligned}

\\ln N \&= \\frac{1}{3} \\ln(3.2 \\times 10^{10}) \\approx \\frac{1}{3} (24.188708) \\approx 8.062903 \\\\

N(64) \&\\approx \\mathbf{3,174.80}

\\end{aligned}$$



Rounding down to the nearest integer grid dimension: \*\*$N\_{\\text{max}} = 3,174$\*\* (forming a $3,174 \\times 3,174 \\times 3,174$ mesh containing $31,975,819,704$ cells).



\---



\### 3.2 512-Node Topology ($P = 512$)



\#### 1. Aggregate Memory Capacity

$$M\_{\\text{sys}}(512) = 512 \\times 32 \\text{ GB} = \\mathbf{16,384 \\text{ GB}} \\quad (16.384 \\text{ TB})$$



\#### 2. Aggregate Grid Cell Capacity ($k = 64 \\text{ bytes/cell}$)

$$C(512) = 512 \\times 500,000,000 = 256,000,000,000 \\text{ total cells}$$



\#### 3. Maximum 3D Grid Dimension $N$

$$N(512) = \\sqrt\[3]{256,000,000,000}$$



$$\\begin1{aligned}

N(512) \&= \\sqrt\[3]{8 \\times 32,000,000,000} \\\\

\&= 2 \\times N(64) \\\\

\&\\approx 2 \\times 3,174.80 = \\mathbf{6,349.60}

\\end{aligned}$$



Rounding down to the nearest integer grid dimension: \*\*$N\_{\\text{max}} = 6,349$\*\* (forming a $6,349 \\times 6,349 \\times 6,349$ mesh containing $255,927,330,449$ cells).



\---



\## 4. Analytical Capacity Summary Matrix



| Metric / Parameter | 64 Nodes ($P = 64$) | 512 Nodes ($P = 512$) | Scaling Ratio ($512 / 64$) |

| :--- | :--- | :--- | :--- |

| \*\*Node RAM Cap ($M\_{\\text{node}}$)\*\* | $32 \\text{ GB}$ | $32 \\text{ GB}$ | $1.0\\times$ |

| \*\*Aggregate Memory ($M\_{\\text{sys}}$)\*\* | \*\*$2,048 \\text{ GB}$\*\* ($2.048 \\text{ TB}$) | \*\*$16,384 \\text{ GB}$\*\* ($16.384 \\text{ TB}$) | \*\*$8.0\\times$\*\* |

| \*\*Total 3D Cells ($C(P)$)\*\* | $3.2 \\times 10^{10}$ cells | $2.56 \\times 10^{11}$ cells | \*\*$8.0\\times$\*\* |

| \*\*Max Grid Dimension ($N\_{\\text{max}}$)\*\* | \*\*$3,174$\*\* | \*\*$6,349$\*\* | \*\*$2.0\\times$ ($\\sqrt\[3]{8}$)\*\* |

| \*\*Per-Node Subdomain Grid\*\* | $793 \\times 793 \\times 793$ | $793 \\times 793 \\times 793$ | $1.0\\times$ |



\### Structural Scaling Deduction

Because spatial grid cells scale cubically ($N^3$), expanding processor nodes eightfold ($8\\times$ from 64 to 512) allows the 3D spatial resolution dimension $N$ to scale by a factor of exactly $\\sqrt\[3]{8} = 2\\times$. Under weak scaling, per-node subdomain size remains invariant at approximately $500 \\times 10^6$ cells ($793^3$), preserving constant computational density per core.

