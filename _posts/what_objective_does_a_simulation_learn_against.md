---
title: "What objective does a simulation learn against?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/objectives.svg"
cites:
- "[[why_should_i_simulate_the_real_world]]"
- "[[how_do_we_get_probabilities_back_from_statistics]]"
nocite: |
  @cranmer2020
---

# What objective does a simulation learn against?
<div style="height:0.75em;"></div>

One we design ourselves, which either scores how closely the simulation replicates data or names the quantity we want to optimise.

Unlike machine learning models, which typically come with standard training algorithms (like [backpropagation](#ref-wiki_backpropagation) for neural networks), simulations often need us to explicitly choose and design procedures for learning their parameters from real-world data or optimising their outputs.

In order to do this, we must first have some objective which either characterises how close simulation trajectories are to replicating the data we have or define the quantity we want to optimise.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/objectives.svg"/></center>

There are a number of techniques we can use to specify what the objective should be, depending on the purpose.

## References and further reading

::: {#refs}
:::
