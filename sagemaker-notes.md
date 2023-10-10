# SageMaker Notes

Amazon SageMaker is a fully managed machine learing service. Users can quickly build and train machine learning models and deploy then instantaneously to a production environment. Built-in training algorithms are provided along with the framework to build your own.

Amazon SageMaker notebook instance is a fully managed machine learning EC2 compute instance that runs ina a Juypter Notebook. SageMaker Studios can be used to manage all notebook instances amd allocated computing power without needing to manage servers.

## Overview of SageMaker Machine Learning Process

1. Generate data
    - Data is require to train any model but before using the data for training, it must be:
        - Fetch
            - Data must be retrived either in-house or via an API call
        - Clean
            - Ensures proper and adequate training of model
        - Transform
            - Some data transformation must be applied to improved training performance
2. Train the model
    - Model can be trained using a training algorithm (eg. stochasitic search algorithms, gradient descent algorithms, random forest, etc.)
    - Choice of algorithm will depend on business case
    - Once model is trained, it must be evaluated to determine whether the accuracy is acceptable or not
3. Deploy the model
    - Typically the model would be integrated into an application before deployment but SageMaker allows for independent deployment

## Experiments

Experimenting is the process of varying certain hyperparameters and evaluating how it affects the output. SageMaker Experiments automatically tracks all inputs, parameters, configurations, and results of an iteration (run). These runs can be grouped into an experiment to be compared.

### Run Class
Experiments can be initialised as shown below:
```py
with Run(
    experiment_name='str',
    run_name='str',
    experiment_display_name='str',
    run_display_name='str',
    tags=list(dict('str', 'str')),
    sagemaker_session=class,
    artifact_bucket='str',
    artifact_prefix='str'
) as run
```
where:
- **experiment_name (string)**: unique name of experiment
- **run_name (string)**: name of run (randomly generated if not provided)
- **run_display_name (string)**: display name shown in the Experiment UI
- **tags (list[dictionary{string, string}])**: list of tags to create calls (default: `None`)
- **sagemaker_session (`sagemaker.session.Session`)**: Session object which manages interactions with the Amazon SageMaker API (one is created if not specified)
- **artifact_bucket (string)**: S3 bucket to upload artifacts 

### Experiment Class

An Amazon SageMaker experiment is a collection of related trials. New experiments are created by calling `experiments.experiments.Experiment.create`. 

Old experiments can be recalled using `experiments.experiments.Experiment.load`. 

```py
sagemaker.experiments.Experiment(
    sagemaker_session=class,
    {
        experiment_name='str',
        display_name='str',
        description='str',
        tags=list[dict['str','str']]
    }
)
```
where:
- **sagemaker_session (`sagemaker.session.Session`)**: Session object which manages interactions with the Amazon SageMaker API (default: `None`)
- **experiment_name (string)**: unique name of experiment
- **display_name (string)**: display name of experimentshown in the Experiment UI
- **description (string)**: description of the experiment
- **tags (list[dictionary{string, string}])**: list of tags to create calls (default: `None`)

Below are a collection of the `Experiment` class methods.

```py
save()
```
Save the current state of the experiment to SageMaker. Returns a dictionary.

```py
delete()
```
Deletes the experiment from SageMaker. Deleted experiments do not delete any associated Trials and their Trial components. It requires ech Trial in the experiment to be deleted first. Returns a dictionary.

```py
load(
    experiment_name='str',
    sagemaker_session=class
)
```
Load an existing experiment and returns an experiment object representing it.

Parameters:
- **experiment_name (string)**: unique name of experiment
- **sagemaker_session (`sagemaker.session.Session`)**: Session object which manages interactions with the Amazon SageMaker API (default: `None`)

```py
create(
    experiment_name='str',
    display_name='str',
    description='str',
    tags=list[dict['str','str']],
    sagemaker_session=class
)
```
Creates a new experiment in SageMaker and return an experiment object.

Parameters:
- **experiment_name (string)**: unique name of experiment
- **display_name (string)**: display name of experimentshown in the Experiment UI (default: `None`)
- **description (string)**: description of the experiment (default: `None`)
- **tags (list[dictionary{string, string}])**: list of tags to create calls (default: `None`)
- **sagemaker_session (`sagemaker.session.Session`)**: Session object which manages interactions with the Amazon SageMaker API (default: `None`)

```py
list_trials(
    created_before=datetime,
    created_after=datetime,
    sort_by='str',
    sort_order='str'
)
```
List trials in the experiment matching specified criteria.

