# Multithreaded Limit Order Book Engine

A high-performance, multithreaded limit order book engine written in Python. This project simulates an exchange-style matching engine that supports concurrent order placement, cancellation, and modification, while maintaining a thread-safe internal state and market depth representation.

### Example Visualization

[![Watch the demo](https://img.youtube.com/vi/xD8S5HcGbtY/hqdefault.jpg)](https://www.youtube.com/watch?v=xD8S5HcGbtY)

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
```
## Future Work
This project is still evolving. Here are some planned enhancements:

- Client-Server Architecture: Implement a socket-based or RESTful API server so that external clients can connect and place trades in real time.

- Order Book Visualization: Create a web-based or terminal-based dashboard to visualize the order book, price levels, and recent trades.

- Multi-Product Support: Extend the engine to support multiple trading products (e.g., BTC/USD, ETH/USD) with isolated order books.

- Extensive Testing: Build a full suite of unit, integration, and performance tests to ensure correctness and robustness under load.

- Data Persistence: Save and reload order and trade data using formats such as SQLite, CSV, or JSON for historical analysis and replay.

- Trade Replay and Streaming: Add functionality to stream trades live or replay historical sessions for testing or analysis.

- User Simulation: Implement multi-user environments with account-based order tracking and simulated trading competition.