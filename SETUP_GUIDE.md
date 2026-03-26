# 📊 Monitoring System - Setup Guide

## Quick Start

### Option 1: Run Once Manually

```bash
python main.py
```

### Option 2: Run Daily Automatically (Recommended)

```bash
python scheduler.py
```

This runs in the background and monitors at set times daily.

---

## 📧 Email Configuration (FREE)

### Gmail Setup (Recommended)

1. Enable 2-Factor Authentication on your Gmail account
2. Generate App Password:
   - Visit: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password
3. Edit `alerts/email.py`:
   ```python
   SENDER_EMAIL = "your_email@gmail.com"
   SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"  # 16-char app password
   RECEIVER_EMAIL = "recipient@gmail.com"
   ```
4. Done! ✅

### Alternative Email Providers

- **Outlook/Hotmail**: Use `smtp.outlook.com:587`
- **Yahoo**: Use `smtp.mail.yahoo.com:587` (requires app password)
- **Custom Domain**: Use your provider's SMTP server

---

## 📱 Telegram Configuration (FREE)

Already configured! Alerts send automatically.

**To verify:**

1. Chat ID: `7230210433`
2. Bot Token: Active (starts with `8651643159:`)
3. All alerts send automatically when triggered

---

## 🎮 Discord Configuration (FREE)

1. Create a Discord Server: https://discord.com/
2. Create a text channel for alerts
3. Right-click channel → Edit Channel → Integrations → Webhooks
4. "New Webhook" → Copy URL
5. Edit `alerts/discord.py`:
   ```python
   DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"
   ```
6. To enable in monitoring, update `rules/engine.py` to call Discord (optional)

---

## ⏰ Schedule Configuration

Edit `scheduler.py` to change times:

```python
MONITORING_TIME = "09:00"  # Daily monitoring (24-hour format)
EMAIL_TIME = "18:00"       # Daily email report (24-hour format)
```

### Recommended Schedule

- **Monitoring**: 9:00 AM (market open, news updated)
- **Email Report**: 6:00 PM (evening summary)

---

## 🚀 Running as Background Service

### Windows (PowerShell as Admin)

```powershell
# Install NSSM: https://nssm.cc/download
nssm install MonitoringSystem "python scheduler.py"
nssm start MonitoringSystem
```

### Linux/Mac

```bash
# Using nohup
nohup python scheduler.py > monitoring.log 2>&1 &

# Or using screen
screen -S monitoring python scheduler.py
```

---

## 📊 What Gets Monitored Daily

✅ **Cryptocurrency**: Bitcoin, Ethereum prices  
✅ **Markets**: NIFTY, SENSEX indices  
✅ **India Inflation**: Current rate, trend, target  
✅ **Precious Metals**: Gold & Silver prices  
✅ **Breaking News**: War, oil, inflation, gold updates

## 🚨 Alert Thresholds

| Alert         | Trigger                                 |
| ------------- | --------------------------------------- |
| Bitcoin       | < ₹50,00,000                            |
| NIFTY         | > -1.5% drop                            |
| Inflation     | > 6% OR > RBI target + 1.5%             |
| Gold          | > ₹7500/gram                            |
| Silver        | > ₹100/gram                             |
| News Keywords | inflation, war, iran, oil, gold, silver |

---

## 📧 Daily Email Report

Sent at scheduled time (default: 6:00 PM)

Includes:

- Crypto prices
- Market indices
- Inflation data
- Precious metals prices
- Latest news headlines
- All triggered alerts

**Example**: Multiple formats

- HTML (colorful, formatted)
- Plain text (minimal)

---

## ✅ Monitoring Checklist

- [ ] Email configured (Gmail recommended)
- [ ] Telegram bot token verified
- [ ] Scheduler.py runs without errors
- [ ] Check logs for successful runs
- [ ] Test first run: `python scheduler.py`
- [ ] Set up as background service if needed

---

## 🛠️ Troubleshooting

### Email Not Sending

```
❌ Authentication failed
```

- [ ] Check Gmail app password is correct (16 characters with spaces)
- [ ] Verify 2FA is enabled
- [ ] Check SENDER_EMAIL matches account

### Scheduler Not Running

```
❌ APScheduler not found
```

Run: `pip install -r requirements.txt`

### No Telegram Alerts

```
❌ Telegram connection failed
```

- Check internet connection
- Verify CHAT_ID in `alerts/telegram.py`
- Test manually: `python main.py`

---

## 📞 Free Support Channels

**Telegram**: Already integrated (can check bot status)  
**Email**: Daily reports show all collected data  
**Discord**: Optional, free webhook integration

---

## 🔒 Security Notes

- Keep API tokens/passwords secret
- Don't commit credentials to Git
- Use environment variables for production:
  ```python
  import os
  SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
  ```

---

## 📈 Customization

### Add Custom Alert Rules

Edit `rules/engine.py` - add new rules for different thresholds

### Change Data Sources

Edit collectors in `collectors/` directory

### Add More Notifications

Create new alert types in `alerts/` (following email.py pattern)

---

**Last Updated**: 2026-03-27  
**Status**: ✅ Production Ready
