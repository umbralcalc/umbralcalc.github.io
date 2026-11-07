---
title: How are the histories updated after a step?
tag: How can I simulate the real world?
images:
  - https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/update-time-history.svg
aliases:
  - How are the histories updated after a step?
cites:
  - "[[how_are_a_partitions_next_values_calculated]]"
  - "[[how_can_i_simulate_the_real_world]]"
---

# How are the histories updated after a step?
<div style="height:0.75em;"></div>

Having calculated the next values of each state partition and the next timestep, we should perform operations over the cumulative timesteps history and each state partition history to update their structures with this new data.

This is an important procedure to perform all at once to ensure that the all of the state partitions in the simulation are synchronised against its virtual clock.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/update-time-history.svg" /></center>

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/update-state-partition-history.svg" /></center>

## References and further reading

::: {#refs}
:::
