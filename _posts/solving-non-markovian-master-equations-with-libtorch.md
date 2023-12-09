---
title: Solving non-Markovian master equations with Libtorch
author: Hardwick, Robert J.
date: [WIP]
concept: To study a variety of numerical solutions to non-Markovian phenomena. We do this by revealing different orders of temporal correlation that are present in the full master equation of a generalised non-Markovian process. By relating higher-order correlations to a form of time dependence in the pairwise correlation we then show how to numerically solve the system to obtain the time evolution of state probabilities. Since this computation can become very numerically intensive, the algorithm we discuss is implemented in C++ using the Libtorch library to achieve as much performance as possible.
bibtexId: hardwick-[WIP]
year: [WIP]
howPublished: https://umbralcalc.github.io/posts/solving-non-markovian-master-equations-with-libtorch.html
---

## Formalism recap

Let's recap the formalism introduced in [@worlds-of-observation-2023], which considers what happens to the probability that the state history matrix takes a particular set of values over time. To do this, we write down what is known as a _master equation_, which fully describes the time evolution of the _probability density function_ $P_{{\sf t}+1}(X\vert z)$ of $X_{0:{\sf t}+1}=X$ given that the parameters of the process are $z$. This can be written as

$$
\begin{aligned}
P_{{\sf t}+1}(X\vert z) &= P_{{\sf t}}(X'\vert z) P_{({\sf t}+1){\sf t}}(x\vert X',z)\,,
\end{aligned}
$$

