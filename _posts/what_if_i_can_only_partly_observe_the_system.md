---
title: "What if I can only partly observe the system?"
tag: "How can I trust the actions I take in simulations?"
draft: true
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how_can_a_simulation_be_wrong/sampling-prevalence.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how_can_a_simulation_be_wrong/additional-uncertainty-with-trajectories.svg"
aliases:
- "What if I can only partly observe the system?"
cites:
- "[[how_does_an_action_enter_a_simulation]]"
- "[[why_think_about_a_simulation_probabilistically]]"
- "[[how_can_i_trust_the_actions_i_take_in_simulations]]"
nocite: |
  @sargent2013
---

# What if I can only partly observe the system?
<div style="height:0.75em;"></div>

Consider the logic which our [[what_makes_an_action_good|action-to-outcome simulation]] might use when applied to the example of stopping mass treatment in a population when the prevalence of the disease has gone to 0.

Making this example more realistic; you are not normally able to test every individual person in the population for the true disease prevalence because this takes too long and it is too expensive. So you only regularly sample, e.g., 1000 random people out of 1 million.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how_can_a_simulation_be_wrong/sampling-prevalence.svg"/></center>

This immediately introduces a problem: how do you _know_ precisely when you have eliminated the disease? There is uncertainty in the exact state of the system at any moment in time.

So a more complete picture of the [[why_think_about_a_simulation_probabilistically|probabilistic view we had before]] must take into account additional uncertainty into the range of possible states and propagate this into additional uncertainty in the range in possible outcomes.

This essentially means more paths and possible outcomes.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how_can_a_simulation_be_wrong/additional-uncertainty-with-trajectories.svg"/></center>

The key takeaway from this is that even with a perfect simulation of the real world, the realities of real-world data gathering very often mean we can only get a _partial view_ of the true state of the system at best. This leads to additional uncertainty.

## References and further reading

::: {#refs}
:::
