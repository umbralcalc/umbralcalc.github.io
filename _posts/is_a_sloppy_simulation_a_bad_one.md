---
title: "Is a sloppy simulation a bad one?"
tag: "How can I simulate the real world?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/sloppiness-vs-parsimony.svg"
aliases:
- "Is a sloppy simulation a bad one?"
cites:
- "[[how_does_a_simulation_learn_its_parameters_from_data]]"
- "[[how_can_i_simulate_the_real_world]]"
nocite: |
  @transtrum2015, @gutenkunst2007, @mao2024
---

# Is a sloppy simulation a bad one?
<div style="height:0.75em;"></div>

So we have a simulation which is able to learn its parameters from real world data.

How sensitive is the simulation-data fit to changes in the parameters? In other words, how _sloppy_ is the simulation?

If a simulation is [sloppy](https://sethna.lassp.cornell.edu/Teaching/BasicTraining/SloppyBT24.html) it means that it has many additional parameters which can be varied that do not strongly affect the quality of fit to the dataset of interest. We typically call this kind of parameter 'unconstrained' by the data.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/sloppiness-vs-parsimony.svg" width="650"/></center>

Simulation sloppiness sounds bad; but [it has been shown](https://arxiv.org/abs/2505.08915) that machine learning models with more sloppiness have a tendency to generalise better to new datasets.

## References and further reading

::: {#refs}
:::
