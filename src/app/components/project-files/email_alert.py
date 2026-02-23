"""
SecureVigil Email Alert System
Send automated email notifications for high-risk vulnerabilities
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
import os
from datetime import datetime


def send_alert(summary: Dict, high_risk_findings: List[Dict], 
               sender: str = None, receiver: str = None, password: str = None) -> bool:
    """
    Send email alert for high-risk vulnerabilities
    
    Args:
        summary: Risk summary dictionary
        high_risk_findings: List of high-risk findings
        sender: Email sender address (uses env var if not provided)
        receiver: Email receiver address (uses env var if not provided)
        password: Email password (uses env var if not provided)
    
    Returns:
        True if email sent successfully, False otherwise
    """
    # Get credentials from environment variables if not provided
    sender = sender or os.getenv("ALERT_EMAIL_SENDER")
    receiver = receiver or os.getenv("ALERT_EMAIL_RECEIVER")
    password = password or os.getenv("ALERT_EMAIL_PASSWORD")
    
    if not all([sender, receiver, password]):
        print("[!] Email configuration missing. Set environment variables:")
        print("    ALERT_EMAIL_SENDER")
        print("    ALERT_EMAIL_RECEIVER")
        print("    ALERT_EMAIL_PASSWORD")
        return False
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = f"🚨 SecureVigil Alert - {summary['high']} HIGH Risk Vulnerabilities Detected"
    message["From"] = sender
    message["To"] = receiver
    message["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
    
    # Create text version
    text_body = create_text_body(summary, high_risk_findings)
    
    # Create HTML version
    html_body = create_html_body(summary, high_risk_findings)
    
    # Attach both versions
    part1 = MIMEText(text_body, "plain")
    part2 = MIMEText(html_body, "html")
    message.attach(part1)
    message.attach(part2)
    
    try:
        # Send via Gmail SMTP (configure for other providers as needed)
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.send_message(message)
        server.quit()
        print(f"[+] Alert email sent successfully to {receiver}")
        return True
    except Exception as e:
        print(f"[!] Email sending failed: {e}")
        return False


def create_text_body(summary: Dict, findings: List[Dict]) -> str:
    """Create plain text email body"""
    text = f"""
SECUREVIGIL VULNERABILITY ALERT
================================

{summary['high']} HIGH RISK VULNERABILITIES DETECTED

Scan Summary:
- Total Findings: {summary['total']}
- High Risk: {summary['high']}
- Medium Risk: {summary['medium']}
- Low Risk: {summary['low']}
- Risk Score: {summary.get('risk_score', 'N/A')}

High Risk Findings (Top 5):
"""
    
    for i, finding in enumerate(findings[:5], 1):
        text += f"""
{i}. {finding.get('host')}:{finding.get('port')} - {finding.get('service')}
   Product: {finding.get('product', 'Unknown')} {finding.get('version', '')}
   Recommendation: {finding.get('recommendation', 'Review immediately')}
"""
    
    text += """
Please review the full report in the SecureVigil dashboard.

