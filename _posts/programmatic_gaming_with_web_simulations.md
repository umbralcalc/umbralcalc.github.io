---
title: "Programmatic gaming with web simulations"
tag: "Decision-Making Game Design"
order: 1
images:
- "/assets/programmatic_gaming_with_web_simulations/dexetera-main-loop.svg"
---

# Programmatic gaming with web simulations
<div style="height:0.75em;"></div>

## What is programmatic gaming?

'Programmatic Gaming' here describes the activity of playing a computer game using a prescriptive controller programmed as computer code.

In this series of posts, we will explore some designs for these games in a visual way. Those interested in the code behind the posts should also check out the [dexetera project](https://github.com/umbralcalc/dexetera).

In Programmatic Gaming, the gamer must write algorithms which are successful at playing the game itself. This indirectness sounds unusual at first, but yields interesting tactics for the gamer who may switch between algorithms depending on circumstances within the game.

Writing optimal gameplay algorithms also requires a very different skillset to that of more conventional gamers. So this kind of game may appeal to those with machine learning backgrounds, for instance.

## Creating a web simulation architecture for gaming

Let's assume we already have a framework for stepping simulations forward in time, which can be used to represent the game state and how it responds to controller actions.

We then need to specify a technical architecture for how the gamer's code will take actions within the simulation.

<img src="../assets/programmatic_gaming_with_web_simulations/dexetera-main-loop.svg" />
