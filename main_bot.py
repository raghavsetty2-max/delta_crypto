"""
Delta Exchange Trading Bot - FIXED NEWLINE ISSUE
Handles newlines in API secrets
"""

import requests
import time
import os
import hmac
import hashlib
import json
from datetime import datetime, timedelta

# Configuration - STRIP whitespace and handle newlines
API_KEY = os.getenv('DELTA_API_KEY', '').strip()
API_SECRET = os.getenv('DELTA_API_SECRET', '').strip()
TESTNET = os.getenv('DELTA_TESTNET', 'true').lower() == 'true'
SYMBOL = os.getenv('TRADING_SYMBOL', 'BTCUSD').strip()
INTERVAL = int(os.getenv('INTERVAL_SECONDS', '900'))

BASE_URL = 'https://testnet-api.delta.exchange' if TESTNET else 'https://api.delta.exchange'

print(f"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║                🚀 CRYPTO BOT v3.1                         ║
║             Fixed Newline Issue                           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

🔧 CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   API Key:        {API_KEY[:10]}...{API_KEY[-4:] if API_KEY else 'MISSING'}
   Key Length:     {len(API_KEY)}
   Secret Length:  {len(API_SECRET)}
   Symbol:         {SYMBOL}
   Testnet:        {TESTNET}
   Endpoint:       {BASE_URL}
   Time:           {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

def clean_api_secret(secret):
    """Remove newlines and extra whitespace from API secret"""
    if not secret:
        return secret
    
    # Remove all newlines and extra spaces
    cleaned = secret.replace('\n', '').replace('\r', '').strip()
    
    # Show what we're working with
    print(f"🔧 Secret cleaning:")
    print(f"   Original length: {len(secret)}")
    print(f"   Cleaned length:  {len(cleaned)}")
    print(f"   Contains newlines: {'Yes' if '\\n' in secret or '\\r' in secret else 'No'}")
    
    return cleaned

def sign_request(method, endpoint, body=''):
    """Create Delta Exchange signature - HANDLES NEWLINES"""
    try:
        timestamp = str(int(time.time()))
        message = method + timestamp + endpoint + body
        
        # Clean the API secret to remove newlines
        clean_secret = clean_api_secret(API_SECRET)
        
        print(f"🔧 Signing details:")
        print(f"   Method: {method}")
        print(f"   Timestamp: {timestamp}")
        print(f"   Endpoint: {endpoint}")
        print(f"   Message length: {len(message)}")
        print(f"   Clean secret length: {len(clean_secret)}")
        
        signature = hmac.new(
            clean_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        print(f"🔧 Signature: {signature[:20]}...")
        return signature, timestamp
        
    except Exception as e:
        print(f"❌ Signing error: {e}")
        return None, None

def api_call(method, endpoint, payload=None):
    """Make API request with enhanced debugging"""
    try:
        url = BASE_URL + endpoint
        body = json.dumps(payload) if payload else ''
        
        print(f"\n🔧 API CALL: {method} {endpoint}")
        
        sig, ts = sign_request(method, endpoint, body)
        if not sig:
            return {'success': False, 'error': 'Signing failed'}
        
        headers = {
            'api-key': API_KEY,
            'timestamp': ts,
            'signature': sig,
            'Content-Type': 'application/json'
        }
        
        # Make request
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=15)
        else:
            response = requests.post(url, headers=headers, data=body, timeout=15)
        
        print(f"🔧 Response status: {response.status_code}")
        
        # Try to parse JSON response
        try:
            result = response.json()
            return result
        except json.JSONDecodeError:
            print(f"❌ JSON decode error. Raw response: {response.text[:200]}")
            return {'success': False, 'error': 'Invalid JSON response'}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return {'success': False, 'error': f'Network error: {e}'}
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {'success': False, 'error': str(e)}

def wait_for_api_activation():
    """Wait for API key to become active"""
    print("⏳ Waiting for API key activation (Delta says 5 minutes)...")
    for i in range(30):  # 30 attempts = 5 minutes
        print(f"   Attempt {i+1}/30 - Testing connection...")
        result = api_call('GET', '/v2/wallet/balances')
        
        if result.get('success'):
            print("✅ API Key is now ACTIVE!")
            return True
        elif result.get('error', {}).get('code') == 'invalid_api_key':
            print("   ⏳ API key not active yet, waiting 10 seconds...")
            time.sleep(10)
        else:
            # Other error - show details
            error_msg = result.get('error', 'Unknown error')
            print(f"   ⚠️  Error: {error_msg}, retrying...")
            time.sleep(10)
    
    print("❌ API key did not activate within 5 minutes")
    return False

# === MAIN EXECUTION ===
print("🔄 STEP 1: Validating environment...")

if not API_KEY:
    print("❌ CRITICAL: DELTA_API_KEY is missing!")
    exit(1)

if not API_SECRET:
    print("❌ CRITICAL: DELTA_API_SECRET is missing!")
    exit(1)

# Show actual secret content (for debugging)
print(f"✅ Environment check passed")
print(f"   API Key: {API_KEY[:8]}...{API_KEY[-4:]}")
print(f"   API Secret starts with: {API_SECRET[:20]}...")
print(f"   API Secret ends with: ...{API_SECRET[-20:]}")
print(f"   Secret length: {len(API_SECRET)} characters")

# Clean the secret immediately
CLEAN_SECRET = clean_api_secret(API_SECRET)
print(f"   Clean secret length: {len(CLEAN_SECRET)} characters")

print("\n🔄 STEP 2: Testing API key activation...")
if not wait_for_api_activation():
    print("❌ Failed to activate API key. Please check:")
    print("   1. API keys are copied EXACTLY from Delta")
    print("   2. Wait 5+ minutes after generation") 
    print("   3. Keys have proper permissions")
    print("   4. No extra spaces or newlines in Render")
    exit(1)

print("\n🔄 STEP 3: Fetching wallet balances...")
wallet = api_call('GET', '/v2/wallet/balances')

if wallet.get('success'):
    print("🎉 SUCCESSFULLY CONNECTED TO DELTA EXCHANGE!")
    print("\n💰 WALLET BALANCES:")
    print("━" * 50)
    
    total_balance = 0
    for item in wallet.get('result', []):
        balance = float(item.get('balance', 0))
        available = float(item.get('available_balance', 0))
        asset = item.get('asset_symbol', 'UNKNOWN')
        
        if balance > 0:
            print(f"   {asset}: {balance:,.4f} (Available: {available:,.4f})")
            
            if asset == 'USDT':
                total_balance = balance
    
    print("━" * 50)
    print(f"   💵 Total USDT: ${total_balance:,.2f}")
    
else:
    print(f"❌ Wallet fetch failed: {wallet.get('error')}")
    exit(1)

print("\n🔄 STEP 4: Finding trading product...")
products = api_call('GET', '/v2/products')

if products.get('success'):
    product_found = False
    for product in products.get('result', []):
        if product.get('symbol') == SYMBOL:
            product_id = product.get('id')
            product_found = True
            print(f"✅ Trading product found: {SYMBOL} (ID: {product_id})")
            break
    
    if not product_found:
        print(f"⚠️  Product {SYMBOL} not found, showing available BTC products:")
        for product in products.get('result', []):
            if 'BTC' in product.get('symbol', ''):
                print(f"   - {product['symbol']} (ID: {product['id']})")
else:
    print(f"❌ Failed to fetch products: {products.get('error')}")

# === MAIN MONITORING LOOP ===
print(f"\n🎯 STARTING MAIN MONITORING LOOP")
print("   Every 15 minutes | Press Ctrl+C to stop\n")

cycle = 0
while True:
    try:
        cycle += 1
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        
        print("=" * 60)
        print(f"🔄 CYCLE #{cycle} - {current_time}")
        print("=" * 60)
        
        # Check wallet
        wallet = api_call('GET', '/v2/wallet/balances')
        if wallet.get('success'):
            usdt_balance = 0
            for item in wallet.get('result', []):
                if item.get('asset_symbol') == 'USDT':
                    usdt_balance = float(item.get('balance', 0))
                    break
            print(f"💰 USDT Balance: ${usdt_balance:,.2f}")
        
        # Check positions
        positions = api_call('GET', '/v2/positions')
        if positions.get('success'):
            open_positions = [p for p in positions.get('result', []) if int(p.get('size', 0)) != 0]
            if open_positions:
                print("📊 OPEN POSITIONS:")
                for pos in open_positions:
                    symbol = pos.get('product_symbol', 'Unknown')
                    size = pos.get('size', 0)
                    pnl = float(pos.get('unrealized_pnl', 0))
                    print(f"   {symbol}: {size} contracts | P&L: ${pnl:+,.2f}")
            else:
                print("📊 No open positions")
        
        # Calculate next update
        next_time = (datetime.utcnow() + timedelta(seconds=INTERVAL)).strftime('%H:%M:%S UTC')
        print(f"\n💤 Next update in {INTERVAL}s ({INTERVAL//60}min) at {next_time}")
        time.sleep(INTERVAL)
        
    except KeyboardInterrupt:
        print(f"\n🛑 Bot stopped after {cycle} cycles")
        break
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💤 Retrying in 60 seconds...")
        time.sleep(60)

print("✅ Shutdown complete")
