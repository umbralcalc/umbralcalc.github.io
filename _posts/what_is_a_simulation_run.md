---
title: "What is a simulation run?"
tag: "How can I simulate the real world?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/simulation-run.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/termination-condition.svg"
aliases:
- "What is a simulation run?"
cites:
- "[[how_are_the_histories_updated_after_a_step]]"
- "[[how_can_i_simulate_the_real_world_introduction]]"
nocite: |
  @lawkelton2014
---

# What is a simulation run?
<div style="height:0.75em;"></div>

A 'simulation run' defines the evolution of a simulation state over some specified period in time. 

Each simulation run has an initial time defined by an exact value, but the _end_ time may not be known exactly until the simulation has evolved to meet some termination condition.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/simulation-run.svg"/></center>

The termination condition logically determines when the simulation run should end according to a pre-defined calculation.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/termination-condition.svg"/></center>

## References and further reading

::: {#refs}
:::
