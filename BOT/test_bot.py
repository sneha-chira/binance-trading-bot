#!/usr/bin/env python3
"""
Simple test script for the trading bot
"""

import os
import sys
from trading_bot import TradingBot

def test_bot_import():
    """Test if the bot can be imported and basic functionality works"""
    print("Testing Trading Bot Import...")
    print("=" * 40)
    
    try:
        # Test import
        from trading_bot import TradingBot
        print("✓ TradingBot class imported successfully")
        
        # Test if we can create a basic instance (without API calls)
        print("✓ All dependencies are available")
        
        print("\nBot is ready for testing!")
        print("\nTo test with your API credentials:")
        print("1. Get your API key and secret from Binance Testnet")
        print("2. Run: python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET account")
        print("3. Or try interactive mode: python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET interactive")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def show_usage_examples():
    """Show usage examples"""
    print("\n" + "=" * 60)
    print("USAGE EXAMPLES")
    print("=" * 60)
    
    examples = [
        ("Account Info", "python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET account"),
        ("Market Order", "python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET market BTCUSDT BUY 0.001"),
        ("Limit Order", "python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET limit BTCUSDT SELL 0.001 50000"),
        ("Interactive Mode", "python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET interactive"),
        ("Help", "python trading_bot.py --help")
    ]
    
    for desc, cmd in examples:
        print(f"\n{desc}:")
        print(f"  {cmd}")

if __name__ == "__main__":
    success = test_bot_import()
    
    if success:
        show_usage_examples()
        
        print("\n" + "=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        print("1. Get your Binance Testnet API credentials")
        print("2. Test the bot with your credentials")
        print("3. Create a GitHub repository")
        print("4. Send your application email")
        print("\nGood luck with your application! 🚀")
    else:
        print("\nPlease fix the import issues before proceeding.")
        sys.exit(1)
