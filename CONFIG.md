# 🚀 Quick Configuration Checklist

## 📧 STEP 1: Configure Email (Optional but Recommended)

### For Gmail (Free):

1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" + "Windows Computer"
3. Copy 16-character password
4. Edit `alerts/email.py`:
   ```python
   SENDER_EMAIL = "your_email@gmail.com"
   SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"  # Without quotes around spaces
   RECEIVER_EMAIL = "recipient@gmail.com"
   ```

**Status**: Email will send daily reports at 6:00 PM

---

## 📱 STEP 2: Telegram (Already Configured!)

- ✅ Already active and sending alerts
- Alerts send automatically when rules trigger
- No setup needed!

---

## 🎮 STEP 3: Discord (Optional, Free)

1. Create Discord server: https://discord.com/
2. Right-click channel → Edit → Integrations → Webhooks → New
3. Copy webhook URL
4. Edit `alerts/discord.py`:
   ```python
   DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
   ```

**Status**: Optional integration ready if needed

---

## ⏰ STEP 4: Run Scheduler

### Option A: Double-click (Easiest)

- Open `run_scheduler.bat`
- Runs until you close it
- Monitoring: 9:00 AM daily
- Email Report: 6:00 PM daily

### Option B: Custom times

Edit `scheduler.py`:

```python
MONITORING_TIME = "09:00"  # 24-hour format
EMAIL_TIME = "18:00"
```

### Option C: Run once manually

- Open `run_once.bat` OR
- Type: `python main.py`

---

## 📊 What Runs Every Day

**Morning (9:00 AM):**

- ✅ Fetch crypto prices
- ✅ Fetch market indices
- ✅ Check India inflation
- ✅ Check gold/silver prices
- ✅ Fetch latest news
- ✅ Trigger alerts (Telegram + Email)

**Evening (6:00 PM):**

- ✅ Send beautiful HTML email with full report

---

## 🔔 Notifications You'll Get

| Channel      | What           | When                                       |
| ------------ | -------------- | ------------------------------------------ |
| **Telegram** | Instant alerts | When rules trigger (9 AM & throughout day) |
| **Email**    | Full report    | 6:00 PM daily                              |
| **Discord**  | Optional       | If configured                              |

---

## ✅ Test Your Setup

1. **Test Email:**

   ```bash
   python -c "from alerts.email import send_email_alert; send_email_alert('Test', 'It works!')"
   ```

2. **Test Full Monitoring:**

   ```bash
   python main.py
   ```

3. **Test Scheduler** (runs, then ctrl+C to stop):
   ```bash
   python scheduler.py
   ```

---

## 📁 File Structure

```
monitoring-system/
├── main.py                 # Run once
├── scheduler.py            # Run daily (IMPORTANT)
├── run_once.bat           # Double-click to run once
├── run_scheduler.bat      # Double-click to run daily ⭐
├── SETUP_GUIDE.md         # Detailed setup
├── CONFIG.md              # This file
├── alerts/
│   ├── telegram.py        # ✅ Already configured
│   ├── email.py           # 📧 Configure if using Gmail
│   └── discord.py         # 🎮 Optional
├── collectors/
│   ├── crypto.py          # Bitcoin, Ethereum
│   ├── market.py          # NIFTY, SENSEX
│   ├── news.py            # Latest headlines
│   ├── inflation.py       # India inflation rate
│   └── metals.py          # Gold, Silver prices
└── rules/
    └── engine.py          # Alert logic
```

---

## 🆘 Troubleshooting

**Email not sending:**

- Check credentials in `alerts/email.py`
- Use App Password (not regular Gmail password)
- Verify Gmail 2FA is enabled

**Scheduler not working:**

- Run: `pip install -r requirements.txt`
- Check logs: `python scheduler.py` (will show startup messages)

**No Telegram alerts:**

- System sends them automatically
- Check internet connection
- Verify chat ID: 7230210433

---

## 🎯 Next Steps

1. ✅ Read this file
2. ✅ Edit `alerts/email.py` if using Gmail
3. ✅ Double-click `run_scheduler.bat`
4. ✅ Let it run (9 AM & 6 PM daily)
5. ✅ Check email & Telegram for reports

---

## 📞 Support Resources

- **Gmail App Password**: https://myaccount.google.com/apppasswords
- **Telegram Bot**: Already set up (bot ID: 8651643159)
- **Discord Webhooks**: https://discord.com/developers/docs/resources/webhook
- **Detailed Setup**: See `SETUP_GUIDE.md`

---

**🎉 Your monitoring system is ready! Let `run_scheduler.bat` run daily for automated updates.**

Last updated: 2026-03-27
