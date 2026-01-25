import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import re


class EmailClient:
    def __init__(self, user: str, password: str, smtp_host: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Initialize Email client.

        Args:
            user: Email address (sender)
            password: App password
            smtp_host: SMTP server host
            smtp_port: SMTP server port
        """
        self.user = user
        self.password = password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def _markdown_to_html(self, text: str) -> str:
        """
        Convert simple Markdown to HTML for email.
        Supports: **bold**, list items (* or -), and headers (#, ##, ###).
        """
        # Encode HTML special characters to prevent injection/broken layout
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        lines = text.split('\n')
        html_lines = []
        in_list = False

        for line in lines:
            stripped = line.strip()

            # Handle empty lines
            if not stripped:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append("<br>")
                continue

            # Handle List Items
            if stripped.startswith('* ') or stripped.startswith('- '):
                if not in_list:
                    html_lines.append('<ul style="padding-left: 20px; margin: 10px 0;">')
                    in_list = True
                content = stripped[2:]
                # Bold parsing within list item
                content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
                html_lines.append(f'<li style="margin-bottom: 5px;">{content}</li>')
                continue

            # Close list if line is not a list item
            if in_list:
                html_lines.append("</ul>")
                in_list = False

            # Handle Headers
            if stripped.startswith('### '):
                header_text = stripped[4:]
                html_lines.append(f'<h4 style="margin-top: 15px; margin-bottom: 5px; color: #444;">{header_text}</h4>')
            elif stripped.startswith('## '):
                header_text = stripped[3:]
                html_lines.append(f'<h3 style="margin-top: 20px; margin-bottom: 10px; color: #333;">{header_text}</h3>')
            elif stripped.startswith('# '):
                header_text = stripped[2:]
                html_lines.append(f'<h2 style="margin-top: 20px; margin-bottom: 10px; color: #222;">{header_text}</h2>')
            else:
                # Regular paragraph
                # Bold parsing
                line_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', stripped)
                html_lines.append(f'<p style="margin: 0 0 10px 0; line-height: 1.6;">{line_content}</p>')

        if in_list:
            html_lines.append("</ul>")

        return "".join(html_lines)

    def create_html_body(self, intro_text: str, reports: list) -> str:
        """
        Create structured and styled HTML content from reports.

        Args:
            intro_text: Introduction paragraph
            reports: List of dictionaries containing repository info and gemini analysis/digest

        Returns:
            HTML string
        """
        # Outer Container & Header
        html_parts = [
            '<!DOCTYPE html>',
            '<html><body style="font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; background-color: #f4f4f4; padding: 20px; margin: 0; color: #333;">',
            '<div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">',
            '  <div style="background-color: #007bff; padding: 20px; text-align: center;">',
            '    <h2 style="color: #ffffff; margin: 0; font-weight: 500;">Weekly GitHub Digest</h2>',
            '  </div>',
            '  <div style="padding: 30px;">',
            f'    <p style="font-size: 16px; color: #555; line-height: 1.6; margin-bottom: 25px;">{intro_text}</p>',
        ]

        for report in reports:
            # Convert Markdown digest to HTML
            digest_html = self._markdown_to_html(report['digest'])

            # Repository Card
            repo_section = f"""
            <div style="margin-bottom: 35px; border: 1px solid #e1e4e8; border-radius: 6px; overflow: hidden;">
                <div style="background-color: #f6f8fa; padding: 12px 15px; border-bottom: 1px solid #e1e4e8; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; font-size: 18px;">
                            <a href="{report['url']}" style="color: #0366d6; text-decoration: none;">{report['name']}</a>
                        </h3>
                    </div>
                </div>
                <div style="padding: 10px 15px; background-color: #ffffff; border-bottom: 1px solid #eaeaea; font-size: 12px; color: #586069;">
                    <span style="margin-right: 15px;">⭐ <strong>{report['stars']}</strong> Stars</span>
                    <span>🏷️ {report.get('language', 'N/A')}</span>
                </div>
                <div style="padding: 15px; background-color: #ffffff; font-size: 14px; color: #24292e;">
                    {digest_html}
                </div>
            </div>
            """
            html_parts.append(repo_section)

        # Footer
        html_parts.append('  </div>')
        html_parts.append('  <div style="background-color: #f8f9fa; color: #888; padding: 15px; text-align: center; font-size: 12px; border-top: 1px solid #eaeaea;">Generated by Trends Digest AI</div>')
        html_parts.append('</div>')
        html_parts.append('</body></html>')

        return "\n".join(html_parts)

    def send_email(self, to_address: str, subject: str, body: str) -> bool:
        """
        Send HTML email.
        """
        msg = MIMEMultipart()
        msg["From"] = self.user
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        server = None
        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.set_debuglevel(0)
            server.starttls()
            server.login(self.user, self.password)
            server.send_message(msg)
            print(f"Email sent successfully to {to_address}.")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

        finally:
            if server:
                server.quit()
