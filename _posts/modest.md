---
title: Adaptive sequential Monte Carlo sampling from noisy weighted input samples
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

We can motivate the density smoothing model through specifying the following functional 'distribution over distributions' which uses a symmetrised form of the Kullback-Leibler divergence [@kullback1951information]

$$
\begin{align}
{\cal P}_{{\sf t}+1}[Q] &\propto e^{-D^{\rm sym}_{\rm KL}[Q,P_{{\sf t}+1}]} \\
D^{\rm sym}_{\rm KL}[Q,P_{{\sf t}+1}] &= \frac{1}{2}D_{\rm KL}[Q\vert\vert P_{{\sf t}+1}] + \frac{1}{2}D_{\rm KL}[P_{{\sf t}+1} \vert\vert Q] \\
 &= \frac{1}{2}\int {\rm d}Z \, Q(Z)\ln \frac{Q(Z)}{P_{{\sf t}+1}(Z)} + \frac{1}{2}\int {\rm d}Z \, P_{{\sf t}+1}(Z)\ln \frac{P_{{\sf t}+1}(Z)}{Q(Z)} \,,
\end{align}
$$

where we are using the state history matrix formalism used in [@stochadexI-2024] such that $Z$ corresponds to a matrix which adds a row for every new instantaneous $z$ state vector which time evolves to. Note that we can take 'functional expectation values' with this distribution, such that

$$
\begin{align}
{\rm E}_{{\sf t}+1}[Q(Z)] &= \frac{\int {\cal D}[Q(Z)] Q(Z) e^{-D^{\rm sym}_{\rm KL}[Q(Z),P_{{\sf t}+1}(Z)]}}{\int {\cal D}[Q(Z)] e^{-D^{\rm sym}_{\rm KL}[Q(Z),P_{{\sf t}+1}(Z)]}} \,.
\end{align}
$$

If we then expand $D^{\rm sym}_{\rm KL}$ logarithmically around $\ln P_{{\sf t}+1}$ such that $\ln Q=\ln P_{{\sf t}+1} + \delta \ln P_{{\sf t}+1}$, we arrive at the following approximation up to second order in the expansion

$$
\begin{align}
D^{\rm sym}_{\rm KL}[e^{\ln P_{{\sf t}+1} + \delta \ln P_{{\sf t}+1}},P_{{\sf t}+1}] &\simeq \frac{1}{2}\int {\rm d}Z \,P_{{\sf t}+1}(Z) [\delta \ln P_{{\sf t}+1}(Z)]^2 \,.
\end{align}
$$

Idea is to dynamically train the noise scale $\sigma$ and kernel bandwidth matrix $H$ of a Gaussian Process-based [@williams2006gaussian] density estimation algorithm which can be used to calculate the latest density

