# Introduction

在零售行业，预测销售额和访客人数是直接影响您业务的一个重要话题。准确的销售预测可帮助您避免库存过多的商品、失去销售机会并实现更多业务。准确预测访客人数还可让您正确规划员工班次，并将信息用作预测销售额的帮助。另一方面，虽然 POS 数据存储在系统上，但很多人认为，可能很难利用 AI 和机器学习。在本博客中，我将向您展示 Amazon Forecse（AWS 提供的用于时间序列预测的 AI 服务）如何用于预测，而无需编程困难或其他任何其他任何内容。我们还将进一步解释如何通过每日批次轻松系统地实现它。通过系统化，您只需将数据传送到名为 S3 的存储中，执行数据管道，并且预测结果可以输出到 S3。


# Problem definition

本博客使用英国电子商务公司在互联网上公布的销售数据来预测下周的销售额。我们将使用亚马逊预测进行销售预测，可以在 GUI 中手动或通过构建管道自动进行销售预测。使用 Amazon QuickSight 可视化预测结果，使管理层能够立即查看销售预测。


# Architecture design



## first : manual forecasting and visualization

第一步是通过操作控制台执行销售预测。在控制台中，您可以在 Amazon 预测中导入数据、培训预测员、运行预测并导出预测结果。然后，导出的预测结果将在 Amazon QuickSight 中可视化。

