---
title: "Programmatic gaming through a browser"
tag: "Loose Threads"
order: 3
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/programmatic_gaming_through_a_browser/programmatic-gaming.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/programmatic_gaming_through_a_browser/dexetera-main-loop.svg"
---

# Programmatic gaming through a browser
<div style="height:0.75em;"></div>

## Programmatic gaming

Programmatic gaming means that the user controls their actions in the game indirectly with computer code that they write.

This forms a feedback loop where the user must modify their code in order to affect the game, iteratively designing a decision-making algorithm.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/programmatic_gaming_through_a_browser/programmatic-gaming.svg" width="400"/></center>

## The dexetera project

The [dexetera project](https://github.com/umbralcalc/dexetera) powers decision-making games for the Python programmer using the [stochadex](https://umbralcalc.github.io/stochadex) simulation framework as a core dependency. 

These games are Go simulations compiled to WebAssembly and run in the browser with real-time visualizations.

The project gets programmatic gaming to work entirely over a websocket connection to the user's browser using an architecture which makes the frontend simulation a client and the user's local (Python) code run the websocket server.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/programmatic_gaming_through_a_browser/dexetera-main-loop.svg" width="500"/></center>

A static website can host the game web worker launchers (at no cost with GitHub pages!) while the user's machine provides the compute.

Those interested in playing the games should take a look at [dexetera](https://umbralcalc.github.io/dexetera/).
