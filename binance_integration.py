from typing import Optional, Dict, Any
from decimal import Decimal
import logging
import hmac
import time
from urllib.parse import urlencode
import requests
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class BinanceCredentials:
    api_key: str
    api_secret: str
    testnet: bool = False

class BinanceClient:
    def __init__(self, credentials: BinanceCredentials):
        self.credentials = credentials
        self.base_url = 'https://testnet.binance.vision/api/v3' if credentials.testnet else 'https://api.binance.com/api/v3'
        
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        query_string = urlencode(params)
        return hmac.new(
            self.credentials.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            'sha256'
        ).hexdigest()
        
    def _send_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, signed: bool = False) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'X-MBX-APIKEY': self.credentials.api_key}
        
        if params is None:
            params = {}
            
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        try:
            response = requests.request(method, url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Binance API error: {str(e)}")
            raise
            
    def get_account_info(self) -> Dict:
        """Get current account information."""
        return self._send_request('GET', '/account', signed=True)
        
    def create_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> Dict:
        """Create a new order."""
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }
        
        if price and order_type != 'MARKET':
            params['price'] = price
            
        return self._send_request('POST', '/order', params=params, signed=True)
        
    def get_exchange_info(self) -> Dict:
        """Get exchange trading rules and symbol information."""
        return self._send_request('GET', '/exchangeInfo')
        
    def get_symbol_price(self, symbol: str) -> Dict:
        """Get latest price for a symbol."""
        return self._send_request('GET', '/ticker/price', params={'symbol': symbol})

class BinanceTrader:
    def __init__(self, client: BinanceClient):
        self.client = client
        self.logger = logging.getLogger(__name__)
        
    def execute_trade(self, symbol: str, side: str, quantity: float, price: Optional[float] = None) -> Dict:
        """Execute a trade on Binance."""
        try:
            # Normalize the trading pair symbol
            symbol = symbol.upper().replace('/', '')
            
            # Validate the side
            if side not in ['BUY', 'SELL']:
                raise ValueError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'.")
                
            # Get current market price if not specified
            if not price:
                price_info = self.client.get_symbol_price(symbol)
                price = float(price_info['price'])
                
            # Create the order
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                order_type='LIMIT',
                quantity=quantity,
                price=price
            )
            
            self.logger.info(f"Executed {side} order for {quantity} {symbol} at {price}")
            return order
            
        except Exception as e:
            self.logger.error(f"Error executing trade: {str(e)}")
            raise
            
    def get_account_balance(self, asset: str) -> float:
        """Get the balance of a specific asset."""
        try:
            account_info = self.client.get_account_info()
            balances = {b['asset']: float(b['free']) for b in account_info['balances']}
            return balances.get(asset.upper(), 0.0)
        except Exception as e:
            self.logger.error(f"Error getting balance: {str(e)}")
            raise