![01_arch_design_1](https://user-images.githubusercontent.com/27226946/89359516-0100f300-d701-11ea-8bf0-f4fbe3204119.png)


## second : auto forecasting with AWS Step Functions and AWS Lambda

由数据上传到 S3 触发，它会自动导入数据、学习预测变量、执行预测和导出预测结果，所有这些都通过手动执行完成。管道使用 AWS Lambda 和 AWS 步骤信息进行配置。使用亚马逊 QuickSight 可视化输出预测结果。

![01_arch_design_2](https://user-images.githubusercontent.com/27226946/89359520-02cab680-d701-11ea-979c-c1f35cb07292.png)


# Data - Download data - Data analysis (see missing data etc.)

运行 1_prepare_dataset.ipynb 下载数据并计算销售额作为目标变量。准备从 2009/12 年 12 月至 2010 年 12 月期间的数据作为培训数据，并将其上传到第三阶段。作为其他培训数据，我们将从 2009/12 月 1 日至 09 年 12 月 12 日期间的数据上传到中等数据。

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/1_prepare_dataset.ipynb



# Forecast - import dataset - AutoML - Evaluation

一旦我们将培训数据存储在 S3 中，我们就可以转到 Amazon 预测控制台并创建数据集。

## Step 1: Import dataset

输入数据集组的名称（retail_uk_sales_predictin），选择 “零售” 作为域，然后单击 “下一步”。


![02_import_1](https://user-images.githubusercontent.com/27226946/89359522-03fbe380-d701-11ea-8ffd-9d0ffbd0290d.png)

输入数据集的名称 (uk_sales)，然后选择日期作为预测单位，保持数据方案不变，然后单击下一步。

![02_import_2](https://user-images.githubusercontent.com/27226946/89359523-04947a00-d701-11ea-86e0-15d5768a08db.png)

输入数据集导入名称（uk_sales_2009120101_20101202），然后创建一个新的 IAM 角色。在 “数据位置” 字段中，输入您在上一次准备过程中存储的训练数据的 S3 路径，然后单击 “创建”。

![02_import_3](https://user-images.githubusercontent.com/27226946/89359527-052d1080-d701-11ea-83c4-e1c751041a77.png)

等待目标时间序列数据变为活动状态。接下来，我们训练预测器。

![02_import_4](https://user-images.githubusercontent.com/27226946/89359528-05c5a700-d701-11ea-9e49-3ed2cd399bc8.png)


## Step 2: Build predictor with AutoML

单击 “开始” 进行预测变量训练。输入预测变量名称，然后在 “预测” 展望期中输入 7（您要预测的期间）。您可能希望使用亚马逊预测中内置的日历信息来获得更准确的预测。选择英国作为假期的国家/地区-可选，然后单击创建。

![03_predictor_1](https://user-images.githubusercontent.com/27226946/89359529-05c5a700-d701-11ea-9e7a-eff879bb6bae.png)

培训将开始。短时间后，训练完成，你会看到 “预测器” 训练中的 “酸性” 一词。单击 “预测变量” 训练中的 “查看” 以查看训练结果。

![03_predictor_2](https://user-images.githubusercontent.com/27226946/89359532-065e3d80-d701-11ea-8ab5-c1a6cde65d99.png)



## Step 3: Evaluation

自动化结果表明，选择深度 AR_Plus 作为算法，误差为 14.23%。

![03_predictor_3](https://user-images.githubusercontent.com/27226946/89359534-065e3d80-d701-11ea-9497-275cfe7d9e9b.png)

接下来，生成预测并单击创建预测。


## Step 4: Create a forecast

输入预测名称，然后选择您刚刚学到的预测变量名称。单击创建预测。

![04_forecast_1](https://user-images.githubusercontent.com/27226946/89359535-06f6d400-d701-11ea-845d-89c759fa7a9f.png)

生成预测后，复查详细信息。


## Step 5: Export forecast

将预测结果导出到 S3，然后单击 “导出” 右侧的 “创建预测导出”。

![05_export_1](https://user-images.githubusercontent.com/27226946/89359537-078f6a80-d701-11ea-9701-a703502ca9e5.png)

输入导出名称并指定已生成的预测。指定要将预测结果导出到 S3 的位置，然后单击创建预测导出。

![05_export_2](https://user-images.githubusercontent.com/27226946/89359538-078f6a80-d701-11ea-8f8c-915adb7f9fd7.png)
![05_export_3](https://user-images.githubusercontent.com/27226946/89359539-08280100-d701-11ea-9ce5-24e04fc96ade.png)


预测值已导出到指定的 S3 路径。

![05_export_4](https://user-images.githubusercontent.com/27226946/89359540-08c09780-d701-11ea-8376-9fc21cd40164.png)


## Step 6: Visualization by QuickSight

让我们可视化在 Amazon QuickSight 中导出到 S3 的预测结果。首先，单击 “安全和权限” 中添加或删除对 AWS 服务的 QuickSight 访问权限，以允许从 S3 读取文件。


![06_quicksight_1](https://user-images.githubusercontent.com/27226946/89359541-08c09780-d701-11ea-92f6-3183fc2ca187.png)

选择将预测导出到的 S3 存储桶，然后选中 Athena 工作组的写入权限框。您现在已完成预配置。

![06_quicksight_2](https://user-images.githubusercontent.com/27226946/89359543-09592e00-d701-11ea-8b3d-25538c7a1cff.png)

加载数据并将其可视化。单击首页上的 “新建分析”。

![06_quicksight_3](https://user-images.githubusercontent.com/27226946/89359544-09592e00-d701-11ea-97a4-84644d21e73d.png)

选择 S3。

![06_quicksight_4](https://user-images.githubusercontent.com/27226946/89359545-09f1c480-d701-11ea-83c5-812eec305287.png)

在数据源名称中输入任意值，以指定用于 S3 加载的清单文件。清单文件是在执行笔记本并上传到 S3 时创建的。

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/manifest_for_quicksight/manifest_uk_sales_pred.json


![06_quicksight_5](https://user-images.githubusercontent.com/27226946/89359546-0a8a5b00-d701-11ea-8d8a-c3b8dd12b1dd.png)

将数据加载到 SPICE 中时，单击可视化。

![06_quicksight_6](https://user-images.githubusercontent.com/27226946/89359547-0a8a5b00-d701-11ea-819f-f4bf2010965d.png)

选择折线图并为 X 轴选择日期，为值选择 p10（sum）、p50（sum）和 p90（sum）。您现在可以可视化。

![06_quicksight_7](https://user-images.githubusercontent.com/27226946/89359548-0b22f180-d701-11ea-8229-13590e2f63b0.png)
![06_quicksight_8](https://user-images.githubusercontent.com/27226946/89359549-0bbb8800-d701-11ea-9e5d-ff1859058533.png)

为了简单起见，我们直接加载 S3 数据，但如果您想提前处理查询，您也可以使用 Amazon Athena。


# Lambda trigger - lambda job to trigger retrain and report building when new data posted to s3

接下来，我们将利用 AWS Lambda 和 AWS 步骤函数构建管道。AWS 步骤函数由 S3 的数据输入触发，后者会自动从 Amazon 预测导入数据、构建预测器、预测并导出结果。


![07_arch](https://user-images.githubusercontent.com/27226946/89359550-0bbb8800-d701-11ea-82f1-7e8ec30952f6.png)

在 2_building_pipeline.ipynb 中运行笔记本以构建管道并将数据上传到 S3。

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/2_building_pipeline.ipynb


## Step 1: create Lambda functions

使用 boto3，我们将创建从 Amazon 预测导入数据、创建预测变量、预测和导出预测结果的函数。我们还将创建一个函数来获取每个作业的状态。

## Step 2: create Step Functions state machine

步骤函数通过发出作业、检查作业状态、等待作业是否未完成，然后在完成后转到下一作业。

![08_stepfunctions](https://user-images.githubusercontent.com/27226946/89359551-0c541e80-d701-11ea-93f1-404066bf3fcd.png)


## Step 3: Cloud Trail and Cloud Watch Events

将云跟踪和 CloudWatch 配置为在文件存储在 S3 中时运行步骤功能。步骤函数开发人员指南很有帮助。

https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-cloudwatch-events-s3.html


## Step 4: put additional data and visualize

步骤函数管道作为数据放置和触发到 S3 执行。它需要一些时间才能运行到最后。作业完成后，结果将存储在 S3 中。当我们使用附加数据检查预测变量时，选择 Deep_AR-plus，误差边距为 8.14%。


![09_predictor](https://user-images.githubusercontent.com/27226946/89359552-0cecb500-d701-11ea-8e29-93bee36a2cae.png)


## Step 5: Visualize with QuickSight

本节前半部分中的相同步骤可用于显示

![10_quicksight](https://user-images.githubusercontent.com/27226946/89359553-0cecb500-d701-11ea-83e5-e618ca164fa5.png)



# Conclusion
时间序列预测有很多机会可用于业务的各个方面，并可以让您的业务更大。正如我所解释的那样，你可以轻松地从 GUI 验证它，那么为什么不先试一试呢？在将其实际集成到业务流程中时，您可以使用 AWS Step 函数和 AWS Lambda 轻松配置自动化管道。为什么不先尝试使用现有数据？

我们已经涵盖了 4 个大场景来处理时间表数据。你可以在下面找到其他帖子:

* Introduction to time series forecasting with SageMaker and Python by Eric Greene
* Benchmarking popular time series forecasting algorithms on electricity demand forecast by Yin Song
* Anomaly Detection of timeseries by Seongmoon Kang


