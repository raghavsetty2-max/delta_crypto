# 🚀 Crypto Trading Bot for Delta Exchange

Automated trading bot using Delta Exchange Native API.

## Features
- ✅ Native Delta Exchange API (no ccxt dependency)
- ✅ Testnet support for safe testing
- ✅ Real-time wallet monitoring
- ✅ Position tracking
- ✅ Web dashboard

## Deployment Status
- Mode: TESTNET (Fake Money)
- API: Native Delta Exchange API
- Update Interval: 15 minutes

## Environment Variables Required
- DELTA_API_KEY
- DELTA_API_SECRET
- DELTA_TESTNET
- TRADING_SYMBOL
- INTERVAL_SECONDS
```

---

# 🔧 **RENDER ENVIRONMENT VARIABLES**

**In Render → delta_crypto → Environment, set these:**
```
DELTA_API_KEY = epqAzxuLds3EnlBi8E0RjZudatk8T4
DELTA_API_SECRET = F1X2nUPaTWouanTWxLxsZOZKYGCYZFbQvrf8PosjtbPAI1o6ps2kEjRcOzvx
DELTA_TESTNET = true
TRADING_SYMBOL = BTCUSD
INTERVAL_SECONDS = 900
```

**⚠️ Important: `BTCUSD` not `BTC/USDT`!**

---

# 📋 **COMPLETE FILE STRUCTURE**
```
delta_crypto/
├── .python-version       # Force Python 3.11
├── README.md             # Documentation
├── requirements.txt      # Dependencies (simplified!)
├── main_bot.py          # Main bot (native API)
├── web_dashboard.py     # Dashboard
├── Procfile             # Render worker config
└── render.yaml          # Render deployment config
```

---

# 🚀 **DEPLOYMENT STEPS**

## **Step 1: Update GitHub Files**

1. Go to: https://github.com/raghavsetty2-max/delta_crypto
2. **Delete or replace** `main_bot.py` with FILE 1 above
3. **Replace** `requirements.txt` with FILE 2
4. **Verify** `web_dashboard.py`, `Procfile`, `render.yaml` exist
5. **Create** `.python-version` with content: `3.11`
6. **Update** `README.md` (optional)

---

## **Step 2: Update Render Environment**

1. Go to Render → **delta_crypto** → **Environment**
2. Update/Add these 5 variables:
```
DELTA_API_KEY → epqAzxuLds3EnlBi8E0RjZudatk8T4
DELTA_API_SECRET → F1X2nUPaTWouanTWxLxsZOZKYGCYZFbQvrf8PosjtbPAI1o6ps2kEjRcOzvx
DELTA_TESTNET → true
TRADING_SYMBOL → BTCUSD  (⚠️ changed from BTC/USDT!)
INTERVAL_SECONDS → 900
```

3. Click **"Save Changes"**

---

## **Step 3: Deploy**

1. Click **"Manual Deploy"**
2. Select **"Clear build cache & deploy"**
3. Click **"Deploy"**
4. Wait 2-3 minutes
5. Check **"Logs"**

---

# ✅ **SUCCESS OUTPUT:**
```
╔════════════════════════════════════════════════════════════╗
║          🚀 CRYPTO TRADING BOT STARTED                    ║
║             Delta Exchange Native API                     ║
╚════════════════════════════════════════════════════════════╝

✅ Successfully connected to Delta Exchange!
💡 Using FAKE money - Safe for testing!

💰 WALLET BALANCES:
   USDT:
      Available: 10000.0000
      Total:     10000.0000
   Total Portfolio Value: $10,000.00

✅ Found product: BTCUSD

🔄 CYCLE #1
💰 WALLET STATUS:
   USDT: $10,000.00 (Available: $10,000.00)
   Total Value: $10,000.00

📊 POSITIONS:
   No open positions

💡 Status: Monitoring market
⏳ Next update in 900s (15 min)
