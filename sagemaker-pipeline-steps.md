# SageMaker Pipelines

SageMaker pipelines consist of various step where each step defines a set of procedures to deployed a fully-trained machine learning model. The most basic SageMaker pipeline will consist if the four following stages (also known as steps):
1. Pre-processing
2. Training
3. Evaluation
4. Deployment

## Pre-processing Step

SageMaker allows data scientist to train and deploy machine learning models. These models can then make predictions of outcomes based on input data feed into it. However, if bad data is fed into the model, the model will continually output bad predictions. Hence, data must be cleaned and prepared for ingestion. Pre-processing is an integral step as preparing data for model ingestion improves training quality and training time.

There are various methods that can be taken to clean and process the raw data. Depending on the business specification, some or all these methods can be implemented in the pre-processing step. 

Data cleaning is a major pre-processing step in which errors or discrepancies are located and fixed in the raw data. Furthermore, duplicates, outliers, and missing data are found and either removed or filled with expected data. Whilst filling missing data with expected data is an option for dealing with missing data, it damages the integretity of the data.

Data transformation is another major pre-processing step. This step entails formating the data into a form that allows for analysis by the model. Normalisation, standardisation, and discretisation are common data transformation techniques. Whilst standardisation transforms that data to have zero mean and unit variance, normalisation scales the data to a common range. Continous data is discretized into discrete categories using discretisation.

The last two pre-processsing methods are data integration and data reduction. Data integration is the process of merging data from multiple sources into a single dataset that can be ingested by the machine learning model. Data reduction involves selectly removing data so only crucial information remains. Doing so reduces the dimensions of the data making it easier to ingest and read by the model.

## Training Step

The training step will take the outputs of the pre-processing step and feed it into the model, along with a mcahine learning algorithm, in order to train the model to make predictions. Here, the model will continually alter its weights and bias to minimise a loss function. Once the loss function is minimised, the best mathematical represenation of the relationship between the data features and trget value is formualted. When training the machine learning model, a local optima of the loss function can be found instead of the global optimum resulting in a sub-optimal model. One solution to avoiding such a problem is by implementing the most suitable training algorithm (based on the business problem). As such, there are a variety of training algorithm available in SageMaker that the user can implement. Below are three example algorithms for training on tabular data.

### XGBoost

XGBoost (eXtreme Gradiaent Boosting) is a popular and efficient implementation of the gradient boosted tree algorithm. Gradient boosting is a supervised learning approach that combines an ensemble of estimates from a number of weaker and simpler models in an effort to accurately predict target variables. Due to its exceptional robustness in managing a wide range of data types and hyperparameters, XGBoost excels at solving a multitude of machine learning problems such as regression, classification, and ranking problems.

### CatBoost

CatBoost is another well-known and efficient variant of the Gradient Boosting Decision Tree algorithm.  It has been specifically designed to efficiently handle categorical data, making it well-suited for tasks involving both numerical and categorical variables. CatBoost algorithm differs from XGBoost as it attempts to reduce prediction shift caused by the leakage of the target variable in the input data.

### LinearLearner

LinearLearner is a binary and multiclass classification and regression algorithm. It is based on linear models, which means that linear functions are used to model the relationship between the input data and the target variable. The LinearLearner algorithm provides a scalable and distributed implementation, allowing it to handle large datasets.

One benefitial feature of the LinearLearner algorithm is that it supports the automatic model tuning meaning that the hyperpararmeters of the model are automatically optimised allowing for most optimal algorithm performance.


## Evaluation Step

Model evaluation is the process of the using different evaluation metrics to determine the quality of the model and the model predictions. Model evaluation is important as it ensures that the model is reliable and behaves as expected, and that the model is optimally trained and can effectively predict from unseen data. There are a multitude of evaluation metrics can be used to identify the model quality. The implementation of these metrics are dependant on the model and the model's usecase. The following is a list of a few evaluation metrics:
- Confusion matrices
- F1 score
- Log loss
- Root mean square error
- Mean square error
- R-squared
- Area under curve

Model evaluation can be either be performed offline or online. In offline model evaluation, the model is evaluated right after training or re-training. 

Online evaluation is performed after the model has been deployed. It is  conducted as a step in Model Monitoring. Online evaluations are completed to ensure that the model maintains high-quality predictions and does not experience any model decay or drift.

