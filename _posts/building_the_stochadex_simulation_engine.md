---
title: "Building the stochadex simulation engine"
tag: "Simulating Real-World Systems as a Programmer"
order: 3
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/stochadex-data-types.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/fundamental-loop-code.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/wiener-process.svg"
---

# Building the stochadex simulation engine
<div style="height:0.75em;"></div>

## Introducing the stochadex

The [stochadex](https://umbralcalc.github.io/stochadex) is a simulation engine written in Go which can be used to sample from, and learn computational models for, a whole 'Pokédex' of possible real-world systems. Hence the name!

It was designed and created with the basic conceptual building blocks of simulations we have already discussed in mind.

Armed with these fundamentals, we can now describe the engine in more specific technical detail, supported by the appropriate system diagrams.

## Interfaces and data types

The fundamental data types in the stochadex simulation engine are Go types which can be configured as Settings (pure data) or Implementations (code which implements the provided interfaces).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/stochadex-data-types.svg" /></center>

For example, the Iteration interface can be implemented.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/fundamental-loop-code.svg" /></center>

The Iteration interface is very general. For example, it can support the [Wiener process](https://en.wikipedia.org/wiki/Wiener_process).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/wiener-process.svg" /></center>

Or [Itô's lemma](https://en.wikipedia.org/wiki/It%C3%B4%27s_lemma), which has more function calls inside to, e.g., calculate the derivatives.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/ito-lemma.svg" /></center>

Or the time-inhomogeneous [Poisson process](https://en.wikipedia.org/wiki/Poisson_point_process), as an example of a event-based process with discrete sample paths, which varies its event rate in time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/inhomogeneous-poisson.svg" /></center>

Or the [Hawkes process](https://en.wikipedia.org/wiki/Hawkes_process), which couples the history of events to the current event rate (making it non-Markovian).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/hawkes-process.svg" /></center>

## Serial dependency graphs and modularity

Multiple Iterations can run within the stochadex for each step in time. In order to construct serial dependency graphs between them, we can utilise upstream-downstream Iteration relationships.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/stochadex-parallel-serial.svg" /></center>

Structuring groups of Iterations in this way can increase modularity. For example, the time-inhomogeneous Poisson process can be implemented serially.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/inhomo-poisson-parallel-serial.svg" /></center>

## Simulation loop and embedded simulation runs

The full simulation loop coordinates the serial relationships between Iterations while maximising concurrency in execution of each Iteration per step in time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/stochadex-loop.svg" /></center>

Given that this loop always runs for any stochadex simulation, it is sufficient to describe any simulation uniquely through the dependency diagram between its Iterations. 

Embedded simulation runs are Iterations which perform entire simulations from start to end for every step in time. Their presence can make dependency diagrams a little more complex, but much more flexible.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_the_stochadex_simulation_engine/embedded-simulations.svg" /></center>
