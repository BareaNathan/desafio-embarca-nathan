import boto3
import pandas as pd
import os
import io
import chardet

s3_client = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def handler(event, context):
  print(event)

  # filename = event['body']['filename']
  # file_obj = s3_client.get_object(Bucket=bucket_name, Key=filename)

  # csv_content = file_obj['Body'].read()

  csv_content = event['body']['dataFrame']

  # encoding = chardet.detect(csv_content)['encoding']
  # data_stream = io.BytesIO(csv_content)
    
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
  return {
    'statusCode': 200,
    'message': 'Success',
    'body': {
      # # Inclua as informações relevantes para o usuário
      # 'total_deaths': grouped_df['number_deaths'].sum(),  # Total de mortes
      # 'vehicle_deaths': grouped_df.to_dict('records'),  # Detalhes por veículo, data e rua
    }
  }


  # return {
  #   "statusCode": 200,
  #   "message": f"{filename} successfully loaded from S3",
  #   "body": {
  #     "df": 'dataframe'
  #   }
  # }