where for the time being we are assuming the state space is continuous in each of the matrix elements and $P_{({\sf t}+1){\sf t}}(x\vert X',z)$ is the conditional probability that $X_{{\sf t}+1}=x$ given that $X_{0:{\sf t}}=X'$ at time ${\sf t}$ and the parameters of the process are $z$.

If we only consider the probability that the latest state history row is $X_{{\sf t}+1}=x$, it's possible to show that this is product of sub-domain integrals over each matrix row

$$
\begin{aligned}
P_{{\sf t}+1}(x\vert z) &= \frac{1}{{\sf t}}\sum_{{\sf t}''=0}^{{\sf t}} \int_{\Omega_{{\sf t}''}}{\rm d}X'' P_{{\sf t}''}(X''\vert z) P_{({\sf t}+1){\sf t}''}(x \vert X'',z)  \,.
\end{aligned}
$$

## Markovian phenomena

For Markovian phenomena, the equations no longer depend on timesteps older than the immediately previous one, hence the master equation over the latest row reduces to just

$$
\begin{aligned}
P_{{\sf t}+1}(x\vert z) &= \int_{\omega_{\sf t}}{\rm d}^nx' \, P_{\sf t}(x'\vert z) P_{({\sf t}+1){\sf t}}(x\vert x',z)  \,.
\end{aligned}
$$

By performing a Kramers-Moyal expansion on the $P_{({\sf t}+1){\sf t}}(x\vert x',z)$ distribution up to second order (limited by the Pawula theorem [@pawula1967generalizations]), we can approximate the right hand side of the Markovian master equation like this

$$
\begin{aligned}
P_{({\sf t}+1)}(x\vert z) &\simeq P_{{\sf t}}(x\vert z) - \sum_{i=0}^n\frac{\partial}{\partial x^i}\bigg[ f_{{\sf t}}(x,z)P_{{\sf t}}(x\vert z)\bigg] + \frac{1}{2}\sum_{i=0}^n\sum_{j=0}^n\frac{\partial}{\partial x^i}\frac{\partial}{\partial x^j}\bigg[ K_{{\sf t}}(x,z)P_{{\sf t}}(x\vert z)\bigg]  \,,
\end{aligned}
$$

where the components of $f_{{\sf t}}(x,z)$ and $K_{{\sf t}}(x,z)$ have been defined as

$$
\begin{aligned}
f^i_{{\sf t}}(x,z) &= \int_{\omega_{{\sf t}+1}} {\rm d}^nx' (x'-x)^iP_{({\sf t}+1){\sf t}}(x'\vert x,z) \\
K_{{\sf t}}^{ij}(x,z) &= \int_{\omega_{{\sf t}+1}} {\rm d}^nx' (x'-x)^i(x'-x)^jP_{({\sf t}+1){\sf t}}(x'\vert x,z)\,.
\end{aligned}
$$

By inspection of the expanded expression, we can define the `probability current'

$$
\begin{aligned}
J_{{\sf t}}(x,z) &= f_{{\sf t}}(x,z)P_{{\sf t}}(x\vert z) - \frac{1}{2}\sum_{j=0}^{n}\frac{\partial}{\partial x^j}\bigg[ K_{{\sf t}}(x,z)P_{{\sf t}}(x\vert z)\bigg] \,.
\end{aligned}
$$

If the probability current vanishes $J_{{\sf t}}(x,z)=0$ individually (this also implies that the distribution is stationary such that $P_{{\sf t}+1}(x\vert z)=P_{{\sf t}}(x\vert z)$ ), the implicit solution of the expanded expression can be found to be

$$
\begin{aligned}
P_{{\sf t}}(x\vert z) \propto K_{{\sf t}}^{-1}(x,z)\exp \bigg[ \int {\rm d}^nx\, K_{{\sf t}}^{-1}(x,z)f_{{\sf t}}(x,z)\bigg] \,.
\end{aligned}
$$

An analog of the Markovian master equation exists for discrete state spaces as well. We just need to replace the integral with a sum and the schematic would look something like this

$$
\begin{aligned}
P_{{\sf t}+1}(x\vert z) &= \sum_{\Omega_{{\sf t}}} P_{{\sf t}}(X'\vert z) P_{({\sf t}+1){\sf t}}(x \vert X', z) \,,
\end{aligned}
$$

where we note that the $P$'s in the expression above all now refer to _probability mass functions_.

## Non-Markovian phenomena

Returning back to the full master equation we wrote at the beginning. We can also approximate the probability $P_{{\sf t}+1}(X\vert z)$ with a logarithmic expansion like this

$$
\begin{aligned}
\ln P_{{\sf t}+1}(X\vert z) &\simeq \ln P_{{\sf t}+1}(X_* \vert z) + \frac{1}{2}\sum_{{\sf t}'=0}^{{\sf t}+1}\sum_{i=0}^{n}\sum_{j=0}^{n} (x-x_* )^i {\cal I}^{ij}_{({\sf t}+1){\sf t}'}(x_*,x'_*) (x'-x'_*)^j  \\
{\cal I}^{ij}_{({\sf t}+1){\sf t}'}(x_*,x'_*) &= \frac{\partial}{\partial x^i}\frac{\partial}{\partial (x')^j}\ln P_{{\sf t}+1}(X\vert z) \bigg\vert_{X=X_*} \,,
\end{aligned}
$$

where the values for $X=X_*$ are defined by the vanishing of the first derivative, i.e., these are chosen such that

$$
\begin{aligned}
\frac{\partial}{\partial x^i}\ln P_{{\sf t}+1}(X\vert z) \bigg\vert_{X=X_*} &= 0 \,.
\end{aligned}
$$

If we keep the truncation up to second order in the logarithmic expansion, note that this expression implies a pairwise correlation structure of the form

$$
\begin{aligned}
P_{{\sf t}+1}(X\vert z) &\rightarrow \prod_{{\sf t}'=0}^{{\sf t}}P_{({\sf t}+1){\sf t}'}(x,x'\vert z) = \prod_{{\sf t}'=0}^{{\sf t}}P_{{\sf t}'}(x'\vert z)P_{({\sf t}+1){\sf t}'}(x\vert x', z) \,.
\end{aligned}
$$

Given this pairwise temporal correlation structure, the master equation over the latest row reduces to this simpler sum of integrals

$$
\begin{aligned}
P_{{\sf t}+1}(x\vert z) &= \frac{1}{{\sf t}}\sum_{{\sf t}'=0}^{{\sf t}}\int_{\omega_{{\sf t}'}}{\rm d}^nx' P_{{\sf t}'}(x'\vert z)P_{({\sf t}+1){\sf t}'}(x\vert x',z)  \,.
\end{aligned}
$$

In a similar fashion, we can increase the truncation order of the logarithmic expansion to include third-order correlations such that

$$
\begin{aligned}
P_{{\sf t}+1}(X\vert z) &\rightarrow \prod_{{\sf t}'=0}^{{\sf t}}\prod_{{\sf t}''=0}^{{\sf t}'-1} P_{{\sf t}'{\sf t}''}(x',x''\vert z)P_{({\sf t}+1){\sf t}'{\sf t}''}(x\vert x',x'',z) \,,
\end{aligned}
$$

and, in this instance, one can show that the master equation over the latest row reduces to

$$
\begin{aligned}
P_{{\sf t}+1}(x\vert z) &= \frac{1}{{\sf t}}\sum_{{\sf t}'=0}^{{\sf t}}\frac{1}{{\sf t}'-1}\sum_{{\sf t}''=0}^{{\sf t}'-1}\int_{\omega_{{\sf t}'}}{\rm d}^nx'\int_{\omega_{{\sf t}''}}{\rm d}^nx'' P_{{\sf t}'{\sf t}''}(x',x''\vert z)P_{({\sf t}+1){\sf t}'{\sf t}''}(x\vert x',x'',z)  \,.
\end{aligned}
$$

Using $P_{{\sf t}'{\sf t}''}(x',x''\vert z) = P_{{\sf t}''}(x''\vert z) P_{{\sf t}'{\sf t}''}(x'\vert x'', z)$ one can also show that this integral is a marginalisation of this expression

$$
\begin{aligned}
P_{({\sf t}+1){\sf t}''}(x\vert x'', z) &= \frac{1}{{\sf t}}\sum_{{\sf t}'=0}^{{\sf t}}\int_{\omega_{{\sf t}'}}{\rm d}^nx'P_{{\sf t}'{\sf t}''}(x'\vert x'',z)P_{({\sf t}+1){\sf t}'{\sf t}''}(x\vert x',x'',z) \,,
\end{aligned}
$$

which describes the time evolution of the conditional probabilities.

Let's imagine that $x$ is just a scalar (as opposed to a row vector) for simplicity in the expressions. We can then discretise the 1D space over $x$ into separate $i$-labelled regions such that $P^i_{{\sf t}+1} - P^i_{{\sf t}} = {\cal J}^i_{{\sf t}+1}$, where the probability current ${\cal J}^i_{{\sf t}+1}$ for the factorised processes above would be defined as

$$
\begin{aligned}
{\cal J}^i_{{\sf t}+1} &= - P^i_{{\sf t}} + \frac{1}{{\sf t}}\sum_{{\sf t}'=0}^{{\sf t}}\sum_{i'=0}^N\Delta x P_{{\sf t}'}^{i'} P_{({\sf t}+1){\sf t}'}^{ii'} \\
{\cal J}^i_{{\sf t}+1} &= - P^i_{{\sf t}} + \frac{1}{{\sf t}}\sum_{{\sf t}'=1}^{{\sf t}}\frac{1}{{\sf t}'-1}\sum_{{\sf t}''=0}^{{\sf t}'-1}\sum_{i'=0}^N\sum_{i''=0}^N\Delta x^2P_{{\sf t}''}^{i''}P_{{\sf t}'{\sf t}''}^{i'i''}P^{ii'i''}_{({\sf t}+1){\sf t}'{\sf t}''}\,.
\end{aligned}
$$

The $P^{ii'i''}_{({\sf t}+1){\sf t}'{\sf t}''}$ tensor, in particular, will have $N^3{\sf t}({\sf t}^2-1)$ elements. Note that the third-order temporal correlations can be evolved by identifying the pairwise conditional probabilities as time-dependent state variables and evolving them according to the following relation

$$
\begin{aligned}
P_{({\sf t}+1){\sf t}''}^{ii''} &= \frac{1}{{\sf t}}\sum_{{\sf t}'=1}^{{\sf t}}\sum_{i'=0}^N\Delta xP_{{\sf t}'{\sf t}''}^{i'i''}P_{({\sf t}+1){\sf t}'{\sf t}''}^{ii'i''}\,.
\end{aligned}
$$

The code is being developed here: [https://github.com/umbralcalc/dennm-torch](https://github.com/umbralcalc/dennm-torch).

## References
