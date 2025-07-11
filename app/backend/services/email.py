import os
import boto3


def send_email(to_address: str, subject: str, body: str) -> None:
    """Send an email via AWS SES."""
    from_address = os.getenv("SES_FROM_ADDRESS")
    region = os.getenv("AWS_REGION", "us-east-1")
    if not from_address:
        raise ValueError("SES_FROM_ADDRESS not set")

    client = boto3.client("ses", region_name=region)
    client.send_email(
        Source=from_address,
        Destination={"ToAddresses": [to_address]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}},
        },
    )