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

When we talk about 'classical' hardware here, we just mean standard CPUs. This naming will make sense as we progress through the post.

On CPUs, simulation architectures may be constructed out of several ingredients. Loosely speaking, these are: Memory, Threads, Channels between Threads, Processes and Inter-Process Communication (IPC).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/architectures_for_current_and_future_hardware/cpu-graph-edges.svg"/></center>

All of these ingredients have their own tradeoffs in performance. But they are all useful in constructing the right simulation architectures to satisfy the right use cases.

In all of the previous posts so far, the main simulation architectures we have been considering are defined as Stepwise; simulation architectures which describe how components of the system/algorithm fit together for a single point in Time.

Stepwise simulation architectures on CPUs are typically more performant when using Memory, Threads and Channels between Threads in the right combinations.

<diagrams of different stepwise architectures mapped from those in drive already>

Processes, and IPC in particular, are typically more useful when we consider Batch simulation architectures. This is because IPC comes with more performance limitations.

Batch simulation architectures involve...

## Specialised classical hardware

GPUs and TPUs...

## Quantum hardware

So if I wanted to measure a time series metric of the system I would have to create some partition of the quantum state which recorded this time series as a whole in memory before collapsing the quantum state at the end to retrieve the time series.

Therefore, you only get a quantum advantage at all if you can store more than one timestep worth of simulation metric states in qubit memory. Otherwise, if you only effectively have one instantaneous timestep of qubit memory to use the runtime will be denominated by I/O writing to and from the qubit states during the simulation runtime. This is the quantum I/O bottleneck.