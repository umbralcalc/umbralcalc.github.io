---
title: "Why think about a simulation probabilistically?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/probabilites-vs-trajectories.svg"
cites:
- "[[why_should_i_simulate_the_real_world]]"
- "[[what_is_a_simulation_run]]"
nocite: |
  @owen2013
---

# Why think about a simulation probabilistically?
<div style="height:0.75em;"></div>

Because it lets us reason about every path the simulation could take at once, rather than one run at a time.

The 'trajectory' of a simulation is the sequence of possible state values that its partitions actually take during a specific simulation run.

Probabilities can represent sampling all of the possible trajectories that a simulation could take in time, simultaneously.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/probabilites-vs-trajectories.svg" /></center>

Using this representation of a simulation, there are two important use cases.

The first uses all of the possible trajectories the simulation can take to represent how likely it is to take them. This makes it possible to create algorithms which learn the most likely parameters for state partitions to match real-world data.

The second uses the probabilities to represent a model in place of the simulation itself. In the right circumstances, this results in algorithms which are much more efficient than sampling multiple trajectories explicitly.

## References and further reading

::: {#refs}
:::
