---
title: "Programmatic gaming with dexetera"
tag: "System Diagrams Series"
order: 2
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/programmatic_gaming_with_dexetera/programmatic-gaming.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/programmatic_gaming_with_dexetera/dexetera-main-loop.svg"
---

# Programmatic gaming with dexetera
<div style="height:0.75em;"></div>

These system diagrams track progress on the [dexetera project](https://github.com/umbralcalc/dexetera).

Dexetera powers decision-making games for the Python programmer built using the [stochadex](https://umbralcalc.github.io/stochadex) simulation framework. These games are Go simulations compiled to WebAssembly and run in the browser with real-time visualizations.

Those interested in playing the games should take a look at [dexetera](https://umbralcalc.github.io/dexetera/).

Programmatic gaming means that the user controls their actions in the game indirectly with computer code that they write.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/programmatic_gaming_with_dexetera/programmatic-gaming.svg" width="400"/></center>

We can expose a way for user-written code to run as the controller of actions taken in the game with a user server-web simulation client architecture.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/programmatic_gaming_with_dexetera/dexetera-main-loop.svg" width="500"/></center>
