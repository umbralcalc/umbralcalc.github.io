---
title: Serving a wide array of interactive simulations through a static web application
author: Hardwick, Robert J
date: [WIP]
concept: To outline the design of a static web application which enables pure Python programmers to interact with stochadex simulations and visualise their outputs. In order to illustrate the flexibility in interactive user experience and simulation type supported by the stochadex engine, we then define some archetype simulation components which apply to a wide variety of real-world problems. We demonstrate how these archetypes can be used to simulate everything from sports matches and spatial disease spread to traffic networks, or even supply chain logistics. With these examples (and many others) in mind, we also consider the typical action state spaces and partial observability concerns in each case.
articleId: dexetera
codeLink: https://github.com/umbralcalc/dexetera
year: [WIP]
---

## Web application design

Previously, we have conceptualised and built the stochadex engine [@stochadexI-2024]; which provides a generalised framework for constructing stochastic simulations of practically any kind. In addition to enabling the construction of simulations which model real-world phenomena, we would also like to enable interactivity with these simulations and empower users to build their own control algorithms over them. Even though an API was built to minimise the amount of code required in these constructions, the requirement that new simulation components are written in Go may be a higher barrier to entry than is desirable --- especially for pure python programmers and machine learning engineers.

In this article, we're going to sidestep this barrier by providing the necessary tools to support web applications out of pre-built stochadex simulations. This application-building framework makes use of both WebAssembly [@wasm] technology for browser-based user experience (eliminating the need for a Go compiler on the user's side), and websocket client I/O with a local python server run by the user.

## Archetype simulation components

In this section we're going to define some archetype components which are typically useful in developing simulations of real-world systems. These archetypes will help to both illustrate how partitioning the state can be helpful to conceptualise the phenomena one wishes to simulate, and provide some practical insights into how the stochadex may be configured for different purposes.

We begin with the _entity state transition archetype_, which refers to state transitions of any individual 'entity' that occur stochastically according to their respective transition rates. These transition rates may themselves be time-varying (even stochastically) and so it is useful to separate their values into a separate state partition and create a direct dependency channel on them, as in the rough schematic below.

![](../assets/dexetera/dexetera-simple-state-partition-graph.drawio.png)

Note how this computational structure is slightly more generic than (but related to) the event-based simulation schematics in [@stochadexI-2024].

Observations of the entity state transition archetype in the real world typically take the form of either partial or noisy detections of the state transition times themselves over some period. Interactions with systems which require this archetype take the form of either direct changes to the entity state itself at some points in time or modifications to the rates at which state transitions occur. We won't provide any explict examples for this archetype as it applies extremely generally, and so it will be more informative to discuss these examples in the context of archetypes which apply to more specific situations.

The _weighted mean point archetype_ refers to components which perform a weighted average over a specified collection of neighbouring states. Given that one of the more natural uses for this archetype is in spatial field averaging, the graph toplogy of this archetype is typically totally connected and highly structured. However, some connections matter more than others, according to the weighting. We have created a rough schematic for this archetype below.

![](../assets/dexetera/dexetera-spatial-state-partition-graph.drawio.png)

In the case of spatial fields, you can think of each point as being structured topologically in a kind of 'lattice' configuration where connections to other points are controlled indirectly by the relationship between states and their weighted point averages over time. Different distances in the lattice can contribute different importance weights in affecting each local average.

Which real-world control problems would this archetype be useful for? Given the natural spatial interpetation, the kinds of simulation that would leverage this component are:

- Spatial simulations of population disease spread and control in the context of global disease outbreaks [@ohi2020exploring] or endemic, spatially-clustered infections like malaria [@carter2000spatial].
- Spatial ecosystem management environments to infer forest wildfire dynamics [@ganapathi2018using] or improve conservation decision-making [@lapeyrolerie2022deep].
- Weather system simulations to improve decision-making for agricultural yields [@chen2021reinforcement] or enhance stormwater flood mitigations [@saliba2020deep].





Within this topological archetype there will also be other categories to think are applicable:

- Types of observation that can be made about the state.
- Types of action that can be taken by an agent.
- Types of agent? How frequently do these actions get taken? On what part of the state?

Types of actor in this archetype:

- public health authority and wildlife/national park control authority and livestock/crop farmer 1. spatially detect disease or damage 2. change state of a subset of the population

The _distributed state network archetype_ refers to simulation environments whose bidirectional state partition graph topology is completely arbitrary, requiring no particular connectivity structure at all. Each state partition in this archetype typically refers to the same type of real-world node, object or sub-model. Due to the flexibility in topological structure, this archetype is well-suited to 'network' models of realistic phenomena. We have illustrated the state partition graph which fits into this category in the rough schematic below.

![](../assets/dexetera/dexetera-network-state-partition-graph.drawio.png)

