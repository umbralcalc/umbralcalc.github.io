---
title: "What is a conditional probability in a simulation?"
tag: "How can I simulate the real world?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/conditional-probability.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evolving-state-partition-history-probability.svg"
aliases:
- "What is a conditional probability in a simulation?"
cites:
- "[[how_is_the_probability_of_a_state_partition_history_evaluated]]"
- "[[how_can_i_simulate_the_real_world_introduction]]"
nocite: |
  @sarkka2013, @chopin2020
---

# What is a conditional probability in a simulation?
<div style="height:0.75em;"></div>

We can relate two successive probability evaluations in time together by making the answer of the second depend on the outcome of the first.

We call the second of these two evaluations a conditional probability because its probability is _conditional_ on the probability of the first.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/conditional-probability.svg" /></center>

The probabilities for the whole state partition history change as the simulation advances in time by adding the next state partition values into the history.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evolving-state-partition-history-probability.svg" /></center>

This concept also applies to the probability of regions.

Note how this relationship also describes how the probabilities of state partition histories can evolve in time. One applies the same calculation to the output from the previous one, and so on, recursively.

## References and further reading

::: {#refs}
:::