$$
\begin{align}
{\cal P}_{{\sf t}+1}[Q(z);H,\sigma] &\simeq \frac{\exp \bigg[ -\frac{1}{2} \sum_{{\sf t}+1\geq {\sf t}'}\sum_{{\sf t}'\geq {\sf t}''}\sum_{{\cal S}}(\ell_{{\sf t}'}-\ell)K^{-1}_{({\sf t}+1){\sf t}'{\sf t}''}(z;H,\sigma)(\ell_{{\sf t}''}-\ell) \bigg]}{\prod_{{\sf t}+1\geq {\sf t}'}\prod_{{\sf t}'\geq {\sf t}''}\prod_{{\cal S}}\sqrt{2\pi K_{({\sf t}+1){\sf t}'{\sf t}''}(z;H,\sigma)}} \,,
\end{align}
$$

where ${\cal S}$ indicates the set of weighted samples and we may choose to define the kernel $K_{({\sf t}+1){\sf t}'{\sf t}''}(z;H,\sigma)$ itself as

$$
\begin{align}
K_{({\sf t}+1){\sf t}'{\sf t}''}(z;H,\sigma) &= \sigma^2 \beta^{{\sf t}''-{\sf t}-1} B_{{\sf t}+1} \exp \bigg[ -\frac{1}{2}\sum_{i,j}(z_{{\sf t}'}-z)^i(H^{-1})^{ij}(z_{{\sf t}''}-z)^j\bigg] \\
B_{{\sf t}+1} &= \sum_{{\sf t}+1\geq {\sf t}'}\sum_{{\sf t}'\geq {\sf t}''}\sum_{{\cal S}}\beta^{{\sf t}+1-{\sf t}''} \,.
\end{align}
$$

If we were to vary $\ell$, $H$ and $\sigma$, the 'distribution over distributions' represents a probabilistic weighting for cross-validation which maximises when the best representation of $P_{{\sf t}+1}$ has been found. To find this maximum, we may use the gradient in the direction of the weights

$$
\begin{align}
\frac{\partial}{\partial \ell}\ln {\cal P}_{{\sf t}+1}[Q(z);H,\sigma] &\simeq \frac{1}{2} \sum_{{\sf t}+1\geq {\sf t}'}\sum_{{\sf t}'\geq {\sf t}''}\sum_{{\cal S}} \big[ (\ell_{{\sf t}'}-\ell)K^{-1}_{({\sf t}+1){\sf t}'{\sf t}''}(z;H,\sigma) + K^{-1}_{({\sf t}+1){\sf t}'{\sf t}''}(z;H,\sigma)(\ell_{{\sf t}''}-\ell) \big] \,,
\end{align}
$$

or the gradient defined over the $(H,\sigma)$ parameter space

$$
\begin{align}
&\frac{\partial}{\partial (H,\sigma )}\ln {\cal P}_{{\sf t}+1}[Q(z);H,\sigma] \simeq \\
&\qquad \quad \frac{1}{2}\sum_{{\sf t}+1\geq {\sf t}'}\sum_{{\sf t}'\geq {\sf t}''}\sum_{{\cal S}}\big[(\ell_{{\sf t}'}-\ell)K^{-1}_{({\sf t}+1){\sf t}'{\sf t}''}(z;H,\sigma)(\ell_{{\sf t}''}-\ell) - 1\big]\frac{\partial}{\partial (H,\sigma)}\ln K_{({\sf t}+1){\sf t}'{\sf t}''}(z;H,\sigma) \,,
\end{align}
$$

in either a global optimisation program or alternating between maximising individual samples with respect to $\ell$ and maximising globally with respect to $(H,\sigma)$.

Another pattern to consider is that of the Expectation-Maximisation algorithm, where we can alternate between optimising with respect to $\ell$ and computing the marginal expectation values for $H$ and $\sigma$ using the resulting samples and their corresponding weights like this

$$
\begin{align}
{\rm E}_{{\sf t}+1}[(H,\sigma )] &\simeq \frac{\sum_{z_{{\sf t}+1}} (H,\sigma ){\cal P}_{{\sf t}+1}[Q(z_{{\sf t}+1});H,\sigma]}{\sum_{z_{{\sf t}+1}}{\cal P}_{{\sf t}+1}[Q(z_{{\sf t}+1});H,\sigma]} \,.
\end{align}
$$

We could then input these expectation values as the centre of the sampler for the next $H$ (inverse-Wishart distribution) and $\sigma$ (Gaussian distribution) values in the sequence.

Scaling in time history is probably the main nuisance here! Might motivate the use of Rust though since having a really good handle on what memory is actually necessary will be very useful.

## Resampling

Start by drawing samples centred from different points, where each centre is randomly chosen from the current pool of samples with a frequency weighted by the smoothed new density of that point. If we then sample around each point using $fH$ as the covariance around the point (where $f$ is some exploration factor $<1$), we end up being able to effectively sample from the smoothed density.

## Implementation

Initial implementation should be in the stochadex to try out the ideas. Then the article can turn to implementing it from scratch in Rust (and a Python interop) using a custom shared-memory actor pattern design which improves on the initial design with the stochadex by allowing the number of samples to scale up or down dynamically through successive generations of actors producing more or less future actors.

Probably fits into the shared-memory actor pattern nicely!

The rough schematic for the simulation parameter posterior sampler is below.

![](../assets/modest/modest-previous-sampler.drawio.png)

We are suggesting to make the following change to this schematic.

![](../assets/modest/modest-modest-sampler.drawio.png)

## References
