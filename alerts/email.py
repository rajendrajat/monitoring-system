import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Email Configuration - Load from environment variables
SENDER_EMAIL = os.getenv("EMAIL_SENDER", "USE_YOUR_EMAIL@gmail.com")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD", "USE_YOUR_APP_PASSWORD")
RECEIVER_EMAIL = os.getenv(
    "EMAIL_RECEIVER", "USE_YOUR_RECEIVER_EMAIL@gmail.com")
SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))


def send_email_alert(subject, message, is_html=False):
    """
    Send an email alert

    Args:
        subject (str): Email subject
        message (str): Email body/message
        is_html (bool): Whether message is HTML formatted
    """
    try:
        # Check if credentials are set
        if SENDER_EMAIL == "USE_YOUR_EMAIL@gmail.com":
            print(
                "[EMAIL WARNING] Email not configured. Please set SENDER_EMAIL in alerts/email.py")
            return False

        # Create email message
        email_message = MIMEMultipart()
        email_message["From"] = SENDER_EMAIL
        email_message["To"] = RECEIVER_EMAIL
        email_message["Subject"] = subject

        # Add message body
        if is_html:
            email_message.attach(MIMEText(message, "html"))
        else:
            email_message.attach(MIMEText(message, "plain"))

        # Connect to SMTP server and send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Encrypt connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(email_message)
        server.quit()

        print(f"[EMAIL ✅ SENT] Subject: {subject}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("[EMAIL ERROR] Authentication failed. Check email and password.")
        print("  Tip: For Gmail, use App Password from: https://myaccount.google.com/apppasswords")
        return False
    except smtplib.SMTPException as e:
        print(f"[EMAIL ERROR] SMTP error: {e}")
        return False
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


def send_daily_report(data, alerts):
    """
    Send formatted daily monitoring report via email

    Args:
        data (dict): Collected monitoring data
        alerts (list): List of triggered alerts
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build HTML report
    html_report = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
            .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; background: #ecf0f1; }}
            .alert {{ background-color: #e74c3c; color: white; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .success {{ color: green; }}
            .warning {{ color: orange; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #34495e; color: white; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>📊 Daily Monitoring Report</h2>
            <p>{timestamp}</p>
        </div>
        
        <div class="section">
            <h3>💰 Cryptocurrency Prices</h3>
            <table>
                <tr><th>Asset</th><th>Price (₹)</th></tr>
    """

    # Add crypto data
    if data.get("crypto"):
        for crypto, price in data['crypto'].items():
            html_report += f"<tr><td>{crypto.title()}</td><td>₹{price:,.0f}</td></tr>"
    else:
        html_report += "<tr><td colspan='2'>No data available</td></tr>"

    html_report += """
            </table>
        </div>
        
        <div class="section">
            <h3>📈 Market Indices</h3>
            <table>
                <tr><th>Index</th><th>Price</th><th>Change</th></tr>
    """

    # Add market data
    if data.get("market"):
        for symbol, values in data['market'].items():
            price = values.get('price', 'N/A')
            change = values.get('change_percent', 'N/A')
            change_color = "success" if change < 0 else "warning" if change > 0 else ""
            html_report += f"<tr><td>{symbol}</td><td>₹{price:,.0f}</td><td class='{change_color}'>{change:.2f}%</td></tr>"
    else:
        html_report += "<tr><td colspan='3'>No data available</td></tr>"

    html_report += """
            </table>
        </div>
        
        <div class="section">
            <h3>🌍 Inflation & Precious Metals</h3>
    """

    # Add inflation data
    if data.get("inflation"):
        inf = data['inflation']
        html_report += f"""
            <p><strong>India Inflation Rate:</strong> {inf['current_rate']}% (Expected: {inf['expected_rate']}%, RBI Target: {inf['rbi_target']}%)</p>
            <p><strong>Trend:</strong> {inf['trend'].capitalize()} | <strong>Status:</strong> {inf['status'].replace('_', ' ').title()}</p>
        """

    # Add metals data
    if data.get("metals"):
        metals = data['metals']
        gold = metals.get('gold', {}).get('price_inr', 'N/A')
        silver = metals.get('silver', {}).get('price_inr', 'N/A')
        html_report += f"""
            <p><strong>Gold:</strong> ₹{gold:,.2f}/gram | <strong>Silver:</strong> ₹{silver:,.2f}/gram</p>
        """

    html_report += """
        </div>
        
        <div class="section">
            <h3>📰 Latest News Headlines</h3>
    """

    # Add news data
    if data.get("news"):
        for i, item in enumerate(data['news'][:5], 1):
            if isinstance(item, dict):
                headline = item.get("title", "")
                date = item.get("date", "")
                html_report += f"<p><strong>{i}.</strong> {headline}<br><em>{date}</em></p>"
            else:
                html_report += f"<p><strong>{i}.</strong> {item}</p>"
    else:
        html_report += "<p>No news data available</p>"

    html_report += """
        </div>
    """

    # Add alerts
    if alerts:
        html_report += f"""
        <div class="section">
            <h3>🚨 Alerts Triggered ({len(alerts)})</h3>
        """
        for alert in alerts:
            html_report += f"<div class='alert'>{alert}</div>"
        html_report += """
        </div>
        """
    else:
        html_report += """
        <div class="section">
            <p><span class="success">✅ No alerts triggered this period</span></p>
        </div>
        """

    html_report += """
    </body>
    </html>
    """

    # Send email
    return send_email_alert(
        subject=f"📊 Daily Monitoring Report - {timestamp.split()[0]}",
        message=html_report,
        is_html=True
    )
