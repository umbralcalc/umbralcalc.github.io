---
title: "Architectures for current and future hardware"
tag: "Simulating Real-World Systems as a Programmer"
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
order: 4
images: []
---

# Architectures for current and future hardware
<div style="height:0.75em;"></div>

Work In Progress...

## Classical hardware

CPUs...

## Specialised classical hardware

GPUs and TPUs...

## Quantum hardware

So if I wanted to measure a time series metric of the system I would have to create some partition of the quantum state which recorded this time series as a whole in memory before collapsing the quantum state at the end to retrieve the time series.

Therefore, you only get a quantum advantage at all if you can store more than one timestep worth of simulation metric states in qubit memory. Otherwise, if you only effectively have one instantaneous timestep of qubit memory to use the runtime will be denominated by I/O writing to and from the qubit states during the simulation runtime. This is the quantum I/O bottleneck.