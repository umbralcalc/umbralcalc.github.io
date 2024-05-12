---
title: Adaptive sequential Monte Carlo sampling with a discounted history
author: Hardwick, Robert J
date: [WIP]
concept: To describe the design and implementation of an adaptive sequential Monte Carlo sampler which can dynamically adapt to sampling new points from nonstationary, multivariate and potentially multi-modal distributions in the context of online learning. We control the sensitivity of this algorithm to temporal changes in the target distribution through a discounted history approach.
articleId: modesampler
codeLink: https://github.com/umbralcalc/modesampler
year: [WIP]
---

## Online learning the density

Idea is to dynamically train the bandwidth matrix $H$ of a kernel $K_{H}(z,{\sf t};z',{\sf t}')$ density estimation algorithm using the following iterative cross-validation formula

$$
\begin{align}
D_{\rm KL} = \int {\rm d}z p(z)\ln \frac{p(z)}{p_H(z)} = \sum_{z_{i{\sf t}}}w_{i{\sf t}} \ln \frac{w_{i{\sf t}}}{\sum_{z_{j{\sf t}'}:{\sf t}>{\sf t}'}w_{j{\sf t}'}K_{H}(z_{i{\sf t}},{\sf t};z_{j{\sf t}'},{\sf t}')} \,.
\end{align}
$$

The modes are then detected by initialising a $z$-optimising step at time ${\sf t}$ with initial conditions set by all of the current samples and an objective given by

$$
\begin{align}
{\sf obj}(z) = \sum_{z_{i{\sf t}}}w_{i{\sf t}}K_{H}(z,{\sf t};z_{i{\sf t}},{\sf t}) \,.
\end{align}
$$

Scaling in time history is probably the main nuisance here! Might motivate the use of Rust though since having a really good handle on what memory is actually necessary will be very useful.

Probably fits into the actor pattern nicely!

## Sampling

- Ensemble slice sampling using rejection step?
  1. Choose starting $z$ value and validate that $p(z)>0$
  2. Sample the next $p$ value uniformally between $0$ and $p(z)$
  3. Use rejection sampling to find new $z$ which has a bigger $p$ than the last
  4. Return to 2.
- Maybe the proposal could be better informed by using a Gaussian approximation to local mode density (maybe even restricted to the samples in a specific quartile)?

## References
