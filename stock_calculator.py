from datetime import datetime, timedelta
import pandas as pd
import logging
import random

logger = logging.getLogger('Stock Calculator')
logging.basicConfig(level=logging.INFO)

class StockCalc:
    def __init__(self, stock_symbol: str, stock_type: str, last_dividend: float, fixed_dividend: float, par_value: float):
        self.stock_symbol = stock_symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value
        self.trades = []

    def calculate_yield(self, price: int) -> float:
        try:
            if self.stock_type.lower() == 'common':
                return self.last_dividend / price if price > 0 else 0
            elif self.stock_type.lower() == 'preferred':
                return (self.fixed_dividend * self.par_value) / price if price > 0 else 0
            else:
                raise ValueError(f"For {self.stock_symbol}, Invalid stock type {self.stock_type}")
        except Exception as e:
            logger.warning(f"Error calculating dividend yield: {str(e)}")
            return 0.0

    def calculate_pe_ratio(self, price: int) -> float:
        try:
            if self.last_dividend > 0:
                return price / self.last_dividend
            else:
                raise ValueError(
                    f"For {self.stock_symbol}, Last Dividend must be greater than 0 to calculate P/E ratio.")
        except Exception as e:
            logger.info(f"Error calculating P/E Ratio: {str(e)}")
            return 0.0

    def calculate_stock_data(self, quantity: int, buy_or_sell: str, traded_price: int):
        logger.debug('Calcukate Stock Data')

        div_yield = self.calculate_yield(stock_price)
        logger.info(f"Dividend Yield for {data.get('Stock Symbol')} = {div_yield}")

        pe_ratio = self.calculate_pe_ratio(stock_price)
        logger.info(f"P/E Ratio for {data.get('Stock Symbol')} = {pe_ratio}")

        trade = {
            'timestamp': datetime.now(),
            'quantity': quantity,
            'buy_or_sell': buy_or_sell,
            'traded_price': traded_price
        }
        self.trades.append(trade)
        logger.info(f"Trade processed & recorded for {self.stock_symbol}: {trade}")

    def calculate_volume_weighted_stock_price(self) -> float:
        try:
            current_time = datetime.now()
            time_limit = current_time - timedelta(minutes=15)

            recent_trades = [trade for trade in self.trades if trade['timestamp'] >= time_limit]

            total_quantity = sum(trade['quantity'] for trade in recent_trades)
            total_value = sum(trade['quantity'] * trade['traded_price'] for trade in recent_trades)

            if total_quantity > 0:
                return total_value / total_quantity
            else:
                return 0.0
        except Exception as e:
            logger.warning(f"Error calculating Volume Weighted Stock Price: {str(e)}")
            return 0.0

if __name__ == '__main__':
    try:
        df = pd.read_csv('sample_data.csv').fillna(0)
    except Exception as e:
        df = pd.DataFrame()
        logger.warning(f'Unable to read data from file, Error as {str(e)}')

    logger.info(f"Data Extracted From File -\n {df}")
    if df.empty:
        raise Exception("Empty File has been received")

    record = df.to_dict('records')
    prices = []
    for data in record:
        stock_calc = StockCalc(stock_symbol=data.get('Stock Symbol'), stock_type=data.get('Type'),
                      last_dividend=data.get('Last Dividend'), fixed_dividend=data.get('Fixed Dividend'),
                      par_value=data.get('Par Value'))

        stock_qty = random.randrange(100, 151)
        stock_price = random.randrange(90, 101)
        direction = random.choice(["BUY", "SELL"])
        stock_calc.calculate_stock_data(quantity=stock_qty, buy_or_sell=direction, traded_price=stock_price)
        vwsp = stock_calc.calculate_volume_weighted_stock_price()
        logger.info(f"Volume Weighted Stock Price for {data.get('Stock Symbol')} =  {vwsp}")
        prices.append(vwsp)

    try:
        if len(prices) > 0:
            product = 1
            for price in prices:
                product *= price
            gbce =  product ** (1 / len(prices))
        else:
            raise ValueError("No prices are available to calculate GBCE.")
    except Exception as e:
        logger.warning(f"Error calculating GBCE All Share Index: {str(e)}")
        gbce =  0.0
    logger.info(f"GBCE All Share Index: {gbce}")
