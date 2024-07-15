import boto3
import pandas as pd
import os

s3_client = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def handler(event, context):
  print(event)

  filename = event['filename']
  file = s3_client.get_object(Bucket=bucket_name, Key=filename)
  if not file: return {"status": "failure", "message": "Unable to get file from S3 Bucket"}

  df = pd.read_csv(file['Body'])
  return {
    "statusCode": "success",
    "body": df
  }