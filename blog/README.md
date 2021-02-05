# Automate sales projections with Amazon Forecast, QuickSight and AWS Step Functions

Accurate demand forecasting has the potential to make a huge impact on your business: For example optimizing stocked inventory, avoiding lost revenue opportunities due to stock-out, and planning efficient employee shifts that serve your customers better.

In this example, we show how to build an automated, serverless pipeline to generate forecasts as new data batches become available - and then visualize the results in an Amazon QuickSight dashboard.

We'll model the [Online Retail II Data Set](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II#) from the public [UC Irvine Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php) - recording just over 1 million transactions from a UK-based online retail company.


## The AWS Well-Architected Framework (Machine Learning Lens)

This module applies principles from the [Machine Learning Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/welcome.html) ([PDF](https://d1.awsstatic.com/whitepapers/architecture/wellarchitected-Machine-Learning-Lens.pdf)) of the [AWS Well-Architected](https://d1.awsstatic.com/whitepapers/architecture/wellarchitected-Machine-Learning-Lens.pdf) framework.

In particular noting from the [Operational Excellence Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/evolve.html) section (PDF p43):

> **Additional Training Data:** AWS supports mechanisms for automatically triggering retraining based on new data PUT to an Amazon S3 bucket. The preferred method to initiate a controlled execution of model retraining is to set up an ML pipeline that includes an event trigger based on changes to a source Amazon S3 bucket. To detect the presence of new training data in an S3 bucket, CloudTrail combined with CloudWatch Events allows you to trigger an AWS Lambda function or AWS Step Functions workflow to initiate retraining tasks in your training pipeline. The following figure illustrates the practice showing AWS CodePipeline with ML Services: 
This module is based on Well-Architected Machine Learning Lends


## Architecture overview

![01_arch_design_2](https://user-images.githubusercontent.com/27226946/89359520-02cab680-d701-11ea-979c-c1f35cb07292.png)


### AWS services used

* Amazon Forecast
* Amazon QuickSight
* Amazon S3
* AWS Lambda
* AWS Step Functions


## Visualisations

* Screen Shots of forecast console during data import, training and evaluation
* Screen shots of creating QuickSight report
* Architecture diagram


## Blog Outline

1. Introduction
2. Problem definition
3. Architecture design
4. Data    - Download data   - Data analysis (see missing data etc.)
5. Forecast   - import dataset    - AutoML and HPO   - Evaluation
6. QuickSight - Build report
7. Lambda trigger   - lambda job to trigger retrain and report building when new data posted to s3
8. Conclusion   - Other resources   - Intro next blog post in series


## Reference

* [AWS Well-Architected Framework – Machine Learning Lens](https://d1.awsstatic.com/whitepapers/architecture/wellarchitected-Machine-Learning-Lens.pdf)
* (AWS ML Blog) [Automated and continuous deployment of Amazon SageMaker models with AWS Step Functions](https://aws.amazon.com/blogs/machine-learning/automated-and-continuous-deployment-of-amazon-sagemaker-models-with-aws-step-functions/)
* (AWS Step Functions Developer Guide) [Manage Amazon SageMaker with Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html)
* (AWS ML Blog) [Automating your Amazon Forecast workflow with Lambda, Step Functions, and CloudWatch Events rule](https://aws.amazon.com/blogs/machine-learning/automating-your-amazon-forecast-workflow-with-lambda-step-functions-and-cloudwatch-events-rule/)
* (AWS ML Blog) [Building AI-powered forecasting automation with Amazon Forecast by applying MLOps](https://aws.amazon.com/blogs/machine-learning/building-ai-powered-forecasting-automation-with-amazon-forecast-by-applying-mlops/)
* (AWS Step Functions Developer Guide) [Starting a State Machine Execution in Response to Amazon S3 Events](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-cloudwatch-events-s3.html)
* (Amazon QuickSight User Guide) [Creating a Dataset Using Amazon S3 Files](https://docs.aws.amazon.com/quicksight/latest/user/create-a-data-set-s3.html)
* (AWS Samples) [Forecast Visualization Automation Blog](https://github.com/aws-samples/amazon-forecast-samples/tree/master/ml_ops/visualization_blog)
* (AWS ML Blog) [Analyzing contact center calls—Part 1: Use Amazon Transcribe and Amazon Comprehend to analyze customer sentiment](https://aws.amazon.com/blogs/machine-learning/analyzing-contact-center-calls-part-1-use-amazon-transcribe-and-amazon-comprehend-to-analyze-customer-sentiment/)
