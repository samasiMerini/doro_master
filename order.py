
import format_order  as order


usdtQty = order.get_usdt_balance(fee=0)

def  startOrder(ticker):
    if usdtQty >= 60:
        return (order.execute_buy_market_order(symbol=ticker,usdt_amount=(usdtQty*0.5)))

