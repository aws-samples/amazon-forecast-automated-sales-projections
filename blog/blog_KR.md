# 소개

리테일 업계에서는 판매 및 방문자 수를 예측하는 것이 비즈니스에 직접적인 영향을 미치는 중요한 주제입니다. 정확한 판매 예측을 통해 과잉 재고가 발생하지 않도록 하거나, 판매 기회를 잃지 않도록 하여 비즈니스를 더 효율적으로 운영할 수 있습니다. 방문자 수를 정확하게 예측하면 직원 교대를 적절하게 계획하고 판매량을 예측할 수 있습니다. 하지만 POS 데이터가 시스템에 저장됨에도 불구하고, 여기에 AI와 머신 러닝을 활용하기가 어려울 수 있다고 생각하는 사람들도 많습니다. 이 블로그에서는 AWS에서 시계열 예측을 위해 제공하는 AI 서비스인 Amazon Forecast (Amazon Forecast) 를 사용하여 어려운 프로그래밍이나 기타 작업 없이 예측을 수행하는 방법을 보여 드릴 예정입니다. 그리고 한 걸음 더 나아가 이러한 예측이 일일 배치를 통해 얼마나 쉽게 시스템으로 구현될 수 있는지 예를 들어 설명해 드릴 겁니다. 이 시스템을 통해 S3라는 스토리지에 데이터를 공급하면 바로 데이터 파이프라인이 실행되어 예측 결과가 S3로 출력됩니다.

# 문제 정의

이 블로그는 인터넷에 게시된 영국 전자 상거래 회사의 판매 데이터를 사용하여 다음 주 판매량을 예측합니다. 우리는 Amazon Forecast 를 사용하여 판매를 예측할 겁니다. 이 작업은 GUI에서 직접 수동으로 수행할 수도 있고, 자동화된 파이프라인을 구축하는 방식으로도 수행할 수 있습니다. 예측 결과는 Amazon QuickSight를 사용하여 시각화되므로 관리자는 판매 예측을 즉시 확인할 수 있습니다.

# 아키텍쳐 디자인



## 하나 : 수동 예측 및 시각화

첫 번째 단계는 콘솔을 이용하여 판매 예측을 수행하는 것입니다. Amazon Forecast 콘솔에서 데이터를 가져오고, 예측자를 학습시키고, 예측을 실행하고, 예측 결과를 내보냅니다. 내보낸 예측 결과는 Amazon QuickSight에서 시각화됩니다.

