"""
Crypto Trading Bot for Delta Exchange
Monitors BTC/USDT and tracks account balance
"""

import ccxt
import time
import os
from datetime import datetime, timedelta

# Configuration from environment variables
API_KEY = os.getenv('DELTA_API_KEY', '')
API_SECRET = os.getenv('DELTA_API_SECRET', '')
TESTNET = os.getenv('DELTA_TESTNET', 'true').lower() == 'true'
SYMBOL = os.getenv('TRADING_SYMBOL', 'BTC/USDT')
INTERVAL = int(os.getenv('INTERVAL_SECONDS', '900'))

# Startup banner
print(f"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║          🚀 CRYPTO TRADING BOT STARTED                    ║
║             Delta Exchange Trading System                 ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

⚙️  CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Trading Pair:   {SYMBOL}
   Mode:           {'🧪 TESTNET (Fake Money)' if TESTNET else '🔴 LIVE TRADING'}
   Update Every:   {INTERVAL} seconds ({INTERVAL//60} minutes)
   Started:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 Connecting to Delta Exchange...
""")

# Initialize Delta Exchange
try:
    exchange = ccxt.delta({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
    })
    
    if TESTNET:
        exchange.set_sandbox_mode(True)
        print("✅ Connected to Delta Exchange TESTNET")
        print("💡 Using FAKE money - Safe for practice!\n")
    else:
        print("🔴 Connected to Delta Exchange LIVE")
        print("⚠️  Using REAL MONEY - Be careful!\n")
    
    # Test connection
    balance = exchange.fetch_balance()
    usdt_balance = balance['total'].get('USDT', 0)
    usdt_free = balance['free'].get('USDT', 0)
    
    print(f"💰 ACCOUNT BALANCE")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Total:      ${usdt_balance:,.2f}")
    print(f"   Available:  ${usdt_free:,.2f}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
except Exception as e:
    print(f"\n❌ CONNECTION ERROR")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Error: {str(e)}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"\n⚠️  TROUBLESHOOTING:")
    print(f"   • Check API keys in Render environment")
    print(f"   • Verify DELTA_TESTNET = 'true'")
    print(f"   • Ensure keys have trading permissions\n")
    time.sleep(10)
    exit(1)

# Main monitoring loop
cycle = 0
print("🔄 Starting market monitoring...\n")
print("=" * 70 + "\n")

while True:
    try:
        cycle += 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print("=" * 70)
        print(f"🔄 CYCLE #{cycle} - {timestamp}")
        print("=" * 70 + "\n")
        
        # Fetch market data
        ticker = exchange.fetch_ticker(SYMBOL)
        
        price = ticker['last']
        change = ticker.get('percentage', 0)
        high = ticker.get('high', 0)
        low = ticker.get('low', 0)
        volume = ticker.get('quoteVolume', 0)
        
        print(f"📊 MARKET DATA ({SYMBOL})")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   Price:      ${price:,.2f}")
        print(f"   24h Change: {change:+.2f}%")
        print(f"   24h High:   ${high:,.2f}")
        print(f"   24h Low:    ${low:,.2f}")
        print(f"   Volume:     ${volume:,.0f}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Account balance
        balance = exchange.fetch_balance()
        free = balance['free'].get('USDT', 0)
        total = balance['total'].get('USDT', 0)
        
        print(f"\n💰 ACCOUNT STATUS")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   Available:  ${free:,.2f}")
        print(f"   Total:      ${total:,.2f}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Check positions
        try:
            positions = exchange.fetch_positions([SYMBOL])
            open_pos = [p for p in positions if float(p.get('contracts', 0)) != 0]
            
            if open_pos:
                print(f"\n📊 OPEN POSITIONS: {len(open_pos)}")
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                for pos in open_pos:
                    side = pos.get('side', 'N/A')
                    size = pos.get('contracts', 0)
                    entry = pos.get('entryPrice', 0)
                    pnl = pos.get('unrealizedPnl', 0)
                    print(f"   {side.upper()}: {size} @ ${entry:,.2f} | P&L: ${pnl:+,.2f}")
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            else:
                print(f"\n✅ No open positions")
        except:
            print(f"\n✅ No open positions")
        
        # Status
        print(f"\n💡 Bot monitoring market (no auto-trading yet)")
        
        # Wait
        next_time = (datetime.now() + timedelta(seconds=INTERVAL)).strftime('%H:%M:%S')
        print(f"\n⏳ Next update in {INTERVAL}s ({INTERVAL//60} min) at {next_time}")
        print("\n" + "=" * 70 + "\n")
        
        time.sleep(INTERVAL)
        
    except KeyboardInterrupt:
        print(f"\n{'='*70}")
        print(f"🛑 BOT STOPPED")
        print(f"{'='*70}")
        print(f"   Cycles: {cycle}")
        print(f"   Final Balance: ${total:,.2f}")
        print(f"{'='*70}\n")
        break
        
    except Exception as e:
        print(f"\n❌ Error in cycle {cycle}: {e}")
        print(f"⏳ Retrying in 60 seconds...\n")
        time.sleep(60)

print("✅ Bot shutdown complete\n")
