---
title: "Stock market simulations can model price impacts"
# tag: "Engineering Smart Actions in Practice"
order: 2
---

# Stock market simulations can model price impacts
<div style="height:0.75em;"></div>

- qwakes project setup on data from polygon and get something basic working.
- Use this also as a way of validating the stochadex analysis package is fit for purpose.
- Goal: Build a stock portfolio management system which can do backtesting by looking at historical actions/shifts in portfolio positions as training data for price impacts.
  - Project todos:
    - Use the Polygon Go client (https://github.com/polygon-io/client-go) to create functions for reading stock market data and loading it into `simulator.StateTimeStorage` objects 
    - Create a custom Q-Hawkes simulation iterator and some convenience functions for running them with the market data
    - Develop a custom online inference methodology and mechanism for cross-validation against the data, then create some custom functions for this
    - Create a portfolio agent iterator which acquires positions in the market and affects the market liquidity (and possibly price) through its actions via the Hawkes model
    - Develop some more convenience functions for backtesting portfolio configurations - Obviously need to reconcile simulation disparity with historical data…
    - So is it possible to use the historical trade data as possible actions/shifts in portfolio positions?
