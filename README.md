# 🚀 Crypto Trading Bot

Automated cryptocurrency trading bot for Delta Exchange. Monitors BTC/USDT and tracks account performance 24/7.

---

## ✨ Features

- 🤖 **Automated Monitoring**: Checks BTC/USDT price every 15 minutes
- 💰 **Account Tracking**: Real-time balance and position monitoring
- 📊 **Web Dashboard**: Beautiful web interface to check bot status
- 🔒 **Safe Testing**: Testnet mode with fake money for practice
- ☁️ **Cloud Hosted**: Runs 24/7 on Render.com
- 📝 **Detailed Logging**: Complete activity logs for transparency

---

## 🎯 Current Status

**Mode:** Monitoring Only (No Auto-Trading)

The bot currently:
- ✅ Monitors market prices
- ✅ Tracks account balance
- ✅ Shows open positions
- ✅ Logs all activity
- ❌ Does NOT trade automatically (safe!)

---

## 📋 Requirements

- Delta Exchange account (testnet or live)
- GitHub account
- Render.com account (free tier)
- API keys from Delta Exchange

---

## 🚀 Quick Start

### 1. Delta Exchange Setup

1. Create account at [testnet.delta.exchange](https://testnet.delta.exchange)
2. Go to Settings → API
3. Create API key with Read and Trade permissions
4. Save API key and secret securely

### 2. Deploy to Render

1. Fork or clone this repository
2. Sign up at [render.com](https://render.com) with GitHub
3. Create new Background Worker
4. Connect this repository
5. Add environment variables (see below)
6. Deploy!

### 3. Configure Environment Variables

Add these in Render dashboard:
