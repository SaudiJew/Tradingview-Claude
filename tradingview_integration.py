import json
import hmac
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify
from dataclasses import dataclass
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TradingSignal:
    symbol: str
    action: str  # 'BUY' or 'SELL'
    price: float
    timestamp: datetime
    strategy_name: Optional[str] = None
    additional_params: Optional[Dict[str, Any]] = None

class TradingViewWebhookHandler:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        
    def validate_webhook(self, payload: dict, signature: str) -> bool:
        calculated_signature = hmac.new(
            self.secret_key.encode(),
            json.dumps(payload, sort_keys=True).encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(calculated_signature, signature)

    def parse_signal(self, payload: dict) -> TradingSignal:
        try:
            return TradingSignal(
                symbol=payload['symbol'],
                action=payload['action'].upper(),
                price=float(payload['price']),
                timestamp=datetime.fromtimestamp(payload['timestamp'])
                    if 'timestamp' in payload
                    else datetime.utcnow(),
                strategy_name=payload.get('strategy'),
                additional_params=payload.get('parameters', {})
            )
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing signal: {e}")
            raise ValueError(f"Invalid payload format: {e}")

class TradingViewIntegration:
    def __init__(self, secret_key: str):
        self.app = Flask(__name__)
        self.webhook_handler = TradingViewWebhookHandler(secret_key)
        
        # Register routes
        self.app.route('/webhook', methods=['POST'])(self.webhook_endpoint)
        
    def webhook_endpoint(self):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
            
        payload = request.json
        signature = request.headers.get('X-TradingView-Signature')
        
        if not signature:
            return jsonify({'error': 'Missing signature'}), 401
            
        if not self.webhook_handler.validate_webhook(payload, signature):
            return jsonify({'error': 'Invalid signature'}), 401
            
        try:
            signal = self.webhook_handler.parse_signal(payload)
            self.handle_trading_signal(signal)
            return jsonify({'status': 'success', 'message': 'Signal processed'}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
            
    def handle_trading_signal(self, signal: TradingSignal):
        logger.info(f"Received signal: {signal}")
        # Implement your trading logic here
        pass

def create_app(secret_key: str) -> Flask:
    integration = TradingViewIntegration(secret_key)
    return integration.app

if __name__ == '__main__':
    import os
    
    # Get secret key from environment variable
    SECRET_KEY = os.getenv('TRADINGVIEW_SECRET_KEY', 'your-secret-key')
    
    app = create_app(SECRET_KEY)
    app.run(host='0.0.0.0', port=5000, debug=False)