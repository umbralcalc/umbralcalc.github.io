---
title: "Generalised simulations with the stochadex"
tag: "System Diagrams Series"
order: 1
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/stochadex-data-types.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/fundamental-loop-code.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/wiener-process.svg"
---

# Generalised simulations with the stochadex
<div style="height:0.75em;"></div>

These system diagrams track progress on the [stochadex project](https://umbralcalc.github.io/stochadex).

The stochadex is a simulation engine written in Go which can be used to sample from, and learn computational models for, a whole 'Pokédex' of possible real-world systems.

The fundamental data types in the stochadex simulation engine are Go types which can be configured as Settings (pure data) or Implementations (code which implements the provided interfaces).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/stochadex-data-types.svg" /></center>

For example, the Iteration interface can be implemented.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/fundamental-loop-code.svg" /></center>

The Iteration interface is very general. For example, it can support the [Wiener process](https://en.wikipedia.org/wiki/Wiener_process).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/wiener-process.svg" /></center>

Or [Itô's lemma](https://en.wikipedia.org/wiki/It%C3%B4%27s_lemma), which has more function calls inside to, e.g., calculate the derivatives.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/ito-lemma.svg" /></center>

Or the time-inhomogeneous [Poisson process](https://en.wikipedia.org/wiki/Poisson_point_process), as an example of a event-based process with discrete sample paths, which varies its event rate in time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/inhomogeneous-poisson.svg" /></center>

Or the [Hawkes process](https://en.wikipedia.org/wiki/Hawkes_process), which couples the history of events to the current event rate (making it non-Markovian).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/hawkes-process.svg" /></center>

Multiple Iterations can run within the stochadex for each step in time. In order to construct serial dependency graphs between them, we can utilise upstream-downstream Iteration relationships.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/stochadex-parallel-serial.svg" /></center>

Structuring groups of Iterations in this way can increase modularity. For example, the time-inhomogeneous Poisson process can be implemented serially.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/inhomo-poisson-parallel-serial.svg" /></center>

The full simulation loop coordinates these serial relationships between Iterations while maximising concurrency in execution of each Iteration per step in time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/stochadex-loop.svg" /></center>

Given that this loop always runs for any stochadex simulation, it is sufficient to describe any simulation uniquely through the dependency diagram between its Iterations. 

For example, we can define a probabilistic reweighting algorithm through just its dependency diagram.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/prob-reweighting-code.svg" /></center>

Embedded simulation runs are Iterations which perform entire simulations from start to end for every step in time. Their presence can make dependency diagrams a little more complex, but much more flexible.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/embedded-simulations.svg" /></center>

For example, we can define an algorithm for simulation inference which uses embedded simulation runs as part of its structure.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/generalised_simulations_with_the_stochadex/simulation-inference-code.svg" /></center>