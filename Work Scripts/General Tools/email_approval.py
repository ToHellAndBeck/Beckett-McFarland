import os
import re
import win32com.client
from pathlib import Path

# Configuration
base_destination_folder_path = Path(r"L:\Rollout\97820 WM - Switch-Fiber FYE25 Network Refresh - CJE\Shipping\Leah Approvals")
specific_sender = "Leah.Doyle@walmart.com"

def save_email_attachments(email, destination_folder):
    for attachment in email.Attachments:
        print(f"Saving attachment: {attachment.FileName}")
        attachment.SaveAsFile(str(destination_folder / attachment.FileName))

def main():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 is the index for Inbox
    messages = inbox.Items

    print("Searching through emails...")
    for message in messages:
        print(f"Checking message: {message.Subject}")
        try:
            sender_email = message.SenderEmailAddress.lower()
        except AttributeError:
            print("Cannot get sender's email address. Skipping message.")
            continue

        if specific_sender.lower() in sender_email:
            print(f"Email is from {specific_sender}")
            if "approved" in message.Body.lower():
                print("Email is approved. Processing...")
                match = re.search(r'\d+', message.Subject)
                if match:
                    number_string = match.group()
                    print(f"Found number string in subject: {number_string}")
                    destination_folder = base_destination_folder_path / number_string
                    if destination_folder.exists() and destination_folder.is_dir():
                        print(f"Folder for site {number_string} already exists. Adding email to folder.")
                    else:
                        print(f"Creating new folder for site {number_string}.")
                        os.makedirs(destination_folder, exist_ok=True)
                    save_email_attachments(message, destination_folder)
                else:
                    print(f"No number string found in subject: {message.Subject}")
            else:
                print(f"Email from {message.SenderEmailAddress} with subject '{message.Subject}' does not contain 'approved'.")
        else:
            print(f"Email not from {specific_sender}")

if __name__ == "__main__":
    main()
