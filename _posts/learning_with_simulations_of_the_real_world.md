---
title: "Learning with simulations of the real world"
tag: "Simulating Real-World Systems as a Programmer"
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
order: 6
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_with_simulations_of_the_real_world/objectives.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_with_simulations_of_the_real_world/simulation-inference-code.svg"
---

# Learning with simulations of the real world
<div style="height:0.75em;"></div>

Work In Progress...

## How do we learn with a simulation?

Unlike Machine Learning models, which typically come with standard training algorithms (like [Backpropagation](https://en.wikipedia.org/wiki/Backpropagation) for Neural Networks), simulations often need us to explicitly choose and design procedures for learning their Parameters from real-world data or optimising their outputs.

In order to do this, we must first have some Objective which either characterises how close simulation Trajectories are to replicating the data we have or define the quantity we want to optimise.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_with_simulations_of_the_real_world/objectives.svg"/></center>

There are a number of techniques we can use to specify what the Objective should be, depending on the purpose.

## Learning simulations from data

If we want to learn the Parameters which correspond to a simulation fitting real-world data trends more closely, it is natural to use an Objective based on the Probabilities of State Partition Histories that we computed in the previous post.

We start by streaming time-series data into our simulation by specifying it as a State Partition.

<Data as a state partition in simulation>

We can then use a method to estimate the Probabilities of State Values within the data, e.g., the Probabilistic Sample Weighting we discussed in the previous post.

So we have a way to calculate these 'Data Probabilities' for any Possible State Values the data can take in Time.

By then evaluating these Data Probabilities at the points which coincide with simulation Trajectories, we have an Objective which quantifies how close the simulation is to the data.

## Example: Online simulation parameter estimation

The Data Probabilities of simulation Trajectories can also be interpreted as Probabilities of simulation Parameters; often accompanied with some simulation noise to account for differences between Trajectories even with the same Parameters.

We can create an algorithm which uses this sequence of Probabilities to estimate the Probabilities of simulation Parameters in a very similar way to Probabilistic Sample Weighting (see the last post for details on the latter).

<Online Simulation Parameter Estimation diagram>

We might call this algorithm 'Online Simulation Parameter Estimation'; where 'Online' here means that the simulation is being adaptively learned to the data iteratively in time, as opposed to a whole Batch all at once.

<Interactive widget which shows how sample Online Simulation Parameter Estimation works>

There is also an implementation of this Online Simulation Parameter Estimation algorithm within the [stochadex simulation engine](https://umbralcalc.github.io/stochadex).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_with_simulations_of_the_real_world/simulation-inference-code.svg"/></center>

## Learning smarter simulated actions

- Talk about extensions, including Bayesian optimisation and MCA-ES
- Cover that 'optimality' isn't usually needed in practice
- Cover that simulating actions isn't usually like simulating other parts of systems because the data isn't usually good at all!
- Cover Bayesian optimisation and MCA-ES
- Cover how to chunk up action domains into seperate sub-domains
- vanilla ES  + discreteEA optimisers that can handle constraints and hierarchies in params
- Should be easy to combine the two in the same architecture by using the same collection sorting iteration to retain the samples with the best fitness over time and then the recombination into offspring is just different depending on the discrete/continuous space
- Consider also adding in a 'forgetting' collection which uses the state history to only retain best sample in the last N iterations - this can be combined with the long-term memory collection to make it a more generally flexible optimiser! Talk about how this is similar to LSTMs!

