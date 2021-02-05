def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    responce = forecast.create_predictor(
        PredictorName=event['detail']['requestParameters']['key'].replace('input/','').replace('.csv',''),
        AlgorithmArn='arn:aws:forecast:::algorithm/Prophet',
        ForecastHorizon=7,
        PerformAutoML=False,
        PerformHPO=False,
        EvaluationParameters={
            'NumberOfBacktestWindows': 1,
            'BackTestWindowOffset': 7
        },
        InputDataConfig={
            #'DatasetGroupArn': 'arn:aws:forecast:' + event['region'] + ':' + event['account'] + ':dataset-group/demo_timeseries_retail',
            'DatasetGroupArn': event['DatasetGroupArn'],
            'SupplementaryFeatures': [
                {
                    'Name': 'holiday',
                    'Value': 'UK'
                },
            ]
        },
        FeaturizationConfig={
            'ForecastFrequency': 'D',
            'Featurizations': [
                {
                    'AttributeName': 'demand',
                },
            ]
        },
    )
    
    event['PredictorArn'] = responce['PredictorArn']
    return event
