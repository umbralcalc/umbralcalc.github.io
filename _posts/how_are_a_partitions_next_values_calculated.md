---
title: "How are a partition's next values calculated?"
tag: "How can I simulate the real world?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partition-histories.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/partition-iteration.svg"
aliases:
- "How are a partition's next values calculated?"
cites:
- "[[what_is_a_state_partition]]"
- "[[what_decides_when_the_next_timestep_happens]]"
- "[[how_can_i_simulate_the_real_world_introduction]]"
nocite: |
  @durbinkoopman2012
---

# How are a partition's next values calculated?
<div style="height:0.75em;"></div>

For an overall simulation data view, we can create a 'state partition histories' structure. This is a collection of each state partition history that exists within the simulation.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partition-histories.svg" width=600/></center>

How do we determine the 'next values' of each state partition in time?

This is where we should maintain full flexibility in choice of calculation so that our simulation is able to represent many different real-world systems.

Each of these calculations for a given partition specifies how the state partition histories and cumulative timesteps history data are used to determine the next values of the state partition.

In order to support even more flexibility in configuration, the calculation should also take in a set of parameters which are specific to that partition.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/partition-iteration.svg" /></center>

## References and further reading

::: {#refs}
:::
