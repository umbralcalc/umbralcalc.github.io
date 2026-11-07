---
title: "How does a simulation keep track of time?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/cumulative-timesteps-history.svg"
cites:
- "[[how_can_i_simulate_the_real_world]]"
nocite: |
  @lawkelton2014
---

# How does a simulation keep track of time?
<div style="height:0.75em;"></div>

Time is probably the most important variable to track in a simulation. This is because everything that happens within a simulation only has meaning with respect to the real world if we can trace what point in simulated time that it happened.

Time is a variable in the simulation which always increases in value. We often want to track how it increases after each discrete simulation 'step' in increments which we shall call 'timesteps'.

The first data structure which we shall introduce here is a 'cumulative timesteps history', which indexes simulated times that the simulation _had_ according to _decreasing recency_.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/cumulative-timesteps-history.svg" width=600/></center>

## References and further reading

::: {#refs}
:::
