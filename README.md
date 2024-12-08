# TradingView-Claude Integration

A Python-based integration for handling TradingView webhooks and automating trading signals. This implementation provides a secure and extensible foundation for building automated trading systems based on TradingView alerts.

## Features

- Secure webhook handling with HMAC signature validation
- Type-safe signal processing using dataclasses
- Comprehensive error handling and logging
- Flexible extension points for custom trading logic
- Flask-based web server for receiving webhooks

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SaudiJew/Tradingview-Claude.git
cd Tradingview-Claude
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your secret key:
```bash
export TRADINGVIEW_SECRET_KEY=your-secret-key
```

## Usage

### Basic Setup

1. Run the server:
```bash
python tradingview_integration.py
```

2. Configure TradingView Alert:
- Create a new alert in TradingView
- Set the webhook URL to: `http://your-server:5000/webhook`
- Format the alert message as JSON:
```json
{
    "symbol": "{{ticker}}",
    "action": "{{strategy.order.action}}",
    "price": {{close}},
    "strategy": "YOUR_STRATEGY_NAME",
    "parameters": {
        "timeframe": "{{interval}}",
        "volume": {{volume}}
    }
}
```

### Implementing Custom Trading Logic

Extend the `TradingViewIntegration` class and override the `handle_trading_signal` method:

```python
from tradingview_integration import TradingViewIntegration, TradingSignal

class MyTradingStrategy(TradingViewIntegration):
    def handle_trading_signal(self, signal: TradingSignal):
        if signal.action == "BUY":
            # Implement buy logic
            print(f"Executing BUY for {signal.symbol} at {signal.price}")
        elif signal.action == "SELL":
            # Implement sell logic
            print(f"Executing SELL for {signal.symbol} at {signal.price}")
```

## Security

- Webhook endpoints are protected with HMAC signature validation
- Environment variables are used for sensitive configuration
- Comprehensive input validation and error handling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.