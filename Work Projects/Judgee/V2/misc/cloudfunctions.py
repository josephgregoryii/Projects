import logging
import boto3
from botocore.exceptions import ClientError
import os

def upload(filename, f):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    s3 = boto3.client('s3')
    s3.upload_fileobj(f, "rate-pics", filename)

def download(filename,expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param filename: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': 'rate-pics',
                                                            'Key': filename},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response
