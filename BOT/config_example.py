# Configuration Example for Trading Bot
# Copy this file to config.py and fill in your API credentials

# Binance Futures Testnet API Credentials
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"

# Trading Configuration
TESTNET = True  # Set to False for mainnet (NOT RECOMMENDED for testing)

# Logging Configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE = True
LOG_TO_CONSOLE = True

# Default Trading Parameters
DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_QUANTITY = 0.001
DEFAULT_LEVERAGE = 1

# Risk Management
MAX_POSITION_SIZE = 0.01  # Maximum position size in BTC
STOP_LOSS_PERCENTAGE = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENTAGE = 0.05  # 5% take profit
