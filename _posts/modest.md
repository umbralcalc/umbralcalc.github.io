---
title: Adaptive sequential Monte Carlo sampling with a discounted history
author: Hardwick, Robert J
date: [WIP]
concept: To describe the design and implementation of a sequential Monte Carlo sampler which can dynamically adapt to sampling new points from nonstationary, multivariate and potentially multi-modal distributions using only a stream of noisy weighted samples as input. We control the sensitivity of this algorithm to temporal changes in the target distribution through a discounted history approach.
articleId: modest
codeLink: https://github.com/umbralcalc/modest
year: [WIP]
---

## Problem statement

Say that we have a generator of probabilistic weights which takes a vector of parameters $z$ as input. This generator represents a non-stationary probability distribution and the weights are effectively stochastic around the true value for each given $z$ as input. The problem is that we would like to be able to efficiently sample from the underlying distribution regardless of its shape or modality.

Solution we will study is to create an adaptive sequential Monte Carlo algorithm, e.g., see [@del2006sequential] or [@wills2023sequential].

## Adaptively estimating a smoothed density

Idea is to dynamically train the noise vector $\sigma$ of a Gaussian Process-based [@williams2006gaussian] density estimation algorithm which can be used to calculate the latest density

$$
\begin{align}
Q_{{\sf t}+1}(z) &= \frac{\sum_{{\sf t}+1\geq {\sf t}'}\sum_{(w_{{\sf t}'},z_{{\sf t}'})}\beta^{{\sf t}+1-{\sf t}'}w_{{\sf t}'}{\sf NPDF}[z;0,C_{{\sf t}'}(z)]}{\sum_{{\sf t}+1\geq {\sf t}'}\sum_{w_{{\sf t}'}}\beta^{{\sf t}+1-{\sf t}'}w_{{\sf t}'}} \\
C^{ij}_{{\sf t}'}(z) &= \frac{\sum_{{\sf t}'\geq {\sf t}''}\sum_{(w_{{\sf t}''},z_{{\sf t}''})}\beta^{{\sf t}'-{\sf t}''}w_{{\sf t}''}(z-z_{{\sf t}'})^i(z-z_{{\sf t}''})^j}{\sum_{{\sf t}'\geq {\sf t}''}\sum_{w_{{\sf t}''}}\beta^{{\sf t}'-{\sf t}''}w_{{\sf t}''}} + (\sigma^i)^2\delta^{ij} \,,
\end{align}
$$

where: $\delta^{ij}$ is the Kronecker delta (taking a value of 1 when $i=j$, else 0); $(\sigma^i)^2$ is a weights variance scale associated to each dimension; and ${\sf NPDF}[z;0,C_{{\sf t}'}(z)]$ is the probability density function of a multivariate normal distribution. The adaptive learning occurs through minimising the following iterative cross-validation formula derived from the Kullback-Leibler divergence [@kullback1951information]

$$
\begin{align}
D_{\rm KL} &= \int_{\zeta_{{\sf t}+1}} {\rm d}z \, P_{{\sf t}+1}(z)\ln \frac{P_{{\sf t}+1}(z)}{Q_{{\sf t}}(z)} \\
&\simeq \frac{1}{\sum_{w_{{\sf t}+1}}w_{{\sf t}+1}}\sum_{(w_{{\sf t}+1},z_{{\sf t}+1})}w_{{\sf t}+1} \ln \frac{w_{{\sf t}+1}\sum_{{\sf t}\geq {\sf t}'}\sum_{w_{{\sf t}'}}\beta^{{\sf t}-{\sf t}'}w_{{\sf t}'}}{\sum_{{\sf t}\geq {\sf t}'}\sum_{(w_{{\sf t}'},z_{{\sf t}'})}\beta^{{\sf t}-{\sf t}'}w_{{\sf t}'}{\sf NPDF}[z_{{\sf t}+1};0,C_{{\sf t}'}(z_{{\sf t}+1})]} \,.
\end{align}
$$

Optimising the $D_{\rm KL}$ directly using gradients is likely to be a problem because the weights are only stochastically related to the underlying probabilities. This potential instability implies that it may be more robust to consider methods which do not rely on directly-computed gradients to optimise the objective, like using some kind of expectation-maximisation sampling (from an inverse-Wishart distribution using the weighted mean matrix from the history as input) with annealing where the weights are $\propto \beta e^{-\gamma D_{\rm KL}}$ and $\gamma$ is the annealing factor to the solution.

The modes are then detected by initialising a $z$-optimising step at time ${\sf t}$ with initial conditions set by all of the current samples and an objective given by the $Q_{{\sf t}+1}(z)$ formula.

Scaling in time history is probably the main nuisance here! Might motivate the use of Rust though since having a really good handle on what memory is actually necessary will be very useful.

## Resampling

- Start by drawing samples centred from different points, where each centre is randomly chosen from the current pool of samples with a frequency weighted by the kernel-smoothed new density of that point (this weight can be iteratively updated for each point so it's more efficient to reweight all of the current pool of points than to completely resample from scratch)
- If we then sample around each point using a locally-computed weighted (where the weights are the kernel-smoothed ones) covariance multiplied by some exploration factor $f \leq 1$ the resulting resampled points should be representative of the underlying density

## Implementation

Initial implementation should be in the stochadex to try out the ideas. Then the article can turn to implementing it from scratch in Rust (and a Python interop) using a custom shared-memory actor pattern design which improves on the initial design with the stochadex by allowing the number of samples to scale up or down dynamically through successive generations of actors producing more or less future actors.

Probably fits into the shared-memory actor pattern nicely!

## References
