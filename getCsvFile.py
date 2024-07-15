import requests
import json
import boto3
import os

s3_client = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def handler(event, context):
  print(event)

  url = event['url']
  filename = url.split('/')[-1]

  response = requests.get(url)
  data = response.content

  s3_client.put_object(Bucket=bucket_name, Key=filename, Body=data)

  return {
    "statusCode": 200,
    "message": f"{filename} Sucessfully saved in S3",
    "body": {
      "filename": f"{filename}"
    }
  }