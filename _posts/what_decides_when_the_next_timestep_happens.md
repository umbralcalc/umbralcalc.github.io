---
title: What decides when the next timestep happens?
images:
  - https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/timeline.svg
cites:
  - "[[how_can_i_simulate_the_real_world]]"
  - "[[how_does_a_simulation_keep_track_of_time]]"
nocite: |
  @lawkelton2014
---

# What decides when the next timestep happens?
<div style="height:0.75em;"></div>

A calculation of our own choosing, which we call 'advance time'. New states of the simulation may happen at different times, so something has to determine where those times fall along the simulation timeline.

When simulating systems in the real world, it can be desireable in some situations to be able to structure the times along the timeline at regular intervals.

In other situations it can be desirable to have an unstructured or randomly-drawn set of times along the timeline.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/timeline.svg" /></center>

In order to allow this flexibility in choice between situations, let's specify an 'advance time' calculation which takes in the current cumulative timesteps history and outputs the next timestep following the latest time found in the history (at index 0).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/advance-time.svg" /></center>

## References and further reading

::: {#refs}
:::
