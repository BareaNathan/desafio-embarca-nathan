def handler(event, context):
  print(event)

  return {
    "message": "hello from lambda 1"
  }