#!/usr/bin/env python3
"""
Quick Start Script for Trading Bot
This script provides a simple way to test the trading bot functionality
"""

import os
import sys
from trading_bot import TradingBot

def quick_test():
    """Quick test function to verify bot functionality"""
    
    print("Trading Bot Quick Start")
    print("=" * 50)
    
    # Get API credentials
    api_key = input("Enter your Binance Testnet API Key: ").strip()
    api_secret = input("Enter your Binance Testnet API Secret: ").strip()
    
    if not api_key or not api_secret:
        print("ERROR: API credentials are required!")
        return
    
    try:
        # Initialize bot
        print("\nInitializing trading bot...")
        bot = TradingBot(api_key=api_key, api_secret=api_secret, testnet=True)
        print("SUCCESS: Bot initialized successfully!")
        
        # Display account info
        print("\nAccount Information:")
        bot.display_account_summary()
        
        # Test market order (small amount)
        print("\nTesting market order...")
        test_symbol = "BTCUSDT"
        test_quantity = 0.001
        
        try:
            order = bot.place_market_order(test_symbol, "BUY", test_quantity)
            print(f"SUCCESS: Test market order placed! Order ID: {order['orderId']}")
            
            # Check order status
            order_status = bot.get_order_status(test_symbol, order['orderId'])
            print(f"Order Status: {order_status['status']}")
            
        except Exception as e:
            print(f"WARNING: Market order test failed: {e}")
            print("This might be due to insufficient balance or other API restrictions")
        
        print("\nQuick test completed!")
        print("\nNext steps:")
        print("1. Use 'python trading_bot.py --help' to see all available commands")
        print("2. Try interactive mode: 'python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET interactive'")
        print("3. Check the logs/ directory for detailed operation logs")
        
    except Exception as e:
        print(f"ERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Verify your API credentials are correct")
        print("2. Ensure futures trading is enabled in your testnet account")
        print("3. Check your internet connection")
        print("4. Make sure you have testnet funds available")

if __name__ == "__main__":
    quick_test()
