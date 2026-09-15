---
title: "What makes an action good?"
# tag: "How can I trust the actions I take in simulations?"
series-blurb: "A collection of posts on how we decide whether an action chosen with a simulation can be trusted. Written especially for programmers and non-technical readers wanting to learn about how to take better actions under uncertainty, while trusting the tools they use to help take them. No maths; just diagrams and straightforward descriptions all the way through."
order: 1
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_makes_an_action_good/action-taking.svg"
---

# What makes an action good?
<div style="height:0.75em;"></div>

## Good outcomes and good actions

What does it even mean to take a 'good' action?

Let's start by thinking about how our action-taking fits into a simulation of the outcomes. 

The simplest way to do this is to apply changes to parameters in the iterations of the simulation. This can effectively simulate an action taken at any point in time, so long as the simulation logic supports this behaviour and exposes the relevant parameters.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_makes_an_action_good/action-taking.svg"/></center>

From the probabilistic perspective, we only ever see _one_ action-to-outcome pairing in most real world action-taking scenarios. The fuller range of possibilities that a simulation represents is much larger.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_makes_an_action_good/iterate-simulated-action.svg"/></center>

Different simulation trajectories follow multiple paths through the space of possible outcomes from our actions in time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_makes_an_action_good/possible-outcome-trajectories.svg"/></center>

Some paths may be more likely than others, depending on our actions. So the challenge of taking 'good' actions under an uncertain future is to pick those which make the the desireable outcomes more likely, or perhaps making undesireable outcomes less likely (if risk averse).

## The difference between luck and skill

What else does this simulation with multiple trajectories help us understand about taking actions in the real world? Individual measurements of outcomes can be wrong, or misleading.

Think about what it actually means to measure outcomes in the real world: only a single path among the possibilities is actually _taken_, so chance events can strongly affect how we learn the relationship between actions and outcomes.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_makes_an_action_good/data-outcomes-trajectory.svg"/></center>

So, in many situations, data can be very misleading when trying to connect actions to outcomes. How do we know we didn't just 'get lucky' at the previous point in time when the data was collected? How can we tell the difference between luck and skill?

This is where a simulation can be very helpful.

... Add stuff here about using the simulation to validate luck vs skill
... Note that this depends on the model
... Conclude that all of this relies on the simulation being 'correct'

