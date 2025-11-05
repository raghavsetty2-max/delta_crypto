"""
Web Dashboard for Trading Bot
"""

from flask import Flask, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Bot Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 50px;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            font-size: 36px;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            color: #999;
            text-align: center;
            margin-bottom: 40px;
        }
        .card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
        }
        .row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .row:last-child { border-bottom: none; }
        .label {
            color: #666;
            font-weight: 600;
        }
        .value {
            color: #333;
            font-weight: bold;
        }
        .badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 13px;
        }
        .badge-test {
            background: #4CAF50;
            color: white;
        }
        .badge-live {
            background: #f44336;
            color: white;
        }
        .alert {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            color: #155724;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 14px;
        }
        .status-dot {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #4CAF50;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Crypto Trading Bot</h1>
        <p class="subtitle">Delta Exchange Automated Trading</p>
        
        <div class="card">
            <div class="row">
                <span class="label">Status:</span>
                <span class="value">
                    <span class="status-dot"></span>Running
                </span>
            </div>
            <div class="row">
                <span class="label">Mode:</span>
                <span class="value">
                    <span class="badge {{ 'badge-test' if testnet else 'badge-live' }}">
                        {{ 'TESTNET' if testnet else 'LIVE' }}
                    </span>
                </span>
            </div>
            <div class="row">
                <span class="label">Symbol:</span>
                <span class="value">{{ symbol }}</span>
            </div>
            <div class="row">
                <span class="label">Interval:</span>
                <span class="value">{{ interval }} minutes</span>
            </div>
        </div>
        
        <div class="alert">
            <strong>{{ '✅ Testing Mode' if testnet else '🔴 LIVE Trading' }}</strong><br>
            {{ 'Using fake money - Safe for learning!' if testnet else 'Using REAL money - Monitor closely!' }}
        </div>
        
        <div class="card">
            <h3 style="margin-bottom: 15px; color: #667eea;">📊 Monitor Bot</h3>
            <p style="color: #666;">
                1. Go to Render Dashboard<br>
                2. Click "delta_crypto"<br>
                3. Click "Logs" tab<br>
                4. View real-time activity
            </p>
        </div>
        
        <div class="footer">
            Deployed on Render.com<br>
            Powered by Delta Exchange
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    testnet = os.getenv('DELTA_TESTNET', 'true').lower() == 'true'
    symbol = os.getenv('TRADING_SYMBOL', 'BTCUSD')
    interval = int(os.getenv('INTERVAL_SECONDS', '900')) // 60
    
    return render_template_string(HTML, testnet=testnet, symbol=symbol, interval=interval)

@app.route('/health')
def health():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