## Register Step

Once the model has been fully trained, the model can be deployed onto production. Once the model has been deployed, it is advise to further explore ways to optimise the model while maintaining model availability. When new updates are ready to be deployed, an appropiate deployment strategy must be employed it minimise model downtime and the effect of model rollback.

# Example Code: Deploying a House Price Prediction Model

In this example, we will be showcasing and explaining the python code and steps to pre-process data, and deploy a fully-trained machine learning model onto production. We will be using housing price data to train the model (https://www.kaggle.com/datasets/yasserh/housing-prices-dataset).

The dataset consist of the following features:
- `price` - Price of the house
- `area` - Area of the house
- `bedrooms` - Number of house bedrooms
- `bathrooms` - Number of house bathrooms
- `stories` - Number of house stories
- `mainroad` - Whether connected to main road
- `guestroom` - Whether has a guestroom
- `basement` - Whether has a basement
- `hotwaterheating` - Whether has a hotware heater
- `airconditioning` - Whether has an airconditioning
- `furnishingstatus` - Whether has furnishing or not

The code was written in three Python (.py) files:
- pipeline.py
- preprocess.py
- evaluate.py

### 1 Define pipeline session
Firstly, a new SageMaker session must be set up. This can be done using the following code block. 

```py
# import relevant modules
import boto3
import sagemaker
import sagemaker.session

# initialise variables
region = boto3.Session().region_name
sagemaker_session = sagemaker.session.Session()
role = sagemaker.get_execution_role()
default_bucket = sagemaker_session.default_bucket()
model_package_group_name = f"HousePriceModelPackageGroupName"
```

### 2 Download dataset
Afterwards, the neccesary data must be downloaded. In this scenario, the housing data was stored in an S3 bucket and downloaded the `opt/ml` directory. This directory is used to structure all the artifacts and files associated with training the model.

```py
# create a new folder in "opt/ml/" to store the downloaded data in
pathlib.Path("/opt/ml/processing/data").mkdir(parents=True, exist_ok=True)

# initialise boto3 resource and download data from bucket
s3 = boto3.resource("s3")
s3.Bucket("example-bucket").download_file(
    "bucket-data/Housing.csv",
    "/opt/ml/processing/data/Housing.csv"
)
```

### 3 Define pipeline parameters
Once the data has been downloaded, the pipelines parameters must be defined. This is done in order to initialise an instance of the pipeline.

```py
from sagemaker.workflow.parameters import (
    ParameterInteger,
    ParameterString,
)

# number of EC2 instance to run 
processing_instance_count = ParameterInteger(
    name="ProcessingInstanceCount",
    default_value=1
)

# whether the model should be immediately deployed or requires human intervention to deploy
model_approval_status = ParameterString(
    name="ModelApprovalStatus",
    default_value="PendingManualApproval"
)

# location of the input data in an S3 bucket
input_data = ParameterString(
    name="InputData",
    default_value=input_data_uri,
)
```

### 4 Define a pre-processing step
The pre-processing steps are defined in a separte python file called `preprocess.py`. This is then passed into a processing step for execution on the input data. The following code:
- Split the data into training, test, and validation datasets
- Converts multiple columns into boolean values
- Implements integer-encoding to `furnishingstatus`
The feature engineering code is shown below.

```py
%%writefile preprocess.py
# import relevant modules
import numpy as np

# read the dataset
raw_data = pd.read_csv("/opt/ml/processing/data/Housing.csv")

# defining data transformation
# implementing boolean values into dataset
boolmap = {
    "yes": 1,
    "no": 0
}

# implementing integer-encoding to furnishingstatus
catemap = {
    "furnished": 2, 
    "semi-furnished": 1, 
    "unfurnished": 0
}

# applying transformations (mapping input data with above defined dictionaries)
processed_data = raw_data.replace({
    "mainroad": boolmap,
    "guestroom": boolmap,
    "basement": boolmap,
    "hotwaterheating": boolmap,
    "airconditioning": boolmap,
    "prefarea": boolmap,
    "furnishingstatus": catemap
})

# splitting input data into training, validation, and test datasets
train, test, validation = np.split(processed_data, [int(0.7 * len(processed_data)), int(0.85 * len(processed_data))])

# saving new datasets into "opt/ml"
pd.DataFrame(train).to_csv("/opt/ml/processing/data/train/train.csv", header=False, index=False)
pd.DataFrame(validation).to_csv("/opt/ml/processing/data/validation/validation.csv", header=False, index=False)
pd.DataFrame(test).to_csv("/opt/ml/processing/data/test/test.csv", header=False, index=False)
```

An instance of SKLearnProcessor can be initialised and fed into the processing step, along with the `preprocessing.py` file.

```py
# import relevant modules
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput

# initialise processor
sklearn_processor = SKLearnProcessor(
    framework_version="0.23-1",
    instance_type="ml.m5.xlarge",
    instance_count=processing_instance_count,
    base_job_name="sklearn-house-preprocess",
    sagemaker_session=pipeline_session,
    role=role
)

# provide input, output paths, and code to processor instance
step_args = sklearn_processor.run(
    inputs=[
        ProcessingInput(
            source=input_data, 
            destination="/opt/ml/processing/input"
        ),  
    ],
    outputs=[
        ProcessingOutput(
            output_name="train",
            source="/opt/ml/processing/train"
        ),
        ProcessingOutput(
            output_name="validation",
            source="/opt/ml/processing/validation"
        ),
        ProcessingOutput(
            output_name="test",
            source="/opt/ml/processing/test"
        )
    ],
    code="preprocess.py",
)

# define processing step
step_process = ProcessingStep(
    name="PreprocessingHousingPriceData",
    step_args=step_args
)
```

### 5 Define a training step

This section demonstrates how to use SageMaker XGBoost Algorithm to train a model on training data output from the processing step. 

```py
# specify the model pathto save the model after training
model_path = f"s3://{default_bucket}/HousePriceTrain"
```

Set up an estimator for the input dataset and the XGBoost algorithm. The training instance type is passed into the estimator. Hyperparameters are also initialised.

```py
# initialise XGBoost training algorithm
image_uri = sagemaker.image_uris.retrieve(
    framework="xgboost",
    region=region,
    version="1.0-1",
    py_version="py3",
    instance_type=training_instance_type,
)

# initialise esitmator
xgb_train = Estimator(
    image_uri=image_uri,
    instance_type=training_instance_type,
    instance_count=1,
    output_path=model_path,
    base_job_name=f"{base_job_prefix}/house-price-train",
    sagemaker_session=pipeline_session,
    role=role
)

# set XGBoost hyperparameters
xgb_train.set_hyperparameters(
    objective="reg:linear",
    num_round=50,
    max_depth=5,
    eta=0.2,
    gamma=4,
    min_child_weight=6,
    subsample=0.7,
    silent=0
)
```

Initialise training step and feed it the input data.

```py
# provide input, output paths, and code to estimator instance
step_args = xgb_train.fit(
    inputs={
        "train": TrainingInput(
            s3_data=step_process.properties.ProcessingOutputConfig.Outputs[
                "train"
            ].S3Output.S3Uri,
            content_type="text/csv"
        ),
        "validation": TrainingInput(
            s3_data=step_process.properties.ProcessingOutputConfig.Outputs[
                "validation"
            ].S3Output.S3Uri,
            content_type="text/csv"
        )
    }
)

# define training step
step_train = TrainingStep(
    name="TrainHousePriceModel",
    step_args=step_args
)
```

### 6 Define an evaluating step

Once the model has been trained, it is ready for evaluation. The evaluation code is written in a seperated Python file `evaluate.py` and is passed as an argument into a processing step. In the `evaluate.py`, the model and a test dataset are used as inputs, and a JSON file is produced.

```py
%%writefile evalualtion.py
import pickle
import tarfile
import numpy as np
import pandas as pd
import xgboost
import pathlib
import json

from sklearn.metrics import mean_squared_error

# starting evaluation
# define model path and extracting model parameters
model_path = "/opt/ml/processing/model/model.tar.gz"
with tarfile.open(model_path) as tar:
    tar.extractall(path=".")

# loading xgboost model
model = pickle.load(open("xgboost-model", "rb"))

# reading test data
test_path = "/opt/ml/processing/test/test.csv"
df = pd.read_csv(test_path, header=None)
y_test = df.iloc[:, 0].to_numpy()

# dropping target variable from test data
df.drop(df.columns[0], axis=1, inplace=True)
X_test = xgboost.DMatrix(df.values)

# performing predictions against test data
predictions = model.predict(X_test)

# calculating mean squared error
mse = mean_squared_error(y_test, predictions)
std = np.std(y_test - predictions)
report_dict = {
    "regression_metrics": {
        "mse": {
            "value": mse,
            "standard_deviation": std
        },
    },
}

#creating output directory
output_dir = "/opt/ml/processing/evaluation"
pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

# writing out evaluation report with mean square error
evaluation_path = f"{output_dir}/evaluation.json"
with open(evaluation_path, "w") as f:
    f.write(json.dumps(report_dict))
```

Initialise a script processor and use it to defined a processing step for evaluation.

```py
    script_eval = ScriptProcessor(
        image_uri=image_uri,
        command=["python3"],
        instance_type="ml.m5.xlarge",
        instance_count=1,
        base_job_name="script-housing-price-eval",
        role=role
    )

# provide input, output paths, and code to processor instance
step_args = script_eval.run(
    inputs=[
        ProcessingInput(
            source=step_train.properties.ModelArtifacts.S3ModelArtifacts,
            destination="/opt/ml/processing/model",
        ),
        ProcessingInput(
            source=step_process.properties.ProcessingOutputConfig.Outputs[
                "test"
            ].S3Output.S3Uri,
            destination="/opt/ml/processing/test"
        )
    ],
    outputs=[
        ProcessingOutput(
            output_name="evaluation",
            source="/opt/ml/processing/evaluation"
        )
    ],
    code=os.path.join(BASE_DIR, "evaluate.py")
)

# define a property file to export evaluation results
evaluation_report = PropertyFile(
    name="HousePriceEvaluationReport",
    output_name="evaluation",
    path="evaluation.json"
)

# define processing step
step_eval = ProcessingStep(
    name="EvaluateHousePriceModel",
    step_args=step_args,
    property_files=[evaluation_report]
) 
```

### 7 Regiseter model

Next, a model package group can be generated from the trained model. A model package group is a reusable model artifacts that packages all the necessary components for inference.

```py
# define the metrics used to evaluate the model
model_metrics = ModelMetrics(
    model_statistics=MetricsSource(
        s3_uri="{}/evaluation.json".format(
            step_eval.arguments["ProcessingOutputConfig"]["Outputs"][0]["S3Output"]["S3Uri"]
        ),
        content_type="application/json"
    )
)

# define the model
model = Model(
    image_uri=image_uri,
    model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
    sagemaker_session=pipeline_session,
    role=role
)

# define the steps to register the model
step_args = model.register(
    content_types=["text/csv"],
    response_types=["text/csv"],
    inference_instances=["ml.t2.medium", "ml.m5.large"],
    transform_instances=["ml.m5.large"],
    model_package_group_name=model_package_group_name,
    approval_status=model_approval_status,
    model_metrics=model_metrics
)
```

### 8 Condition step to verify model accuracy

A condition step can be used a to ensure only high quality models will be deployed or registered. In this example, we only want to register models that meet a certain accuracy.

First, define a `ConditionLessThanOrEqualTo` condition to ensure minimum accuracy. Here, models will only pass the condition if the mean squared error is less than 6.0. Once this has been defined, the condition step can be initialised.

```py
from sagemaker.workflow.conditions import ConditionLessThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.functions import JsonGet

# define the condition to pass
cond_lte = ConditionLessThanOrEqualTo(
    left=JsonGet(
        step_name=step_eval.name,
        property_file=evaluation_report,
        json_path="regression_metrics.mse.value"
    ),
    right=6.0
)

# define condition step
step_cond = ConditionStep(
    name="CheckMSEHousePriceEvaluation",
    conditions=[cond_lte],
    if_steps=[step_register],
    else_steps=[]
)
```

### 9 Create the pipeline

Lastly, after all the steps have been made, they can be combined to create a pipeline.

```py
from sagemaker.workflow.pipeline import Pipeline

pipeline = Pipeline(
    name=HousePricePipeline,
    parameters=[
        processing_instance_count,
        model_approval_status,
        input_data,
    ],
    steps=[step_process, step_train, step_eval, step_cond]
)
```

### 