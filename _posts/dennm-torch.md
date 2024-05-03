---
title: Solving non-Markovian master equations with Libtorch
author: Hardwick, Robert J
date: [WIP]
concept: To study a variety of numerical solutions to non-Markovian phenomena. We do this by revealing different orders of temporal correlation that are present in the full master equation of a generalised non-Markovian process. By relating higher-order correlations to a form of time dependence in the pairwise correlation we then show how to numerically solve the system to obtain the time evolution of state probabilities. Since this computation can become very numerically intensive, the algorithm we discuss is implemented in C++ using the Libtorch library to achieve as much performance as possible.
articleId: dennm-torch
codeLink: https://github.com/umbralcalc/dennm-torch
year: [WIP]
---

## Formalism recap

Let's recall the formalism introduced in [@stochadexII-WIP], which considers what happens to the probability that the state history matrix takes a particular set of values over time. To do this, we write down what is known as a _master equation_, which fully describes the time evolution of the _probability density function_ $P_{{\sf t}+1}(X\vert z)$ of $X_{({\sf t}+1)-{\sf s}:({\sf t}+1)}=X$ given that the parameters of the process are $z$ and the state history window size is ${\sf s}$. This can be written as

$$
\begin{aligned}
P_{{\sf t}+1}(X\vert z) &= P_{{\sf t}}(X'\vert z) P_{({\sf t}+1){\sf t}}(x\vert X',z)\,,
\end{aligned}
$$

where for the time being we are assuming the state space is continuous in each of the matrix elements and $P_{({\sf t}+1){\sf t}}(x\vert X',z)$ is the conditional probability that $X_{{\sf t}+1}=x$ given that $X_{{\sf t}-{\sf s}:{\sf t}}=X'$ at time ${\sf t}$ and the parameters of the process are $z$.

If we only consider the probability that the latest state history row is $X_{{\sf t}+1}=x$, it's possible to show that this is product of sub-domain integrals over each matrix row

$$
\begin{aligned}
P_{{\sf t}+1}(x\vert z) &= \frac{1}{{\sf t}}\sum_{{\sf t}''={\sf t}-{\sf s}}^{{\sf t}} \int_{\Omega_{{\sf t}''}}{\rm d}X'' P_{{\sf t}''}(X''\vert z) P_{({\sf t}+1){\sf t}''}(x \vert X'',z)  \,.
\end{aligned}
$$

## Non-Markovian phenomena

Let's now return back to the full master equation we wrote at the beginning. As was shown in [@stochadexII-WIP], we can also approximate the probability $P_{{\sf t}+1}(X\vert z)$ with a logarithmic expansion like this

$$
\begin{aligned}
\ln P_{{\sf t}+1}(X\vert z) &\simeq \ln P_{{\sf t}+1}(X_* \vert z) + \frac{1}{2}\sum_{{\sf t}'=({\sf t}+1)-{\sf s}}^{({\sf t}+1)}\sum_{i=0}^{n}\sum_{j=0}^{n} (x-x_* )^i {\cal I}^{ij}_{({\sf t}+1){\sf t}'}(z) (x'-x'_*)^j  \\
{\cal I}^{ij}_{({\sf t}+1){\sf t}'}(z) &= \frac{\partial}{\partial x^i}\frac{\partial}{\partial (x')^j}\ln P_{{\sf t}+1}(X\vert z) \bigg\vert_{X=X_*} \,,
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
P_{{\sf t}+1}(X\vert z) &\rightarrow \prod_{{\sf t}'={\sf t}-{\sf s}}^{{\sf t}}P_{({\sf t}+1){\sf t}'}(x,x'\vert z) = \prod_{{\sf t}'={\sf t}-{\sf s}}^{{\sf t}}P_{{\sf t}'}(x'\vert z)P_{({\sf t}+1){\sf t}'}(x\vert x', z) \,.
\end{aligned}
$$

Given this pairwise temporal correlation structure, the master equation over the latest row reduces to this simpler sum of integrals

