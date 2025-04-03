from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Deque
from Level.Level import LevelInfo, OrderBookLevelInfos
from Order.OrderEnums import OrderType, OrderSide
from Order.Order import Order
from Order.OrderModify import OrderModify
from Trade.TradeInfo import Trade, TradeInfo

@dataclass
class OrderEntry:
    _order: Order
    _location: Deque[Order]
    
    @property
    def order(self) -> Order:
        return self._order
    
    @property
    def location(self) -> deque:
        return self._location
    
    @order.setter
    def order(self, order: Order):
        if not isinstance(order, Order):
            raise ValueError("order must be an instance of Order")
        self._order = order
    
    @location.setter
    def location(self, location: Deque[Order]):
        if not isinstance(location, deque):
            raise ValueError("location must be a deque of Orders")
        self._location = location
    
    def __repr__(self):
        return f"OrderEntry(order={self.order}, location=deque(len={len(self.location)}))"
    

class OrderBook:
    def __init__(self):
        self._bids: Dict[float, deque] = defaultdict(deque) ## example: {101.5: deque([Order1, Order2])}
        self._asks: Dict[float, deque] = defaultdict(deque)
        self._orders: Dict[int, OrderEntry] = {}
        self._level_data: Dict[float, LevelInfo] = {}
        
        
    def can_match(self, side: OrderSide, price: float) -> bool: 
        if side == OrderSide.BUY:
            if not self._asks:
                return False
            best_ask = min(self._asks.keys())
            return price >= best_ask
        else:
            if not self._bids:
                return False
            best_bid = max(self._bids.keys())
            return price >= best_bid
        
    def match_orders(self) -> List[Trade]:
        trades: List[Trade] = []
        while self._asks and self._bids:
            best_bid_price: float = max(self._bids.keys())
            best_ask_price: float = min(self._asks.keys())
            
            if best_bid_price < best_ask_price:
                break
            
            best_bids_queue: deque = self._bids[best_bid_price]
            best_asks_queue: deque = self._asks[best_ask_price]
            
            while best_bids_queue and best_asks_queue:
                bid: Order = best_bids_queue[0]
                ask: Order = best_asks_queue[0]
                
                quantity = min(bid._remaining_quantity, ask._remaining_quantity)
                
                bid.fill_order(quantity)
                ask.fill_order(quantity)
                
                if bid.is_filled():
                    best_bids_queue.popleft()
                    del self._orders[bid.order_id]
                    
                if ask.is_filled():
                    best_asks_queue.popleft()
                    del self._orders[ask.order_id]
                                    
                bid_trade_info: TradeInfo = TradeInfo(bid.order_id, bid.price, quantity)
                ask_trade_info: TradeInfo = TradeInfo(ask.order_id, ask.price, quantity)
                trade: Trade = Trade(bid_trade_info, ask_trade_info)
                trades.append(trade)
                
                
                
            if not best_bids_queue:
                del self._bids[best_bid_price]
                self._level_data.pop(best_bid_price, None)
                
            if not best_asks_queue:
                del self._bids[best_ask_price]
                self._level_data.pop(best_ask_price, None)
        if self._bids:
            _, queue = max(self._bids.items())
            order: Order = queue[0]
            if order.order_type == OrderType.FillAndKill:
                self.cancel_order(order.order_id)
        if self._asks:
            _, queue = max(self._asks.items())
            order: Order = queue[0]
            if order.order_type == OrderType.FillAndKill:
                self.cancel_order(order.order_id)
        return trades
    
    def add_order(self, order: Order) -> List[Trade]: 
        if order.order_id in self._orders:
            return []
        
        if order.order_type == OrderType.FillAndKill and not self.can_match(order.side, order.price):
            return []
        
        applicable_book = self._bids if order.side == OrderSide.BUY else self._asks
        
        if order.price not in applicable_book:
            applicable_book[order.price] = deque()
            self._level_data[order.price] = LevelInfo(order.price, 0)
            
        applicable_book[order.price].append(order)
        self._orders[order.order_id] = OrderEntry(order, applicable_book[order.price])
        
        self._level_data[order.price].add_quantity(order.remaining_quantity)
        
        
        return self.match_orders()
        
    def cancel_order(self, order_id: int) -> bool:
        order_entry: OrderEntry = self._orders.get(order_id, None)
        if not order_entry:
            return False
        order: Order = order_entry.order
        queue: deque = order_entry.location
        
        applicable_book = self._bids if order.side == OrderSide.BUY else self._asks
        
        
        if order in queue:
            queue.remove(order)
            self._orders.pop(order_id, None)
        
            if order.price in self._level_data:
                self._level_data[order.price].remove_quantity(order.remaining_quantity)
                
                if self._level_data[order.price].quantity == 0:
                    self._level_data.pop(order.price, None)
            if not queue:
                applicable_book.pop(order.price, None)
                
            return True
        return False
    
    
    def order_modify(self, order: OrderModify) -> List[Trade]: 
        order_entry = self._orders.get(order.order_id)
        if not order_entry:
            return []
        
        self.cancel_order(order.order_id)
        
        new_order: Order = Order(
            _order_type = order_entry.order.order_type,
            _order_id = order.order_id,
            _side = order.side,
            _price = order.price,
            _initial_quantity = order.quantity
        )
        
        self.cancel_order(order.order_id)
        return self.add_order(new_order)
    
    def size(self):
        return len(self._orders)
    
    def get_order_infos(self) -> OrderBookLevelInfos:
        bid_infos = []
        ask_infos = []
        level_info = lambda price, orders: LevelInfo(
            _price=price,
            _quantity = sum(order.remaining_quantity for order in orders)
        )
        
        for price, orders in self._bids.items():
            bid_infos.append(level_info(price, orders))
        
        for price, orders in self._asks.items():
            ask_infos.append(level_info(price, orders))
        
        return OrderBookLevelInfos(bid_infos, ask_infos)
            
            
            
        
        
        
        
        
                
            
        