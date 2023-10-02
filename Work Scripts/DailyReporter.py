import imaplib
import email
import os
from openpyxl import load_workbook

# Email account credentials and server settings
IMAP_SERVER = 'imap.wachter.com'
EMAIL = 'beckett.mcfarland@wachter.com'
PASSWORD = 'Summer2023'

# Folder to save the Excel attachment
SAVE_FOLDER = r"C:\Users\beckett.mcfarland\Documents\output_excel_files"

def download_excel_attachment(msg):
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart' and part.get('Content-Disposition') is None:
            continue

        if part.get('Content-Disposition') and 'excel' in part.get_filename().lower():
            filename = part.get_filename()
            filepath = os.path.join(SAVE_FOLDER, filename)
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))
            return filepath

def check_emails():
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')

        # Search for emails from a specific sender with "master switch report" in the subject
        result, data = mail.search(None, '(FROM "CJ.Ewell@wachter.com")', '(SUBJECT "master switch report")')

        # Get the list of email IDs
        email_ids = data[0].split()
        
        # Process only the most recent eligible email
        for email_id in email_ids[:1]:
            result, message_data = mail.fetch(email_id, '(RFC822)')
            raw_email = message_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Download the Excel attachment
            excel_filepath = download_excel_attachment(msg)
            if excel_filepath:
                print(f"Excel file saved at: {excel_filepath}")
                break  # Break the loop after processing the first eligible email

        # Logout and close the connection
        mail.logout()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    check_emails()
