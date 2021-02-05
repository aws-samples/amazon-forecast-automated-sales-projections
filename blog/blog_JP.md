# はじめに

小売業において、売り上げの予測や来客数の予測はビジネスに直結する重要なテーマです。
売り上げを正確に予測することで、商品の過剰在庫や、販売機会の損失を回避し、より大きなビジネスを達成することができます。
来客数を正確に予測することで、従業員のシフト計画を適切に作成したり、売り上げ予測のための補助情報として利用することも可能になります。
一方で、POSデータはシステム上に保管されているものの、AIや機械学習を活用するのは難しそうだと思われている方も多いのではないのでしょうか？
本ブログでは、AWSが提供する時系列予測のためのAIサービスである Amazon Forecast を利用することで、難しいプログラミングなどは使わずに予測ができることをご紹介します。
また、一歩進んだ内容として、日次バッチなどでシステム化をする場合も簡単に実装できることをご説明します。
システム化することで、S3というストレージにデータを投入するだけで、データパイプラインが実行され、予測結果をS3に出力することが可能になります。


# 実施すること

本ブログでは、インターネットで公開されているイギリスのEC会社の売り上げデータを用いて、翌一週間の売り上げ予測を行います。
Amazon Forecast を用いて売り上げ予測を行いますが、GUIでの手動実行と、パイプライン構築による自動実行を行います。
予測の結果は Amazon QuickSight を用いて可視化することで、経営者が売り上げの見通しを即座に把握することができるようにします。


# アーキテクチャ

## Amazon Forecast の手動実行

まずは、コンソールの操作によって売り上げ予測を行います。コンソール上では、Amazon Forecast でのデータインポート、予測子の学習、予測の実行、予測結果のエクスポートを行います。
エクスポートされた予測結果は、Amazon QuickSight にて可視化を行います。

