#!/usr/bin/env python3
"""
Simplified Trading Bot for Binance Futures Testnet
A comprehensive trading bot implementation with CLI interface
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from decimal import Decimal, ROUND_DOWN

try:
    from binance.client import Client
    from binance.exceptions import BinanceAPIException, BinanceOrderException
except ImportError:
    print("Error: python-binance library not found. Please install it using: pip install python-binance")
    sys.exit(1)

from colorama import init, Fore, Style
from tabulate import tabulate

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class TradingBot:
    """
    A simplified trading bot for Binance Futures Testnet
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the trading bot
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Whether to use testnet (default: True)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # Setup logging
        self.setup_logging()
        
        # Initialize Binance client
        try:
            if testnet:
                self.client = Client(
                    api_key=api_key,
                    api_secret=api_secret,
                    testnet=True
                )
                self.logger.info("Connected to Binance Futures Testnet")
            else:
                self.client = Client(api_key=api_key, api_secret=api_secret)
                self.logger.info("Connected to Binance Futures Mainnet")
                
            # Test connection
            self.client.futures_account()
            self.logger.info("Successfully authenticated with Binance API")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Binance client: {e}")
            raise
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Setup logger
        self.logger = logging.getLogger('TradingBot')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handler for detailed logs
        file_handler = logging.FileHandler(
            f'logs/trading_bot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler for user feedback
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_account_info(self) -> Dict:
        """Get account information"""
        try:
            account_info = self.client.futures_account()
            self.logger.info("Retrieved account information")
            return account_info
        except Exception as e:
            self.logger.error(f"Failed to get account info: {e}")
            raise
    
    def get_symbol_info(self, symbol: str) -> Dict:
        """Get symbol information"""
        try:
            exchange_info = self.client.futures_exchange_info()
            for symbol_info in exchange_info['symbols']:
                if symbol_info['symbol'] == symbol:
                    return symbol_info
            raise ValueError(f"Symbol {symbol} not found")
        except Exception as e:
            self.logger.error(f"Failed to get symbol info for {symbol}: {e}")
            raise
    
    def validate_order_params(self, symbol: str, side: str, order_type: str, 
                            quantity: float, price: Optional[float] = None) -> Tuple[bool, str]:
        """
        Validate order parameters
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Get symbol info
            symbol_info = self.get_symbol_info(symbol)
            
            # Validate side
            if side.upper() not in ['BUY', 'SELL']:
                return False, "Side must be 'BUY' or 'SELL'"
            
            # Validate order type
            if order_type.upper() not in ['MARKET', 'LIMIT']:
                return False, "Order type must be 'MARKET' or 'LIMIT'"
            
            # Validate quantity
            if quantity <= 0:
                return False, "Quantity must be positive"
            
            # For limit orders, validate price
            if order_type.upper() == 'LIMIT':
                if price is None or price <= 0:
                    return False, "Price must be specified and positive for limit orders"
            
            # Get quantity precision
            for filter_info in symbol_info['filters']:
                if filter_info['filterType'] == 'LOT_SIZE':
                    step_size = float(filter_info['stepSize'])
                    min_qty = float(filter_info['minQty'])
                    
                    # Check minimum quantity
                    if quantity < min_qty:
                        return False, f"Quantity must be at least {min_qty}"
                    
                    # Check step size
                    if (quantity / step_size) % 1 != 0:
                        return False, f"Quantity must be a multiple of {step_size}"
            
            return True, ""
            
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict:
        """
        Place a market order
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            
        Returns:
            Order response from Binance
        """
        try:
            # Validate parameters
            is_valid, error_msg = self.validate_order_params(symbol, side, 'MARKET', quantity)
            if not is_valid:
                raise ValueError(error_msg)
            
            # Place order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='MARKET',
                quantity=quantity
            )
            
            self.logger.info(f"Market order placed: {order}")
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error placing market order: {e}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict:
        """
        Place a limit order
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            price: Order price
            
        Returns:
            Order response from Binance
        """
        try:
            # Validate parameters
            is_valid, error_msg = self.validate_order_params(symbol, side, 'LIMIT', quantity, price)
            if not is_valid:
                raise ValueError(error_msg)
            
            # Place order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC'  # Good Till Cancel
            )
            
            self.logger.info(f"Limit order placed: {order}")
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error placing limit order: {e}")
            raise
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, 
                              price: float, stop_price: float) -> Dict:
        """
        Place a stop-limit order (Bonus feature)
        
        Args:
            symbol: Trading pair symbol
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            price: Limit price
            stop_price: Stop price
            
        Returns:
            Order response from Binance
        """
        try:
            # Validate parameters
            is_valid, error_msg = self.validate_order_params(symbol, side, 'LIMIT', quantity, price)
            if not is_valid:
                raise ValueError(error_msg)
            
            if stop_price <= 0:
                raise ValueError("Stop price must be positive")
            
            # Place stop-limit order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='STOP',
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                timeInForce='GTC'
            )
            
            self.logger.info(f"Stop-limit order placed: {order}")
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error placing stop-limit order: {e}")
            raise
    
    def place_oco_order(self, symbol: str, side: str, quantity: float, 
                       price: float, stop_price: float, stop_limit_price: float) -> Dict:
        """
        Place an OCO (One-Cancels-Other) order (Bonus feature)
        
        Args:
            symbol: Trading pair symbol
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            price: Limit price
            stop_price: Stop price
            stop_limit_price: Stop limit price
            
        Returns:
            Order response from Binance
        """
        try:
            # Validate parameters
            is_valid, error_msg = self.validate_order_params(symbol, side, 'LIMIT', quantity, price)
            if not is_valid:
                raise ValueError(error_msg)
            
            if stop_price <= 0 or stop_limit_price <= 0:
                raise ValueError("Stop prices must be positive")
            
            # Place OCO order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='OCO',
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                stopLimitPrice=stop_limit_price,
                stopLimitTimeInForce='GTC'
            )
            
            self.logger.info(f"OCO order placed: {order}")
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error placing OCO order: {e}")
            raise
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """Get order status"""
        try:
            order = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            self.logger.info(f"Retrieved order status: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Failed to get order status: {e}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel an order"""
        try:
            result = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            self.logger.info(f"Order cancelled: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to cancel order: {e}")
            raise
    
    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get open orders"""
        try:
            if symbol:
                orders = self.client.futures_get_open_orders(symbol=symbol)
            else:
                orders = self.client.futures_get_open_orders()
            
            self.logger.info(f"Retrieved {len(orders)} open orders")
            return orders
        except Exception as e:
            self.logger.error(f"Failed to get open orders: {e}")
            raise
    
    def get_positions(self) -> List[Dict]:
        """Get current positions"""
        try:
            positions = self.client.futures_position_information()
            # Filter out positions with zero size
            active_positions = [pos for pos in positions if float(pos['positionAmt']) != 0]
            self.logger.info(f"Retrieved {len(active_positions)} active positions")
            return active_positions
        except Exception as e:
            self.logger.error(f"Failed to get positions: {e}")
            raise
    
    def display_account_summary(self):
        """Display account summary"""
        try:
            account_info = self.get_account_info()
            
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.CYAN}ACCOUNT SUMMARY")
            print(f"{Fore.CYAN}{'='*60}")
            
            # Account balance
            total_wallet_balance = float(account_info['totalWalletBalance'])
            total_unrealized_pnl = float(account_info['totalUnrealizedProfit'])
            total_margin_balance = float(account_info['totalMarginBalance'])
            
            print(f"{Fore.GREEN}Total Wallet Balance: {total_wallet_balance:.4f} USDT")
            print(f"{Fore.YELLOW}Total Unrealized PnL: {total_unrealized_pnl:.4f} USDT")
            print(f"{Fore.BLUE}Total Margin Balance: {total_margin_balance:.4f} USDT")
            
            # Positions
            positions = self.get_positions()
            if positions:
                print(f"\n{Fore.CYAN}ACTIVE POSITIONS:")
                print(f"{Fore.CYAN}{'-'*60}")
                
                position_data = []
                for pos in positions:
                    position_data.append([
                        pos['symbol'],
                        pos['positionSide'],
                        f"{float(pos['positionAmt']):.6f}",
                        f"{float(pos['entryPrice']):.4f}",
                        f"{float(pos['markPrice']):.4f}",
                        f"{float(pos['unRealizedProfit']):.4f} USDT"
                    ])
                
                headers = ['Symbol', 'Side', 'Size', 'Entry Price', 'Mark Price', 'Unrealized PnL']
                print(tabulate(position_data, headers=headers, tablefmt='grid'))
            
            # Open orders
            open_orders = self.get_open_orders()
            if open_orders:
                print(f"\n{Fore.CYAN}OPEN ORDERS:")
                print(f"{Fore.CYAN}{'-'*60}")
                
                order_data = []
                for order in open_orders:
                    order_data.append([
                        order['symbol'],
                        order['side'],
                        order['type'],
                        f"{float(order['origQty']):.6f}",
                        f"{float(order['price']):.4f}" if order['price'] != '0.00000000' else 'Market',
                        order['status']
                    ])
                
                headers = ['Symbol', 'Side', 'Type', 'Quantity', 'Price', 'Status']
                print(tabulate(order_data, headers=headers, tablefmt='grid'))
            
            print(f"{Fore.CYAN}{'='*60}\n")
            
        except Exception as e:
            self.logger.error(f"Failed to display account summary: {e}")
            print(f"{Fore.RED}Error displaying account summary: {e}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Simplified Trading Bot for Binance Futures Testnet')
    parser.add_argument('--api-key', required=True, help='Binance API key')
    parser.add_argument('--api-secret', required=True, help='Binance API secret')
    parser.add_argument('--mainnet', action='store_true', help='Use mainnet instead of testnet')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Market order command
    market_parser = subparsers.add_parser('market', help='Place a market order')
    market_parser.add_argument('symbol', help='Trading pair symbol (e.g., BTCUSDT)')
    market_parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    market_parser.add_argument('quantity', type=float, help='Order quantity')
    
    # Limit order command
    limit_parser = subparsers.add_parser('limit', help='Place a limit order')
    limit_parser.add_argument('symbol', help='Trading pair symbol (e.g., BTCUSDT)')
    limit_parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    limit_parser.add_argument('quantity', type=float, help='Order quantity')
    limit_parser.add_argument('price', type=float, help='Order price')
    
    # Stop-limit order command
    stop_limit_parser = subparsers.add_parser('stop-limit', help='Place a stop-limit order')
    stop_limit_parser.add_argument('symbol', help='Trading pair symbol (e.g., BTCUSDT)')
    stop_limit_parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    stop_limit_parser.add_argument('quantity', type=float, help='Order quantity')
    stop_limit_parser.add_argument('price', type=float, help='Limit price')
    stop_limit_parser.add_argument('stop_price', type=float, help='Stop price')
    
    # OCO order command
    oco_parser = subparsers.add_parser('oco', help='Place an OCO order')
    oco_parser.add_argument('symbol', help='Trading pair symbol (e.g., BTCUSDT)')
    oco_parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    oco_parser.add_argument('quantity', type=float, help='Order quantity')
    oco_parser.add_argument('price', type=float, help='Limit price')
    oco_parser.add_argument('stop_price', type=float, help='Stop price')
    oco_parser.add_argument('stop_limit_price', type=float, help='Stop limit price')
    
    # Account info command
    subparsers.add_parser('account', help='Display account information')
    
    # Order status command
    status_parser = subparsers.add_parser('status', help='Get order status')
    status_parser.add_argument('symbol', help='Trading pair symbol')
    status_parser.add_argument('order_id', type=int, help='Order ID')
    
    # Cancel order command
    cancel_parser = subparsers.add_parser('cancel', help='Cancel an order')
    cancel_parser.add_argument('symbol', help='Trading pair symbol')
    cancel_parser.add_argument('order_id', type=int, help='Order ID')
    
    # Interactive mode
    subparsers.add_parser('interactive', help='Start interactive mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Initialize bot
        bot = TradingBot(
            api_key=args.api_key,
            api_secret=args.api_secret,
            testnet=not args.mainnet
        )
        
        # Execute command
        if args.command == 'market':
            order = bot.place_market_order(args.symbol, args.side, args.quantity)
            print(f"{Fore.GREEN}Market order placed successfully!")
            print(f"{Fore.CYAN}Order ID: {order['orderId']}")
            print(f"{Fore.CYAN}Status: {order['status']}")
            
        elif args.command == 'limit':
            order = bot.place_limit_order(args.symbol, args.side, args.quantity, args.price)
            print(f"{Fore.GREEN}Limit order placed successfully!")
            print(f"{Fore.CYAN}Order ID: {order['orderId']}")
            print(f"{Fore.CYAN}Status: {order['status']}")
            
        elif args.command == 'stop-limit':
            order = bot.place_stop_limit_order(args.symbol, args.side, args.quantity, 
                                             args.price, args.stop_price)
            print(f"{Fore.GREEN}Stop-limit order placed successfully!")
            print(f"{Fore.CYAN}Order ID: {order['orderId']}")
            print(f"{Fore.CYAN}Status: {order['status']}")
            
        elif args.command == 'oco':
            order = bot.place_oco_order(args.symbol, args.side, args.quantity, 
                                      args.price, args.stop_price, args.stop_limit_price)
            print(f"{Fore.GREEN}OCO order placed successfully!")
            print(f"{Fore.CYAN}Order ID: {order['orderId']}")
            print(f"{Fore.CYAN}Status: {order['status']}")
            
        elif args.command == 'account':
            bot.display_account_summary()
            
        elif args.command == 'status':
            order = bot.get_order_status(args.symbol, args.order_id)
            print(f"{Fore.CYAN}Order Status:")
            print(f"ID: {order['orderId']}")
            print(f"Symbol: {order['symbol']}")
            print(f"Side: {order['side']}")
            print(f"Type: {order['type']}")
            print(f"Quantity: {order['origQty']}")
            print(f"Price: {order['price']}")
            print(f"Status: {order['status']}")
            
        elif args.command == 'cancel':
            result = bot.cancel_order(args.symbol, args.order_id)
            print(f"{Fore.GREEN}Order cancelled successfully!")
            print(f"{Fore.CYAN}Order ID: {result['orderId']}")
            
        elif args.command == 'interactive':
            interactive_mode(bot)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        sys.exit(1)


def interactive_mode(bot: TradingBot):
    """Interactive mode for the trading bot"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}TRADING BOT INTERACTIVE MODE")
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}Type 'help' for available commands or 'quit' to exit")
    
    while True:
        try:
            command = input(f"\n{Fore.GREEN}Bot> ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                print(f"{Fore.YELLOW}Goodbye!")
                break
                
            elif command == 'help':
                print(f"\n{Fore.CYAN}Available commands:")
                print(f"{Fore.WHITE}  account     - Display account summary")
                print(f"{Fore.WHITE}  market      - Place market order")
                print(f"{Fore.WHITE}  limit       - Place limit order")
                print(f"{Fore.WHITE}  stop-limit  - Place stop-limit order")
                print(f"{Fore.WHITE}  oco         - Place OCO order")
                print(f"{Fore.WHITE}  status      - Get order status")
                print(f"{Fore.WHITE}  cancel      - Cancel order")
                print(f"{Fore.WHITE}  orders      - Show open orders")
                print(f"{Fore.WHITE}  positions   - Show positions")
                print(f"{Fore.WHITE}  help        - Show this help")
                print(f"{Fore.WHITE}  quit        - Exit interactive mode")
                
            elif command == 'account':
                bot.display_account_summary()
                
            elif command == 'market':
                symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Side (BUY/SELL): ").strip().upper()
                quantity = float(input("Quantity: "))
                
                order = bot.place_market_order(symbol, side, quantity)
                print(f"{Fore.GREEN}Market order placed! ID: {order['orderId']}")
                
            elif command == 'limit':
                symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Side (BUY/SELL): ").strip().upper()
                quantity = float(input("Quantity: "))
                price = float(input("Price: "))
                
                order = bot.place_limit_order(symbol, side, quantity, price)
                print(f"{Fore.GREEN}Limit order placed! ID: {order['orderId']}")
                
            elif command == 'stop-limit':
                symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Side (BUY/SELL): ").strip().upper()
                quantity = float(input("Quantity: "))
                price = float(input("Limit Price: "))
                stop_price = float(input("Stop Price: "))
                
                order = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                print(f"{Fore.GREEN}Stop-limit order placed! ID: {order['orderId']}")
                
            elif command == 'oco':
                symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Side (BUY/SELL): ").strip().upper()
                quantity = float(input("Quantity: "))
                price = float(input("Limit Price: "))
                stop_price = float(input("Stop Price: "))
                stop_limit_price = float(input("Stop Limit Price: "))
                
                order = bot.place_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price)
                print(f"{Fore.GREEN}OCO order placed! ID: {order['orderId']}")
                
            elif command == 'status':
                symbol = input("Symbol: ").strip().upper()
                order_id = int(input("Order ID: "))
                
                order = bot.get_order_status(symbol, order_id)
                print(f"{Fore.CYAN}Order Status: {order['status']}")
                
            elif command == 'cancel':
                symbol = input("Symbol: ").strip().upper()
                order_id = int(input("Order ID: "))
                
                result = bot.cancel_order(symbol, order_id)
                print(f"{Fore.GREEN}Order cancelled! ID: {result['orderId']}")
                
            elif command == 'orders':
                orders = bot.get_open_orders()
                if orders:
                    print(f"\n{Fore.CYAN}Open Orders:")
                    for order in orders:
                        print(f"  {order['symbol']} {order['side']} {order['type']} "
                              f"{order['origQty']} @ {order['price']} - {order['status']}")
                else:
                    print(f"{Fore.YELLOW}No open orders")
                    
            elif command == 'positions':
                positions = bot.get_positions()
                if positions:
                    print(f"\n{Fore.CYAN}Active Positions:")
                    for pos in positions:
                        print(f"  {pos['symbol']} {pos['positionSide']} "
                              f"{pos['positionAmt']} @ {pos['entryPrice']} "
                              f"PnL: {pos['unRealizedProfit']} USDT")
                else:
                    print(f"{Fore.YELLOW}No active positions")
                    
            else:
                print(f"{Fore.RED}Unknown command: {command}")
                print(f"{Fore.YELLOW}Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operation cancelled")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")


if __name__ == "__main__":
    main()