$$
\begin{aligned}
P_{{\sf t}+1}(x\vert z) &= \frac{1}{{\sf t}}\sum_{{\sf t}'={\sf t}-{\sf s}}^{{\sf t}}\int_{\omega_{{\sf t}'}}{\rm d}^nx' P_{{\sf t}'}(x'\vert z)P_{({\sf t}+1){\sf t}'}(x\vert x',z)  \,.
\end{aligned}
$$

In a similar fashion, we can increase the truncation order of the logarithmic expansion to include third-order correlations such that

$$
\begin{aligned}
P_{{\sf t}+1}(X\vert z) &\rightarrow \prod_{{\sf t}'={\sf t}-{\sf s}}^{{\sf t}}\prod_{{\sf t}''={\sf t}-{\sf s}}^{{\sf t}'-1} P_{{\sf t}'{\sf t}''}(x',x''\vert z)P_{({\sf t}+1){\sf t}'{\sf t}''}(x\vert x',x'',z) \,,
\end{aligned}
$$

and, in this instance, one can show that the master equation over the latest row reduces to

$$
\begin{aligned}
P_{{\sf t}+1}(x\vert z) &= \frac{1}{{\sf t}}\sum_{{\sf t}'={\sf t}-{\sf s}}^{{\sf t}}\frac{1}{{\sf t}'-1}\sum_{{\sf t}''={\sf t}-{\sf s}}^{{\sf t}'-1}\int_{\omega_{{\sf t}'}}{\rm d}^nx'\int_{\omega_{{\sf t}''}}{\rm d}^nx'' P_{{\sf t}'{\sf t}''}(x',x''\vert z)P_{({\sf t}+1){\sf t}'{\sf t}''}(x\vert x',x'',z)  \,.
\end{aligned}
$$

Using $P_{{\sf t}'{\sf t}''}(x',x''\vert z) = P_{{\sf t}''}(x''\vert z) P_{{\sf t}'{\sf t}''}(x'\vert x'', z)$ one can also show that this integral is a marginalisation of this expression

$$
\begin{aligned}
P_{({\sf t}+1){\sf t}''}(x\vert x'', z) &= \frac{1}{{\sf t}}\sum_{{\sf t}'={\sf t}-{\sf s}}^{{\sf t}}\int_{\omega_{{\sf t}'}}{\rm d}^nx'P_{{\sf t}'{\sf t}''}(x'\vert x'',z)P_{({\sf t}+1){\sf t}'{\sf t}''}(x\vert x',x'',z) \,,
\end{aligned}
$$

which describes the time evolution of the conditional probabilities.

## Discretising and working with Libtorch

Let's now imagine that $x$ is just a scalar (as opposed to a row vector) for simplicity in the expressions. We can then discretise the 1D space over $x$ into separate $i$-labelled regions such that $P^i_{{\sf t}+1} - P^i_{{\sf t}} = {\cal J}^i_{{\sf t}+1}$, where the probability current ${\cal J}^i_{{\sf t}+1}$ for the factorised processes above would be defined as

$$
\begin{aligned}
{\cal J}^i_{{\sf t}+1} &= - P^i_{{\sf t}} + \frac{1}{{\sf t}}\sum_{{\sf t}'={\sf t}-{\sf s}}^{{\sf t}}\sum_{i'=0}^N\Delta x P_{{\sf t}'}^{i'} P_{({\sf t}+1){\sf t}'}^{ii'} \\
{\cal J}^i_{{\sf t}+1} &= - P^i_{{\sf t}} + \frac{1}{{\sf t}}\sum_{{\sf t}'={\sf t}-{\sf s}}^{{\sf t}}\frac{1}{{\sf t}'-1}\sum_{{\sf t}''={\sf t}-{\sf s}}^{{\sf t}'-1}\sum_{i'=0}^N\sum_{i''=0}^N\Delta x^2P_{{\sf t}''}^{i''}P_{{\sf t}'{\sf t}''}^{i'i''}P^{ii'i''}_{({\sf t}+1){\sf t}'{\sf t}''}\,.
\end{aligned}
$$

The $P^{ii'i''}_{({\sf t}+1){\sf t}'{\sf t}''}$ tensor, in particular, will have $N^3{\sf t}({\sf t}^2-1)$ elements. Note that the third-order temporal correlations can be evolved by identifying the pairwise conditional probabilities as time-dependent state variables and evolving them according to the following relation

$$
\begin{aligned}
P_{({\sf t}+1){\sf t}''}^{ii''} &= \frac{1}{{\sf t}}\sum_{{\sf t}'={\sf t}-{\sf s}}^{{\sf t}}\sum_{i'=0}^N\Delta xP_{{\sf t}'{\sf t}''}^{i'i''}P_{({\sf t}+1){\sf t}'{\sf t}''}^{ii'i''}\,.
\end{aligned}
$$

Pytorch provides a C++ API known as Libtorch [@libtorch] which can be used as a library to handle the abstractions of tensor operations in a computationally efficent way. The key libary calls which will make the operations above possible are $\texttt{torch::tensordot}$ (to handle contractions over indices between different tensors) and $\texttt{torch::cat}$ (to extend the windowed state history from initialisation up to the point at which the full state history window size is reached).

The discretised iteration formulae above have been implemented with Libtorch in this small C++ package here: [https://github.com/umbralcalc/dennm-torch](https://github.com/umbralcalc/dennm-torch). Possible extensions to this work include implementing even higher-order correlations as well as trying out some specific systems.

## References
