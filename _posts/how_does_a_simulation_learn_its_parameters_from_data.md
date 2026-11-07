---
title: "How does a simulation learn its parameters from data?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/data-streaming.svg"
cites:
- "[[how_can_i_simulate_the_real_world]]"
- "[[what_objective_does_a_simulation_learn_against]]"
- "[[what_is_a_state_partition]]"
nocite: |
  @cranmer2020, @gordon1993
---

# How does a simulation learn its parameters from data?
<div style="height:0.75em;"></div>

If we want to learn the parameters which correspond to simulation trajectories fitting real-world data trends more closely, it is natural to use an objective based on the probabilities of state partition histories.

We start by streaming time-series data into our simulation by specifying it as a state partition.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/data-streaming.svg" width="650"/></center>

We can then use a method to estimate the probabilities of state values within the data, e.g., probabilistic sample weighting.

So we have a way to calculate these 'data probabilities' for any possible state values the data can take in time.

By then evaluating these data probabilities at the points which coincide with simulation trajectories, we have an objective which quantifies how close the simulation is to the data.

When talking about different values for this objective, we often use the terminology 'quality of fit' or 'fit to the data' to describe how close the simulation is to replicating the data, and hence how good the value of the objective is.

## References and further reading

::: {#refs}
:::