---
This is an automated alert from SecureVigil
"""
    return text


def create_html_body(summary: Dict, findings: List[Dict]) -> str:
    """Create HTML email body"""
    
    # Generate findings list HTML
    findings_html = ""
    for i, finding in enumerate(findings[:5], 1):
        findings_html += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">{finding.get('host')}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{finding.get('port')}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{finding.get('service')}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{finding.get('product', '')} {finding.get('version', '')}</td>
        </tr>
        """
    
    html = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
          }}
          .header {{
            background-color: #dc3545;
            color: white;
            padding: 20px;
            text-align: center;
          }}
          .content {{
            padding: 20px;
          }}
          .summary {{
            background-color: #f8f9fa;
            border-left: 4px solid #dc3545;
            padding: 15px;
            margin: 20px 0;
          }}
          .summary-item {{
            margin: 10px 0;
          }}
          table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
          }}
          th {{
            background-color: #343a40;
            color: white;
            padding: 10px;
            text-align: left;
          }}
          td {{
            padding: 8px;
            border: 1px solid #ddd;
          }}
          tr:nth-child(even) {{
            background-color: #f8f9fa;
          }}
          .footer {{
            background-color: #f8f9fa;
            padding: 15px;
            text-align: center;
            font-size: 12px;
            color: #666;
          }}
          .high-risk {{
            color: #dc3545;
            font-weight: bold;
          }}
        </style>
      </head>
      <body>
        <div class="header">
          <h1>🚨 SecureVigil Security Alert</h1>
          <p class="high-risk" style="font-size: 24px; margin: 10px 0;">
            {summary['high']} HIGH Risk Vulnerabilities Detected
          </p>
        </div>
        
        <div class="content">
          <div class="summary">
            <h2>Scan Summary</h2>
            <div class="summary-item">
              <strong>Total Findings:</strong> {summary['total']}
            </div>
            <div class="summary-item">
              <strong>High Risk:</strong> <span class="high-risk">{summary['high']}</span>
            </div>
            <div class="summary-item">
              <strong>Medium Risk:</strong> {summary['medium']}
            </div>
            <div class="summary-item">
              <strong>Low Risk:</strong> {summary['low']}
            </div>
            <div class="summary-item">
              <strong>Risk Score:</strong> {summary.get('risk_score', 'N/A')}
            </div>
          </div>
          
          <h2>High Risk Findings (Top 5)</h2>
          <table>
            <thead>
              <tr>
                <th>Host</th>
                <th>Port</th>
                <th>Service</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody>
              {findings_html}
            </tbody>
          </table>
          
          <p>
            <strong>Action Required:</strong> Please review these findings immediately and 
            implement recommended remediations. Access the full report in the SecureVigil 
            dashboard for detailed analysis and remediation steps.
          </p>
        </div>
        
        <div class="footer">
          <p>This is an automated security alert from SecureVigil</p>
          <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
      </body>
    </html>
    """
    return html


def should_send_alert(summary: Dict, threshold: int = 1) -> bool:
    """
    Determine if alert threshold is met
    
    Args:
        summary: Risk summary dictionary
        threshold: Minimum number of high-risk findings to trigger alert
    
    Returns:
        True if alert should be sent
    """
    return summary.get("high", 0) >= threshold


def send_scan_complete_notification(target: str, summary: Dict) -> bool:
    """
    Send notification that scan is complete (regardless of findings)
    
    Args:
        target: Target that was scanned
        summary: Scan summary
    
    Returns:
        True if sent successfully
    """
    sender = os.getenv("ALERT_EMAIL_SENDER")
    receiver = os.getenv("ALERT_EMAIL_RECEIVER")
    password = os.getenv("ALERT_EMAIL_PASSWORD")
    
    if not all([sender, receiver, password]):
        return False
    
    message = MIMEMultipart("alternative")
    message["Subject"] = f"✅ SecureVigil Scan Complete - {target}"
    message["From"] = sender
    message["To"] = receiver
    
    text = f"""
Scan Complete: {target}

Results:
- Total Findings: {summary['total']}
- High: {summary['high']}
- Medium: {summary['medium']}
- Low: {summary['low']}

View full report in SecureVigil dashboard.
"""
    
    message.attach(MIMEText(text, "plain"))
    
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.send_message(message)
        server.quit()
        return True
    except:
        return False


if __name__ == "__main__":
    # Example usage
    print("Testing email alert system...")
    print("\nRequired environment variables:")
    print("  ALERT_EMAIL_SENDER=your-email@gmail.com")
    print("  ALERT_EMAIL_RECEIVER=security-team@company.com")
    print("  ALERT_EMAIL_PASSWORD=your-app-password")
    
    # Test with sample data
    test_summary = {
        "total": 10,
        "high": 3,
        "medium": 5,
        "low": 2,
        "risk_score": 65
    }
    
    test_findings = [
        {"host": "192.168.1.10", "port": 23, "service": "telnet", 
         "product": "Linux telnetd", "version": "1.0"},
        {"host": "192.168.1.10", "port": 21, "service": "ftp", 
         "product": "vsftpd", "version": "2.3.4"},
    ]
    
    if should_send_alert(test_summary):
        print("\n[+] Alert threshold met")
        # Uncomment to actually send test email:
        # send_alert(test_summary, test_findings)
    else:
        print("\n[-] Alert threshold not met")
