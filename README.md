# Multithreaded Limit Order Book Engine

A high-performance, multithreaded limit order book engine written in Python. This project simulates an exchange-style matching engine that supports concurrent order placement, cancellation, and modification, while maintaining a thread-safe internal state and market depth representation.

## Features

- Thread-safe design with concurrent order handling using `threading` and `ThreadPoolExecutor`
- FIFO-based limit order matching with bid/ask book structure
- Support for FillOrKill, FillAndKill, and GoodTillCancel order types
- Good-for-Day (GFD) order pruning based on market close (4:00 PM)
- Order modification and cancellation support
- Level 2 market data tracking: price levels and quantities

## Technologies

- Python 3.10+
- `threading`, `concurrent.futures`
- `dataclasses` for order modeling
- `logging` for debug and runtime tracking
- Type hints for maintainability

## Installation

```bash
git clone https://github.com/DForDespair/OrderBook.git
cd orderbook