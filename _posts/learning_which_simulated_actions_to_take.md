---
title: "Learning which simulated actions to take"
# tag: "Simulating Real-World Systems as a Programmer"
order: 5
---

# Learning which simulated actions to take
<div style="height:0.75em;"></div>

- Cover that 'optimality' isn't usually needed in practice
- Cover that simulating actions isn't usually like simulating other parts of systems because the data isn't usually good at all!
- Cover Bayesian optimisation and MCA-ES
- Cover how to chunk up action domains into seperate sub-domains
- vanilla ES  + discreteEA optimisers that can handle constraints and hierarchies in params
- Should be easy to combine the two in the same architecture by using the same collection sorting iteration to retain the samples with the best fitness over time and then the recombination into offspring is just different depending on the discrete/continuous space
- Consider also adding in a ‘forgetting’ collection which uses the state history to only retain best sample in the last N iterations - this can be combined with the long-term memory collection to make it a more generally flexible optimiser! Talk about how this is similar to LSTMs!

