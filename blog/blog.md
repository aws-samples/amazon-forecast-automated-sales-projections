# Automate sales projections with Amazon Forecast, QuickSight and AWS Step Functions

In the retail industry, forecasting sales and visitor numbers is an important topic that directly affects your business. Accurate sales forecasting can help you avoid overstocked merchandise and lost sales opportunities: reducing costs and increasing revenue. Accurately predicting the number of visitors will also enable you to efficiently plan employee shifts and provide better customer service.

Even though POS data is available, it might seem daunting to get started applying AI and machine learning to improve forecasts. In this blog, We'll show you how Amazon Forecast, an AI service provided by AWS for time-series forecasting, can be used to make predictions without any machine learning or complex programming experience needed. We'll also go one step further and show how Forecast can be easily integrated with a data pipeline so that updated forecasts can be automatically generated and exported whenever a new batch of data is uploaded to Amazon S3.


## Problem definition

This blog uses sales data from a UK e-commerce company published on the internet to forecast sales for the following week. We will use Amazon Forecast to create sales forecasts, either manually in the GUI or automatically by building a pipeline. The results of the forecast are visualized using Amazon QuickSight, allowing management to get an immediate view of the sales forecast.


## Architecture design

### First Phase: Manual forecasting and visualization

For the initial solution, we'll perform sales forecasting using the AWS Console: importing data to Amazon Forecast, training models, runing forecasts, and exporting the results. We'll then visualize the exported forecasts in Amazon QuickSight.

