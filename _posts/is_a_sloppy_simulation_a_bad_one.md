---
title: "Is a sloppy simulation a bad one?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/sloppiness-vs-parsimony.svg"
cites:
- "[[how_can_i_simulate_the_real_world]]"
- "[[how_does_a_simulation_learn_its_parameters_from_data]]"
nocite: |
  @transtrum2015, @gutenkunst2007, @mao2024
---

# Is a sloppy simulation a bad one?
<div style="height:0.75em;"></div>

Not necessarily, and often the opposite. Once a simulation can learn its parameters from real-world data, a natural next question is how sensitive the simulation-data fit is to changes in those parameters. In other words, how _sloppy_ is the simulation?

If a simulation is [sloppy](#ref-sethna2024sloppy) it means that it has many additional parameters which can be varied that do not strongly affect the quality of fit to the dataset of interest. We typically call this kind of parameter 'unconstrained' by the data.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/sloppiness-vs-parsimony.svg" width="650"/></center>

Simulation sloppiness sounds bad; but [it has been shown](#ref-mao2025) that machine learning models with more sloppiness have a tendency to generalise better to new datasets.

## References and further reading

::: {#refs}
:::
