import boto3
import pandas as pd
import os
import io
import chardet

s3_client = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def handler(event, context):
  print(event)

  csv_content = event['body']['dataFrame']
    
  df = pd.DataFrame(csv_content)
  print(df)

  vehicles = ['automovel', 'bicicleta', 'caminhao', 'moto', 'onibus']

  # df = df[df['mortos'] > 0]
  df.loc(df['mortos'] > 0)
  df = df.sort_values(by=['data'])
  df = df.loc[:, ['data', 'trecho', 'automovel', 'bicicleta', 'caminhao', 'moto', 'onibus', 'mortos']]

  result_df = pd.DataFrame(columns=['created_at', 'road_name', 'vehicle', 'number_deaths'])

  for index, row in df.iterrows():
      created_at = row['data']
      road_name = row['trecho']

      for vehicle in vehicles:
          number_deaths = row[vehicle]

          if number_deaths > 0:
            result_df = pd.concat([result_df, pd.DataFrame([[created_at, road_name, vehicle, number_deaths]], columns=['created_at', 'road_name', 'vehicle', 'number_deaths'])], ignore_index=True)

  result_df = result_df.groupby(['created_at', 'road_name', 'vehicle']).sum().reset_index()

  print(result_df)
  return result_df