Parameters:
- **created_before (datetime.datetime)**: return trials created before this instant (default: `None`)
- **created_after (datetime.datetime)**: return trials created after this instant (default: `None`)
- **sort_by (string)**: sort by either `Name` or `CreationTime` (default: `None`)
- **sort_order (string)**: sort by either `Ascending` or `Descending` (default: `None`)

## SageMaker Processing

SageMaker allows data scientist to train and deploy machine learning models. These models can then make predictions of outcomes based on input data feed into it but before data can be inputed, it must be cleaned and prepared for ingestion. Processing is an integral step as preparing data for model ingestion improves training quality and training time.

SageMaker processing allows one to run processing jobs in a machine learning pipeline to prepare data for training.

### SKLearn Processing

SKLearn package provides a script to do the data processing for SageMaker. To do so, one must initialise the `SKLearnProcessor` class.

```py
from sagemaker.sklearn.processing import SKLearnProcessor

sklearn_processor = SKLearnProcessor(
    framework_version='str',
    role='str',
    instance_type='str',
    instance_count=int,
    command='str',
    volume_size_in_gb=int,
    volume_kms_key='str',
    output_kms_key='str',
    max_runtime_in_seconds=int,
    base_job_name='str',
    sagemaker_session=class,
    env=dict[str,str],
    tags=list[dict['str','str']],
    network_config=class
)
```
where:
- **framework_version (string)**: version of `scikit-learn`
- **role (string)**: AWS IAM role name or ARN (role needs access to training data and model artifacts)
- **instance_type (string)**: type of EC2 instance used for processing
- **instance_count (string)**: number of instances to run the processing job (default: `1`)
- **command (string)**: command to run, along with any command line (eg. `python3`, `-v`)
    - if not provided, `python3` or `python2` will be chosen based on the `py_version` parameter
- **volume_size_in_gb (int)**: size in GB of EBS volumn to use for storing data during processing (default: `30`)
- **volumn_kms_key (string)**: KMS key for processing volume
- **output_kms_key (string)**: KMS key id for all ProcessingOutputs
- **max_runtime_in_seconds (int)**: terminates job after time is reached
- **base_job_name (string)**: prefix for processing name
- **sagemaker_session (`sagemaker.session.Session`)**: Session object which manages interactions with the Amazon SageMaker API (default: `None`)
- **env (dict[string, string])**: environment variables to be passed to processing job
- **tags (list[dictionary{string, string}])**: list of tags to create calls (default: `None`)
- **network_config (`sagemaker.network.NetworkConfig`)**: NetworkConfig object that configures network isolation, encryption of inter-container, traffic, security group IDs, and subnet

## Built-In Algorithms

### Tabular
#### AutoGluon
#### CatBoost
#### Factorization Machines
#### K-Nearest Neighbours
#### LightGBM
#### LinearLearner
#### TabTransformer
#### XGBoost

## SageMaker Library

## SageMaker Pipelines

Pipelines are an easy-to-use *continuous integration and continuous delivary* (CI/CD) service for machine learning. With SageMaker, one can create, automate, and manage end-to-end ML workflow at scale.

Pipelines are a series of interconencted steps that are defined by a JSON pipeline definition. SageMaker Python SDK offers a convienient abstractions to help construct pipelines with ease.

### Pipeline Session

Pipeline Sessions help manage AWS services interact with one another during pipeline development. Pipelines manage the interaction between SageMaker APIs and AWS services such as AWS S3 and AWS Lambda.

When creating a pipeline to run the `TrainingJob`, one would need to define a `sagemaker.workflow.steps.TrainingStep`, and we need the `TrainingJob` to only be executed when the `sagemaker.workflow.steps.TrainingStep` triggers. `PipelineSession` allows for this.

```py
from sagemaker.workflow.pipeline_context import PipelineSession

# training job creation
pytorch_estimator = PyTorch(
    sagemaker_session=sagemaker.Session(),
    role=sagemaker.get_execution_role(),
    instance_type="str",
    instance_count=int,
    framework_version="str",
    py_version="str",
    entry_point="str",
)

# training step creation
step = TrainingStep(
    name='str',
    step_args=pytorch_estimator.fit(
        inputs=TrainingInput(s3_data="bucket_path"),
    ),
    displayName='str',
    description='str',
    cache_config=CacheConfig(...),
    retry_policies=list(),
    depends_on=list(),
)
```
`sagemaker.estimator.EstimatorBase.fit` method will call the SageMaker `CreateTrainingJob` API to start the `TrainingJob` immediately.

### Local Pipelines Session

Local pipeline sessions provide a convient way to capture an input job arguments without starting the job. Input arguments can be provided in `step_args` parameter

