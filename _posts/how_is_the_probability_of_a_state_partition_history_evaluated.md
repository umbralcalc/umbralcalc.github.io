---
title: How is the probability of a state partition history evaluated?
images:
  - https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evaluate-probability-partition.svg
cites:
  - "[[how_can_i_simulate_the_real_world]]"
  - "[[how_are_a_partitions_next_values_calculated]]"
nocite: |
  @sarkka2013
---

# How is the probability of a state partition history evaluated?
<div style="height:0.75em;"></div>

Evaluating the probability of a particular state partition history, given parameters and a cumulative timesteps history, looks a similar to the iterate computation. However, in contrast, this computation does _not_ progress forward in time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evaluate-probability-partition.svg" /></center>

We might also want to evaluate the probability of regions which join together possible values that the whole state partition history can take.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/possible-region.svg" /></center>

In many situations, it would be impossible to count the all of the possible values in some regions, but we can still imagine the computation in this way.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evaluate-probability-partition-region.svg" /></center>

## References and further reading

::: {#refs}
:::
