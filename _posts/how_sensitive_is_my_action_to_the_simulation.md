---
title: How sensitive is my action to the simulation?
images:
  - https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/preparing_a_simulation_for_action_taking/changing-parameters.svg
  - https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/preparing_a_simulation_for_action_taking/changing-simulation.svg
cites:
  - "[[how_can_a_simulation_be_wrong]]"
  - "[[is_a_sloppy_simulation_a_bad_one]]"
nocite: |
  @saltelli2019, @sobol2001
---

# How sensitive is my action to the simulation?
<div style="height:0.75em;"></div>

When we change the parameters of a simulation, its iteration at the same point in time may produce different outcomes, depending on the system state and its history (which may also have changed due to previous iterations in time being different).

<center><img src=https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/preparing_a_simulation_for_action_taking/changing-parameters.svg /></center>

Similarly, when we change the simulation itself, its iteration at the same point in time may also produce different outcomes.

<center><img src=https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/preparing_a_simulation_for_action_taking/changing-simulation.svg /></center>

In both cases, the simulated outcomes help us to determine which action to take, but in order to do this we need to define what outcomes we are targeting in the first place.

## References and further reading

::: {#refs}
:::
