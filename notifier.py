import yagmail
import os

def send_security_alert(recipient_email, intruder_info="Unauthorized Access Detected"):
    """
    Sends a silent email alert to the specified recipient.
    Note: Requires APP_USER and APP_PASSWORD environment variables for Gmail.
    """
    try:
        # It's better to use environment variables for security
        # However, for this prompt, we'll set up the structure
        sender_email = os.getenv("SENDER_EMAIL")
        app_password = os.getenv("SENDER_PASSWORD") # Gmail App Password
        
        if not sender_email or not app_password:
            print("Email credentials not found in environment variables.")
            return False

        yag = yagmail.SMTP(sender_email, app_password)
        subject = 'Security Alert: Unauthorized Access Detected'
        contents = [
            f"An unauthorized person was detected monitoring your laptop.",
            f"Details: {intruder_info}",
            "This is a silent automated notification."
        ]
        
        yag.send(to=recipient_email, subject=subject, contents=contents)
        print(f"Alert sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
