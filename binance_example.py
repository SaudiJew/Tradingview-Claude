from tradingview_integration import TradingViewIntegration, TradingSignal
from binance_integration import BinanceClient, BinanceCredentials, BinanceTrader
import os
from dotenv import load_dotenv
import logging

class BinanceTradingStrategy(TradingViewIntegration):
    def __init__(self, tv_secret_key: str, binance_credentials: BinanceCredentials):
        super().__init__(tv_secret_key)
        self.client = BinanceClient(binance_credentials)
        self.trader = BinanceTrader(self.client)
        self.logger = logging.getLogger(__name__)
        
    def handle_trading_signal(self, signal: TradingSignal):
        try:
            # Get position size from parameters or use default
            position_size = signal.additional_params.get('position_size', 1.0)
            
            # Execute the trade
            order = self.trader.execute_trade(
                symbol=signal.symbol,
                side=signal.action,
                quantity=position_size,
                price=signal.price
            )
            
            self.logger.info(f"Order executed: {order}")
            
        except Exception as e:
            self.logger.error(f"Error handling signal: {str(e)}")
            raise

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Get configuration from environment variables
    TV_SECRET_KEY = os.getenv("TRADINGVIEW_SECRET_KEY")
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
    USE_TESTNET = os.getenv("USE_BINANCE_TESTNET", "true").lower() == "true"
    
    if not all([TV_SECRET_KEY, BINANCE_API_KEY, BINANCE_API_SECRET]):
        raise ValueError("Missing required environment variables")
    
    # Initialize Binance credentials
    credentials = BinanceCredentials(
        api_key=BINANCE_API_KEY,
        api_secret=BINANCE_API_SECRET,
        testnet=USE_TESTNET
    )
    
    # Create and run the trading strategy
    strategy = BinanceTradingStrategy(TV_SECRET_KEY, credentials)
    app = strategy.app
    
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=False)