![01_arch_design_1](https://user-images.githubusercontent.com/27226946/89359516-0100f300-d701-11ea-8bf0-f4fbe3204119.png)


## 둘 : AWS Step Functions 과 AWS Lambda를 사용하여 자동 예측 파이프라인 구성

S3로 데이터를 업로드하면 자동적으로 트리거가 동작하여 데이터를 가져오고, 예측자를 학습하고, 예측을 실행하고, 예측 결과를 내보냅니다. S3에 데이터를 올리는 작업을 제외하면 이 모든 작업은 자동으로 수행됩니다. 파이프라인은 AWS Lambda 및 AWS Step Function으로 구성됩니다. 출력 예측 결과는 Amazon QuickSight를 사용하여 시각화됩니다.

![01_arch_design_2](https://user-images.githubusercontent.com/27226946/89359520-02cab680-d701-11ea-979c-c1f35cb07292.png)


# 데이터 - 데이터 다운로드 - 데이터 분석 (누락 데이터 확인 등)

1_prepare_dataset.ipynb 를 실행합니다. 데이터를 다운로드하고 매출을 목표 변수로 계산합니다. 트레이닝 데이터로 2009/12/01에서 2010/12/02까지의 데이터를 준비하고 S3에 업로드합니다. 그리고 2009/12/01에서 2010/12/09까지의 데이터를 추가 트레이닝 데이터로 S3에 업로드합니다.

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/1_prepare_dataset.ipynb



# Forecast - 데이터셋 가져오기 - AutoML - 평가

트레이닝 데이터를 S3에 저장했으면 Amazon Forecast 콘솔로 이동하여 데이터 집합을 생성합니다.

## 단계 1: 데이터셋 가져오기

Dataset group의 이름을 (retail_uk_sales_predictin)로 입력하고 domain으로 Retail을 선택한 후 Next를 클릭합니다.

![02_import_1](https://user-images.githubusercontent.com/27226946/89359522-03fbe380-d701-11ea-8ffd-9d0ffbd0290d.png)

Dataset의 이름을 (uk_sales)로 입력하고 Forecast unit으로 day를 선택합니다. Data schema란은 그대로 두고 Next를 누릅니다.

![02_import_2](https://user-images.githubusercontent.com/27226946/89359523-04947a00-d701-11ea-86e0-15d5768a08db.png)

Dataset Import name을 (uk_sales_2009120101_20101202)로 입력하고, 새 IAM 역할을 생성합니다. Data location 란에 이전 준비 단계에서 저장해 둔 트레이닝 데이터의 S3 경로를 입력하고 [Create] 를 클릭합니다.


![02_import_3](https://user-images.githubusercontent.com/27226946/89359527-052d1080-d701-11ea-83c4-e1c751041a77.png)

대상 시계열 데이터가 활성화될 때까지 기다립니다. 다음으로 예측자를 훈련시킵니다.

![02_import_4](https://user-images.githubusercontent.com/27226946/89359528-05c5a700-d701-11ea-9e49-3ed2cd399bc8.png)


## Step 2: AutoML로 Predictor 만들기

Train Predictor에서 Start 버튼을 클릭합니다. Predictor name에 이름을 입력하고, Forecast horizon에 예측하려는 기간인 7을 입력합니다. 잠재적으로 더 정확한 예측을 위해 Amazon Forecast 에 내장된 달력 정보를 활용할 수 있습니다. 여기서는 휴일 달력 적용 국가로 영국을 선택합니다(선택 사항). Create를 클릭합니다.


![03_predictor_1](https://user-images.githubusercontent.com/27226946/89359529-05c5a700-d701-11ea-9e7a-eff879bb6bae.png)

트레이닝이 시작됩니다. 조금 지나면 트레이닝이 완료되고 Predictor training 란이 Active로 표시될 겁니다. 트레이닝 결과를 보려면 Predictor training에서 View를 클릭합니다.


![03_predictor_2](https://user-images.githubusercontent.com/27226946/89359532-065e3d80-d701-11ea-8ab5-c1a6cde65d99.png)



## 단계 3: 평가

AutoML 결과 Deep_AR_Plus가 14.23% 의 오류 비율로 가장 적합한 알고리즘으로 선택되었습니다.

![03_predictor_3](https://user-images.githubusercontent.com/27226946/89359534-065e3d80-d701-11ea-9497-275cfe7d9e9b.png)

예측을 생성하기 위해 Create a Forecast를 누릅니다.


## 단계 4: 예측 생성하기 

Forecast name에 이름을 입력하고 방금 트레이닝을 완료한 Predictor 를 선택합니다. Create a forecast 버튼을 누릅니다.

![04_forecast_1](https://user-images.githubusercontent.com/27226946/89359535-06f6d400-d701-11ea-845d-89c759fa7a9f.png)

예측이 생성되면 상세 내역을 검토합니다.


## 단계 5: 예측 결과 내보내기 

예측 결과를 S3에 내보냅니다. Exports 란의 오른쪽에 있는 Create forecast export 버튼을 누릅니다.

![05_export_1](https://user-images.githubusercontent.com/27226946/89359537-078f6a80-d701-11ea-9701-a703502ca9e5.png)

Export name을 입력하고 Generated forcast를 선택합니다. 예측 결과를 내보낼 S3 경로를 지정하고 Create forcast export 버튼을 누릅니다.

![05_export_2](https://user-images.githubusercontent.com/27226946/89359538-078f6a80-d701-11ea-8f8c-915adb7f9fd7.png)
![05_export_3](https://user-images.githubusercontent.com/27226946/89359539-08280100-d701-11ea-9ce5-24e04fc96ade.png)


예측이 지정된 S3 경로로 내보내졌습니다.

![05_export_4](https://user-images.githubusercontent.com/27226946/89359540-08c09780-d701-11ea-8376-9fc21cd40164.png)


## 단계 6: QuickSight로 시각화

Amazon QuickSight에서 S3로 내보낸 예측 결과를 시각화해 보겠습니다. 먼저 Quicksight 콘솔의 Quicksight 관리 메뉴로 들어가 보안 및 권한을 선택하고, AWS 서비스에 대한 QuickSight 액세스 추가 또는 제거 버튼을 클릭하여 S3에서 파일을 읽을 수 있도록 허용합니다.


![06_quicksight_1](https://user-images.githubusercontent.com/27226946/89359541-08c09780-d701-11ea-92f6-3183fc2ca187.png)

예측을 내보낸 S3 버킷을 선택하고 Athena Workgroup에 대한 Write permission for Athena Workgroup 체크박스를 선택합니다. 이제 사전 구성을 완료했습니다.

![06_quicksight_2](https://user-images.githubusercontent.com/27226946/89359543-09592e00-d701-11ea-8b3d-25538c7a1cff.png)

데이터를 로드하고 시각화해 봅시다. 상단 페이지에서 새 분석을 클릭합니다.

![06_quicksight_3](https://user-images.githubusercontent.com/27226946/89359544-09592e00-d701-11ea-97a4-84644d21e73d.png)

S3를 선택합니다.

![06_quicksight_4](https://user-images.githubusercontent.com/27226946/89359545-09f1c480-d701-11ea-83c5-812eec305287.png)

데이터 소스 이름에 임의의 값을 입력하여 S3 로딩을 위한 매니페스트 파일을 지정합니다. 매니페스트 파일은 노트북이 실행되고 S3에 업로드 될 때 생성됩니다.

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/manifest_for_quicksight/manifest_uk_sales_pred.json


![06_quicksight_5](https://user-images.githubusercontent.com/27226946/89359546-0a8a5b00-d701-11ea-8d8a-c3b8dd12b1dd.png)

데이터가 SPICE로 로드되면 시각화를 클릭합니다.

![06_quicksight_6](https://user-images.githubusercontent.com/27226946/89359547-0a8a5b00-d701-11ea-819f-f4bf2010965d.png)

선 그래프를 선택한 후, X축에 대해서는 날짜를 선택하고 값으로 p10 (sum), p50 (sum), p90 (sum) 을 선택합니다.이제 시각화할 수 있습니다.

![06_quicksight_7](https://user-images.githubusercontent.com/27226946/89359548-0b22f180-d701-11ea-8229-13590e2f63b0.png)
![06_quicksight_8](https://user-images.githubusercontent.com/27226946/89359549-0bbb8800-d701-11ea-9e5d-ff1859058533.png)

여기서는 단순화를 위해 S3 데이터를 직접 로드했습니다만, Amazon Athena의 쿼리를 이용하여 데이터를 전처리한 후 시각화 할 수도 있습니다.


# Lambda 트리거 - 새로운 데이터가 S3에 업로드되면 트레이닝을 다시 수행하고 리포트를 생성하도록 Lambda 작업 트리거

다음으로 AWS Lambda와 AWS Step Functions을 활용하여 파이프라인을 구축해 보겠습니다. 여기서 AWS Step Functions는 S3에 데이터가 들어오면 실행되어 자동으로 Amazon Forecast로 데이터를 가져오고, 예측자를 구성하고, 결과를 예측하는 작업을 자동화합니다.

![07_arch](https://user-images.githubusercontent.com/27226946/89359550-0bbb8800-d701-11ea-82f1-7e8ec30952f6.png)

2_building_pipeline.ipynb 에서 노트북을 실행하여 파이프라인을 빌드하고 데이터를 S3에 업로드합니다.

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/2_building_pipeline.ipynb


## 단계 1: Lambda 함수 생성하기

boto3을 사용하여 Amazon Forecast로 데이터를 가져오고, 예측자를 만들고, 예측하고, 예측 결과를 내보내는 함수들을 생성할 예정입니다. 그리고 각 작업의 상태를 확인하는 함수를 만들 것입니다.

## 단계 2: Step Functions 상태 머신 생성하기

Step Functions는 작업을 실행시킨 후 상태를 확인하여 진행 여부를 결정합니다. 만약 작업이 완료되지 않은 경우 완료될 때까지 대기하고, 완료된 경우 다음 작업으로 넘어가는 형태로 구성합니다.

![08_stepfunctions](https://user-images.githubusercontent.com/27226946/89359551-0c541e80-d701-11ea-93f1-404066bf3fcd.png)


## 단계 3: Cloud Trail과 Cloud Watch Events 구성하기

S3에 파일이 업로드되면 Step Functions를 실행하도록 CloudTrail 및 CloudWatch를 설정합니다. 자세한 사항이 궁금하신 경우 Step Functions 개발자 가이드를 참고하세요.

https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-cloudwatch-events-s3.html


## 단계 4: 추가 데이터 입력 및 시각화 

S3에 데이터가 업로드되면 Step Functions 파이프라인이 실행됩니다. 모든 단계가 실행되기까지는 시간이 조금 걸릴 수 있습니다. 작업이 완료된 후 S3에 결과가 저장됩니다. 추가 데이터로 예측자를 테스트해 보면, 오차 한계 8.14%로 Deep_AR-Plus가 적합한 알고리즘으로 선택됩니다.

![09_predictor](https://user-images.githubusercontent.com/27226946/89359552-0cecb500-d701-11ea-8e29-93bee36a2cae.png)


## 단계 5: QuickSight로 시각화하기

앞서 QuickSight를 구성한 것과 동일한 방법으로 시각화 할 수 있습니다.

![10_quicksight](https://user-images.githubusercontent.com/27226946/89359553-0cecb500-d701-11ea-83e5-e618ca164fa5.png)



# 결론
시계열 예측은 비즈니스의 다양한 측면에 활용되어 비즈니스를 확장시킬 수 있는 기회를 제공합니다. 위에서 보신 것과 같이 GUI를 이용하여 쉽게 테스트하고 그 결과를 확인할 수 있습니다. 실제로 비즈니스 프로세스에 통합하고자 하실 때는 AWS Step Functions 및 AWS Lambda 를 사용하여 자동화된 파이프라인을 쉽게 구성할 수 있습니다. 가지고 계신 데이터를 이용하여 한 번 시도해 보시는 게 어떨까요?

저희는 이 글을 포함하여, 시계열 데이터 처리를 위한 네 가지 방법들을 블로그로 포스팅하였습니다. 아래에서 다른 시나리오들도 확인해 보세요.

* Introduction to time series forecasting with SageMaker and Python by Eric Greene
* Benchmarking popular time series forecasting algorithms on electricity demand forecast by Yin Song
* Anomaly Detection of timeseries by Seongmoon Kang


