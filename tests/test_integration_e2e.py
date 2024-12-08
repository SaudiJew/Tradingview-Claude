import pytest
import json
from flask.testing import FlaskClient
from tradingview_integration import create_app
from binance_integration import BinanceCredentials, BinanceTrader
from unittest.mock import Mock, patch

@pytest.fixture
def app():
    return create_app('test-secret-key')

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def valid_webhook_payload():
    return {
        'symbol': 'BTCUSDT',
        'action': 'BUY',
        'price': 50000.0,
        'timestamp': 1639000000,
        'strategy': 'TestStrategy',
        'parameters': {
            'timeframe': '1h',
            'position_size': 1.0
        }
    }

def create_signature(payload: dict, secret_key: str) -> str:
    import hmac
    import hashlib
    return hmac.new(
        secret_key.encode(),
        json.dumps(payload, sort_keys=True).encode(),
        hashlib.sha256
    ).hexdigest()

def test_webhook_endpoint_valid_request(client, valid_webhook_payload):
    # Create valid signature
    signature = create_signature(valid_webhook_payload, 'test-secret-key')
    
    # Send request
    response = client.post(
        '/webhook',
        json=valid_webhook_payload,
        headers={'X-TradingView-Signature': signature}
    )
    
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_webhook_endpoint_invalid_signature(client, valid_webhook_payload):
    response = client.post(
        '/webhook',
        json=valid_webhook_payload,
        headers={'X-TradingView-Signature': 'invalid-signature'}
    )
    
    assert response.status_code == 401
    assert 'error' in response.json

def test_webhook_endpoint_missing_signature(client, valid_webhook_payload):
    response = client.post(
        '/webhook',
        json=valid_webhook_payload
    )
    
    assert response.status_code == 401
    assert 'error' in response.json

def test_webhook_endpoint_invalid_json(client):
    response = client.post(
        '/webhook',
        data='invalid-json',
        headers={'X-TradingView-Signature': 'some-signature'}
    )
    
    assert response.status_code == 400
    assert 'error' in response.json

@patch('binance_integration.BinanceClient')
def test_full_integration_flow(mock_binance_client, client, valid_webhook_payload):
    # Mock Binance client responses
    mock_client = mock_binance_client.return_value
    mock_client.get_symbol_price.return_value = {'price': '50000.0'}
    mock_client.create_order.return_value = {
        'orderId': '12345',
        'status': 'FILLED'
    }
    
    # Create valid signature
    signature = create_signature(valid_webhook_payload, 'test-secret-key')
    
    # Send webhook request
    response = client.post(
        '/webhook',
        json=valid_webhook_payload,
        headers={'X-TradingView-Signature': signature}
    )
    
    assert response.status_code == 200
    
    # Verify Binance client interactions
    mock_client.get_symbol_price.assert_called_once_with('BTCUSDT')
    mock_client.create_order.assert_called_once()