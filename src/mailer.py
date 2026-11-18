"""
Mailer Module.
Formats Markdown reports into modern executive HTML emails and delivers them via SMTP.
"""

import os
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def markdown_to_html(md: str) -> str:
    """Converts markdown headers, bold, italics, lists, and links into styled HTML."""
    html = md

    # Escape HTML tags that might interfere
    html = html.replace("<", "&lt;").replace(">", "&gt;")

    # Convert headers
    html = re.sub(r"^# (.*?)$", r'<h1 style="color:#0f172a; font-size:24px; border-bottom:2px solid #e2e8f0; padding-bottom:8px; margin-top:24px; margin-bottom:12px;">\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r"^## (.*?)$", r'<h2 style="color:#1e293b; font-size:19px; background:#f8fafc; padding:8px 12px; border-left:4px solid #3b82f6; border-radius:4px; margin-top:20px; margin-bottom:10px;">\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r"^### (.*?)$", r'<h3 style="color:#334155; font-size:16px; margin-top:14px; margin-bottom:6px;">\1</h3>', html, flags=re.MULTILINE)

    # Convert bold and italics
    html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html)

    # Convert bullet points
    html = re.sub(r"^- (.*?)$", r'<li style="margin-bottom:6px; color:#334155; line-height:1.6;">\1</li>', html, flags=re.MULTILINE)

    # Wrap list items
    html = re.sub(r"(<li.*?>.*?</li>)+", r'<ul style="padding-left:20px; margin-top:6px; margin-bottom:14px;">\g<0></ul>', html, flags=re.DOTALL)

    # Convert paragraphs (double newline)
    paragraphs = html.split("\n\n")
    processed_paragraphs = []
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
        if p_clean.startswith("<h1") or p_clean.startswith("<h2") or p_clean.startswith("<h3") or p_clean.startswith("<ul"):
            processed_paragraphs.append(p_clean)
        else:
            processed_paragraphs.append(f'<p style="color:#334155; line-height:1.6; margin-bottom:12px;">{p_clean}</p>')

    html = "\n".join(processed_paragraphs)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Executive Morning Intelligence</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f1f5f9; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f5f9; padding:24px 12px;">
        <tr>
          <td align="center">
            <table width="640" cellpadding="0" cellspacing="0" style="max-width:640px; width:100%; background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);">
              <!-- Top Banner -->
              <tr>
                <td style="background:linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding:28px 24px; text-align:left;">
                  <span style="display:inline-block; font-size:11px; text-transform:uppercase; letter-spacing:1.5px; background:rgba(59,130,246,0.25); color:#93c5fd; padding:4px 10px; border-radius:999px; font-weight:600; margin-bottom:10px;">Daily Intelligence Briefing</span>
                  <h1 style="margin:0; color:#ffffff; font-size:22px; font-weight:700; letter-spacing:-0.5px;">Antigravity Autonomous Report</h1>
                  <p style="margin:6px 0 0 0; color:#94a3b8; font-size:13px;">Prepared for Anesu • 6:00 AM Mauritius Time</p>
                </td>
              </tr>
              <!-- Body Content -->
              <tr>
                <td style="padding:28px 24px 20px 24px;">
                  {html}
                </td>
              </tr>
              <!-- Footer -->
              <tr>
                <td style="background:#f8fafc; border-top:1px solid #e2e8f0; padding:18px 24px; text-align:center;">
                  <p style="margin:0; color:#64748b; font-size:12px; line-height:1.5;">
                    Autonomous Morning Briefing • Powered by Gemini AI on GitHub Actions.<br>
                    Goal: Continuous intellectual sharpening & conversational mastery.
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """


def send_email(subject: str, markdown_content: str, recipient_email: str, smtp_user: str, smtp_password: str) -> bool:
    """Sends the daily briefing email using standard SMTP (e.g. Gmail)."""
    if not smtp_user or not smtp_password:
        print("\n" + "=" * 60)
        print("NOTICE: Email sending skipped (SMTP credentials not configured).")
        print("To receive daily emails in your inbox, set these GitHub Secrets:")
        print("  - EMAIL_USER (e.g. anesumupesa@gmail.com)")
        print("  - EMAIL_APP_PASSWORD (16-character Google App Password)")
        print("=" * 60 + "\n")
        return False

    html_content = markdown_to_html(markdown_content)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Daily Intelligence <{smtp_user}>"
    msg["To"] = recipient_email

    # Plain text version
    part1 = MIMEText(markdown_content, "plain", "utf-8")
    # HTML version
    part2 = MIMEText(html_content, "html", "utf-8")

    msg.attach(part1)
    msg.attach(part2)

    try:
        smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.environ.get("SMTP_PORT", "587"))

        print(f"Connecting to SMTP server {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [recipient_email], msg.as_string())

        print(f"SUCCESS: Email sent to {recipient_email}")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
