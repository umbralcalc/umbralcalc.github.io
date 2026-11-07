---
title: "How do I set up a simulation to learn a policy?"
tag: "How do I automate taking actions with simulations?"
draft: true
aliases:
- "How do I set up a simulation to learn a policy?"
cites:
- "[[what_is_a_policy]]"
- "[[what_is_a_state_partition]]"
- "[[how_do_i_automate_taking_actions_with_simulations_introduction]]"
nocite: |
  @suttonbarto2018
---

# How do I set up a simulation to learn a policy?
<div style="height:0.75em;"></div>

Learning using the simulation itself (evolutionary strategies, monte carlo tree search and touch on how these are different to Deep RL but still in the same family of sample-driven - which depend on simulations existing)

If we want to learn parameters which correspond to optimal simulation trajectories, we first need to specify what 'optimal' means.

We do this by defining an objective whose maximum/minimum possible value will be achieved when our goal is met.

For instance, we may define some logic in a state partition iteration of the simulation which replicates taking 'actions' in the real world. This logic can depend on the simulation parameters so that the latter encodes the behaviour quantitatively.

<!-- diagram of setup -->

Given this setup, a very common goal of interest is then in finding the best actions to take; which is analogous to optimising the parameters of the action-taking state partition iteration. We will refer to these parameters as 'policy parameters'.

But what should be use as an objective?

## References and further reading

::: {#refs}
:::
