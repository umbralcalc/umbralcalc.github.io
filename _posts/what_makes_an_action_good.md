---
title: "What makes an action good?"
# tag: "How can I trust the actions I take in simulations?"
series-blurb: "A collection of posts on how we decide whether an action chosen with a simulation can be trusted. Written especially for programmers and non-technical readers wanting to learn about how to take better actions under uncertainty. No maths; just diagrams and straightforward descriptions all the way through."
order: 1
---

# What makes an action good?
<div style="height:0.75em;"></div>

## Good outcomes and good actions

What does it even mean to take a 'good' action?

Let's start by thinking about where action-taking fits into a simulation of the outcomes. One can separate the action-taking from outcome simulation into different partitions.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_makes_an_action_good/action-taking.svg"/></center>

Note that the downstream outcome iteration can be replaced by any kind of downstream simulation that is connected to the action iteration; we only think of it as a single iteration here for convenience.

From the probabilistic perspective, we only ever see _one_ action-to-outcome pairing in most real world action-taking scenarios. The fuller range of possibilities that a simulation represents is much larger.

<!-- Diagram of the possible state - possible action - possible outcome paths -->

Given that only a single path through the range of possibilities is actually taken by the real world, it's quite possible in many situations that any form of data can be misleading when relating actions to their associated outcomes.

Put another way, if there is only one result to validate an outcome from a given action: how do we know we didn't just 'get lucky' at that point in time?

## The difference between luck and skill

... Add stuff here about using the simulation to validate luck vs skill
... Note that this depends on the model
... Conclude that all of this relies on the simulation being 'correct'

