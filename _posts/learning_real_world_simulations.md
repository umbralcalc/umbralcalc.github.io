---
title: "Learning real-world simulations"
tag: "Simulating Real-World Systems as a Programmer"
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
order: 6
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_real_world_simulations/simulation-inference-code.svg"
---

# Learning real-world simulations
<div style="height:0.75em;"></div>

Work In Progress...

## How do we learn a simulation?

Unlike Machine Learning models, which typically come with standard training algorithms (like [Backpropagation](https://en.wikipedia.org/wiki/Backpropagation) for Neural Networks), simulations often need us to explicitly choose and design procedures for learning their Parameters from real-world data or optimising their outputs.

In order to do this, we must first have some Objective of fit which either characterises how close simulation Trajectories are to replicating the data we have or define the quantity we want to optimise.

<Objective of fit explanation diagram>

There are a number of techniques we can use to specify what the Objective should be, depending on the purpose.

## Learning simulations from data

If the purpose is to determine the Parameters which correspond to a simulation more closely fitting real-world data trends, it is natural to use an Objective based on the Probabilities of State Partition Histories that we computed in the previous post.

- Outline how we need to characterise some objective of fit which represents the simulation probabilities.
- Give the online posterior estimation algorithm as one example

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_real_world_simulations/simulation-inference-code.svg"/></center>

## Learning smarter simulated actions

- Talk about extensions, including Bayesian optimisation and MCA-ES
- Cover that 'optimality' isn't usually needed in practice
- Cover that simulating actions isn't usually like simulating other parts of systems because the data isn't usually good at all!
- Cover Bayesian optimisation and MCA-ES
- Cover how to chunk up action domains into seperate sub-domains
- vanilla ES  + discreteEA optimisers that can handle constraints and hierarchies in params
- Should be easy to combine the two in the same architecture by using the same collection sorting iteration to retain the samples with the best fitness over time and then the recombination into offspring is just different depending on the discrete/continuous space
- Consider also adding in a 'forgetting' collection which uses the state history to only retain best sample in the last N iterations - this can be combined with the long-term memory collection to make it a more generally flexible optimiser! Talk about how this is similar to LSTMs!

