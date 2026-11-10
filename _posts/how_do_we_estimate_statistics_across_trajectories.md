---
title: "How do we estimate statistics across trajectories?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/average-across-trajectories.svg"
cites:
- "[[why_cant_we_track_every_possible_trajectory]]"
- "[[why_think_about_a_simulation_probabilistically]]"
nocite: |
  @owen2013
---

# How do we estimate statistics across trajectories?
<div style="height:0.75em;"></div>

By averaging over many simulation runs, timestep by timestep.

The simplest example of these statistics is the estimated mean state value. 

The obvious way to calculate this is to take the average state value for a given timestep across multiple simulation trajectories.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/average-across-trajectories.svg" /></center>

But could we get an estimate of statistics from only one trajectory to avoid all the additional computations?

## References and further reading

::: {#refs}
:::
