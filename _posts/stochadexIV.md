---
title: Online learning of arbitrary probability distributions using a simulation engine
author: Hardwick, Robert J
date: [WIP]
concept: To describe the design and implementation of a sequential Monte Carlo sampler which can dynamically adapt to sampling new points from nonstationary, multivariate and potentially multi-modal distributions using only a stream of noisy weighted samples as input. We control the sensitivity of this algorithm to temporal changes in the target distribution through a discounted history approach.
articleId: stochadexIV
codeLink: https://github.com/umbralcalc/stochadex
year: [WIP]
---

## Research context

**Rewrite this article from the perspective of not just inferring $P(z)$ but also $P(x)$!**

In a previous article [@stochadexIII-2024] we used a simple, but effective, technique for approximating the conditional density of simulation parameters $P_{({\sf t}+1){\sf t}}(z\vert X',{\sf Y})$ such that we are able to both update its shape with the arrival of new data as well as sample new values from it --- in both cases being able to incorporate a discounted distribution ansatz into the model. This technique estimated only the first two moments of this distribution, but with techniques like particle filtering it should be possible to generate approximate samples without this limitation. In this article, we will motivate Sequential Importance Resampling (SIR) using a kernel-smoothed approximation of the distribution which takes the form

$$
\begin{align}
P_{({\sf t}+1){\sf t}}(z\vert X',{\sf Y}) &\simeq \int_{\zeta_{{\sf t}+1}} {\rm d}z' P_{({\sf t}+1){\sf t}}(z'\vert X',{\sf Y})K(z,z';H) \,,
\end{align}
$$

where $K(z,z';H)$ is some smoothing kernel which helps to approximate the posterior distribution up to some specified scale using the bandwidth matrix $H$. Note that the expression above can also be extended to make use of the full history of $z$ samples by applying the discount factor $\beta$.

## Problem statement

Say that we have a generator of probabilistic weights which takes a state history matrix $X$ as input. This generator represents a non-stationary probability distribution and the weights are effectively stochastic around the true value for each given $X$ as input. The problem is that we would like to be able to efficiently sample from the underlying distribution regardless of its shape or modality.

Solution we will study is to create an adaptive sequential Monte Carlo algorithm, e.g., see [@del2006sequential] or [@wills2023sequential].

## Adaptively estimating a smoothed density

We can motivate the density smoothing model through specifying the following functional 'distribution over distributions' which uses a symmetrised form of the Kullback-Leibler divergence [@kullback1951information]

$$
\begin{align}
{\cal P}_{{\sf t}+1}[Q] &\propto e^{-D^{\rm sym}_{\rm KL}[Q,P_{{\sf t}+1}]} \\
D^{\rm sym}_{\rm KL}[Q,P_{{\sf t}+1}] &= \frac{1}{2}D_{\rm KL}[Q\vert\vert P_{{\sf t}+1}] + \frac{1}{2}D_{\rm KL}[P_{{\sf t}+1} \vert\vert Q] \\
 &= \frac{1}{2}\int_{\Omega_{{\sf t}+1}} {\rm d}X \, Q(X)\ln \frac{Q(X)}{P_{{\sf t}+1}(X)} + \frac{1}{2}\int_{\Omega_{{\sf t}+1}} {\rm d}X \, P_{{\sf t}+1}(X)\ln \frac{P_{{\sf t}+1}(X)}{Q(X)} \,,
\end{align}
$$

where we are using the state history matrix formalism used in [@stochadexI-2024] and [@stochadexII-2024] such that $X$ corresponds to a matrix which adds a row for every new instantaneous $x$ state vector which time evolves to. Note that we can take 'functional expectation values' with this distribution, such that

$$
\begin{align}
{\rm E}_{{\sf t}+1}[Q(X)] &= \frac{\int {\cal D}[Q(X)] Q(X) e^{-D^{\rm sym}_{\rm KL}[Q(X),P_{{\sf t}+1}(X)]}}{\int {\cal D}[Q(X)] e^{-D^{\rm sym}_{\rm KL}[Q(X),P_{{\sf t}+1}(X)]}} \,.
\end{align}
$$

If we then expand $D^{\rm sym}_{\rm KL}$ logarithmically around $\ln P_{{\sf t}+1}$ such that $\ln Q=\ln P_{{\sf t}+1} + \delta \ln P_{{\sf t}+1}$, we arrive at the following approximation up to second order in the expansion

$$
\begin{align}
D^{\rm sym}_{\rm KL}[e^{\ln P_{{\sf t}+1} + \delta \ln P_{{\sf t}+1}},P_{{\sf t}+1}] &\simeq \frac{1}{2}\int_{\Omega_{{\sf t}+1}} {\rm d}X \,P_{{\sf t}+1}(X) [\delta \ln P_{{\sf t}+1}(X)]^2 \,.
\end{align}
$$

Idea is to dynamically train the noise scale $\sigma$ and kernel bandwidth matrix $H$ of a Gaussian Process-based [@williams2006gaussian] density estimation algorithm which can be used to calculate the latest density

$$
\begin{align}
{\cal P}_{{\sf t}+1}[Q(x);H,\sigma] &\simeq \frac{\exp \bigg[ -\frac{1}{2} \sum_{{\sf t}+1\geq {\sf t}'}\sum_{{\sf t}'\geq {\sf t}''}\sum_{{\cal S}}(\ell_{{\sf t}'}-\ell)K^{-1}_{({\sf t}+1){\sf t}'{\sf t}''}(x;H,\sigma)(\ell_{{\sf t}''}-\ell) \bigg]}{\prod_{{\sf t}+1\geq {\sf t}'}\prod_{{\sf t}'\geq {\sf t}''}\prod_{{\cal S}}\sqrt{2\pi K_{({\sf t}+1){\sf t}'{\sf t}''}(x;H,\sigma)}} \,,
\end{align}
$$

where ${\cal S}$ indicates the set of weighted samples and we may choose to define the kernel $K_{({\sf t}+1){\sf t}'{\sf t}''}(x;H,\sigma)$ itself as

$$
\begin{align}
K_{({\sf t}+1){\sf t}'{\sf t}''}(x;H,\sigma) &= \sigma^2 \beta^{{\sf t}''-{\sf t}-1} B_{{\sf t}+1} \exp \bigg[ -\frac{1}{2}\sum_{i,j}(x_{{\sf t}'}-x)^i(H^{-1})^{ij}(x_{{\sf t}''}-x)^j\bigg] \\
B_{{\sf t}+1} &= \sum_{{\sf t}+1\geq {\sf t}'}\sum_{{\sf t}'\geq {\sf t}''}\sum_{{\cal S}}\beta^{{\sf t}+1-{\sf t}''} \,.
\end{align}
$$

If we were to vary $\ell$, $H$ and $\sigma$, the 'distribution over distributions' represents a probabilistic weighting for cross-validation which maximises when the best representation of $P_{{\sf t}+1}$ has been found. To find this maximum, we may use the gradient in the direction of the weights

$$
\begin{align}
\frac{\partial}{\partial \ell}\ln {\cal P}_{{\sf t}+1}[Q(x);H,\sigma] &\simeq \frac{1}{2} \sum_{{\sf t}+1\geq {\sf t}'}\sum_{{\sf t}'\geq {\sf t}''}\sum_{{\cal S}} \big[ (\ell_{{\sf t}'}-\ell)K^{-1}_{({\sf t}+1){\sf t}'{\sf t}''}(x;H,\sigma) + K^{-1}_{({\sf t}+1){\sf t}'{\sf t}''}(x;H,\sigma)(\ell_{{\sf t}''}-\ell) \big] \,,
\end{align}
$$

or the gradient defined over the $(H,\sigma)$ parameter space

$$
\begin{align}
&\frac{\partial}{\partial (H,\sigma )}\ln {\cal P}_{{\sf t}+1}[Q(x);H,\sigma] \simeq \\
&\qquad \quad \frac{1}{2}\sum_{{\sf t}+1\geq {\sf t}'}\sum_{{\sf t}'\geq {\sf t}''}\sum_{{\cal S}}\big[(\ell_{{\sf t}'}-\ell)K^{-1}_{({\sf t}+1){\sf t}'{\sf t}''}(x;H,\sigma)(\ell_{{\sf t}''}-\ell) - 1\big]\frac{\partial}{\partial (H,\sigma)}\ln K_{({\sf t}+1){\sf t}'{\sf t}''}(x;H,\sigma) \,,
\end{align}
$$

in either a global optimisation program or alternating between maximising individual samples with respect to $\ell$ and maximising globally with respect to $(H,\sigma)$.

Another pattern to consider is that of the Expectation-Maximisation algorithm, where we can alternate between optimising with respect to $\ell$ and computing the marginal expectation values for $H$ and $\sigma$ using the resulting samples and their corresponding weights like this

$$
\begin{align}
{\rm E}_{{\sf t}+1}[(H,\sigma )] &\simeq \frac{\sum_{X_{{\sf t}+1}} (H,\sigma ){\cal P}_{{\sf t}+1}[Q(X_{{\sf t}+1});H,\sigma]}{\sum_{X_{{\sf t}+1}}{\cal P}_{{\sf t}+1}[Q(X_{{\sf t}+1});H,\sigma]} \,.
\end{align}
$$

We could then input these expectation values as the centre of the sampler for the next $H$ (inverse-Wishart distribution) and $\sigma$ (Gaussian distribution) values in the sequence.

Scaling in time history is probably the main nuisance here! Performance tweaking via controlling the state history depth of the stochadex will become important.

## Resampling

Start by drawing samples centred from different points, where each centre is randomly chosen from the current pool of samples with a frequency weighted by the smoothed new density of that point. If we then sample around each point using $fH$ as the covariance around the point (where $f$ is some exploration factor $<1$), we end up being able to effectively sample from the smoothed density.

## Implementation

In order to get this to work:

- Gaussian processes will need to be implemented in the stochadex framework
- Online learning via gradients will need to be implemented as well

**Notes migrated from another article which are now more relevant here:**

In the case of the purely time-dependent kernel with a choice of Gaussian data linking distribution above, the hyperparameters that would be optimised could relate to the kernel in a wide variety of ways. Optimising them would make our optimised reweighting similar to (but very much _not_ the same as) evaluating maximum a posteriori (MAP) of a Gaussian process regression. In a Gaussian process regression, one is concerned with inferring the the whole of $X_{{\sf t}}$ as a function of time using the pairwise correlations implied by the second-order log expansion we wrote earlier. Based on this expression, the cumulative log-likelihood for a Gaussian process can be calculated as follows

$$
\begin{align}
\ln {\cal L}_{{\sf t}+1}(Y\vert z) &= -\frac{1}{2}\sum_{{\sf t}'=({\sf t}+1)-{\sf s}}^{({\sf t}+1)}\sum_{{\sf t}''=({\sf t}+1)-{\sf s}}^{{\sf t}'} \bigg[ n\ln (2\pi ) + \ln \big\vert {\cal H}_{{\sf t}'{\sf t}''}(z)\big\vert + \sum_{i=0}^{n}\sum_{j=0}^{n} Y^i_{{\sf t}'} {\cal H}^{ij}_{{\sf t}'{\sf t}''}(z) Y^j_{{\sf t}''} \bigg] \,. \label{eq:log-likelihood-gaussian-proc}
\end{align}
$$

**Rewrite from here to cover the theory behind optimisation code that will be put into practice in the follow-up article...**

As we did for the reweighting algorithm, we have illustrated another rough schematic below for the multi-threaded code needed to compute the objective function of a learning algorithm in the stochadex, based on the equation above. Note that, in this diagram, we have assumed that the data has already been shifted such that its values are positioned around the distribution peak. Knowing where this peak will be a priori is not possible. However, for Gaussian data, an unbiased estimator for this peak will be the sample mean and so we have included an initial data standardisation in the steps outlined by the schematic.

![](../assets/stochadexIV/stochadexIV-gaussian-process-code.drawio.png)

**Here should also talk about how this paper shows online learning of gradients should equilibrate and then be used for debiasing the predictions:** [@angelopoulos2025gradientequilibriumonlinelearning]

The optimisation approach that we choose to use for obtaining the best hyperparameters in the conditional probability of the reweighting approach will depend on a few factors. For example, if the number of hyperparameters is relatively low, but their gradients are difficult to calculate exactly; then a gradient-free optimiser (such as the Nelder-Mead [@nelder1965simplex] method or something like a particle swarm; see [@kennedy1995particle] or [@shi1998modified]) would likely be the most effective choice. On the other hand, when the number of hyperparameters ends up being relatively large, it's usually quite desirable to utilise the gradients in algorithms like vanilla Stochastic Gradient Descent [@robbins1951stochastic] (SGD) or Adam [@kingma2014adam].

## References
