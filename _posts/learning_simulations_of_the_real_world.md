---
title: "Learning simulations of the real world"
tag: "Simulating Real-World Systems as a Programmer"
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
order: 6
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/objectives.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/simulation-inference-code.svg"
---

# Learning simulations of the real world
<div style="height:0.75em;"></div>

Work In Progress...

## How do we learn a simulation?

Unlike Machine Learning models, which typically come with standard training algorithms (like [Backpropagation](https://en.wikipedia.org/wiki/Backpropagation) for Neural Networks), simulations often need us to explicitly choose and design procedures for learning their Parameters from real-world data or optimising their outputs.

In order to do this, we must first have some Objective which either characterises how close simulation Trajectories are to replicating the data we have or define the quantity we want to optimise.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/objectives.svg"/></center>

There are a number of techniques we can use to specify what the Objective should be, depending on the purpose.

## Learning simulations from data

If we want to learn the Parameters which correspond to simulation Trajectories fitting real-world data trends more closely, it is natural to use an Objective based on the Probabilities of State Partition Histories that we computed in the previous post.

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

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/simulation-inference-code.svg"/></center>

## Learning optimal simulations

If we want to learn Parameters which correspond to optimal simulation Trajectories, we first need to specify what 'optimal' means.

We do this by defining an Objective whose maximum/minimum possible value will be achieved when our goal is met.

For instance, we may define some logic in a State Partition Iteration of the simulation which replicates taking 'Actions' in the real world. This logic can depend on the simulation Parameters so that the latter encodes the behaviour quantitatively.

<Simulation with action taking partition depending on parameters>

Given this setup, a very common goal of interest is then in finding the best Actions to take; which is analogous to optimising the Parameters of the Action-taking State Partition Iteration.

## Example: Optimising future reward

The [Evolutionary Strategies](https://en.wikipedia.org/wiki/Evolution_strategy) algorithm can be applied to search future simulation Trajectories to find the best set of Parameters needed to achieve some 'Future Discounted Reward'.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/discounted-return-optimiser-code.svg"/></center>
