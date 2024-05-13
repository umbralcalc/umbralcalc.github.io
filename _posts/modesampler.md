---
title: Adaptive sequential Monte Carlo sampling with a discounted history
author: Hardwick, Robert J
date: [WIP]
concept: To describe the design and implementation of an adaptive sequential Monte Carlo sampler which can dynamically adapt to sampling new points from nonstationary, multivariate and potentially multi-modal distributions in the context of online learning. We control the sensitivity of this algorithm to temporal changes in the target distribution through a discounted history approach.
articleId: modesampler
codeLink: https://github.com/umbralcalc/modesampler
year: [WIP]
---

## Problem statement

Say that we have a generator of probabilistic weights which takes a vector of parameters $z$ as input. This generator represents a non-stationary probability distribution and the weights are effectively stochastic around the true value for each given $z$ as input. The problem is that we would like to be able to efficiently sample from the underlying distribution regardless of its shape or modality.

## Online learning the density

Read this first: [https://wires.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/wics.1598](https://wires.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/wics.1598)

Idea is to dynamically train the bandwidth matrix $H$ of a kernel $K_{H}(z,z')$ density estimation algorithm by minimising the following iterative cross-validation formula

$$
\begin{align}
D_{\rm KL} = \int {\rm d}z \, P_{{\sf t}}(z)\ln \frac{P_{{\sf t}}(z)}{Q_{{\sf t}>{\sf t}'}(z)} \simeq \frac{1}{\sum_{z_{i{\sf t}}}w_{i{\sf t}}}\sum_{z_{i{\sf t}}}w_{i{\sf t}} \ln \frac{w_{i{\sf t}}\sum_{z_{j{\sf t}'}:{\sf t}>{\sf t}'}w_{j{\sf t}'}}{\sum_{z_{j{\sf t}'}:{\sf t}>{\sf t}'}w_{j{\sf t}'}K_{H}(z_{i{\sf t}},z_{j{\sf t}'})} \,.
\end{align}
$$

The modes are then detected by initialising a $z$-optimising step at time ${\sf t}$ with initial conditions set by all of the current samples and an objective given by

$$
\begin{align}
Q_{{\sf t}}(z) = \frac{\sum_{z_{i{\sf t}}}w_{i{\sf t}}K_{H}(z,z_{i{\sf t}})}{\sum_{z_{i{\sf t}}}w_{i{\sf t}}} \,.
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
