---
title: "Building a simulation engine"
tag: "Simulating Real-World Systems as a Programmer"
order: 3
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/stochadex-data-types.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/fundamental-loop-code.svg"
---

# Building a simulation engine
<div style="height:0.75em;"></div>

## Introducing the stochadex project

The building blocks of simulations that we have discussed can now be pieced together to form a complete simulation engine.

The [stochadex project](https://umbralcalc.github.io/stochadex) is an actual simulation engine written in Go which is based on these basic conceptual building blocks.

Armed with the fundamentals, we can now describe how this simulation engine was built in specific detail, supported by the appropriate system diagrams.

## Interfaces and data types

The fundamental data types in the stochadex simulation engine are Go types which can be configured as Settings (pure data) or Implementations (code which implements the provided interfaces).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/stochadex-data-types.svg" /></center>

For example, the Iteration interface can be implemented.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/fundamental-loop-code.svg" /></center>

The Iteration interface is very general. For example, it can support the [Wiener process](https://en.wikipedia.org/wiki/Wiener_process).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/wiener-process.svg" /></center>

Or [Itô's lemma](https://en.wikipedia.org/wiki/It%C3%B4%27s_lemma), which has more function calls inside to, e.g., calculate the derivatives.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/ito-lemma.svg" /></center>

Or the time-inhomogeneous [Poisson process](https://en.wikipedia.org/wiki/Poisson_point_process), as an example of a event-based process with discrete sample paths, which varies its event rate in time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/inhomogeneous-poisson.svg" /></center>

Or the [Hawkes process](https://en.wikipedia.org/wiki/Hawkes_process), which couples the history of events to the current event rate (making it non-Markovian).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/hawkes-process.svg" /></center>

## Serial dependency graphs and modularity

Multiple Iterations can run within the stochadex for each step in time. In order to construct serial dependency graphs between them, we can utilise upstream-downstream Iteration relationships.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/stochadex-parallel-serial.svg" /></center>

Structuring groups of Iterations in this way can increase modularity. For example, the time-inhomogeneous Poisson process can be implemented serially.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/inhomo-poisson-parallel-serial.svg" /></center>

## Simulation loop and embedded simulation runs

The full simulation loop coordinates the serial relationships between Iterations while maximising concurrency in execution of each Iteration per step in time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/stochadex-loop.svg" /></center>

Given that this loop always runs for any stochadex simulation, it is sufficient to describe any simulation uniquely through the dependency diagram between its Iterations. 

Embedded simulation runs are Iterations which perform entire simulations from start to end for every step in time. Their presence can make dependency diagrams a little more complex, but much more flexible.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/embedded-simulations.svg" /></center>
