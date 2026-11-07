---
title: "What decides when the next timestep happens?"
tag: "How can I simulate the real world?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/timeline.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/advance-time.svg"
aliases:
- "What decides when the next timestep happens?"
cites:
- "[[how_does_a_simulation_keep_track_of_time]]"
- "[[how_can_i_simulate_the_real_world_introduction]]"
nocite: |
  @lawkelton2014
---

# What decides when the next timestep happens?
<div style="height:0.75em;"></div>

So new states of the simulation may happen at different times. But what determines when these times are along the simulation timeline?

When simulating systems in the real world, it can be desireable in some situations to be able to structure the times along the timeline at regular intervals.

In other situations it can be desirable to have an unstructured or randomly-drawn set of times along the timeline.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/timeline.svg" /></center>

In order to allow this flexibility in choice between situations, let's specify an 'advance time' calculation which takes in the current cumulative timesteps history and outputs the next timestep following the latest time found in the history (at index 0).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/advance-time.svg" /></center>

## References and further reading

::: {#refs}
:::
