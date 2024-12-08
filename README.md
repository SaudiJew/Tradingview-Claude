# TradingView-Claude Integration

A Python-based integration for handling TradingView webhooks and automating trading signals, with built-in support for Binance trading.

## Features

- Secure webhook handling with HMAC signature validation
- Type-safe signal processing using dataclasses
- Comprehensive error handling and logging
- Flexible extension points for custom trading logic
- Built-in Binance integration (supports both mainnet and testnet)
- Flask-based web server for receiving webhooks
- Comprehensive test suite

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

3. Set up environment variables:
```bash
# Required for TradingView webhook validation
export TRADINGVIEW_SECRET_KEY=your-secret-key

# Required for Binance integration
export BINANCE_API_KEY=your-binance-api-key
export BINANCE_API_SECRET=your-binance-api-secret
export USE_BINANCE_TESTNET=true  # Set to false for mainnet
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
        "volume": {{volume}},
        "position_size": 1.0
    }
}
```

### Using Binance Integration

1. Run the Binance example:
```bash
python binance_example.py
```

The Binance integration provides:
- Automatic order execution on Binance
- Support for both mainnet and testnet
- Position size management
- Error handling and logging

Example TradingView alert for Binance:
```json
{
    "symbol": "BTCUSDT",
    "action": "BUY",
    "price": {{close}},
    "strategy": "RSI_Strategy",
    "parameters": {
        "position_size": 0.01,
        "timeframe": "1h"
    }
}
```

### Custom Trading Logic

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

## Testing

The project includes a comprehensive test suite using pytest. To run the tests:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=.

# Run specific test file
pytest tests/test_binance_integration.py
```

The test suite includes:
- Unit tests for TradingView integration
- Unit tests for Binance integration
- End-to-end integration tests
- Mock tests for external dependencies

## Security

- Webhook endpoints are protected with HMAC signature validation
- Environment variables are used for sensitive configuration
- Comprehensive input validation and error handling
- Testnet support for safe testing

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.