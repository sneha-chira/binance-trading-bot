#!/usr/bin/env python3
"""
Simple verification script for the trading bot
"""

import sys
import os

def verify_imports():
    """Verify all required modules can be imported"""
    print("Verifying Trading Bot...")
    print("=" * 40)
    
    try:
        # Test main bot import
        from trading_bot import TradingBot
        print("✓ TradingBot class imported successfully")
        
        # Test demo bot import
        from demo_bot import DemoTradingBot
        print("✓ DemoTradingBot class imported successfully")
        
        # Test dependencies
        import binance
        print("✓ python-binance library available")
        
        import colorama
        print("✓ colorama library available")
        
        import tabulate
        print("✓ tabulate library available")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def verify_files():
    """Verify all required files exist"""
    print("\nVerifying project files...")
    print("=" * 40)
    
    required_files = [
        'trading_bot.py',
        'demo_bot.py', 
        'README.md',
        'requirements.txt',
        'quick_start.py',
        'config_example.py',
        'FINAL_EMAIL.md',
        'PROJECT_SUMMARY.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_exist = False
    
    return all_exist

def verify_demo():
    """Verify demo works"""
    print("\nVerifying demo functionality...")
    print("=" * 40)
    
    try:
        from demo_bot import DemoTradingBot
        bot = DemoTradingBot()
        
        # Test basic functionality
        bot.display_account_summary()
        print("✓ Demo account summary works")
        
        # Test order placement
        order = bot.place_market_order("BTCUSDT", "BUY", 0.001)
        print("✓ Demo market order works")
        
        order = bot.place_limit_order("BTCUSDT", "SELL", 0.001, 50000)
        print("✓ Demo limit order works")
        
        return True
        
    except Exception as e:
        print(f"✗ Demo error: {e}")
        return False

def main():
    """Main verification function"""
    print("TRADING BOT VERIFICATION")
    print("=" * 50)
    
    # Run all checks
    imports_ok = verify_imports()
    files_ok = verify_files()
    demo_ok = verify_demo()
    
    print("\n" + "=" * 50)
    print("VERIFICATION RESULTS")
    print("=" * 50)
    
    if imports_ok:
        print("✓ All imports successful")
    else:
        print("✗ Import issues found")
    
    if files_ok:
        print("✓ All required files present")
    else:
        print("✗ Some files missing")
    
    if demo_ok:
        print("✓ Demo functionality works")
    else:
        print("✗ Demo issues found")
    
    if imports_ok and files_ok and demo_ok:
        print("\n🎉 ALL CHECKS PASSED!")
        print("Your trading bot is ready for submission!")
        print("\nNext steps:")
        print("1. Create GitHub repository")
        print("2. Upload all files")
        print("3. Send application email")
        return True
    else:
        print("\n❌ Some issues found. Please fix before submitting.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
