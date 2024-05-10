---
title: Evolutionary distribution mode sampling with a discounted history
author: Hardwick, Robert J
date: [WIP]
concept: To describe the design of a new algorithm which can dynamically learn and sample new points from multi-modal distributions, which are themselves represented only by a history of noisy weighted log-probability samples.
articleId: modesampler
codeLink: https://github.com/umbralcalc/modesampler
year: [WIP]
---

## Online learning the density

- Discounted evolutionary kernel density clustering based on optimising joint $(z,h)$ for each mode-clustered sample group
- Upshot of this ^ is you get the maximum of each mode for free as a byproduct
- Need to figure out how to separate the logic for optimising just $h$ (to capture heterogeneity - do we need this even?) vs optimising a suspected mode with $(z,h)$
- Also fits into the actor pattern nicely!

## Sampling

- Ensemble slice sampling using rejection step?
  1. Choose starting $z$ value and validate that $p(z)>0$
  2. Sample the next $p$ value uniformally between $0$ and $p(z)$
  3. Use rejection sampling to find new $z$ which has a bigger $p$ than the last
  4. Return to 2.
- Maybe the proposal could be better informed by using a Gaussian approximation to local mode density (maybe even restricted to the samples in a specific quartile)?

## References