![arch overview diagram simple](https://user-images.githubusercontent.com/27226946/89359516-0100f300-d701-11ea-8bf0-f4fbe3204119.png)


### Second Phase: Automatic forecasting with AWS Step Functions and AWS Lambda

Next, we'll set up a pipeline powered by AWS Step Functions and AWS Lambda: Automating the manual steps. New data uploaded to Amazon S3 will automatically be imported and analyzed - creating forecasts ready to be visualized in Amazon QuickSight.

![arch overview diagram pipeline](https://user-images.githubusercontent.com/27226946/89359520-02cab680-d701-11ea-979c-c1f35cb07292.png)


## Getting started

**TODO: instructions on initial setup e.g. CF template, instance?**

First, follow through the first notebook [1_prepare_dataset.ipynb](1_prepare_dataset.ipynb) - downloading data and preparing the target variable (sales). In the notebook you'll prepare an initial training data set from 2009/12/01 to 2010/12/02, and an additional dataset from 2009/12/01 to 2010/12/09. At the end, both will be uploaded to Amazon S3.


## Using Amazon Forecast through the Console GUI

Once we have stored the training data in S3, we can go to the Amazon Forecast console and create the dataset.

### Step 1: Import the dataset

Enter the name of the dataset group (`retail_uk_sales_prediction`), select **Retail** as the domain and click Next.

![Create dataset group screen](https://user-images.githubusercontent.com/27226946/89359522-03fbe380-d701-11ea-8ffd-9d0ffbd0290d.png)

Enter a name for the dataset (`uk_sales`) and select **day** as the forecast unit, leave the Data schema as default and click Next.

![Create target time series dataset screen](https://user-images.githubusercontent.com/27226946/89359523-04947a00-d701-11ea-86e0-15d5768a08db.png)

Enter Dataset Import name (`uk_sales_2009120101_20101202`) and create a new IAM Role. In the Data location field, enter the S3 path of the training data that you uploaded in the data preparation notebook and click Create.

![Import target time series data screen](https://user-images.githubusercontent.com/27226946/89359527-052d1080-d701-11ea-83c4-e1c751041a77.png)

Wait until the target time series data becomes active before moving on to the next step.

![Forecast dashboard screen](https://user-images.githubusercontent.com/27226946/89359528-05c5a700-d701-11ea-9e49-3ed2cd399bc8.png)


### Step 2: Build a predictor with AutoML

Click the **Start** button under *Predictor training*. Name your predictor and set the time period you want to forecast (the *Forecast Horizon*) to `7`. You may want to use the calendar information built into Amazon Forecast for a potentially more accurate forecast: Select United Kingdom as the *Country for holidays - optional*. Leave other options as default and click **Create**.

![Train predictor screen](https://user-images.githubusercontent.com/27226946/89359529-05c5a700-d701-11ea-9e7a-eff879bb6bae.png)

Amazon Forecast will now begin training models on your imported data. After some time, *Predictor training* status will update to **Active** indicating the training is complete. Click **View** in *Predictor training* to explore the training results.

![Forecast dashboard screen](https://user-images.githubusercontent.com/27226946/89359532-065e3d80-d701-11ea-8ab5-c1a6cde65d99.png)


### Step 3: Evaluate the model

AutoML results will show which algorithm was selected as the best for your dataset, along with metrics describing the best performance on the training data. In our example below, `Deep_AR_Plus` was the most accurate algorithm reaching an average error of 14.23%:

![Predictor details screen](https://user-images.githubusercontent.com/27226946/89359534-065e3d80-d701-11ea-9497-275cfe7d9e9b.png)

To generate a prediction, click **Create a Forecast**.


### Step 4: Create a forecast

Enter a forecast name and choose the Predictor you just trained. Click **Create a forecast**.

![Create a forecast screen](https://user-images.githubusercontent.com/27226946/89359535-06f6d400-d701-11ea-845d-89c759fa7a9f.png)

Once the forecast is generated after a short period of time, review the details.


### Step 5: Export the forecast

Forecasts can be queried through the Amazon Forecast API in real time, or exported to Amazon S3 which is what we'll do here. To get started, click the **Create forecast export** button to the right of *Exports*.

![Forecast details screen](https://user-images.githubusercontent.com/27226946/89359537-078f6a80-d701-11ea-9701-a703502ca9e5.png)

Enter an *Export name* and specify the *Generated forecast* you just created. Specify where you want to export the forecast results to in Amazon S3, and click **Create forecast export**.

![Create forecast export screen](https://user-images.githubusercontent.com/27226946/89359538-078f6a80-d701-11ea-8f8c-915adb7f9fd7.png)

The export process will appear in the Amazon Forecast console, and take a short period of time to complete:

![Forecast details screen](https://user-images.githubusercontent.com/27226946/89359539-08280100-d701-11ea-9ce5-24e04fc96ade.png)

Once the export is done, you'll be able to access the prediction results at the location you specified in Amazon S3.

![S3 Console screen](https://user-images.githubusercontent.com/27226946/89359540-08c09780-d701-11ea-8376-9fc21cd40164.png)


### Step 6: Visualize in Amazon QuickSight

Let's visualize the prediction results exported to S3 in Amazon QuickSight. First, click **Add or remove QuickSight access to AWS services** from *Security & permissions* to allow the file to be read from S3.

![QuickSight security screen](https://user-images.githubusercontent.com/27226946/89359541-08c09780-d701-11ea-92f6-3183fc2ca187.png)

Select the S3 bucket to which you exported the predictions and check the *Write permission for Athena Workgroup* box. You have now completed your preconfiguration.

![QuickSight select buckets screen](https://user-images.githubusercontent.com/27226946/89359543-09592e00-d701-11ea-8b3d-25538c7a1cff.png)

Load the data and visualize it. Click **New analysis** on the top page.

![QuickSight home screen](https://user-images.githubusercontent.com/27226946/89359544-09592e00-d701-11ea-97a4-84644d21e73d.png)

Select **S3** as the data set source.

![QuickSight create data set screen](https://user-images.githubusercontent.com/27226946/89359545-09f1c480-d701-11ea-83c5-812eec305287.png)

**TODO: Not clear, broken?**

Name your Data source to specify a manifest file for S3 loading. The manifest file is created when the notebook is executed and uploaded to S3.

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/manifest_for_quicksight/manifest_uk_sales_pred.json


![QuickSight new S3 data source screen](https://user-images.githubusercontent.com/27226946/89359546-0a8a5b00-d701-11ea-8d8a-c3b8dd12b1dd.png)

When the data is loaded into SPICE, click Visualize.

![QuickSight finish data set creation screen](https://user-images.githubusercontent.com/27226946/89359547-0a8a5b00-d701-11ea-819f-f4bf2010965d.png)

Select the **line graph** visual type.

![QuickSight Visualize screen](https://user-images.githubusercontent.com/27226946/89359548-0b22f180-d701-11ea-8229-13590e2f63b0.png)

Select `date` for *X axis* and three series `p10(sum)`, `p50(sum)` and `p90(sum)` for *Value*. You can now visualize.

![QuickSight rendered line graph](https://user-images.githubusercontent.com/27226946/89359549-0bbb8800-d701-11ea-9e5d-ff1859058533.png)

For simplicity we loaded the S3 data directly, but you can also use Amazon Athena if you want to process it in advance with queries.


## Automating forecasts with AWS Step Functions and AWS Lambda Lambda trigger - lambda job to trigger retrain and report building when new data posted to s3

Next, we'll leverage AWS Lambda and AWS Step Functions to build a pipeline. Uploading data input to S3 triggers an AWS Step Functions *state machine*. The state machine defines the flow of steps in the pipeline, using AWS Lambda functions to import data into Amazon Forecast and then create and export forecasts.

![arch overview diagram pipeline](https://user-images.githubusercontent.com/27226946/89359550-0bbb8800-d701-11ea-82f1-7e8ec30952f6.png)

Run the second notebook [2_building_pipeline.ipynb](2_building_pipeline.ipynb) to set up the pipeline and upload sample data to Amazon S3.


### Step 1: create Lambda functions

Using boto3, we will create functions to import data from Amazon Forecast, create a predictor, forecast, and export the forecast results. We will also create a function to get the status of each job.


### Step 2: create Step Functions state machine

StepFunctions proceeds by issuing a job, checking the status of the job, waiting if it is not completed, and moving on to the next job when it is completed.

![State machine diagram](https://user-images.githubusercontent.com/27226946/89359551-0c541e80-d701-11ea-93f1-404066bf3fcd.png)


### Step 3: Cloud Trail and Cloud Watch Events

Configure Cloud Trail and CloudWatch to run Step Functions when the files are stored in S3. The Step Functions developer's guide is helpful.

https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-cloudwatch-events-s3.html


### Step 4: put additional data and visualize

The Step Functions pipeline is executed as a data put and trigger to S3. It takes a bit of time for it to run to the end. Once the job is completed, the results are stored in S3. When we check the predictor with the additional data, Deep_AR-Plus is selected, with a margin of error of 8.14%.

![Predictor detail screen](https://user-images.githubusercontent.com/27226946/89359552-0cecb500-d701-11ea-8e29-93bee36a2cae.png)


### Step 5: Visualize with QuickSight

The same steps as in the first half of this section can be used to visualize

![QuickSight forecast visualization](https://user-images.githubusercontent.com/27226946/89359553-0cecb500-d701-11ea-83e5-e618ca164fa5.png)



## Conclusion

Time series forecasting has a lot of opportunities to be used in various aspects of business and can make your business bigger. As I have explained, you can easily verify it from the GUI, so why not give it a try first? When it comes to actually integrating it into your business processes, you can easily configure an automated pipeline using AWS Step Functions and AWS Lambda. Why not try it out with your existing data first?

We have covered 4 big scenarios to handle timeseres data. You can find other posts below:

- Introduction to time series forecasting with SageMaker and Python by Eric Greene
- Benchmarking popular time series forecasting algorithms on electricity demand forecast by Yin Song
- Anomaly Detection of timeseries by Seongmoon Kang
