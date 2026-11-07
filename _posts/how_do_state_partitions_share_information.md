---
title: How do state partitions share information?
images:
  - https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/partition-timeline-composition.svg
cites:
  - "[[how_can_i_simulate_the_real_world]]"
  - "[[how_are_a_partitions_next_values_calculated]]"
nocite: |
  @grimm2006
---

# How do state partitions share information?
<div style="height:0.75em;"></div>

So far we have considered partition iterations as occurring separately within the simulation. But it is important for these separate partitions to be able to pass information to each other. 

To understand why this is important, think of our sports team example earlier and how each player might change their behaviour depending on the positions of other players on the field. They need to know about each other.

So how do we compose partitions together so that information may be passed between them? 

In some sense, this happens already. Each partition may read information from the state partition histories in the iteration to its next values.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/partition-timeline-composition.svg" /></center>

This composition allows us to correlate the behaviour of partitions in time.

We might also want to coordinate the iterations of partitions to occur in a particular order, where the first iteration may then pass its calculated next values immediately into the second.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/partition-dependencies.svg" /></center>

For example, an iteration might calculate the mean statistic from some data and another might calculate the variance. The variance depends on the mean so we need the mean next values to be passed directly into the variance to make sure these are always aligned in time.

To enable coordination, all we need is for a 'computationally upstream' iteration to be allowed to pass its next values into the parameters of a 'computationally downstream' iteration.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/composing-partitions.svg" /></center>

## References and further reading

::: {#refs}
:::
