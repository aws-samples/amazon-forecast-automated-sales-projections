def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    response = forecast.create_forecast(
        ForecastName=event['detail']['requestParameters']['key'].replace('input/','').replace('.csv',''),
        PredictorArn=event['PredictorArn'],
    )
    
    event['ForecastArn'] = response['ForecastArn']
    return event