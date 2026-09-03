---
title: "How can a simulation be wrong?"
# tag: "Trusting Actions on Simulated Systems"
series-blurb: "A collection of posts on how we decide whether an action chosen with a simulation can be trusted. Written especially for programmers and non-technical readers wanting to learn about how to take better actions under uncertainty. No maths; just diagrams and straightforward descriptions all the way through."
order: 2
---

# How can a simulation be wrong?
<div style="height:0.75em;"></div>

## Data is always limited

Consider the logic which our action iteration might use when applied to the example of stopping mass treatment in a population when the prevalence of the disease has gone to 0.

Making this example more realistic; you are not normally able to test every individual person in the population for the true disease prevalence because this takes too long and it is too expensive. So you only regularly sample, e.g., 1000 random people out of 1 million.

This immediately introduces a problem: how do you _know_ precisely when you have eliminated the disease? There is uncertainty in the exact state of the system at any moment in time.

So a more complete picture of the probabilistic view we had before must take into account additional uncertainty into the range of possible states and propagate this into additional uncertainty in the range in possible outcomes.

<!-- Diagram of the possible state - possible action - possible outcome paths with additional uncertainties -->

The key takeaway from this is that even with a perfect simulation of the real world, the realities of real-world data gathering very often mean we can only get a partial view of the true state of the system at best.

## Every simulation is wrong somewhere

The real world is complicated, and all of its inner workings are unlikely to be reduced into a single simulation modelled by us. A healthy perspective to have on this subject is that simulations are only ever an approximation of the real world, focused on the isolated system of interest.

So [all simulations are wrong, but some are useful](https://en.wikipedia.org/wiki/All_models_are_wrong). The pertinent question is: _where_ are they wrong and how much does this wrongness affect the parts of the simulation we rely on to compute the outcomes from simulated actions?

One might imagine, given our example earlier, that stopping mass treatment on the population depends much more on the accuracy of our prediction for the prevalence of the disease itself than, e.g., the number of new births (which might also be part of the simulation for other reasons).

The key takeaway from this is that simulations may always be wrong to some degree, but isolating how wrong they are to the parts of the system which we are using to learn better actions from is critical to trust.



