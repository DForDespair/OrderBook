from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Deque
from Level.Level import LevelInfo, OrderBookLevelInfos
from Order.OrderEnums import OrderType, OrderSide
from Order.Order import Order
from Order.OrderModify import OrderModify
from Trade.TradeInfo import Trade, TradeInfo
import logging

logger = logging.getLogger(__name__)

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
        
    def determine_aggressor(self, order1: Order, order2: Order) -> Order:
        aggressor: Order = order1 if order1.timestamp < order2.timestamp else order2
        return aggressor
        
    def match_orders(self) -> List[Trade]:
        trades: List[Trade] = []
        logger.info(f"Starting order matching - bids: {len(self._bids)}, asks: {len(self._asks)}")
        while self._asks and self._bids:
            best_bid_price: float = max(self._bids.keys())
            best_ask_price: float = min(self._asks.keys())
            
            logger.debug(f"Best bid: {best_bid_price}, best ask: {best_ask_price}")
            if best_bid_price < best_ask_price:
                logger.debug("No match: best bid < best ask")
                break
            
            best_bids_queue: deque = self._bids[best_bid_price]
            best_asks_queue: deque = self._asks[best_ask_price]
            
            while best_bids_queue and best_asks_queue:
                bid: Order = best_bids_queue[0]
                ask: Order = best_asks_queue[0]
                
                quantity = min(bid._remaining_quantity, ask._remaining_quantity)
                
                bid.fill_order(quantity)
                ask.fill_order(quantity)
                
                aggressor = self.determine_aggressor(bid, ask)
                logger.info(f"Matched {quantity} @ {aggressor.price} between BUY {bid.order_id} and SELL {ask.order_id}")

                if bid.is_filled():
                    best_bids_queue.popleft()
                    del self._orders[bid.order_id]
                    logger.debug(f"Order {bid.order_id} fully filled and removed (BUY)")

                if ask.is_filled():
                    best_asks_queue.popleft()
                    del self._orders[ask.order_id]
                    logger.debug(f"Order {ask.order_id} fully filled and removed (SELL)")
    
                bid_trade_info: TradeInfo = TradeInfo(bid.order_id, aggressor.price, quantity)
                ask_trade_info: TradeInfo = TradeInfo(ask.order_id, aggressor.price, quantity)
                trade: Trade = Trade(bid_trade_info, ask_trade_info)
                trades.append(trade)
                
                
                
            if not best_bids_queue:
                del self._bids[best_bid_price]
                self._level_data.pop(best_bid_price, None)
                logger.debug(f"Removed empty bid level: {best_bid_price}")

                
            if not best_asks_queue:
                del self._asks[best_ask_price]
                self._level_data.pop(best_ask_price, None)
                logger.debug(f"Removed empty ask level: {best_ask_price}")

        if self._bids:
            _, queue = max(self._bids.items())
            order: Order = queue[0]
            if order.order_type == OrderType.FillAndKill:
                self.cancel_order(order.order_id)
                logger.info(f"FillAndKill BUY order {order.order_id} could not be matched and was cancelled")

        if self._asks:
            _, queue = min(self._asks.items())
            order: Order = queue[0]
            if order.order_type == OrderType.FillAndKill:
                self.cancel_order(order.order_id)
                logger.info(f"FillAndKill SELL order {order.order_id} could not be matched and was cancelled")
        return trades
    
    def add_order(self, order: Order) -> List[Trade]: 
        if order.order_id in self._orders:
            logger.warning(f"Duplicate order ID {order.order_id} rejected.")
            return []
        
        if order.order_type == OrderType.FillAndKill and not self.can_match(order.side, order.price):
            logger.info(f"FillAndKill order {order.order_id} was unable to be matched and was discarded")
            return []
        
        applicable_book = self._bids if order.side == OrderSide.BUY else self._asks
        
        if order.price not in applicable_book:
            applicable_book[order.price] = deque()
            self._level_data[order.price] = LevelInfo(order.price, 0)
            
        applicable_book[order.price].append(order)
        self._orders[order.order_id] = OrderEntry(order, applicable_book[order.price])
        
        self._level_data[order.price].add_quantity(order.remaining_quantity)
        
        logger.info(f"Added {order}")
        return self.match_orders()
        
    def cancel_order(self, order_id: int) -> bool:
        order_entry: OrderEntry = self._orders.get(order_id, None)
        if not order_entry:
            logger.warning(f"Cancel failed: Order ID: {order_id} not found.")
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
            logger.info(f"Cancelled order {order_id}")    
            return True
        logger.warning(f"Order {order_id} not found in queue during cancel.")
        return False
    
    
    def order_modify(self, order: OrderModify) -> List[Trade]:
        order_entry = self._orders.get(order.order_id)
        if not order_entry:
            logger.warning(f"Modify failed: order ID {order.order_id} not found.")
            return []

        logger.info(f"Modifying order {order.order_id} -> {order.quantity} @ {order.price}")
        self.cancel_order(order.order_id)

        new_order = Order(
            _order_type=order_entry.order.order_type,
            _order_id=order.order_id,
            _side=order.side,
            _price=order.price,
            _initial_quantity=order.quantity
        )

        return self.add_order(new_order)

    
    def size(self) -> int:
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
            
            
            
        
        
        
        
        
                
            
        