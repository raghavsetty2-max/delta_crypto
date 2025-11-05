"""
Enhanced Delta Exchange Trading Bot
With Basic Trading Strategy
"""

import requests
import time
import os
import hmac
import hashlib
import json
from datetime import datetime, timedelta

# Configuration
API_KEY = os.getenv('DELTA_API_KEY', '')
API_SECRET = os.getenv('DELTA_API_SECRET', '')
TESTNET = os.getenv('DELTA_TESTNET', 'true').lower() == 'true'
SYMBOL = os.getenv('TRADING_SYMBOL', 'BTCUSD')
INTERVAL = int(os.getenv('INTERVAL_SECONDS', '900'))
TRADE_ENABLED = os.getenv('TRADE_ENABLED', 'false').lower() == 'true'

BASE_URL = 'https://testnet-api.delta.exchange' if TESTNET else 'https://api.delta.exchange'

class DeltaTradingBot:
    def __init__(self):
        self.product_id = None
        self.cycle = 0
        self.setup()
    
    def setup(self):
        print(f"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║          🚀 ENHANCED CRYPTO TRADING BOT                   ║
║             Delta Exchange Native API v2.1                ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

⚙️  CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Symbol:         {SYMBOL}
   Mode:           {'🧪 TESTNET' if TESTNET else '🔴 LIVE'}
   Trading:        {'✅ ENABLED' if TRADE_ENABLED else '❌ MONITOR ONLY'}
   Interval:       {INTERVAL}s ({INTERVAL//60} min)
   API Endpoint:   {BASE_URL}
   Started:        {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        
        # Test connection and get product ID
        if not self.test_connection():
            exit(1)
        
        self.get_product_id()
    
    def sign_request(self, method, endpoint, body=''):
        """Create Delta Exchange signature"""
        timestamp = str(int(time.time()))
        message = method + timestamp + endpoint + body
        signature = hmac.new(
            API_SECRET.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature, timestamp

    def api_call(self, method, endpoint, payload=None):
        """Make API request with better error handling"""
        try:
            url = BASE_URL + endpoint
            body = json.dumps(payload) if payload else ''
            sig, ts = self.sign_request(method, endpoint, body)
            
            headers = {
                'api-key': API_KEY,
                'timestamp': ts,
                'signature': sig,
                'Content-Type': 'application/json'
            }
            
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=body, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return {'success': False, 'error': f'Unsupported method: {method}'}
            
            return response.json()
            
        except requests.exceptions.Timeout:
            return {'success': False, 'error': 'Request timeout'}
        except requests.exceptions.ConnectionError:
            return {'success': False, 'error': 'Connection error'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_connection(self):
        """Test API connection"""
        print("🔄 Testing connection...")
        print(f"API Key: {API_KEY[:6]}...{API_KEY[-4:] if len(API_KEY) > 10 else '***'}")
        
        wallet = self.api_call('GET', '/v2/wallet/balances')
        
        if wallet.get('success'):
            print("✅ Connected to Delta Exchange!")
            print(f"💡 Mode: {'TESTNET - Fake Money' if TESTNET else 'LIVE - Real Money'}\n")
            return True
        else:
            print("❌ CONNECTION FAILED")
            print(f"Error: {wallet.get('error', 'Unknown')}")
            return False
    
    def get_product_id(self):
        """Get product ID for trading symbol"""
        products = self.api_call('GET', '/v2/products')
        
        if products.get('success') and 'result' in products:
            for product in products['result']:
                if product.get('symbol') == SYMBOL:
                    self.product_id = product.get('id')
                    print(f"✅ Product found: {SYMBOL} (ID: {self.product_id})\n")
                    return
        
        print(f"❌ Product {SYMBOL} not found\n")
    
    def get_wallet_balance(self):
        """Get wallet balances"""
        wallet = self.api_call('GET', '/v2/wallet/balances')
        if not wallet.get('success'):
            return None
        
        balances = {}
        total_usdt = 0
        
        for item in wallet.get('result', []):
            asset = item.get('asset_symbol')
            balance = float(item.get('balance', 0))
            available = float(item.get('available_balance', 0))
            
            if balance > 0:
                balances[asset] = {
                    'balance': balance,
                    'available': available
                }
                if asset == 'USDT':
                    total_usdt = balance
        
        return balances, total_usdt
    
    def get_positions(self):
        """Get current positions"""
        positions = self.api_call('GET', '/v2/positions')
        if not positions.get('success'):
            return []
        
        open_positions = []
        for pos in positions.get('result', []):
            if int(pos.get('size', 0)) != 0:
                open_positions.append({
                    'symbol': pos.get('product_symbol'),
                    'size': pos.get('size'),
                    'pnl': float(pos.get('unrealized_pnl', 0))
                })
        
        return open_positions
    
    def get_market_price(self):
        """Get current market price"""
        if not self.product_id:
            return None
            
        ticker = self.api_call('GET', f'/v2/tickers/{self.product_id}')
        if ticker.get('success') and 'result' in ticker:
            return float(ticker['result'].get('close', 0))
        return None
    
    def simple_trading_strategy(self, price):
        """
        Simple mean reversion strategy
        This is just an example - implement your own logic
        """
        # This is a placeholder strategy
        # In real implementation, you'd add technical analysis here
        return 'HOLD'  # BUY, SELL, or HOLD
    
    def place_order(self, side, size, order_type='limit', price=None):
        """Place an order"""
        if not TRADE_ENABLED:
            print(f"🛑 Trading disabled - Would place {side} order for {size} {SYMBOL}")
            return {'success': True, 'simulated': True}
        
        if not self.product_id:
            return {'success': False, 'error': 'Product ID not found'}
        
        payload = {
            'product_id': self.product_id,
            'size': str(size),
            'side': side,
            'order_type': order_type,
        }
        
        if order_type == 'limit' and price:
            payload['limit_price'] = str(price)
        
        result = self.api_call('POST', '/v2/orders', payload)
        
        if result.get('success'):
            print(f"✅ Order placed: {side} {size} {SYMBOL}")
        else:
            print(f"❌ Order failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    def run_cycle(self):
        """Run one trading cycle"""
        self.cycle += 1
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        print("=" * 60)
        print(f"🔄 CYCLE #{self.cycle} - {now} UTC")
        print("=" * 60)
        
        # Get wallet balance
        balances, total_usdt = self.get_wallet_balance()
        if balances:
            print("\n💰 WALLET BALANCES:")
            print("━" * 40)
            for asset, data in balances.items():
                print(f"   {asset}: {data['balance']:,.2f} (Available: {data['available']:,.2f})")
            print("━" * 40)
            print(f"   Total USDT: ${total_usdt:,.2f}")
        
        # Get positions
        positions = self.get_positions()
        print("\n📊 OPEN POSITIONS:")
        print("━" * 40)
        if positions:
            for pos in positions:
                print(f"   {pos['symbol']}: {pos['size']} contracts | P&L: ${pos['pnl']:+,.2f}")
        else:
            print("   No open positions")
        print("━" * 40)
        
        # Get market data and run strategy
        price = self.get_market_price()
        if price:
            print(f"\n📈 MARKET PRICE: ${price:,.2f}")
            
            # Run trading strategy
            action = self.simple_trading_strategy(price)
            print(f"🎯 STRATEGY SIGNAL: {action}")
            
            # Example trading logic (customize this)
            if action == 'BUY' and total_usdt > 10:
                self.place_order('buy', 0.001, 'market')
            elif action == 'SELL':
                self.place_order('sell', 0.001, 'market')
        
        print(f"\n💤 Next update in {INTERVAL} seconds...")
    
    def run(self):
        """Main bot loop"""
        print("\n🔄 Starting main trading loop...\n")
        
        while True:
            try:
                self.run_cycle()
                time.sleep(INTERVAL)
                
            except KeyboardInterrupt:
                print(f"\n🛑 Bot stopped after {self.cycle} cycles")
                break
            except Exception as e:
                print(f"\n❌ Error in main loop: {e}")
                print("💤 Retrying in 60 seconds...")
                time.sleep(60)

if __name__ == "__main__":
    bot = DeltaTradingBot()
    bot.run()