![01_arch_design_1](https://user-images.githubusercontent.com/27226946/89359516-0100f300-d701-11ea-8bf0-f4fbe3204119.png)



## パイプライン構築による、Amazon Forecast の自動実行

S3へのデータアップロードをトリガーとして、手動実行で行なったデータのインポート、予測子の学習、予測の実行、予測結果のエクスポートを自動で実施します。
パイプラインは AWS Lambda と AWS Step Funcions を用いて構成します。
出力された予測結果は、Amazon QuickSight を用いて可視化します。

![01_arch_design_2](https://user-images.githubusercontent.com/27226946/89359520-02cab680-d701-11ea-979c-c1f35cb07292.png)


# 前準備 データのダウンロード、整形、S3へのアップロード

1_prepare_dataset.ipynb を実行します。
データのダウンロードと目的変数となる売り上げを算出します。
学習データとして 2009/12/01 から 2010/12/02 までのデータを準備し、S3にアップロードします。
また、追加の学習データとして、2009/12/01 から 2010/12/09 までのデータをS3にアップロードします。

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/1_prepare_dataset.ipynb


# Amazon Forecast の手動実行 - import dataset - AutoML - Evaluation

S3に学習データを格納したら、Amazon Forecastのコンソールに移動して、データセットの作成をしていきます。

## Step 1: Import dataset

データセットグループの名前(retail_uk_sales_predictin)を入力し、ドメインはRetailを選択し、Nextをクリックします。

![02_import_1](https://user-images.githubusercontent.com/27226946/89359522-03fbe380-d701-11ea-8ffd-9d0ffbd0290d.png)

データセットの名前(uk_sales)を入力し、予測単位でdayを選択します。Data schemaはそのままにして、Nextをクリックします。

![02_import_2](https://user-images.githubusercontent.com/27226946/89359523-04947a00-d701-11ea-86e0-15d5768a08db.png)

Dataset Import nameを入力(uk_sales_20091201_20101202)し、IAM Roleを新しく作成します。
Data locationに、前準備にて格納した学習データのS3パスを入力し、Createをクリックします。

![02_import_3](https://user-images.githubusercontent.com/27226946/89359527-052d1080-d701-11ea-83c4-e1c751041a77.png)

Target time series data が Active になるまで待ちます。次に、predictorのtrainingを行います。

![02_import_4](https://user-images.githubusercontent.com/27226946/89359528-05c5a700-d701-11ea-9e49-3ed2cd399bc8.png)


## Step 2: Build predictor with AutoML

Predictor training の Start をクリックします。
Predictor nameを入力し、 Forecast horizonに予測したい期間である7を入力します。
Amazon Forecast に組み込まれているカレンダー情報を使うことで、より精度の高い予測ができる可能性があります。
Country for holidays - optional に United Kingdom を選択します。Create をクリックします。

![03_predictor_1](https://user-images.githubusercontent.com/27226946/89359529-05c5a700-d701-11ea-9e7a-eff879bb6bae.png)

学習が開始されます。しばらく待つと学習が完了し、Predictor trainingにAcitiveと表示されるようになります。
Predictor training の View をクリックし、学習結果を見てみましょう。

![03_predictor_2](https://user-images.githubusercontent.com/27226946/89359532-065e3d80-d701-11ea-8ab5-c1a6cde65d99.png)


## Step 3: Evaluation

AutoMLの結果、アルゴリズムにはDeep_AR_Plusが選択され、誤差は14.23%であることがわかります。

![03_predictor_3](https://user-images.githubusercontent.com/27226946/89359534-065e3d80-d701-11ea-9497-275cfe7d9e9b.png)

次に、予測値を生成します。Create a Forecast をクリックします。


## Step 4: Create a forecast

Forecast nameを入力し、Predictorには先ほど学習したものを選びます。
Create a forecast をクリックします。

![04_forecast_1](https://user-images.githubusercontent.com/27226946/89359535-06f6d400-d701-11ea-845d-89c759fa7a9f.png)

予測の生成が完了したら、詳細を確認します。


## Step 5: Export forecast

予測結果をS3にエクスポートします。Exportsの右にある、Create forecast exportをクリックします。

![05_export_1](https://user-images.githubusercontent.com/27226946/89359537-078f6a80-d701-11ea-9701-a703502ca9e5.png)

Export nameを入力し、Generated forecastを指定します。予測結果のS3へのエクスポート先を指定して、Create forecast exportをクリックします。

![05_export_2](https://user-images.githubusercontent.com/27226946/89359538-078f6a80-d701-11ea-8f8c-915adb7f9fd7.png)
![05_export_3](https://user-images.githubusercontent.com/27226946/89359539-08280100-d701-11ea-9ce5-24e04fc96ade.png)


指定したS3のパスに、予測結果がエクスポートされました。
![05_export_4](https://user-images.githubusercontent.com/27226946/89359540-08c09780-d701-11ea-8376-9fc21cd40164.png)


## Step 6: Visualization by QuickSight

S3にエクスポートされた、予測結果をAmazon QuickSightで可視化してみます。
まず、S3からファイルが読み込めるようにするため、Security & permissions からQuickSight access to AWS servicesの Add or remove をクリックします。

![06_quicksight_1](https://user-images.githubusercontent.com/27226946/89359541-08c09780-d701-11ea-92f6-3183fc2ca187.png)

予測結果をエクスポートしたS3バケットを選択し、 Write permission for Athena Workgroup にチェックを入れます。
これで事前の設定は完了です。

![06_quicksight_2](https://user-images.githubusercontent.com/27226946/89359543-09592e00-d701-11ea-8b3d-25538c7a1cff.png)

データを読み込んで、可視化をします。
トップページのNew analysisをクリックします。

![06_quicksight_3](https://user-images.githubusercontent.com/27226946/89359544-09592e00-d701-11ea-97a4-84644d21e73d.png)

S3を選択します。

![06_quicksight_4](https://user-images.githubusercontent.com/27226946/89359545-09f1c480-d701-11ea-83c5-812eec305287.png)

Data source nameに任意の値を入力し、S3読み込み用のマニフェストファイルを指定します。
マニフェストファイルは、ノートブック実行の際に作成され、S3にアップロードされています。

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/manifest_for_quicksight/manifest_uk_sales_pred.json
![06_quicksight_5](https://user-images.githubusercontent.com/27226946/89359546-0a8a5b00-d701-11ea-8d8a-c3b8dd12b1dd.png)

SPICEにデータの読み込みが完了されたら、Visualizeをクリックします。

![06_quicksight_6](https://user-images.githubusercontent.com/27226946/89359547-0a8a5b00-d701-11ea-819f-f4bf2010965d.png)

折れ線グラフを選択し、X axisにdate、Valueにp10(sum)、p50(sum)、p90(sum)を選択します。
可視化することができました。

![06_quicksight_7](https://user-images.githubusercontent.com/27226946/89359548-0b22f180-d701-11ea-8229-13590e2f63b0.png)
![06_quicksight_8](https://user-images.githubusercontent.com/27226946/89359549-0bbb8800-d701-11ea-9e5d-ff1859058533.png)

今回はシンプルな構成のためにS3のデータを直接読み込みましたが、
事前にクエリで加工したい場合、Amazon Athenaを利用することもできます。


# パイプライン構築による、Amazon Forecast の自動実行

次に、AWS Lambda と AWS Step Functions を活用することで、パイプラインを構築します。
S3へのデータ投入をトリガーとして AWS Step Functions が起動し、Amazon Forecastのデータインポート、予測子の構築、予測、結果のエクスポートを自動で行います。

![07_arch](https://user-images.githubusercontent.com/27226946/89359550-0bbb8800-d701-11ea-82f1-7e8ec30952f6.png)

2_building_pipeline.ipynb のノートブックを実行することで、パイプラインを構築し、S3にデータをアップロードします。
https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/2_building_pipeline.ipynb


## Step 1: create Lambda functions

boto3を使って、Amazon Forecastのデータインポート、predictor作成、forecast、forecast結果のexportを行う関数を作成します。また、各ジョブのステータスを取得する関数を作成します。

## Step 2: create Step Functions state machine

StepFunctionsでは、ジョブの発行、ジョブの状態確認、完了していない場合待つ、完了した場合次のジョブへ、という流れで進めていきます。

![08_stepfunctions](https://user-images.githubusercontent.com/27226946/89359551-0c541e80-d701-11ea-93f1-404066bf3fcd.png)


## Step 3: Cloud Trail and Cloud Watch Events

S3にファイルが格納された時にStep Functionsを実行するために、Cloud TrailとCloudWatchを設定します。
Step Functionsの開発者ガイドが参考になります。

https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-cloudwatch-events-s3.html


## Step 4: put additional data and visualize

S3へのデータputとトリガとして、Step Functionsのパイプラインが実行されます。
最後まで実行されるのに少し時間がかかります。
ジョブが完了したら、結果がS3に格納されています。
追加データによるpredictorを確認すると、Deep_AR-Plusが選択され、誤差は8.14%となりました。

![09_predictor](https://user-images.githubusercontent.com/27226946/89359552-0cecb500-d701-11ea-8e29-93bee36a2cae.png)


## Step 5: Visualize with QuickSight

前半と同じ手順で、可視化することができます。

![10_quicksight](https://user-images.githubusercontent.com/27226946/89359553-0cecb500-d701-11ea-83e5-e618ca164fa5.png)


# Conclusion

時系列予測は、ビジネスの様々なシーンで活用機会があり、よりビジネスを大きくできる可能性があります。
今回ご説明したように、GUIからお手軽に検証することができるので、まずは試してみてはいかがでしょうか。
実際に業務プロセスに組み込む際も、AWS Step Functions と AWS Lambda を利用することで、自動パイプラインを簡単に構成することができます。
今あるデータを元にまずはトライアルをしてみてはいかがでしょうか。

本ブログシリーズでは、シナリオ別に様々な時系列データを用いて、時系列分析のアプローチを紹介しています。
* Introduction to time series forecasting with SageMaker and Python by Eric Greene
* Benchmarking popular time series forecasting algorithms on electricity demand forecast by Yin Song
* Anomaly Detection of timeseries by Seongmoon Kang

