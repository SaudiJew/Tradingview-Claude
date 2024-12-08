# Example configuration file

# Server settings
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False

# Security
SECRET_KEY = 'your-secret-key'  # Replace with your actual secret key

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Trading parameters
DEFAULT_POSITION_SIZE = 1.0
MAX_POSITION_SIZE = 10.0
RISK_PERCENTAGE = 0.02  # 2% risk per trade