The difference between `PipelineSession` and `LocalPipelineSession` is that `LocalPipelineSession` is used to run SageMaker pipelines locally (in local mode) whereas using `PipelineSession` runs the job on the managed service.

```py
from sagemaker.workflow.pipeline_context import LocalPipelineSession

local_pipeline_session = LocalPipelineSession()

pytorch_estimator = PyTorch(
    sagemaker_session=local_pipeline_session,
    role=sagemaker.get_execution_role(),
    instance_type='str',
    instance_count=int,
    framework_version='str',
    py_version='str',
    entry_point='str',
)

step = TrainingStep(
    name='str',
    step_args=pytorch_estimator.fit(
        inputs=TrainingInput(s3_data='bucket_path'),
    )
)

pipeline = Pipeline(
    name='str',
    steps=[step],
    sagemaker_session=local_pipeline_session
)

pipeline.create(
    role_arn=sagemaker.get_execution_role(),
    description='str'
)

steps = pipeline.list_steps()

training_job_name = steps['PipelineExecutionSteps'][0]['Metadata']['TrainingJob']['Arn']

step_outputs = pipeline_session.sagemaker_client.describe_training_job(TrainingJobName = training_job_name)
```

### Pipeline Parameters

One can parameterise pipeline definitions using pipeline parameters. Parameters will have default vales which can be overridden by specifying parameter values when starting pipeline execution. All parameters can be found in the `sagemaker.workflow.parameters` package.

#### Parameters:
```py
ParameterString(
    name='str',
    default_value='str',
    enum_value=list['str']
)
``` 
String parameter for pipeline
- **name (string)**: name of parameter
- **default_value (string)**: default value for parameter which can be overridden (default: `None`)
- **enum_values (list[string])**: enum values for this parameter (default: `None`)

```py
ParameterInteger(
    name='str',
    default_value=int,
)
``` 
Integer parameter for pipeline
- **name (string)**: name of parameter
- **default_value (int)**: default value for parameter which can be overridden (default: `None`)

```py
ParameterFloat(
    name='str',
    default_value=float,
)
``` 
Float parameter for pipeline
- **name (string)**: name of parameter
- **default_value (float)**: default value for parameter which can be overridden (default: `None`)

```py
ParameterBoolean(
    name='str',
    default_value=bool,
)
``` 
Boolean parameter for pipeline
- **name (string)**: name of parameter
- **default_value (boolean)**: default value for parameter which can be overridden (default: `None`)

## SageMaker Model Monitoring

After a model has been trained and deployed, it must be continously monitored to ensure it maintains production criteria and gets re-trained if it does not.

Amazon SageMaker Model Monitor allows one to log the input, output, and metadata of every invocation of a model after deployment. This enables the user to constantly analyse and evaluate whether the model is still fit for deployment.

To capture real-time inference data for monitoring model data quality, `DataCaptureConfig` must be defined as a new capture option when the model is deployed to the endpoint.

```py
sagemaker.model_monitor.data_capture_config.DataCaptureConfig(
    enable_capture=bool,
    sampling_percentage=int,
    destination_s3_uri='str',
    kms_key_id='str',
    capture_options=list['str'],
    csv_content_types=list['str'],
    json_content_types=list['str'],
    sagemaker_session=class 
)
```
where:
- **enable_decay (bool)**: whether data is captured or not
- **sampling_percentage (int)**: Percentage of data to sample between 0 to 100 (default: `20`)
- **destination_s3_uri (string)**: output bucket for data (default: `s3//<default-session-bucket>/model-monitor/data-capture`)
- **kms_key_id (string)**: kms key used to write into s3 bucket (default: `None`)
- **capture_options (list[string])**: denotes whether to capture `REQUEST`/input and/or `RESPONSE`/output data (default: `None`)
- **csv_content_types (list[string])**: data type of csv content (default: `["text/csv"]`)
- **json_content_types (list[string])**: data type of json content (default: `["application/json"]`)
- **sagemaker_session (`sagemaker.session.Session`)**: Session object which manages interactions with the Amazon SageMaker API (default: `None`)

### Model Decay
### Confusion Matrix
### Threshold
### Re-Training

## Step-by-Step Guide to Creating a SageMaker CI/CD Pipeline

link: https://www.edlitera.com/en/blog/posts/aws-sagemaker-ci-cd-pipelines#mcetoc_1g2b6icbj37

1. How to create a studio instance and user
2. How to define pipeline parameter
3. How to code the processing step
4. How to train your model
5. How to code the processing step to evaluate the models
6. How to set registration of models
7. How to define a condition for the model