Before discussing what kinds of data are typically available to infer states and parameters of environments in this archetype, it will be informative to consider the various real-world problem domains which apply. The particular subset of these domains which seem to fit well within this classification include:

- Computational models of human brain conditions, e.g., Parkinson's disease [@lu2019application], epilepsy [@pineau2009treating], Alzheimer's [@saboo2021reinforcement], etc., for deep brain stimulation control and other forms of treatment.
- Simulations of complex urban infrastructure networks to target various kinds of optimisation, e.g., traffic signal control [@yau2017survey], power dispatch [@li2021integrating] and water pipe maintainance [@bukhsh2023maintenance].

Within this topological archetype there will also be other categories to think are applicable:

- Types of observation that can be made about the state.
- Types of action that can be taken by an agent.
- Types of agent? How frequently do these actions get taken? On what part of the state?

Types of actor in this archetype:

- brain doctor and traffic light controller and city infrastructure maintainer 1. change the state of a subset of nodes in the network

The _multi-stage pipeline archetype_ refers to simulation environments with a directional state partition graph with arbitrary connection topology. In this case, each state partition corresponds to a separate stage in some pipeline model of the real-world phenomenon. Directionality in the connection structure is the key distinction between this archetype and the others in our classification scheme. We've provided one illustrated example of a multi-stage pipeline state partition graph below.

![](../assets/dexetera/dexetera-pipeline-state-partition-graph.drawio.png)

We're now ready to discuss how multi-stage pipelines are typically observed with data from realistic scenarios. To do this, it will help to first consider which real-world problem domains are best-suited to this archetype structure. From the literature, we can identify these as:

- Sequential design simulations to change the configuration or data collection strategies of, e.g., astronomical telescopes (see [@jia2023observation] and [@yatawatta2021deep]), biological experiments [@treloar2022deep] and user interface journeys [@lomas2016interface], which typically define a finite set of possible actions that can be taken.
- Simulations of logistics pipelines, e.g., organised supply chains [@yan2022reinforcement], humanitarian aid distribution pipelines [@yu2021reinforcement], hospital capacity planning [@shuvo2021deep], etc.
- Environments which emulate data pipeline optimisation problems [@nagrecha2023intune].

Within this topological archetype there will also be other categories to think are applicable:

- Types of observation that can be made about the state.
- Types of action that can be taken by an agent.
- Types of agent? How frequently do these actions get taken? On what part of the state?

Types of actor in this archetype:

- supply/relief chain controller and hospital logistics manager and data pipeline controller 1. modify the relative flows between different pipeline stages

The _centralised exchange archetype_ refers to simulation environments with a very specific bidirectional state partition graph topology. The graph connection structure is a star configuration where every state partition is connected to the same, centralised state partition which itself has a unique function in the model. In case this description isn't that clear, we've added an illustration of the graph for this archetype in the rough schematic below.

![](../assets/dexetera/dexetera-star-state-partition-graph.drawio.png)

Before moving on to discuss how data is typically collected for centralised exchanges, it will be informative to list the examples of phenomena where this archetype can be found in the real-world. These problem domains are:

- Simulations of sports matches, e.g., football [@pulis2022reinforcement], rugby [@sawczuk2022markov], tennis [@ding2022deep], etc., and other forms of game --- all of which typically define a relatively simple global match/gameplay context as their 'centralised state' and players as their 'entity states'.
- Financial (see [@fischer2018reinforcement] and [@meng2019reinforcement]) and sports betting [@cliff2021bbe] market simulations for developing algo-trading strategies and portfolio optimisation [@dangi2013financial], as well as housing market simulations (see [@yilmaz2018stochastic] and [@carro2023heterogeneous]) to evaluate government policies.
- Simulations of other forms of resource exchange through centralised mediation, such as in prosumer energy markets [@may2023multi].

In the case of team sports matches, a team manager could have access to a large body of data which assesses the capabilities of their players before a game, but they must rely on more subjective or limited data to assess the performance of their team (and the opposition) in the middle of a match. The 'state' of the whole system in this case can be not only the state of play, but also information about, e.g., fatigue or on-the-day performance of each player for both teams and sets of substitutes.

In a general offline learning setting, realistic historical data collected about the state values for this archetype will typically provide an important mechanism for model determination. Users of this archetype in the real world also typically have access to independent datasets that can be used offline to better determine some parameters of the simulation environment which are not observed directly. In the online learning setting, one typically directly observes some portion of the state values, and may only indirectly observe the other state values, if at all.

Within this topological archetype there will also be other categories to think are applicable:

- Types of observation that can be made about the state.
- Types of action that can be taken by an agent.
- Types of agent? How frequently do these actions get taken? On what part of the state?

Types of actor in this archetype:

- Sports team manager and other game player 1. substitute players 2. changes to tactics
- financial/betting/other market trader and market exchange mediator 1. interact with the market using an agent or collection of agents

## References
