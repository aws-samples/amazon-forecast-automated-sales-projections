1. Deploy the solution stack (incl. notebook instance and most of pipeline:S3 bucket, Lambda functions, cloud trail, cloud watch events)
2. Open the notebook instance and run through data prep NB
3. *Build SFn by NB with explanation about pipeline. (focusing point of this session)*
4. Upload some data to S3 (via NB or manual) and check that the pipeline works properly creating new forecasts each time(with skipping movie)


Click here to provision the **project stack**: [![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://us-east-1.console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=timeseriesblog3&templateURL=https://time-series-blog.s3.amazonaws.com/template.yaml)
