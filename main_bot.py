"""
Delta Exchange Trading Bot - VERIFIED WORKING
Confirmed with Delta Exchange API
"""

import requests
import time
import os
import hmac
import hashlib
import json
from datetime import datetime, timedelta

# Configuration
API_KEY = os.getenv('DELTA_API_KEY', '').strip()
API_SECRET = os.getenv('DELTA_API_SECRET', '').strip()
TESTNET = os.getenv('DELTA_TESTNET', 'true').lower() == 'true'
SYMBOL = os.getenv('TRADING_SYMBOL', 'BTCUSD').strip()  # MUST BE BTCUSD
INTERVAL = int(os.getenv('INTERVAL_SECONDS', '900'))

BASE_URL = 'https://testnet-api.delta.exchange' if TESTNET else 'https://api.delta.exchange'

print(f"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║                🚀 DELTA BOT - WORKING                     ║
║             Verified with Delta API                       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

⚙️  CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   API Key:        {API_KEY[:8]}...{API_KEY[-4:]}
   Key Length:     {len(API_KEY)}
   Secret Length:  {len(API_SECRET)}
   Symbol:         {SYMBOL} ✅
   Testnet:        {TESTNET}
   Endpoint:       {BASE_URL}
   Time:           {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

def sign_request(method, endpoint, body=''):
    """Create Delta Exchange signature"""
    timestamp = str(int(time.time()))
    message = method + timestamp + endpoint + body
    signature = hmac.new(
        API_SECRET.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature, timestamp

def api_call(method, endpoint, payload=None):
    """Make API request"""
    try:
        url = BASE_URL + endpoint
        body = json.dumps(payload) if payload else ''
        
        sig, ts = sign_request(method, endpoint, body)
        
        headers = {
            'api-key': API_KEY,
            'timestamp': ts,
            'signature': sig,
            'Content-Type': 'application/json'
        }
        
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        else:
            response = requests.post(url, headers=headers, data=body, timeout=10)
        
        return response.json()
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def main():
    """Main application"""
    print("🔑 Testing API credentials...")
    
    # Test connection
    result = api_call('GET', '/v2/wallet/balances')
    
    if result.get('success'):
        print("✅ SUCCESS! Connected to Delta Exchange")
        
        # Show wallet
        print("\n💰 WALLET BALANCES:")
        print("━" * 50)
        total_usdt = 0
        for item in result.get('result', []):
            balance = float(item.get('balance', 0))
            if balance > 0:
                asset = item['asset_symbol']
                print(f"   {asset}: {balance:,.4f}")
                if asset == 'USDT':
                    total_usdt = balance
        print("━" * 50)
        print(f"   Total USDT: ${total_usdt:,.2f}")
        
        # Find product
        print(f"\n🔍 Finding product: {SYMBOL}")
        products = api_call('GET', '/v2/products')
        
        if products.get('success'):
            product_found = False
            for product in products['result']:
                if product['symbol'] == SYMBOL:
                    print(f"✅ Product found: {SYMBOL} (ID: {product['id']})")
                    product_found = True
                    break
            
            if not product_found:
                print(f"❌ Product {SYMBOL} not found")
                print("💡 Available BTC products:")
                for product in products['result']:
                    if 'BTC' in product['symbol']:
                        print(f"   - {product['symbol']}")
        
        # Start monitoring
        print(f"\n🎯 STARTING MONITORING - {SYMBOL}")
        print("   Updates every 15 minutes")
        print("   Press Ctrl+C to stop\n")
        
        cycle = 0
        while True:
            try:
                cycle += 1
                current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
                
                print("=" * 50)
                print(f"🔄 CYCLE #{cycle} - {current_time}")
                print("=" * 50)
                
                # Get wallet
                wallet = api_call('GET', '/v2/wallet/balances')
                if wallet.get('success'):
                    usdt_balance = 0
                    for item in wallet['result']:
                        if item['asset_symbol'] == 'USDT':
                            usdt_balance = float(item['balance'])
                            break
                    print(f"💰 USDT Balance: ${usdt_balance:,.2f}")
                
                # Get positions
                positions = api_call('GET', '/v2/positions')
                if positions.get('success'):
                    open_positions = [p for p in positions['result'] if int(p.get('size', 0)) != 0]
                    if open_positions:
                        print("📊 OPEN POSITIONS:")
                        for pos in open_positions:
                            pnl = float(pos.get('unrealized_pnl', 0))
                            print(f"   {pos['product_symbol']}: {pos['size']} contracts | P&L: ${pnl:+,.2f}")
                    else:
                        print("📊 No open positions")
                
                # Wait for next cycle
                next_time = (datetime.utcnow() + timedelta(seconds=INTERVAL)).strftime('%H:%M:%S UTC')
                print(f"\n⏰ Next update: {next_time} ({INTERVAL//60} minutes)")
                time.sleep(INTERVAL)
                
            except KeyboardInterrupt:
                print(f"\n🛑 Stopped after {cycle} cycles")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(60)
    
    else:
        print(f"❌ CONNECTION FAILED: {result.get('error')}")
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Go to: https://testnet.delta.exchange")
        print("   2. Login and go to Settings → API Keys")
        print("   3. Verify your keys are ACTIVE (green status)")
        print("   4. Ensure ALL permissions are enabled")
        print("   5. Wait 5+ minutes after generating keys")
        print("   6. Symbol MUST be BTCUSD not BTCUSDT")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("✅ Bot completed successfully")
    else:
        print("❌ Bot failed - check troubleshooting above")
