"""
Crypto Trading Bot for Delta Exchange
Using Delta's Official Native API
"""

import requests
import time
import os
from datetime import datetime, timedelta
import hmac
import hashlib
import json

# Configuration from environment variables
API_KEY = os.getenv('DELTA_API_KEY', '')
API_SECRET = os.getenv('DELTA_API_SECRET', '')
TESTNET = os.getenv('DELTA_TESTNET', 'true').lower() == 'true'
SYMBOL = os.getenv('TRADING_SYMBOL', 'BTCUSD')
INTERVAL = int(os.getenv('INTERVAL_SECONDS', '900'))

# Base URL
BASE_URL = 'https://testnet-api.delta.exchange' if TESTNET else 'https://api.delta.exchange'

print(f"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║          🚀 CRYPTO TRADING BOT STARTED                    ║
║             Delta Exchange Native API                     ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

⚙️  CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Trading Symbol: {SYMBOL}
   Mode:           {'🧪 TESTNET (Fake Money)' if TESTNET else '🔴 LIVE TRADING'}
   Update Every:   {INTERVAL} seconds ({INTERVAL//60} minutes)
   API Endpoint:   {BASE_URL}
   Started:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 Initializing Delta Exchange connection...
""")

def generate_signature(method, endpoint, payload=''):
    """Generate HMAC signature for Delta Exchange API"""
    timestamp = str(int(time.time()))
    
    # Create signature string: method + timestamp + endpoint + payload
    signature_data = method + timestamp + endpoint + payload
    
    # Generate HMAC SHA256 signature
    signature = hmac.new(
        bytes(API_SECRET, 'utf-8'),
        bytes(signature_data, 'utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return signature, timestamp

def make_api_request(method, endpoint, payload=None):
    """Make authenticated request to Delta Exchange API"""
    try:
        url = BASE_URL + endpoint
        body = ''
        
        if payload:
            body = json.dumps(payload)
        
        # Generate signature
        signature, timestamp = generate_signature(method, endpoint, body)
        
        # Prepare headers
        headers = {
            'api-key': API_KEY,
            'timestamp': timestamp,
            'signature': signature,
            'User-Agent': 'DeltaTradingBot/1.0',
            'Content-Type': 'application/json'
        }
        
        # Make request
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=body, timeout=10)
        else:
            return {'success': False, 'error': f'Unsupported method: {method}'}
        
        # Parse response
        try:
            return response.json()
        except:
            return {'success': False, 'error': f'Invalid JSON: {response.text[:100]}'}
            
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Request timeout'}
    except requests.exceptions.ConnectionError:
        return {'success': False, 'error': 'Connection error'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Test API connection
print("Testing API authentication...")
print(f"API Key: {API_KEY[:8]}...{API_KEY[-4:]}")
print(f"API Key Length: {len(API_KEY)} characters")
print(f"API Secret Length: {len(API_SECRET)} characters\n")

# Get wallet balances
wallet_response = make_api_request('GET', '/v2/wallet/balances')

if wallet_response.get('success'):
    print("✅ Successfully connected to Delta Exchange!")
    print(f"💡 Using {'FAKE money - Safe for testing!' if TESTNET else 'REAL MONEY - Trade carefully!'}\n")
    
    # Display wallet balances
    if 'result' in wallet_response and wallet_response['result']:
        print("💰 WALLET BALANCES:")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        total_usdt = 0
        for balance_item in wallet_response['result']:
            asset = balance_item.get('asset_symbol', 'Unknown')
            available = float(balance_item.get('available_balance', 0))
            total = float(balance_item.get('balance', 0))
            
            if total > 0:
                print(f"   {asset}:")
                print(f"      Available: {available:,.4f}")
                print(f"      Total:     {total:,.4f}")
                
                if asset == 'USDT':
                    total_usdt = total
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   Total Portfolio Value: ${total_usdt:,.2f}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    else:
        print("⚠️  No balance data found\n")
        
else:
    print("\n❌ CONNECTION ERROR")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Error: {wallet_response.get('error', 'Unknown error')}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\n⚠️  TROUBLESHOOTING:")
    print("   1. Verify API keys are correct in Render Environment")
    print("   2. Check Delta Exchange testnet is online")
    print("   3. Ensure API key has proper permissions")
    print("   4. Regenerate keys if needed\n")
    time.sleep(10)
    exit(1)

# Get products list
print("📊 Fetching market products...")
products_response = make_api_request('GET', '/v2/products')

target_product = None
if products_response.get('success') and 'result' in products_response:
    for product in products_response['result']:
        if product.get('symbol') == SYMBOL:
            target_product = product
            print(f"✅ Found product: {SYMBOL}")
            print(f"   Product ID: {product.get('id')}")
            print(f"   Contract Type: {product.get('contract_type', 'N/A')}")
            print(f"   Trading Status: {product.get('trading_status', 'N/A')}\n")
            break

if not target_product:
    print(f"⚠️  Product {SYMBOL} not found. Will monitor wallet only.\n")

# Main monitoring loop
cycle = 0
print("🔄 Starting market monitoring loop...")
print("=" * 70 + "\n")

while True:
    try:
        cycle += 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print("=" * 70)
        print(f"🔄 CYCLE #{cycle} - {timestamp}")
        print("=" * 70 + "\n")
        
        # Fetch wallet balances
        wallet_response = make_api_request('GET', '/v2/wallet/balances')
        
        if wallet_response.get('success'):
            print("💰 WALLET STATUS:")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            
            portfolio_value = 0
            if 'result' in wallet_response and wallet_response['result']:
                for balance_item in wallet_response['result']:
                    asset = balance_item.get('asset_symbol', 'Unknown')
                    available = float(balance_item.get('available_balance', 0))
                    total = float(balance_item.get('balance', 0))
                    
                    if total > 0:
                        print(f"   {asset}: ${total:,.2f} (Available: ${available:,.2f})")
                        if asset == 'USDT':
                            portfolio_value = total
            
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"   Total Value: ${portfolio_value:,.2f}")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        else:
            print(f"⚠️  Could not fetch wallet: {wallet_response.get('error', 'Unknown')}")
        
        # Fetch positions
        print("\n📊 POSITIONS:")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        positions_response = make_api_request('GET', '/v2/positions')
        
        if positions_response.get('success') and 'result' in positions_response:
            open_positions = [p for p in positions_response['result'] if int(p.get('size', 0)) != 0]
            
            if open_positions:
                for pos in open_positions:
                    symbol = pos.get('product_symbol', 'N/A')
                    size = pos.get('size', 0)
                    side = 'LONG' if int(size) > 0 else 'SHORT'
                    entry = float(pos.get('entry_price', 0))
                    pnl = float(pos.get('unrealized_pnl', 0))
                    
                    pnl_emoji = "📈" if pnl > 0 else "📉"
                    
                    print(f"   {symbol} | {side}")
                    print(f"      Size: {size} contracts")
                    print(f"      Entry: ${entry:,.2f}")
                    print(f"      {pnl_emoji} P&L: ${pnl:+,.2f}")
                    print("   " + "─" * 60)
            else:
                print("   No open positions")
        else:
            print("   No open positions")
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Status message
        print(f"\n💡 Status: Monitoring market (no auto-trading)")
        
        # Wait for next cycle
        next_time = (datetime.now() + timedelta(seconds=INTERVAL)).strftime('%H:%M:%S')
        print(f"\n⏳ Next update in {INTERVAL}s ({INTERVAL//60} min) at {next_time}")
        print("\n" + "=" * 70 + "\n")
        
        time.sleep(INTERVAL)
        
    except KeyboardInterrupt:
        print(f"\n{'='*70}")
        print("🛑 BOT STOPPED BY USER")
        print(f"{'='*70}")
        print(f"   Total Cycles: {cycle}")
        print(f"   Stopped At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        break
        
    except Exception as e:
        print(f"\n❌ Error in cycle #{cycle}: {str(e)}")
        print("⏳ Retrying in 60 seconds...\n")
        time.sleep(60)

print("✅ Bot shutdown complete\n")
