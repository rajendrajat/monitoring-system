# 📊 Financial Monitoring System

A comprehensive Python-based monitoring system that tracks cryptocurrency prices, market indices, India inflation rates, and precious metals prices. Sends automated alerts via Telegram and daily reports via email.

## ✨ Features

- **📈 Real-time Monitoring**: Crypto, markets, inflation, and metals
- **🚨 Smart Alerts**: Telegram notifications for price movements
- **📧 Daily Reports**: Beautiful HTML email summaries
- **⏰ Automated**: Runs daily at scheduled times
- **🔒 Secure**: Environment variables for sensitive data
- **🎯 Customizable**: Configurable alert thresholds

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/monitoring-system.git
cd monitoring-system
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
python setup.py
```

This interactive script will help you configure:

- Telegram bot for alerts
- Email for daily reports (optional)
- Discord webhook (optional)
- API keys (optional)
- Alert thresholds

### 3. Test the System

```bash
# Test once
python main.py

# Run daily automation
python scheduler.py
```

## 📋 Requirements

- Python 3.7+
- Internet connection
- Telegram account (for alerts)
- Gmail account (for email reports, optional)

## 🔧 Configuration

### Environment Variables

The system uses environment variables for security. Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
# Edit .env with your configuration
```

### Key Settings

| Variable             | Description             | Example                                     |
| -------------------- | ----------------------- | ------------------------------------------- |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `TELEGRAM_CHAT_ID`   | Your Telegram chat ID   | `7230210433`                                |
| `EMAIL_SENDER`       | Gmail address           | `your.email@gmail.com`                      |
| `EMAIL_PASSWORD`     | Gmail App Password      | `abcd efgh ijkl mnop`                       |
| `MONITORING_TIME`    | Daily check time        | `09:00`                                     |
| `EMAIL_REPORT_TIME`  | Daily email time        | `18:00`                                     |

## 📊 What Gets Monitored

### Data Sources

- **Cryptocurrency**: CoinGecko API (Bitcoin, Ethereum)
- **Market Indices**: Alpha Vantage API or mock data (NIFTY, SENSEX)
- **Inflation**: World Bank API + RBI estimates
- **Precious Metals**: Market estimates (Gold, Silver)
- **News**: Google News RSS (latest headlines)

### Alert Thresholds (Default)

- Bitcoin: < ₹50,00,000
- NIFTY: > -1.5% drop
- Inflation: > 6.0%
- Gold: > ₹7,500/gram
- Silver: > ₹100/gram
- News: Keywords (war, oil, inflation, gold, silver)

## 🔔 Notifications

### Telegram Alerts

- Instant notifications when conditions are met
- Breaking news alerts
- Price movement alerts
- System status updates

### Email Reports

- Daily HTML reports at specified time
- Complete data summary
- Alert history
- Trend analysis

## 🛠️ Customization

### Change Alert Thresholds

Edit `.env` file:

```bash
BITCOIN_ALERT_THRESHOLD=4500000
NIFTY_DROP_THRESHOLD=-2.0
GOLD_HIGH_THRESHOLD=8000
```

### Modify Schedule

```bash
MONITORING_TIME=08:30
EMAIL_REPORT_TIME=19:00
```

### Add New Data Sources

Extend collectors in the `collectors/` directory:

- `crypto.py` - Add more cryptocurrencies
- `market.py` - Add more indices
- `inflation.py` - Add more economic indicators
- `metals.py` - Add more precious metals

## 📁 Project Structure

```
monitoring-system/
├── 📄 README.md              # This file
├── 📄 .env.example           # Environment template
├── 📄 .gitignore             # Git ignore rules
├── 📄 requirements.txt       # Python dependencies
├── 📄 setup.py               # Interactive setup script
├── 📄 main.py                # Single run script
├── 📄 scheduler.py           # Daily automation
├── 📄 run_once.bat           # Windows launcher
├── 📄 run_scheduler.bat      # Windows scheduler launcher
├── alerts/
│   ├── telegram.py           # Telegram notifications
│   ├── email.py              # Email reports
│   └── discord.py            # Discord webhooks
├── collectors/
│   ├── crypto.py             # Cryptocurrency data
│   ├── market.py             # Market indices
│   ├── news.py               # News headlines
│   ├── inflation.py          # Inflation rates
│   └── metals.py             # Precious metals
├── rules/
│   └── engine.py             # Alert logic
└── CONFIG.md                 # Detailed setup guide
```

## 🔒 Security

- **Never commit `.env` file** - Contains sensitive tokens
- **Use App Passwords** - For Gmail authentication
- **Environment Variables** - All secrets loaded from `.env`
- **Restrictive Permissions** - `.env` file permissions set to owner-only

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError"**

```bash
pip install -r requirements.txt
```

**Telegram not working**

- Check bot token format (starts with numbers, contains ':')
- Verify chat ID is numeric
- Test: Visit `https://api.telegram.org/bot<TOKEN>/getMe`

**Email not sending**

- Use Gmail App Password (not regular password)
- Enable 2FA on Gmail account
- Check SMTP settings

**Scheduler not running**

- Install APScheduler: `pip install apscheduler`
- Check system time format

### Debug Mode

Set in `.env`:

```bash
DEBUG_MODE=true
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. See LICENSE file for details.

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: See `CONFIG.md` and `SETUP_GUIDE.md`

---

**⚠️ Important**: Never commit sensitive information like API keys, passwords, or tokens to GitHub. Always use environment variables and keep `.env` files private.

**🚀 Ready to monitor? Run `python setup.py` to get started!**
