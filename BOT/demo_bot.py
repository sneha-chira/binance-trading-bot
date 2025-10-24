#!/usr/bin/env python3
"""
Demo Trading Bot - Shows functionality without real API calls
Perfect for demonstrating your implementation
"""

import json
from datetime import datetime
from colorama import init, Fore, Style
from tabulate import tabulate

init(autoreset=True)

class DemoTradingBot:
    """Demo version of the trading bot for demonstration purposes"""
    
    def __init__(self):
        self.demo_mode = True
        print(f"{Fore.CYAN}Demo Trading Bot - Binance Futures Testnet")
        print(f"{Fore.YELLOW}This is a demonstration of the trading bot functionality")
        print("=" * 60)
    
    def display_account_summary(self):
        """Display demo account summary"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}ACCOUNT SUMMARY (DEMO)")
        print(f"{Fore.CYAN}{'='*60}")
        
        print(f"{Fore.GREEN}Total Wallet Balance: 1000.0000 USDT")
        print(f"{Fore.YELLOW}Total Unrealized PnL: 15.2500 USDT")
        print(f"{Fore.BLUE}Total Margin Balance: 1015.2500 USDT")
        
        # Demo positions
        print(f"\n{Fore.CYAN}ACTIVE POSITIONS:")
        print(f"{Fore.CYAN}{'-'*60}")
        
        position_data = [
            ["BTCUSDT", "LONG", "0.001000", "45000.00", "46500.00", "1.50 USDT"],
            ["ETHUSDT", "SHORT", "0.010000", "3000.00", "2950.00", "5.00 USDT"]
        ]
        
        headers = ['Symbol', 'Side', 'Size', 'Entry Price', 'Mark Price', 'Unrealized PnL']
        print(tabulate(position_data, headers=headers, tablefmt='grid'))
        
        # Demo open orders
        print(f"\n{Fore.CYAN}OPEN ORDERS:")
        print(f"{Fore.CYAN}{'-'*60}")
        
        order_data = [
            ["BTCUSDT", "SELL", "LIMIT", "0.001000", "47000.00", "NEW"],
            ["ETHUSDT", "BUY", "STOP", "0.005000", "Market", "NEW"]
        ]
        
        headers = ['Symbol', 'Side', 'Type', 'Quantity', 'Price', 'Status']
        print(tabulate(order_data, headers=headers, tablefmt='grid'))
        
        print(f"{Fore.CYAN}{'='*60}\n")
    
    def place_market_order(self, symbol, side, quantity):
        """Demo market order placement"""
        print(f"{Fore.GREEN}Placing market order...")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {quantity}")
        
        # Simulate order placement
        order = {
            'orderId': 123456789,
            'symbol': symbol,
            'side': side,
            'type': 'MARKET',
            'quantity': str(quantity),
            'status': 'FILLED',
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"{Fore.GREEN}SUCCESS: Market order placed successfully!")
        print(f"{Fore.CYAN}Order ID: {order['orderId']}")
        print(f"{Fore.CYAN}Status: {order['status']}")
        
        return order
    
    def place_limit_order(self, symbol, side, quantity, price):
        """Demo limit order placement"""
        print(f"{Fore.GREEN}Placing limit order...")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {quantity}")
        print(f"Price: {price}")
        
        # Simulate order placement
        order = {
            'orderId': 123456790,
            'symbol': symbol,
            'side': side,
            'type': 'LIMIT',
            'quantity': str(quantity),
            'price': str(price),
            'status': 'NEW',
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"{Fore.GREEN}SUCCESS: Limit order placed successfully!")
        print(f"{Fore.CYAN}Order ID: {order['orderId']}")
        print(f"{Fore.CYAN}Status: {order['status']}")
        
        return order
    
    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price):
        """Demo stop-limit order placement"""
        print(f"{Fore.GREEN}Placing stop-limit order...")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {quantity}")
        print(f"Price: {price}")
        print(f"Stop Price: {stop_price}")
        
        # Simulate order placement
        order = {
            'orderId': 123456791,
            'symbol': symbol,
            'side': side,
            'type': 'STOP',
            'quantity': str(quantity),
            'price': str(price),
            'stopPrice': str(stop_price),
            'status': 'NEW',
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"{Fore.GREEN}SUCCESS: Stop-limit order placed successfully!")
        print(f"{Fore.CYAN}Order ID: {order['orderId']}")
        print(f"{Fore.CYAN}Status: {order['status']}")
        
        return order
    
    def place_oco_order(self, symbol, side, quantity, price, stop_price, stop_limit_price):
        """Demo OCO order placement"""
        print(f"{Fore.GREEN}Placing OCO order...")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {quantity}")
        print(f"Price: {price}")
        print(f"Stop Price: {stop_price}")
        print(f"Stop Limit Price: {stop_limit_price}")
        
        # Simulate order placement
        order = {
            'orderId': 123456792,
            'symbol': symbol,
            'side': side,
            'type': 'OCO',
            'quantity': str(quantity),
            'price': str(price),
            'stopPrice': str(stop_price),
            'stopLimitPrice': str(stop_limit_price),
            'status': 'NEW',
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"{Fore.GREEN}SUCCESS: OCO order placed successfully!")
        print(f"{Fore.CYAN}Order ID: {order['orderId']}")
        print(f"{Fore.CYAN}Status: {order['status']}")
        
        return order

def demo_interactive_mode():
    """Demo interactive mode"""
    bot = DemoTradingBot()
    
    print(f"\n{Fore.CYAN}INTERACTIVE MODE DEMO")
    print(f"{Fore.CYAN}{'='*40}")
    print(f"{Fore.YELLOW}Type 'help' for available commands or 'quit' to exit")
    
    while True:
        try:
            command = input(f"\n{Fore.GREEN}Demo Bot> ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                print(f"{Fore.YELLOW}Demo completed!")
                break
                
            elif command == 'help':
                print(f"\n{Fore.CYAN}Available commands:")
                print(f"{Fore.WHITE}  account     - Display account summary")
                print(f"{Fore.WHITE}  market      - Place market order")
                print(f"{Fore.WHITE}  limit       - Place limit order")
                print(f"{Fore.WHITE}  stop-limit  - Place stop-limit order")
                print(f"{Fore.WHITE}  oco         - Place OCO order")
                print(f"{Fore.WHITE}  help        - Show this help")
                print(f"{Fore.WHITE}  quit        - Exit demo")
                
            elif command == 'account':
                bot.display_account_summary()
                
            elif command == 'market':
                symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Side (BUY/SELL): ").strip().upper()
                quantity = float(input("Quantity: "))
                
                bot.place_market_order(symbol, side, quantity)
                
            elif command == 'limit':
                symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Side (BUY/SELL): ").strip().upper()
                quantity = float(input("Quantity: "))
                price = float(input("Price: "))
                
                bot.place_limit_order(symbol, side, quantity, price)
                
            elif command == 'stop-limit':
                symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Side (BUY/SELL): ").strip().upper()
                quantity = float(input("Quantity: "))
                price = float(input("Limit Price: "))
                stop_price = float(input("Stop Price: "))
                
                bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                
            elif command == 'oco':
                symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Side (BUY/SELL): ").strip().upper()
                quantity = float(input("Quantity: "))
                price = float(input("Limit Price: "))
                stop_price = float(input("Stop Price: "))
                stop_limit_price = float(input("Stop Limit Price: "))
                
                bot.place_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price)
                
            else:
                print(f"{Fore.RED}Unknown command: {command}")
                print(f"{Fore.YELLOW}Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Demo cancelled")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

def main():
    """Main demo function"""
    print(f"{Fore.CYAN}Trading Bot Demo")
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.YELLOW}This demonstrates the trading bot functionality")
    print(f"{Fore.YELLOW}without requiring real API credentials")
    
    bot = DemoTradingBot()
    
    # Show account summary
    bot.display_account_summary()
    
    # Demo orders
    print(f"{Fore.CYAN}DEMO ORDER PLACEMENTS:")
    print(f"{Fore.CYAN}{'-'*40}")
    
    # Market order demo
    print(f"\n{Fore.CYAN}1. Market Order Demo:")
    bot.place_market_order("BTCUSDT", "BUY", 0.001)
    
    # Limit order demo
    print(f"\n{Fore.CYAN}2. Limit Order Demo:")
    bot.place_limit_order("BTCUSDT", "SELL", 0.001, 50000)
    
    # Stop-limit order demo
    print(f"\n{Fore.CYAN}3. Stop-Limit Order Demo:")
    bot.place_stop_limit_order("BTCUSDT", "BUY", 0.001, 45000, 44000)
    
    # OCO order demo
    print(f"\n{Fore.CYAN}4. OCO Order Demo:")
    bot.place_oco_order("BTCUSDT", "SELL", 0.001, 55000, 56000, 56500)
    
    print(f"\n{Fore.GREEN}Demo completed successfully!")
    print(f"\n{Fore.CYAN}Try interactive mode:")
    print(f"{Fore.WHITE}python demo_bot.py interactive")
    
    # Check if user wants interactive mode
    try:
        choice = input(f"\n{Fore.YELLOW}Start interactive demo? (y/n): ").strip().lower()
        if choice == 'y':
            demo_interactive_mode()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Demo ended")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        demo_interactive_mode()
    else:
        main()
