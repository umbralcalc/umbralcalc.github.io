---
title: "How can a simulation be wrong?"
draft: true
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how_can_a_simulation_be_wrong/predictions-leading-to-actions.svg"
aliases:
- "How can a simulation be wrong?"
cites:
- "[[how_can_i_trust_the_actions_i_take_in_simulations]]"
- "[[what_if_i_can_only_partly_observe_the_system]]"
nocite: |
  @box1976, @sargent2013, @saltelli2019
---

# How can a simulation be wrong?
<div style="height:0.75em;"></div>

In addition to simulation states and parameters being uncertain, simulation logic can be wrong too. Simulations are only ever an approximation of the real world, after all.

The real world is complicated, and all of its inner workings are unlikely to be reduced into a single simulation modelled by us. Simulations are typically more focused on the details surrounding the system of interest.

So [all simulations are wrong, but some are useful](#ref-box1976). The pertinent question is: _where_ are they wrong and how much does this wrongness affect the parts of the simulation we rely on to compute outcomes from simulated actions?

One might imagine, given our example earlier, that stopping mass treatment on the population depends much more on the accuracy of our prediction for the prevalence of the disease itself than, e.g., the number of new births (which might also be part of the simulation for other reasons).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how_can_a_simulation_be_wrong/predictions-leading-to-actions.svg"/></center>

The key takeaway from this is that simulations may always be wrong to some degree, but isolating how wrong they are to the parts of the system which we are using to learn better actions from is critical to trust.

## References and further reading

::: {#refs}
:::
