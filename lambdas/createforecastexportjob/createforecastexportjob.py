def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    response = forecast.create_forecast_export_job(
        ForecastExportJobName=event['detail']['requestParameters']['key'].replace('input/','').replace('.csv',''),
        ForecastArn=event['ForecastArn'],
        Destination={
            'S3Config': {
                'Path': 's3://' + event['detail']['requestParameters']['bucketName'] + '/output',
                'RoleArn': event['detail']['userIdentity']['sessionContext']['sessionIssuer']['arn'],
            }
        },
    )
    
    event['ForecastExportJobArn'] = response['ForecastExportJobArn']
    return event