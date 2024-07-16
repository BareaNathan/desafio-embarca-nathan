import requests
import boto3
import os
import chardet
import io
import pandas as pd

s3_client = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def handler(event, context):
  print(event)

  url = event['url']
  filename = url.split('/')[-1]

  response = requests.get(url)
  data = response.content

  s3_client.put_object(Bucket=bucket_name, Key=filename, Body=data)

  encoding = chardet.detect(data)['encoding']

  # Carregue o conteúdo do CSV em um DataFrame
  data_stream = io.BytesIO(data)
  df = pd.read_csv(data_stream, encoding=encoding)

  return {
    "statusCode": 200,
    "message": f"{filename} sucessfully saved in S3",
    "body": {
      "filename": f"{filename}",
      "dataFrame": df.to_dict('records')
    }
  }