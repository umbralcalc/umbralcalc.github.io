---
title: "The building blocks of simulations"
tag: "Simulating Real-World Systems as a Programmer"
order: 2
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world and what you can use them for. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/cumulative-timesteps-history.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partitions.svg"
---

# The building blocks of simulations
<div style="height:0.75em;"></div>

## Time and its 'history'

Time is probably the most important variable to track in a simulation. This is because everything that happens within a simulation only has meaning with respect to the real world if we can trace what point in simulated Time that it happened.

Time is a variable in the simulation which always increases in value. We often want to track how it increases after each discrete simulation 'step' in increments which we shall call 'Timesteps'.

The first data structure which we shall introduce here is a 'Cumulative Timesteps History', which indexes simulated Times that the simulation _had_ according to _decreasing recency_.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/cumulative-timesteps-history.svg" width=600/></center>

## State partitions and their history

Simulations also have a 'State' associated to them for each value of Time.

A simulation State holds all of the essential information we want to track to make the simulation useful to us which, crucially, includes _all of the information that is needed for the simulation to proceed_.

In order to simplify how all of this State data is processed and retrieved, we're going to _partition_ this simulation State into several 'State Partition' data structures.

For example, one of these partitions might hold all the data associated to a player in a sports team, and the whole simulation needs all of the players within its overall State.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partitions.svg" width=600/></center>

Each State Partition carries data that can be different for each moment in Time of the simulation. In order to track this evolution, we create a 'State Partition History' data structure for each State Partition.

Each State Partition History has indices which always match those of the Cumulative Timesteps History, so they are always synchronised with each other.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partition-history.svg" width=600/></center>

## Computing the next timesteps

So new States of the simulation may happen at different Times. But what determines when these Times are along the Simulation Timeline?

When simulating systems in the real world, it can be desireable in some situations to be able to structure the Times along the Timeline at regular intervals.

In other situations it can be desirable to have an unstructured or randomly-drawn set of Times along the Timeline.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/timeline.svg" /></center>

In order to allow this flexibility in choice between situations, let's specify an 'Advance Time' calculation which takes in the current Cumulative Timesteps History and outputs the Next Timestep following the latest Time found in the History (at index 0).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/advance-time.svg" /></center>

## State partition iteration

For an overall simulation data view, we can create a 'State Partition Histories' structure. This is a collection of each State Partition History that exists within the simulation.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partition-histories.svg" width=600/></center>

How do we determine the 'Next Values' of each State Partition in Time?

This is where we should maintain full flexibility in choice of calculation so that our simulation is able to represent many different real-world systems.

Each of these calculations for a given Partition specifies how the State Partition Histories and Cumulative Timesteps History data are used to determine the Next Values of the State Partition.

In order to support even more flexibility in configuration, the calculation should also take in a set of Parameters which are specific to that Partition.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/partition-iteration.svg" /></center>

## State partition and time updates

Having calculated the Next Values of each State Partition and the Next Timestep, we should perform operations over the Cumulative Timesteps History and each State Partition History to Update their structures with this new data.

This is an important procedure to perform all at once to ensure that the all of the State Partitions in the simulation are synchronised against its virtual clock.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/update-time-history.svg" /></center>

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/update-state-partition-history.svg" /></center>

## Composing and coordinating partitions

So far we have considered Partition Iterations as occurring seperately within the simulation. But it is important for these separate Partitions to be able to pass information to each other. 

To understand why this is important, think of our sports team example earlier and how each player might change their behaviour depending on the positions of other players on the field. They need to know about each other.

So how do we compose Partitions together so that information may be passed between them? 

In some sense, this happens already. Each Partition may read information from the State Partition Histories in the Iteration to its Next Values.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/partition-timeline-composition.svg" /></center>

This composition allows us to correlate the behaviour of Partitions in Time.

We might also want to coordinate the Iterations of Partitions to occur in a particular order, where the first Iteration may then pass its calculated Next Values immediately into the second.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/partition-dependencies.svg" /></center>

For example, an Iteration might calculate the Mean statistic from some data and another might calculate the Variance. The Variance depends on the Mean so we need the Mean Next Values to be passed directly into the Variance to make sure these are always aligned in Time.

To enable coordination, all we need is for a 'Computationally Upstream' Iteration to be allowed to pass its Next Values into the Parameters of a 'Computationally Downstream' Iteration.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/composing-partitions.svg" /></center>

## Simulation runs

A 'Simulation Run' defines the evolution of a simulation State over some specified period in Time. 

Each Simulation Run has an Initial Time defined by an exact value, but the _end_ Time may not be known exactly until the simulation has evolved to meet some Termination Condition.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/simulation-run.svg"/></center>

The Termination Condition logically determines when the Simulation Run should end according to a pre-defined calculation.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/termination-condition.svg"/></center>

## Embedded simulation runs

Enabling whole 'Inner' Simulation Runs to start and complete within each Timestep of an 'Outer' Simulation Run is a very useful, and somewhat fundamental, building block for simulations in practice. We shall call these 'Embedded Simulation Runs'.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/embedded-simulation-run.svg"/></center>

There are then several ways one can think of to pass information from the Outer simulation into the Inner simulation prior to running it on each Timestep.

Treating the Inner simulation as a Partition of the Outer simulation, one example is to simply pass Parameters from the Outer simulation into the Inner simulation, and nothing else.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/embedded-sim-iterate.svg" width=600/></center>

Another example is to pass both the Cumulative Timesteps History and State Partition Histories from the Outer simulation into the Inner simulation, in addition to the Parameters.

Consider how this might be used to create useful statistical operations over the history of the Outer simulation, e.g., like rolling window averages.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/embedded-sim-from-history.svg" width=600/></center>
