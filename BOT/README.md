# Simplified Trading Bot for Binance Futures Testnet

A comprehensive Python trading bot implementation for Binance Futures Testnet with CLI interface, advanced order types, and robust error handling.

## Features

✅ **Core Requirements**
- Market and Limit orders on Binance Futures Testnet (USDT-M)
- Support for both BUY and SELL order sides
- Official Binance API integration (REST)
- Command-line interface with input validation
- Comprehensive logging and error handling
- Order details and execution status output

✅ **Bonus Features**
- Advanced order types: Stop-Limit and OCO (One-Cancels-Other)
- Interactive mode for easy trading
- Account summary with positions and open orders
- Colored terminal output for better UX
- Detailed logging with timestamps

## Installation

1. **Clone or download the project files**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. **Register for Binance Futures Testnet:**
   - Go to [Binance Futures Testnet](https://testnet.binancefuture.com)
   - Create an account and get your API credentials
   - Note: Use the testnet URL: `https://testnet.binancefuture.com`

2. **Get API Credentials:**
   - Generate API Key and Secret from your testnet account
   - Ensure futures trading is enabled

## Usage

### Command Line Interface

**Basic Syntax:**
```bash
python trading_bot.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET [COMMAND] [OPTIONS]
```

**Available Commands:**

#### 1. Market Order
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET market BTCUSDT BUY 0.001
```

#### 2. Limit Order
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET limit BTCUSDT SELL 0.001 50000
```

#### 3. Stop-Limit Order (Bonus)
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET stop-limit BTCUSDT BUY 0.001 45000 44000
```

#### 4. OCO Order (Bonus)
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET oco BTCUSDT SELL 0.001 55000 56000 56500
```

#### 5. Account Information
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET account
```

#### 6. Order Status
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET status BTCUSDT 123456789
```

#### 7. Cancel Order
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET cancel BTCUSDT 123456789
```

#### 8. Interactive Mode
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET interactive
```

### Interactive Mode

The interactive mode provides an easy-to-use interface:

```
Bot> help
Available commands:
  account     - Display account summary
  market      - Place market order
  limit       - Place limit order
  stop-limit  - Place stop-limit order
  oco         - Place OCO order
  status      - Get order status
  cancel      - Cancel order
  orders      - Show open orders
  positions   - Show positions
  help        - Show this help
  quit        - Exit interactive mode
```

## Project Structure

```
BOT/
├── trading_bot.py          # Main trading bot implementation
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
└── logs/                  # Log files (created automatically)
    └── trading_bot_YYYYMMDD_HHMMSS.log
```

## Key Features Explained

### 1. **Robust Error Handling**
- Validates all order parameters before submission
- Handles Binance API exceptions gracefully
- Comprehensive logging of all operations

### 2. **Order Validation**
- Checks symbol availability
- Validates quantity precision and minimum requirements
- Ensures price requirements for limit orders

### 3. **Advanced Order Types**
- **Stop-Limit**: Triggers a limit order when stop price is reached
- **OCO**: Places two orders where one cancels the other

### 4. **Account Management**
- Real-time account balance display
- Active positions overview
- Open orders monitoring

### 5. **Logging System**
- Detailed logs with timestamps
- Separate log files for each session
- Console output for user feedback

## Example Usage Scenarios

### Scenario 1: Quick Market Buy
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET market BTCUSDT BUY 0.001
```

### Scenario 2: Set a Limit Sell Order
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET limit BTCUSDT SELL 0.001 55000
```

### Scenario 3: Check Account Status
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET account
```

### Scenario 4: Interactive Trading Session
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET interactive
```

## Error Handling

The bot includes comprehensive error handling for:
- Invalid API credentials
- Network connectivity issues
- Invalid order parameters
- Insufficient balance
- Symbol not found
- Order execution failures

## Logging

All operations are logged to:
- **Console**: Real-time feedback with colored output
- **Log Files**: Detailed logs in `logs/` directory with timestamps

## Security Notes

- **Testnet Only**: This bot is configured for Binance Futures Testnet by default
- **API Security**: Never share your API credentials
- **Environment Variables**: Consider using environment variables for API keys in production

## Troubleshooting

### Common Issues:

1. **"ModuleNotFoundError: No module named 'binance'"**
   ```bash
   pip install python-binance
   ```

2. **"Invalid API credentials"**
   - Verify your API key and secret
   - Ensure futures trading is enabled in your testnet account

3. **"Symbol not found"**
   - Use correct symbol format (e.g., BTCUSDT, not BTC/USDT)
   - Check if the symbol is available on Binance Futures

4. **"Insufficient balance"**
   - Add testnet funds to your account
   - Check your available balance

## Contributing

This is a submission for a Python Developer position. The implementation includes:
- Clean, well-documented code
- Comprehensive error handling
- Bonus features beyond requirements
- Professional logging system
- User-friendly CLI interface

## License

This project is created for educational and assessment purposes.

---

**Ready to trade!** 🚀

Start with the interactive mode for the best experience:
```bash
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET interactive
```
