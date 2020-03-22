#!/usr/bin/python3.6

import boto3
from botocore.exceptions import ClientError
from slackbot_v2 import config


def auto_mail(receive, company, password):
    # Replace sender@example.com with your "From" address. This address must be verified with Amazon SES.
    SENDER = config.SENDER
    
    # Replace recipient@example.com with a "To" address.
    # If your account is still in the sandbox, this address must be verified.
    RECIPIENT = f"receiver Name <{receive}>"
    
    # Specify a configuration set. If you do not want to use a configuration set,
    # comment the following variable, and the ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = "ConfigSet"
    
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = config.AWS_REGION
    
    # The subject line for the email.
    SUBJECT = "welcome to Terasky SFTP!"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )
                
    # The HTML body of the email.
    BODY_HTML = f"""<html>
    <head></head>
    <body>
      <h1>SFTP details:</h1>
      <p>IP Address: 34.192.3.121<br> Username: {company}<br> Password: {password} </p>
    </body>
    </html>
                """
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set,
            # comment or delete the following line ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def lambda_handler(event, lambda_context):
    receive = event['receive']
    company = event['company']
    password = event['password']
    auto_mail(receive, company, password)

