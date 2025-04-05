from Level.Level import OrderBookLevelInfos
import matplotlib.pyplot as plt

class LevelsPlot:
    def __init__(self, order_book_levels_info: OrderBookLevelInfos):
        self._levels_info: OrderBookLevelInfos = order_book_levels_info
        
    def plot_order_book_depth(self):
        bids = sorted(self._levels_info.bids, key=lambda x: -x.price)
        asks = sorted(self._levels_info.asks, key=lambda x: x.price)

        bid_prices = [level.price for level in bids]
        bid_quantities = [sum(l.quantity for l in bids[:i+1]) for i in range(len(bids))]

        ask_prices = [level.price for level in asks]
        ask_quantities = [sum(l.quantity for l in asks[:i+1]) for i in range(len(asks))]

        plt.figure(figsize=(8, 5))
        plt.step(bid_prices, bid_quantities, label='Bids', where='post')
        plt.step(ask_prices, ask_quantities, label='Asks', where='post')
        plt.xlabel('Price')
        plt.ylabel('Cumulative Quantity')
        plt.title('Order Book Depth Chart')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        