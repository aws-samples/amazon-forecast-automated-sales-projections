def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    #try:
    #    forecast.describe_dataset_group(
    #        DatasetGroupArn='arn:aws:forecast:' + event['region'] + ':' + event['account'] + ':dataset-group/demo_timeseries_retail'
    #    )
    #except:
    response = forecast.create_dataset_group(
        DatasetGroupName='workshop_timeseries_retail',
        Domain='RETAIL',
    )
    event['DatasetGroupArn'] = response['DatasetGroupArn']
    
    return event