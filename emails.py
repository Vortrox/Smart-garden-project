from __future__ import print_function

from typing import List

from constants import PROJECT_ROOT

import base64
import logging
import mimetypes
import os
import os.path
from email import encoders
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import constants

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.send"
]


def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_json_path = os.path.join(PROJECT_ROOT, 'token.json')
    if os.path.exists(token_json_path):
        creds = Credentials.from_authorized_user_file(token_json_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.path.join(PROJECT_ROOT, 'google_credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_json_path, 'w') as token:
            token.write(creds.to_json())
    return creds


def create_email(user_email_addr: str, destination_email_addr: str, subject: str, message: str,
               attachment_images: List[str]=None) -> MIMEMultipart:
    if attachment_images is None:
        attachment_images = []

    # Create a MIMEMultipart message object
    email_messages = MIMEMultipart()

    # Set the To, From, Subject, and other headers
    email_messages['To'] = destination_email_addr
    email_messages['From'] = user_email_addr
    email_messages['Subject'] = subject

    # Create a MIMEText object for the email body
    text_part = MIMEText(message, 'plain')
    email_messages.attach(text_part)

    # Attach images as attachments
    for image_file in attachment_images:
        # Create a MIMEImage object for each image attachment
        with open(image_file, 'rb') as file:
            image_data = file.read()

        image_mime_type, _ = mimetypes.guess_type(image_file)
        image_name = os.path.basename(image_file)
        image_part = MIMEImage(image_data, _subtype=image_mime_type)

        # Set the filename for the image attachment
        image_part.add_header('Content-Disposition', 'attachment', filename=image_name)

        # Attach the encoded image data to the MIMEImage object
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        image_part.set_payload(encoded_image)
        encoders.encode_base64(image_part)

        # Add the image attachment to the email
        email_messages.attach(image_part)

    return email_messages


def send_email(user_email_addr: str, destination_email_addr: str, subject: str, message: str,
               attachment_images: List[str]=None) -> dict:
    """Create and send an email message using Google's API"""

    try:
        email_message = create_email(user_email_addr, destination_email_addr, subject, message, attachment_images)

        # Send the email using the Gmail API
        credentials = get_credentials()
        service = build('gmail', 'v1', credentials=credentials)

        request = service.users().messages().send(userId='me',
                                                  body={'raw': base64.urlsafe_b64encode(email_message.as_bytes()).decode()})
        response = request.execute()

        logging.info('Email sent successfully.')
        return response
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return {}


if __name__ == '__main__':
    sent_email = send_email(constants.USER_EMAIL, constants.DESTINATION_EMAIL, "Smart garden: Test email", "The backend system's emailing has been successfully configured")
    pass
