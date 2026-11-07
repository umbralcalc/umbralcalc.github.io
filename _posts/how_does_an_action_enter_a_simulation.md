---
title: "How does an action enter a simulation?"
draft: true
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_makes_an_action_good/action-taking.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_makes_an_action_good/iterate-simulated-action.svg"
cites:
- "[[how_can_i_trust_the_actions_i_take_in_simulations]]"
- "[[how_are_a_partitions_next_values_calculated]]"
- "[[what_is_a_state_partition]]"
nocite: |
  @suttonbarto2018
---

# How does an action enter a simulation?
<div style="height:0.75em;"></div>

What does it even mean to take a 'good' action?

Let's start by thinking about how our action-taking fits into a simulation of the outcomes. 

The simplest way to do this is to apply changes to parameters in the iterations of the simulation. This can effectively simulate an action taken at any point in time, so long as the simulation logic supports this behaviour and exposes the relevant parameters.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_makes_an_action_good/action-taking.svg"/></center>

For simplicity, we can think of the entire simulation as one operation that produces outcomes as the result of our actions.

This operation represents applying the relevant iteration logic to every [[what_is_a_state_partition|state partition]] given it parameters, and outputting the next values of all partitions for that point in time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_makes_an_action_good/iterate-simulated-action.svg"/></center>

## References and further reading

::: {#refs}
:::
