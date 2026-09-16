---
title: "How can a simulation be wrong?"
# tag: "How can I trust the actions I take in simulations?"
series-blurb: "A collection of posts on how we decide whether an action chosen with a simulation can be trusted. Written especially for programmers and non-technical readers wanting to learn about how to take better actions under uncertainty, while trusting the tools they use to help take them. No maths; just diagrams and straightforward descriptions all the way through."
order: 2
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how_can_a_simulation_be_wrong/sampling-prevalence.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how_can_a_simulation_be_wrong/additional-uncertainty-with-trajectories.svg"
---

# How can a simulation be wrong?
<div style="height:0.75em;"></div>

## Data is always limited

Consider the logic which our action-to-outcome simulation might use when applied to the example of stopping mass treatment in a population when the prevalence of the disease has gone to 0.

Making this example more realistic; you are not normally able to test every individual person in the population for the true disease prevalence because this takes too long and it is too expensive. So you only regularly sample, e.g., 1000 random people out of 1 million.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how_can_a_simulation_be_wrong/sampling-prevalence.svg"/></center>

This immediately introduces a problem: how do you _know_ precisely when you have eliminated the disease? There is uncertainty in the exact state of the system at any moment in time.

So a more complete picture of the probabilistic view we had before must take into account additional uncertainty into the range of possible states and propagate this into additional uncertainty in the range in possible outcomes.

This essentially means more paths and possible outcomes.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how_can_a_simulation_be_wrong/additional-uncertainty-with-trajectories.svg"/></center>

The key takeaway from this is that even with a perfect simulation of the real world, the realities of real-world data gathering very often mean we can only get a _partial view_ of the true state of the system at best. This leads to additional uncertainty.

## Every simulation is wrong somewhere

In addition to simulation states and parameters being uncertain, simulation logic can be wrong too. Simulations are only ever an approximation of the real world, after all.

The real world is complicated, and all of its inner workings are unlikely to be reduced into a single simulation modelled by us. Simulations are typically more focused on the details surrounding the system of interest.

So [all simulations are wrong, but some are useful](https://en.wikipedia.org/wiki/All_models_are_wrong). The pertinent question is: _where_ are they wrong and how much does this wrongness affect the parts of the simulation we rely on to compute outcomes from simulated actions?

One might imagine, given our example earlier, that stopping mass treatment on the population depends much more on the accuracy of our prediction for the prevalence of the disease itself than, e.g., the number of new births (which might also be part of the simulation for other reasons).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how_can_a_simulation_be_wrong/predictions-leading-to-actions.svg"/></center>

The key takeaway from this is that simulations may always be wrong to some degree, but isolating how wrong they are to the parts of the system which we are using to learn better actions from is critical to trust.



